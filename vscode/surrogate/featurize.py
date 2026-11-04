"""README 5. 特徴量化と PCA による圧縮。

    python vscode/surrogate/featurize.py                       # train 60 点（phase 1）
    python vscode/surrogate/featurize.py --set train test      # 集合を指定
    python vscode/surrogate/featurize.py --phase 1 2

手順（Notion「研究室サロゲートモデル」Step 5 の式 D(f;θ) = F[w(t) d(t+t0;θ)] どおり）
----
1-2. 切り出しは sourse_new_2.kiritori2 と同じ（関数をそのまま呼ぶ）。
   - シミュレーションは interpolate_sim_one で実験の刻み exp_dt = 0.5 ns に補間する
   - 先頭 SIM_SKIP = 8000 点（4.0 us、送信パルス）を飛ばし、生波形の正の最大を
     ピーク t0 とする（plot_simdata.py・plotting.py と同じ）
   - t0 の左 left = 1024 点（0.512 us）、右 right = 3072 点（1.536 us）を矩形窓で取る
3. 固定周波数グリッド上で DFT して複素スペクトル D(f) を得る（ゼロ埋めと同じ効果）。
   make_fftdata は振幅しか返さないので使わない。時刻原点は t0
4. 平滑面（design.csv の smooth 行）の D_smooth(f) で割り、R(f) = D / D_smooth とする。
   送信パルスと伝搬の共通部分が消え、きず面の反射特性だけが残る
5. 特徴量は [Re R, Im R] を並べた実ベクトル。位相を角度で持つと ±π の巻き戻りで
   PCA が壊れるので、複素数のまま実部・虚部に分ける
6. 中心化して SVD で PCA。累積寄与率 99% に要る主成分数を出す

コード中の H は Notion の R と同じもの。

出力（vscode/surrogate/tmp_output/features/<tag>/）
    features.npz      params[mm], names, freq, H, X, PCA（mean, components, 寄与率）
    summary.txt       窓・帯域・寄与率の表（まずこれを読む）
    spectra.png       |R| と位相を pitch / width / depth で色分け
    pca_cumulative.png
    pca_loadings.png  PC1-4 の実部・虚部
    pca_scores.png    PC1-PC2 散布図をパラメータで色分け
    window.png        波形全体と切り出し窓
"""

import argparse
import contextlib
import csv
import io
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import MaxNLocator
try:
    import japanize_matplotlib  # noqa: F401  日本語ラベル用
except ImportError:
    pass

import sourse_new_2 as sn2
from run_design import out_name

EXP_DT = sn2.exp_dt          # 0.5 ns。シミュレーションもこの刻みに補間してから切る
LEFT, RIGHT = sn2.left, sn2.right   # kiritori2 のピーク左右の点数（1024 / 3072）
# 補間後の先頭を飛ばす点数（4.0 us）。plot_simdata.py の search_offset、
# project3 の SIM_SKIP と同じ。実験の記録は 5.41 us 始まりなので 0 点になる
SIM_SKIP_T = 8000 * EXP_DT

# 解析帯域 [Hz]。平滑面スペクトルの -20 dB 帯は 1.75-7.85 MHz（ピーク 4.75 MHz）。
# 分母が小さい端を避けて内側に取る
F_MIN = 2.00e6
F_MAX = 7.75e6
DF = 0.05e6

PC_TARGET = 0.99

# window.png に載せる例。後続波が底面エコーより大きい条件と、実験波形 1 本（ex_index.csv の先頭）
WINDOW_HARD_CASE = "kukei_cupy_pitch114_width48_depth30.csv"   # 後続波が底面エコーより大きい
EXP_SAMPLE = os.path.join(HERE, "..", "simulation", "data", "ex_data", "scope_0.csv")

# 色: 系列 1・2 と単色の連続ランプ（dataviz 既定パレット、blue 250 -> 700）
C_RE, C_IM = "#2a78d6", "#eb6834"
SEQ = LinearSegmentedColormap.from_list(
    "blue_seq", ["#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"])
GRID = "#d9d8d4"

AXES = [("pitch", "pitch [mm]"), ("width", "width [mm]"), ("depth", "depth [mm]")]


def freq_grid():
    return np.arange(F_MIN, F_MAX + DF / 2, DF)


