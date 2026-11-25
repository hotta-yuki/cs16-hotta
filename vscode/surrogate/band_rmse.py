"""学習点 180 / 200 と、学習・評価の周波数帯を変えたときの GPR 予測の RMSE を比べる。

    python vscode/surrogate/band_rmse.py                  # 5 帯域 x 2 学習集合（10 モデル、約 10 分）
    python vscode/surrogate/band_rmse.py --restarts 2     # 試しに速く回す

比べるもの
----
- 学習集合: train 180 点（phase 1 4）と、それに adapt1 20 点（phase 7）を足した 200 点
- 学習帯域 B: 平滑面スペクトル |X_ref| から決める 5 通り
    full   2.00-7.75 MHz（featurize.py の解析帯域。今のモデル）
    -6dB   |X_ref| が最大の 1/2 以上
    -10dB  |X_ref| が最大の 1/sqrt(10) 以上
    low    2.00 MHz-ピーク
    high   ピーク-7.75 MHz
  帯域ごとに PCA から作り直し、GPR（train_gpr.py と同じ Matérn 5/2 ARD、入力 invp_duty）を学習する。
  主成分の数 J は、full の J = 17 と同じ累積寄与率に届く最小の数（帯域が狭いほど少なくなる）
- 評価帯域 E: 上の 5 帯域のうち、学習帯域 B の内側に入るもの（B の外は予測していないので評価できない）
- 評価点: test（設計の箱全体の LHS、phase 2 5、50 点）と test_spec（試験体の範囲、phase 6、80 点）。
  どちらも学習には使っていない

RMSE = sqrt( mean_f |R_pred(f) - R(f)|^2 )   f は評価帯域の周波数点、R = D / D_smooth（複素数）
R は無次元。|R| は周波数で大きさが違う（full で 0.06-1.4）ので、評価帯域が違う RMSE どうしは
絶対値ではなく、同じ評価帯域の中で学習集合・学習帯域を比べるのに使う。

R の作り方は featurize.py と同じ（--peak smooth、0.05 MHz 刻み）。最初に full の R が
features/train_ph14_first180_refpeak/features.npz と一致することを確かめてから進む。
寸法は design.csv の実寸法（_m 列、メッシュに刻んだ後）を使う。

出力（vscode/surrogate/tmp_output/gpr/band_rmse/）
    summary.txt                 まずこれを読む。帯域・J・RMSE の表
    rmse_vs_params_full.png     full で学習・評価したときの pitch / depth / width vs RMSE（180 と 200）
    rmse_vs_params_train.png    学習帯域ごと（評価帯域 = 学習帯域）
    rmse_vs_params_eval.png     full で学習し、評価帯域だけ変えたもの
    band_matrix.png             学習帯域 x 評価帯域の RMSE 中央値（180 / 200、test_spec / test）
    rmse_points.csv             全組み合わせの点ごとの RMSE
"""

import argparse
import csv
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
try:
    import japanize_matplotlib  # noqa: F401
except ImportError:
    pass

from eval_specimen_range import specimen_box
from featurize import GRID, _style, cut, freq_grid, load_wave, pca, spectrum
from gpr import GPR
from run_design import out_name
from train_gpr import KEYS, normalize

INPUTS = "invp_duty"
J_FULL = 17
C180, C200 = "#2a78d6", "#eb6834"      # dataviz 既定の系列 1・2（validate_palette で PASS）
C_BOX = "#efe9dc"
SEQ = LinearSegmentedColormap.from_list("blue_seq", ["#f5f8fc", "#86b6ef", "#3987e5", "#184f95", "#0d366b"])
TRAIN_SETS = {"180": (["train"], [1, 4]), "200": (["train", "adapt1"], [1, 4, 7])}
TEST_SETS = {"test": (["test"], [2, 5]), "test_spec": (["test_spec"], [6])}
PLOT_AXES = [("pitch", 0, "pitch [mm]"), ("depth", 2, "depth [mm]"), ("width", 1, "width [mm]")]


def select(rows, sets, phases):
    sel = [r for r in rows if r["set"] in sets and int(r["phase"]) in phases]
    return sorted(sel, key=lambda r: (int(r["phase"]), int(r["order"])))


def bands_from_ref(freq, X_ref):
    """|X_ref| から 5 帯域を決める。返り値は {名前: (f_lo, f_hi)}（グリッド上の値）。"""
    a = np.abs(X_ref)
    k0 = int(np.argmax(a))

    def contiguous(level):
        lo = k0
        while lo > 0 and a[lo - 1] >= level * a[k0]:
            lo -= 1
        hi = k0
        while hi < len(a) - 1 and a[hi + 1] >= level * a[k0]:
            hi += 1
        return freq[lo], freq[hi]

    return {
        "full": (freq[0], freq[-1]),
        "-6dB": contiguous(0.5),
        "-10dB": contiguous(10 ** -0.5),
        "low": (freq[0], freq[k0]),
        "high": (freq[k0], freq[-1]),
    }