def cut(t, w):
    """kiritori2 で切り出す。返り値は (t0 [s], 切り出し波形, t0 基準の時刻 [s])。"""
    off = int(np.searchsorted(t, SIM_SKIP_T))
    k = off + int(np.nanargmax(w[off:]))    # kiritori2 内部と同じピーク
    with contextlib.redirect_stdout(io.StringIO()):   # kiritori2 は毎回 shape を print する
        seg = sn2.kiritori2(w[off:], LEFT, RIGHT)
    tau = (np.arange(len(seg)) - LEFT) * EXP_DT
    return t[k], seg, tau


def spectrum(t, w, freq):
    """kiritori2 で切り出した波形の、固定周波数グリッドでの複素スペクトル。時刻原点は t0。"""
    _, seg, tau = cut(t, w)
    E = np.exp(-2j * np.pi * np.outer(freq, tau))
    return E @ seg * EXP_DT


def load_wave(path):
    """シミュレーション CSV を読み、exp_dt 刻みに補間して (時刻 [s], 波形) を返す。"""
    w = np.loadtxt(path, delimiter=",")
    w = sn2.interpolate_sim_one(w if w.ndim == 1 else w[:, 0])
    return np.arange(len(w)) * EXP_DT, w


def load_scope(path):
    """実験のスコープ CSV（SHIFT-JIS、2 行ヘッダ）を読み、(時刻 [s], 波形) を返す。

    末尾に電圧が空の行があるので落とす。DC オフセット（約 -0.13 V）があり、
    矩形窓だと sinc の裾で帯域に漏れるので記録全体の中央値を引く。
    """
    d = np.genfromtxt(path, delimiter=",", skip_header=2, usecols=(0, 1))
    d = d[np.isfinite(d).all(axis=1)]
    return d[:, 0], d[:, 1] - np.median(d[:, 1])


def pca(X):
    """中心化した X の SVD。components は行が主成分。"""
    mean = X.mean(axis=0)
    _, s, Vt = np.linalg.svd(X - mean, full_matrices=False)
    var = s ** 2
    return mean, Vt, var / var.sum()


def n_for(cum, target):
    return int(np.searchsorted(cum, target) + 1)


# ---------------------------------------------------------------- 図