def mask_of(freq, band):
    return (freq >= band[0] - 1e-3) & (freq <= band[1] + 1e-3)


def load_R(rows, sim_dir, freq, X_ref, t_ref):
    P, R, names = [], [], []
    for r in rows:
        fn = out_name(r, float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"]))
        t, w = load_wave(os.path.join(sim_dir, fn))
        R.append(spectrum(t, w, freq, t_ref) / X_ref)
        P.append([float(r[k + "_m"]) * 1e3 for k in KEYS])
        names.append(fn)
    return np.array(P), np.array(R), names


def fit_predict(P_tr, R_tr, P_te, m_band, J, restarts):
    """帯域 m_band の [Re, Im] で PCA -> J 本の GPR -> テスト点の R（帯域内）を返す。"""
    X = np.concatenate([R_tr[:, m_band].real, R_tr[:, m_band].imag], axis=1)
    mean, V, _ = pca(X)
    V = V[:J]
    Z = (X - mean) @ V.T
    U_tr, U_te = normalize(P_tr, INPUTS), normalize(P_te, INPUTS)
    Zp = np.stack([GPR(n_restarts=restarts, seed=j).fit(U_tr, Z[:, j]).predict(U_te)
                   for j in range(J)], 1)
    Xp = mean + Zp @ V
    K = int(m_band.sum())
    return Xp[:, :K] + 1j * Xp[:, K:]


def j_for(R_tr, m_band, target):
    X = np.concatenate([R_tr[:, m_band].real, R_tr[:, m_band].imag], axis=1)
    cum = np.cumsum(pca(X)[2])
    return int(np.searchsorted(cum, target - 1e-12) + 1)


def rmse(Rp, R):
    return np.sqrt(np.mean(np.abs(Rp - R) ** 2, axis=1))


def binned_median(x, y, edges):
    c, m = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = (x >= a) & (x <= b if b == edges[-1] else x < b)
        if s.sum() >= 3:
            c.append(0.5 * (a + b))
            m.append(np.median(y[s]))
    return np.array(c), np.array(m)


def panel_row(axs, P_te, res, spec_lo, spec_hi, ymax, title=None):
    """1 行 3 枚（pitch / depth / width）。res = {"180": rmse, "200": rmse}。"""
    is_spec = res["_is_spec"]
    for ax, (name, k, label) in zip(axs, PLOT_AXES):
        ax.axvspan(spec_lo[k], spec_hi[k], color=C_BOX, zorder=0, lw=0)
        x = P_te[:, k]
        lo, hi = x.min(), x.max()
        edges = np.linspace(lo, hi, 7)
        for key, col in (("180", C180), ("200", C200)):
            y = res[key]
            ax.scatter(x[is_spec], y[is_spec], s=18, color=col, alpha=0.55, lw=0,
                       label=f"{key} 点 test_spec" if name == "pitch" else None, zorder=2)
            ax.scatter(x[~is_spec], y[~is_spec], s=18, facecolor="none", edgecolor=col, alpha=0.8, lw=1,
                       label=f"{key} 点 test" if name == "pitch" else None, zorder=2)
            c, m = binned_median(x, y, edges)
            ax.plot(c, m, color=col, lw=2, zorder=3, label=f"{key} 点 中央値" if name == "pitch" else None)
        ax.set_xlabel(label)
        ax.set_ylim(0, ymax)
        _style(ax)
    axs[0].set_ylabel("RMSE of R")
    if title:
        axs[0].set_title(title, loc="left", fontsize=10)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--restarts", type=int, default=8, help="train_gpr.py と同じ既定 8")
    args = ap.parse_args()

    out = os.path.join(args.sim_dir, "gpr", "band_rmse")
    os.makedirs(out, exist_ok=True)
    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))

    # ---- R（featurize.py と同じ作り方、full のグリッドで 1 回だけ）
    freq = freq_grid()
    ref = [r for r in rows if r["set"] == "smooth"][0]
    t_s, w_s = load_wave(os.path.join(args.sim_dir, out_name(ref, float(ref["pitch_m"]), float(ref["width_m"]), float(ref["depth_m"]))))
    X_ref = spectrum(t_s, w_s, freq)
    t_ref = cut(t_s, w_s)[0]

    data = {}
    for key, (sets, phases) in {**TRAIN_SETS, **TEST_SETS}.items():
        data[key] = load_R(select(rows, sets, phases), args.sim_dir, freq, X_ref, t_ref)
        print(f"  {key}: {len(data[key][0])} 点", flush=True)

    # 既存の特徴量と一致するか（作り方を取り違えていないことの確認）
    fz = np.load(os.path.join(args.sim_dir, "features", "train_ph14_first180_refpeak", "features.npz"))
    order = {n: i for i, n in enumerate(data["180"][2])}
    idx = [order[n] for n in fz["names"]]
    dev = np.abs(data["180"][1][idx] - fz["H"]).max()
    if dev > 1e-9 or not np.allclose(data["180"][0][idx], fz["params_mm"]):
        raise SystemExit(f"features.npz と一致しない（最大差 {dev:.2e}）")
    print(f"  features.npz と一致（最大差 {dev:.1e}）", flush=True)

    bands = bands_from_ref(freq, X_ref)
    masks = {b: mask_of(freq, v) for b, v in bands.items()}

    # J: full の J_FULL と同じ累積寄与率（180 点の PCA で決め、200 点にも同じ J を使う）
    X180 = np.concatenate([data["180"][1].real, data["180"][1].imag], axis=1)
    target = float(np.cumsum(pca(X180)[2])[J_FULL - 1])
    Js = {b: j_for(data["180"][1], masks[b], target) for b in bands}

    P_te = np.concatenate([data["test"][0], data["test_spec"][0]])
    R_te = np.concatenate([data["test"][1], data["test_spec"][1]])
    names_te = data["test"][2] + data["test_spec"][2]
    is_spec = np.r_[np.zeros(len(data["test"][0]), bool), np.ones(len(data["test_spec"][0]), bool)]

    # ---- 学習と評価
    res = {}          # (model, train_band, eval_band) -> RMSE（テスト 130 点）
    t0 = time.time()
    for b, mb in masks.items():
        for key in TRAIN_SETS:
            P_tr, R_tr, _ = data[key]
            Rp_b = fit_predict(P_tr, R_tr, P_te, mb, Js[b], args.restarts)
            full_p = np.full(R_te.shape, np.nan, complex)
            full_p[:, mb] = Rp_b
            for e, me in masks.items():
                if np.all(mb[me]):           # E が B の内側
                    res[(key, b, e)] = rmse(full_p[:, me], R_te[:, me])
            print(f"  学習 {key} 点 / {b:5s}（J = {Js[b]:2d}）  {time.time() - t0:5.0f} s", flush=True)

    # ---- CSV
    with open(os.path.join(out, "rmse_points.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["train_points", "train_band", "eval_band", "set", "name",
                     "pitch_mm", "width_mm", "depth_mm", "rmse"])
        for (key, b, e), r in res.items():
            for i in range(len(r)):
                wr.writerow([key, b, e, "test_spec" if is_spec[i] else "test", names_te[i],
                             *np.round(P_te[i], 4), f"{r[i]:.6f}"])

    # ---- summary.txt
    spec_lo, spec_hi, _ = specimen_box()
    L = [f"学習: 180 点（train phase 1 4）/ 200 点（+ adapt1 phase 7）  入力 {INPUTS}  restarts {args.restarts}",
         f"評価: test 50 点（箱全体）+ test_spec 80 点（試験体の範囲）。RMSE = sqrt(mean_f |R_pred - R|^2)",
         f"J は full の J = {J_FULL} と同じ累積寄与率 {target * 100:.3f}%（180 点の PCA）に届く最小の数",
         f"features.npz（train_ph14_first180_refpeak）との R の最大差 {dev:.1e}",
         "",
         "---- 帯域（平滑面 |X_ref| から。ピーク "
         f"{freq[int(np.argmax(np.abs(X_ref)))] / 1e6:.2f} MHz）----",
         "  名前      範囲 [MHz]      点数    J"]
    for b, (lo, hi) in bands.items():
        L.append(f"  {b:6s}  {lo / 1e6:5.2f}-{hi / 1e6:5.2f}     {int(masks[b].sum()):4d}   {Js[b]:3d}")

    def stat(r):
        return f"{np.median(r):.4f}  {np.percentile(r, 95):.4f}  {r.max():.4f}"

    for setname, sm in (("test_spec（試験体の範囲、80 点）", is_spec), ("test（箱全体、50 点）", ~is_spec)):
        L += ["", f"---- RMSE {setname}：中央値  95%点  最大 ----",
              "  学習帯域  評価帯域  |  180 点                     |  200 点                     |  中央値 200/180"]
        for (key, b, e) in res:
            if key != "180":
                continue
            a, c = res[("180", b, e)][sm], res[("200", b, e)][sm]
            L.append(f"  {b:7s}   {e:7s}  |  {stat(a)}  |  {stat(c)}  |  {np.median(c) / np.median(a):.3f}")

    # pitch / depth / width で区切った中央値（full / full）。区間は右端を含まない（最後だけ含む）
    L += ["", "---- full で学習・評価、パラメータの区間ごとの RMSE 中央値（test + test_spec）----"]
    for name, k, label in PLOT_AXES:
        x = P_te[:, k]
        edges = np.linspace(x.min(), x.max(), 5)
        L.append(f"  {label}")
        for a, bb in zip(edges[:-1], edges[1:]):
            s = (x >= a) & ((x <= bb) if bb == edges[-1] else (x < bb))
            L.append(f"    {a:.2f}-{bb:.2f}  {int(s.sum()):3d} 点   180: {np.median(res[('180', 'full', 'full')][s]):.4f}"
                     f"   200: {np.median(res[('200', 'full', 'full')][s]):.4f}")
    open(os.path.join(out, "summary.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))

    # ---- 図
    def pair(b, e):
        return {"180": res[("180", b, e)], "200": res[("200", b, e)], "_is_spec": is_spec}

    def legend_once(fig, ax):
        h, lab = ax.get_legend_handles_labels()
        fig.legend(h, lab, loc="upper center", ncol=6, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.0))

    # full / full
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True, constrained_layout=True)
    r = pair("full", "full")
    panel_row(axs, P_te, r, spec_lo, spec_hi, 1.05 * max(r["180"].max(), r["200"].max()),
              "学習・評価とも full（2.00-7.75 MHz）。薄い帯 = 試験体の範囲")
    legend_once(fig, axs[0])
    fig.get_layout_engine().set(rect=(0, 0, 1, 0.9))
    fig.savefig(os.path.join(out, "rmse_vs_params_full.png"), dpi=150)
    plt.close(fig)

    # 学習帯域ごと（E = B）、評価帯域ごと（B = full）
    for fname, combos in (("rmse_vs_params_train.png", [(b, b) for b in bands]),
                          ("rmse_vs_params_eval.png", [("full", e) for e in bands])):
        fig, axs = plt.subplots(len(combos), 3, figsize=(12, 2.9 * len(combos)), sharey="row",
                                constrained_layout=True)
        for row, (b, e) in zip(axs, combos):
            r = pair(b, e)
            lo, hi = bands[e]
            panel_row(row, P_te, r, spec_lo, spec_hi, 1.05 * max(r["180"].max(), r["200"].max()),
                      f"学習 {b}（J = {Js[b]}）／評価 {e} {lo / 1e6:.2f}-{hi / 1e6:.2f} MHz")
        legend_once(fig, axs[0, 0])
        fig.get_layout_engine().set(rect=(0, 0, 1, 1 - 0.25 / len(combos)))
        fig.savefig(os.path.join(out, fname), dpi=130)
        plt.close(fig)

    # 学習帯域 x 評価帯域の中央値
    names = list(bands)
    fig, axs = plt.subplots(2, 2, figsize=(10, 8.4), constrained_layout=True)
    for i, (setname, sm) in enumerate((("test_spec", is_spec), ("test", ~is_spec))):
        M = {key: np.full((len(names), len(names)), np.nan) for key in TRAIN_SETS}
        for (key, b, e), r in res.items():
            M[key][names.index(b), names.index(e)] = np.median(r[sm])
        vmax = np.nanmax([np.nanmax(m) for m in M.values()])
        for j, key in enumerate(TRAIN_SETS):
            ax = axs[i, j]
            im = ax.imshow(M[key], cmap=SEQ, vmin=0, vmax=vmax)
            for a in range(len(names)):
                for c in range(len(names)):
                    v = M[key][a, c]
                    if np.isfinite(v):
                        ax.text(c, a, f"{v:.3f}", ha="center", va="center", fontsize=8,
                                color="white" if v > 0.6 * vmax else "#1f1e1c")
            ax.set_xticks(range(len(names)), names)
            ax.set_yticks(range(len(names)), names)
            ax.set_xlabel("評価帯域")
            ax.set_ylabel("学習帯域")
            ax.set_title(f"{key} 点 / {setname}（RMSE 中央値、空欄 = 学習帯域の外）", loc="left", fontsize=9)
            ax.tick_params(length=0)
            for s in ax.spines.values():
                s.set_visible(False)
        fig.colorbar(im, ax=axs[i, :], shrink=0.8, label="RMSE 中央値")
    fig.savefig(os.path.join(out, "band_matrix.png"), dpi=150)
    plt.close(fig)

    print(f"\n出力: {out}")


if __name__ == "__main__":
    main()