def _style(ax):
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def plot_spectra(out, freq, H, P):
    mag = np.abs(H)
    # unwrap しない。|H| が 0 近くまで落ちる条件で ±2π の偽の段差が出る（位相は概ね ±1 rad）
    ph = np.angle(H)
    fig, axs = plt.subplots(2, 3, figsize=(15, 8), sharex=True, layout="constrained")
    for j, (key, label) in enumerate(AXES):
        norm = Normalize(P[:, j].min(), P[:, j].max())
        for i in np.argsort(P[:, j]):
            c = SEQ(norm(P[i, j]))
            axs[0, j].plot(freq / 1e6, mag[i], color=c, linewidth=1)
            axs[1, j].plot(freq / 1e6, ph[i], color=c, linewidth=1)
        fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=SEQ), ax=axs[:, j], label=label)
        axs[0, j].set_title(f"色 = {key}")
        axs[1, j].set_xlabel("周波数 [MHz]")
    axs[0, 0].set_ylabel("|R| = |D / D_smooth|")
    axs[1, 0].set_ylabel("arg R [rad]")
    for ax in axs.flat:
        _style(ax)
    fig.suptitle(f"平滑面で正規化したスペクトル R（{len(H)} 件、kiritori2 窓 t0 -{LEFT*EXP_DT*1e6:.3f} / +{RIGHT*EXP_DT*1e6:.3f} us）")
    fig.savefig(os.path.join(out, "spectra.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative(out, ratio):
    cum = np.cumsum(ratio)
    k = np.arange(1, len(cum) + 1)
    k99 = n_for(cum, PC_TARGET)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(k, cum * 100, color=C_RE, linewidth=2, marker="o", markersize=4)
    ax.axhline(PC_TARGET * 100, color="#52514e", linewidth=1, linestyle="--")
    ax.annotate(f"{PC_TARGET*100:.0f}% に {k99} 成分", (k99, cum[k99 - 1] * 100),
                xytext=(10, -25), textcoords="offset points", color="#0b0b0b",
                arrowprops=dict(arrowstyle="-", color="#52514e"))
    ax.set_xlim(0.5, min(len(k), max(20, k99 + 5)) + 0.5)
    ax.set_ylim(min(cum[0] * 100 - 5, 90), 100.5)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("主成分の数")
    ax.set_ylabel("累積寄与率 [%]")
    ax.set_title("PCA 累積寄与率")
    _style(ax)
    fig.savefig(os.path.join(out, "pca_cumulative.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_loadings(out, freq, comps, ratio, n=4):
    nf = len(freq)
    fig, axs = plt.subplots(1, n, figsize=(4 * n, 3.5), sharey=True)
    for i, ax in enumerate(axs):
        ax.plot(freq / 1e6, comps[i, :nf], color=C_RE, linewidth=2, label="Re")
        ax.plot(freq / 1e6, comps[i, nf:], color=C_IM, linewidth=2, label="Im")
        ax.set_title(f"PC{i+1}（{ratio[i]*100:.1f}%）")
        ax.set_xlabel("周波数 [MHz]")
        _style(ax)
    axs[0].legend(frameon=False)
    fig.savefig(os.path.join(out, "pca_loadings.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_scores(out, scores, P, ratio):
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.5), layout="constrained")
    for j, (key, label) in enumerate(AXES):
        sc = axs[j].scatter(scores[:, 0], scores[:, 1], c=P[:, j], cmap=SEQ, s=40,
                            edgecolors="#fcfcfb", linewidths=1)
        fig.colorbar(sc, ax=axs[j], label=label)
        axs[j].set_xlabel(f"PC1（{ratio[0]*100:.1f}%）")
        axs[j].set_ylabel(f"PC2（{ratio[1]*100:.1f}%）")
        axs[j].set_title(f"色 = {key}")
        _style(axs[j])
    fig.savefig(os.path.join(out, "pca_scores.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_window(out, examples):
    """波形全体と kiritori2 の切り出し窓。左が全体、右が窓の付近の拡大。

    右には kiritori2 が返した波形そのものを重ねる（窓の位置がずれていないことの確認）。
    examples は (見出し, 時刻 [s], 波形) のリスト。
    """
    fig, axs = plt.subplots(len(examples), 2, figsize=(15, 2.8 * len(examples)),
                            gridspec_kw={"width_ratios": [3, 2]}, layout="constrained")
    for row, (title, t, w) in zip(axs, examples):
        t0, seg, tau = cut(t, w)
        lo, hi = t0 - LEFT * EXP_DT, t0 + RIGHT * EXP_DT
        for ax in row:
            ax.axvspan(lo * 1e6, hi * 1e6, color=GRID, alpha=0.6, linewidth=0)
            ax.axvline(t0 * 1e6, color="#52514e", linestyle="--", linewidth=1)
            ax.plot(t * 1e6, w, color=C_RE, linewidth=0.8, label="全体")
            _style(ax)
        if t[0] < SIM_SKIP_T:
            row[0].axvspan(t[0] * 1e6, SIM_SKIP_T * 1e6, facecolor="none", hatch="//",
                           edgecolor=GRID, linewidth=0)
            row[0].text(SIM_SKIP_T * 1e6, row[0].get_ylim()[1] * 0.9, " ← 先頭 8000 点は\n    ピーク探索から除外",
                        va="top", ha="left", color="#52514e", fontsize=9)
        row[1].plot((t0 + tau) * 1e6, seg, color=C_IM, linewidth=1.2, label="kiritori2 の出力")
        z = (t >= t0 - 1.5e-6) & (t <= t0 + 3.0e-6)
        row[1].set_xlim((t0 - 1.5e-6) * 1e6, (t0 + 3.0e-6) * 1e6)
        top = 1.15 * np.abs(w[z]).max()
        row[1].set_ylim(-top, top)
        row[0].set_title(f"{title}　全体（灰色が切り出し窓 {lo*1e6:.2f}-{hi*1e6:.2f} us）", loc="left")
        row[1].set_title(f"窓の付近　t0 = {t0*1e6:.3f} us（破線、正の最大）", loc="left")
        row[1].text(hi * 1e6, top * 0.9, f" 窓外は捨てる\n （窓内 {len(seg)} 点）",
                    va="top", ha="left", color="#52514e", fontsize=9)
        row[0].set_ylabel("振幅")
    axs[0, 1].legend(frameon=False, loc="lower right")
    axs[-1, 0].set_xlabel("時刻 [us]")
    axs[-1, 1].set_xlabel("時刻 [us]")
    fig.savefig(os.path.join(out, "window.png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=["train"])
    ap.add_argument("--phase", nargs="+", type=int, default=[1],
                    help="既定は phase 1（train の最初の 60 点）")
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--tag", default=None, help="出力サブディレクトリ名")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    ref = [r for r in rows if r["set"] == "smooth"]
    if len(ref) != 1:
        raise SystemExit(f"design.csv の smooth 行が {len(ref)} 行ある（1 行のはず）")
    sel = [r for r in rows if r["set"] in args.set and int(r["phase"]) in args.phase]
    if not sel:
        raise SystemExit("該当する行が無い")

    def path_of(r):
        return os.path.join(args.sim_dir, out_name(r, float(r["pitch_m"]),
                                                   float(r["width_m"]), float(r["depth_m"])))

    missing = [os.path.basename(path_of(r)) for r in sel if not os.path.exists(path_of(r))]
    if missing:
        raise SystemExit(f"未計算が {len(missing)} 件:\n  " + "\n  ".join(missing))

    freq = freq_grid()
    X_ref = spectrum(*load_wave(path_of(ref[0])), freq)

    names, P, H = [], [], []
    for r in sel:
        p = path_of(r)
        names.append(os.path.basename(p))
        # 実際に刻まれた寸法（_m 列）を使う。_mm 列は量子化前の公称値
        P.append([float(r[k + "_m"]) * 1e3 for k, _ in AXES])
        H.append(spectrum(*load_wave(p), freq) / X_ref)
    P, H = np.array(P), np.array(H)
    X = np.concatenate([H.real, H.imag], axis=1)

    mean, comps, ratio = pca(X)
    cum = np.cumsum(ratio)
    scores = (X - mean) @ comps.T

    tag = args.tag or "_".join(args.set) + "_ph" + "".join(map(str, args.phase))
    out = os.path.join(args.sim_dir, "features", tag)
    os.makedirs(out, exist_ok=True)

    np.savez(os.path.join(out, "features.npz"),
             params_mm=P, param_names=np.array([k for k, _ in AXES]), names=np.array(names),
             freq=freq, H=H, X=X, X_ref=X_ref,
             pca_mean=mean, pca_components=comps, pca_ratio=ratio, pca_scores=scores,
             t_window=np.array([-LEFT * EXP_DT, RIGHT * EXP_DT]))

    plot_spectra(out, freq, H, P)
    plot_cumulative(out, ratio)
    plot_loadings(out, freq, comps, ratio)
    plot_scores(out, scores, P, ratio)

    # 窓の図: 平滑面・代表 1 点・t0 の決め方が効く条件・実験 1 本
    examples = [("平滑面（シミュレーション）", *load_wave(path_of(ref[0])))]
    for i in [0] + [i for i, n in enumerate(names) if n == WINDOW_HARD_CASE]:
        examples.append((f"p={P[i,0]:.2f} w={P[i,1]:.2f} d={P[i,2]:.2f} mm（シミュレーション）",
                         *load_wave(os.path.join(args.sim_dir, names[i]))))
    if os.path.isfile(EXP_SAMPLE):
        examples.append((f"実験 {os.path.basename(EXP_SAMPLE)}（p=1.25 w=0.40 d=0.15 mm）",
                         *load_scope(EXP_SAMPLE)))
    plot_window(out, examples)

    lines = [
        f"集合: {' '.join(args.set)} / phase {' '.join(map(str, args.phase))}  ({len(sel)} 件)",
        f"参照: {os.path.basename(path_of(ref[0]))}",
        f"時間窓: kiritori2（exp_dt 補間後、先頭 8000 点を除いた正の最大 t0 から左 {LEFT} 点 / 右 {RIGHT} 点 = -{LEFT*EXP_DT*1e6:.3f} / +{RIGHT*EXP_DT*1e6:.3f} us）",
        f"帯域: {F_MIN/1e6:.2f}-{F_MAX/1e6:.2f} MHz, {DF/1e6:.3f} MHz 刻み = {len(freq)} 点",
        f"特徴量: [Re R, Im R] = {X.shape[1]} 次元",
        f"|R| の範囲: {np.abs(H).min():.3f} - {np.abs(H).max():.3f}",
        "",
        "累積寄与率に要る主成分数",
    ]
    for t in (0.90, 0.95, 0.99, 0.999):
        lines.append(f"  {t*100:5.1f}% : {n_for(cum, t)}")
    lines += ["", " PC   寄与率[%]  累積[%]"]
    for i in range(min(15, len(ratio))):
        lines.append(f"{i+1:3d}  {ratio[i]*100:9.3f}  {cum[i]*100:7.3f}")
    text = "\n".join(lines)
    with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    print(f"\n出力: {out}")


if __name__ == "__main__":
    main()
