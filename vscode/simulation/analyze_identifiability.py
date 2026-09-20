"""Step 0: 識別可能性の確認（矩形 Kukei のみ）

1本の A スキャン波形から (pitch, width, depth) を推定できるのかを、
既存のシミュレーション出力だけで確かめる。逆推定の手法を選ぶ前に、
そもそも情報が波形に入っているのかを見るための解析。

判定の考え方
------------
「パラメータは離れているのに波形がほぼ同じ」ペアがあれば、そこは推定不能。
問題は "ほぼ同じ" の基準をどこに置くか。数値的な差はいくらでも小さく測れるので、
**実験の繰り返し測定のばらつき（ノイズ床）** を基準にする。
実測のばらつきより小さい波形差は、実データでは区別できない。

距離の定義
----------
すべて **角距離** [rad] を使う。

    d(a, b) = arccos( <a,b> / (|a||b|) )

- 振幅で割っているので **ゲイン不変**。探触子の接触状態で振幅が変わる実データでも
  そのまま使える（`extract_features.py` の max_amplitude / energy 等はゲイン依存なので
  この用途には使えない）
- cos 距離 (1 - cos) ではなく角度にするのは、微小変化に対して **線形** に増えるため。
  1 - cos θ ≈ θ²/2 で二次になり、感度 dd/dp の評価が歪む

3 種類の距離を出す。どれが効いているかで、情報が「時間」にあるのか「形」にあるのかが分かる。

    d_cos    共通窓・ラグなし    → 到達時間の差も形の差も両方拾う
    d_shape  ラグ最適化後        → 形だけ（時間差を除去）
    d_spec   2-10 MHz の振幅スペクトル → 形のみ・位相不変

    d_cos ≫ d_shape なら、情報の大半は到達時間差にある。

使い方
------
    python vscode/simulation/analyze_identifiability.py
    python vscode/simulation/analyze_identifiability.py --sim-dir tmp_output/sim_csv

出力（既定 tmp_output/identifiability/）
    summary.txt                 判定結果のまとめ（まずこれを読む）
    pairwise_distances.csv      全ペアのパラメータ距離と波形距離
    scatter_param_vs_wave.png   ★ 中心の図。左下（パラメータは遠いが波形は近い）が縮退
    distance_matrix.png         距離行列のヒートマップ
    sensitivity_<axis>.png      各パラメータ軸に沿った波形変化
"""

import argparse
import csv
import glob
import os
import re
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:
    import japanize_matplotlib  # noqa: F401  日本語ラベル用
except ImportError:
    pass

from naming import SIM_SHAPE

# シミュレーションの時間刻み [s]。sourse_new_2 と同じ式
# （sourse_new_2 は import 時に matplotlib を引くだけで副作用は無いが、
#   この解析に必要なのは dt だけなので依存を増やさず再計算する）
_RHO, _E, _V = 7840, 206e9, 0.27
_CL = np.sqrt(_E / _RHO * (1 - _V) / (1 + _V) / (1 - 2 * _V))
SIM_DT = 1.0e-5 / _CL / np.sqrt(6)

EXP_DT = 0.5e-9      # 実験のサンプリング間隔 [s]
EXP_T_START = 5.5e-6  # 実験波形の切り出し（calculate_avg_waveforms.py と同じ）
EXP_T_END = 9.0e-6

SIM_DIR_CANDIDATES = [
    "tmp_output/sim_csv",
    "tmp_output/sim",
    "data/sim_csv",
    "vscode/simulation/tmp",
]


# ---------------------------------------------------------------- 読み込み

def parse_params(filename):
    """ファイル名から (pitch, width, depth) のコードを取り出す [mm×100]。

    小数コード (depth12.5) を取りこぼさないこと。r'depth(\\d+)' だと "12" だけ拾って
    depth 0.12 と区別できなくなる（AGENTS.md 7章）。
    """
    def _code(key):
        m = re.search(key + r"(\d+(?:\.\d+)?)", filename)
        if m is None:
            raise ValueError(f"{key} がファイル名にない: {filename}")
        v = float(m.group(1))
        return int(v) if v.is_integer() else v

    return _code("pitch"), _code("width"), _code("depth")


def find_sim_dir(explicit=None):
    if explicit:
        if not os.path.isdir(explicit):
            raise SystemExit(f"--sim-dir が存在しない: {explicit}")
        return explicit
    for d in SIM_DIR_CANDIDATES:
        if os.path.isdir(d) and glob.glob(os.path.join(d, f"{SIM_SHAPE.lower()}_cupy_*.csv")):
            return d
    raise SystemExit(
        "シミュレーション CSV が見つからない。--sim-dir で指定してください。\n"
        "  探した場所: " + ", ".join(SIM_DIR_CANDIDATES) + "\n"
        "  （macOS 側には tmp_output/ が同期されていない。研究室の Windows 機で実行）"
    )


def load_sims(sim_dir):
    """シミュレーション CSV を全部読む。返り値は params[n,3] と waves[n, L]。"""
    paths = sorted(glob.glob(os.path.join(sim_dir, f"{SIM_SHAPE.lower()}_cupy_*.csv")))
    if not paths:
        raise SystemExit(f"{sim_dir} に {SIM_SHAPE.lower()}_cupy_*.csv が無い")

    params, waves, names = [], [], []
    for p in paths:
        name = os.path.basename(p)
        try:
            pitch, width, depth = parse_params(name)
        except ValueError as e:
            print(f"  skip: {e}")
            continue
        w = np.loadtxt(p, delimiter=",")
        if w.ndim > 1:
            w = w[:, 0]
        params.append([pitch, width, depth])
        waves.append(w)
        names.append(name)

    lengths = {len(w) for w in waves}
    if len(lengths) > 1:
        L = min(lengths)
        print(f"  ! 波形長が不揃い {sorted(lengths)} → 最短 {L} に切り詰める")
        waves = [w[:L] for w in waves]

    return np.array(params, dtype=float), np.array(waves), names


# ---------------------------------------------------------------- 距離

def _unit(A):
    """行ごとに平均を引いて L2 正規化する（ゲイン・オフセット不変にする）。"""
    A = A - A.mean(axis=1, keepdims=True)
    n = np.linalg.norm(A, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return A / n


def angular_dist(A):
    """行間の角距離 [rad]。A は正規化済みでなくてよい。"""
    U = _unit(A)
    S = np.clip(U @ U.T, -1.0, 1.0)
    return np.arccos(S)


def angular_dist_lagged(A, max_lag):
    """ラグを ±max_lag の範囲で最適化した角距離 [rad]（＝形だけの距離）。

    到達時間差を取り除くので、d_cos との差が「時間に載っている情報量」になる。
    総当たりだと重いので FFT 相互相関で一括計算する。
    """
    U = _unit(A)
    n, L = U.shape
    nfft = 1 << int(np.ceil(np.log2(2 * L)))
    F = np.fft.rfft(U, n=nfft, axis=1)

    D = np.zeros((n, n))
    for i in range(n):
        # 全ペアぶんの相互相関を一度に作る
        cc = np.fft.irfft(np.conj(F[i])[None, :] * F, n=nfft, axis=1)
        # ラグ 0 は先頭、負のラグは末尾側に回り込む
        head = cc[:, : max_lag + 1]
        tail = cc[:, -max_lag:] if max_lag > 0 else cc[:, :0]
        best = np.max(np.concatenate([head, tail], axis=1), axis=1)
        D[i] = np.arccos(np.clip(best, -1.0, 1.0))
    return 0.5 * (D + D.T)   # 数値誤差ぶんの非対称を均す


def spectra(A, dt, fmin, fmax, nfft=2 ** 14):
    """2-10 MHz 帯の振幅スペクトルを返す（位相を捨てるので時間差に鈍感）。"""
    F = np.abs(np.fft.rfft(A - A.mean(axis=1, keepdims=True), n=nfft, axis=1))
    freq = np.fft.rfftfreq(nfft, d=dt)
    band = (freq >= fmin) & (freq <= fmax)
    return F[:, band]


def param_dist(P):
    """パラメータ距離。各軸をデータ範囲で 0-1 に正規化してユークリッド距離。"""
    rng = P.max(axis=0) - P.min(axis=0)
    rng[rng == 0] = 1.0
    Q = (P - P.min(axis=0)) / rng
    return np.sqrt(((Q[:, None, :] - Q[None, :, :]) ** 2).sum(axis=2))


# ---------------------------------------------------------------- ノイズ床

def load_scope(path):
    """スコープ CSV を読み、EXP_T_START..EXP_T_END の区間だけ返す。

    このデータには 2 つ癖がある。
      - 時間軸が 0 でなく 5.41 us から始まる → インデックスでなく時刻で窓を切る
      - 末尾の数行は時刻だけで電圧が空（スコープが取得長を超えて書いている）
        → genfromtxt で NaN にして落とす
    """
    try:
        d = np.genfromtxt(path, delimiter=",", skip_header=2, usecols=(0, 1))
    except Exception:
        return None
    if d.ndim != 2 or len(d) == 0:
        return None
    ok = np.isfinite(d[:, 0]) & np.isfinite(d[:, 1])
    d = d[ok]
    sel = (d[:, 0] >= EXP_T_START) & (d[:, 0] < EXP_T_END)
    v = d[sel, 1]
    return v if len(v) > 100 else None


def experimental_floor(exp_dir, index_file, fmin, fmax):
    """実験の繰り返し測定から、区別できる/できないの基準になるばらつきを測る。

    ex_index.csv の index_start..index_end は同一条件の繰り返し。その中での
    波形間距離が「同じものを測っても出てしまう差」＝ノイズ床。

    注意: この繰り返しが完全な再測定なのか、試験片上の別位置なのかは
    ex_index.csv からは読み取れない。別位置なら位置ばらつきも含んだ値になるが、
    1ショットから逆推定する前提ではむしろそちらが実用的な基準になる。
    """
    if not (os.path.isfile(index_file) and os.path.isdir(exp_dir)):
        return None

    # ex_index.csv は BOM 付き。utf-8-sig で開かないと 1 列目の名前が壊れる
    with open(index_file, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.reader(fh) if r and r[0].strip()]
    rows = rows[1:]

    per_group, all_d, all_d_spec = [], [], []
    for row in rows:
        s, e = int(row[0]), int(row[1])
        ws = []
        for i in range(s, e + 1):
            path = os.path.join(exp_dir, f"scope_{i}.csv")
            if not os.path.isfile(path):
                continue
            v = load_scope(path)
            if v is not None:
                ws.append(v)
        if len(ws) < 2:
            continue
        # 同条件でも点数が 1-2 点ずれることがあるので最短に揃える
        L = min(len(w) for w in ws)
        W = np.array([w[:L] for w in ws])
        D = angular_dist(W)
        Dspec = angular_dist(spectra(W, EXP_DT, fmin, fmax))
        iu = np.triu_indices(len(W), k=1)
        per_group.append({
            "pitch": row[2], "depth": row[3], "width": row[4],
            "n": len(W), "median": np.median(D[iu]), "p95": np.percentile(D[iu], 95),
            "median_spec": np.median(Dspec[iu]),
        })
        all_d.extend(D[iu])
        all_d_spec.extend(Dspec[iu])

    if not all_d:
        return None
    return {
        "groups": per_group,
        "median": float(np.median(all_d)),
        "p95": float(np.percentile(all_d, 95)),
        "median_spec": float(np.median(all_d_spec)),
        "p95_spec": float(np.percentile(all_d_spec, 95)),
        "n_pairs": len(all_d),
    }


# ---------------------------------------------------------------- 感度

AXES = [("pitch", 0), ("width", 1), ("depth", 2)]


def sensitivity(P, D, axis_idx):
    """1 軸だけを動かした隣り合う条件の距離から、感度 [rad/mm] を求める。

    他の 2 軸が同じ条件どうしを拾って、パラメータの差で割る。
    """
    others = [j for _, j in AXES if j != axis_idx]
    groups = {}
    for i, row in enumerate(P):
        key = (row[others[0]], row[others[1]])
        groups.setdefault(key, []).append(i)

    recs = []
    for key, idxs in groups.items():
        if len(idxs) < 2:
            continue
        idxs = sorted(idxs, key=lambda i: P[i, axis_idx])
        for a, b in zip(idxs[:-1], idxs[1:]):
            dp_mm = (P[b, axis_idx] - P[a, axis_idx]) / 100.0   # コード → mm
            if dp_mm <= 0:
                continue
            recs.append({
                "group": key, "p_from": P[a, axis_idx], "p_to": P[b, axis_idx],
                "dp_mm": dp_mm, "dist": D[a, b], "sens": D[a, b] / dp_mm,
            })
    return recs


# ---------------------------------------------------------------- 本体

def main():
    ap = argparse.ArgumentParser(description="Step 0: 識別可能性の確認（矩形のみ）")
    ap.add_argument("--sim-dir", default=None, help="シミュレーション CSV のディレクトリ")
    ap.add_argument("--out-dir", default="tmp_output/identifiability")
    ap.add_argument("--win-start", type=int, default=8000,
                    help="比較に使う窓の開始インデックス（既定 8000: 底面1次エコーの直前）")
    ap.add_argument("--win-end", type=int, default=0, help="窓の終端。0 で末尾まで")
    ap.add_argument("--max-lag", type=int, default=200,
                    help="d_shape で許すラグ [サンプル]（既定 200 ≒ 142 ns）")
    ap.add_argument("--fmin", type=float, default=2e6)
    ap.add_argument("--fmax", type=float, default=10e6)
    ap.add_argument("--exp-dir", default="vscode/simulation/data/ex_data")
    ap.add_argument("--exp-index", default="vscode/simulation/data/ex_index.csv")
    ap.add_argument("--no-exp", action="store_true", help="実験ノイズ床の算出を省く")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    log = []

    def say(s=""):
        print(s)
        log.append(s)

    sim_dir = find_sim_dir(args.sim_dir)
    say(f"シミュレーション: {sim_dir}")
    P, W_full, names = load_sims(sim_dir)
    n = len(P)
    say(f"  {n} 条件, 波形長 {W_full.shape[1]} ({W_full.shape[1] * SIM_DT * 1e6:.2f} us)")

    i1 = args.win_end if args.win_end > 0 else W_full.shape[1]
    W = W_full[:, args.win_start:i1]
    e_win = (W ** 2).sum() / (W_full ** 2).sum()
    say(f"  窓 [{args.win_start}, {i1}) = "
        f"{args.win_start * SIM_DT * 1e6:.2f}-{i1 * SIM_DT * 1e6:.2f} us, "
        f"全エネルギーの {e_win * 100:.1f}%")

    for nm, j in AXES:
        vals = sorted(set(P[:, j]))
        say(f"  {nm}: {len(vals)} 水準 [{', '.join(f'{v / 100:g}' for v in vals)}] mm")
    say()

    # --- 距離
    Dp = param_dist(P)
    Dcos = angular_dist(W)
    Dshape = angular_dist_lagged(W, args.max_lag)
    Dspec = angular_dist(spectra(W, SIM_DT, args.fmin, args.fmax))
    metrics = {"d_cos": Dcos, "d_shape": Dshape, "d_spec": Dspec}

    iu = np.triu_indices(n, k=1)
    say("波形距離 [rad]（中央値 / 最小）")
    for k, D in metrics.items():
        say(f"  {k:8s} {np.median(D[iu]):.4f} / {D[iu].min():.4f}")
    if np.median(Dcos[iu]) > 0:
        say(f"  → d_shape / d_cos = {np.median(Dshape[iu]) / np.median(Dcos[iu]):.2f} "
            f"（小さいほど到達時間差に情報が載っている）")
    say()

    # --- ノイズ床
    floor = None
    if not args.no_exp:
        floor = experimental_floor(args.exp_dir, args.exp_index, args.fmin, args.fmax)
    if floor:
        say(f"実験の繰り返しばらつき（ノイズ床, {floor['n_pairs']} ペア）")
        say(f"  時間波形   中央値 {floor['median']:.4f} rad, 95% {floor['p95']:.4f} rad")
        say(f"  スペクトル 中央値 {floor['median_spec']:.4f} rad, 95% {floor['p95_spec']:.4f} rad")
        say("  注意: 時間波形の床は実験 0.5ns / シミュ 0.712ns でサンプリングが違うため概算。")
        say("        帯域を揃えているスペクトル側のほうが比較として素直。")
        floor_t, floor_s = floor["median"], floor["median_spec"]
    else:
        say("実験ノイズ床: 算出せず（データ無し or --no-exp）。")
        say("  基準が無いので以下は相対評価にとどまる。")
        floor_t = floor_s = None
    say()

    # --- 感度と分解能
    say("パラメータ感度と、ノイズ床から決まる分解能")
    say(f"  {'axis':6s} {'感度[rad/mm]':>14s} {'d_cos 分解能[mm]':>18s} {'d_spec 分解能[mm]':>18s}")
    sens_summary = {}
    for nm, j in AXES:
        rc = sensitivity(P, Dcos, j)
        rs = sensitivity(P, Dspec, j)
        if not rc:
            say(f"  {nm:6s} {'—':>14s}  （1 軸だけ動かした組が無い）")
            continue
        vals_c = [r["sens"] for r in rc]
        s_cos = float(np.median(vals_c))
        s_spec = float(np.median([r["sens"] for r in rs])) if rs else np.nan
        res_c = floor_t / s_cos if (floor_t and s_cos > 0) else np.nan
        res_s = floor_s / s_spec if (floor_s and s_spec > 0) else np.nan
        sens_summary[nm] = {"cos": s_cos, "spec": s_spec, "res_cos": res_c, "res_spec": res_s}
        say(f"  {nm:6s} {s_cos:14.3f} {res_c:18.4f} {res_s:18.4f}"
            f"   （{len(vals_c)} 組, 幅 {min(vals_c):.3f}-{max(vals_c):.3f}）")
    say("  分解能 = ノイズ床 / 感度。この値より細かい差は実データでは区別できない。")
    say("  感度は隣接する 2 条件の距離 / パラメータ差。組ごとの幅が大きいときは")
    say("  距離が線形に増えていない（＝飽和している）ので、分解能の値を鵜呑みにしない。")
    say("  d_spec 側の分解能が d_cos より大幅に悪いなら、情報は位相・到達時間に載っている。")
    say()

    # --- 縮退ペア
    if floor_t is not None:
        deg = [(i, j) for i, j in zip(*iu)
               if Dcos[i, j] < floor_t and Dp[i, j] > 0.1]
        say(f"縮退の疑いがあるペア（波形距離 < ノイズ床 かつ パラメータ距離 > 0.1）: {len(deg)} 組")
        for i, j in sorted(deg, key=lambda t: -Dp[t])[:15]:
            say(f"  d_wave={Dcos[i, j]:.4f} d_param={Dp[i, j]:.3f}  "
                f"p{P[i,0]:g}/w{P[i,1]:g}/d{P[i,2]:g}  vs  p{P[j,0]:g}/w{P[j,1]:g}/d{P[j,2]:g}")
        if len(deg) > 15:
            say(f"  ... 他 {len(deg) - 15} 組（pairwise_distances.csv 参照）")
        say()

    # --- 最近傍の一致
    Dw = Dcos.copy()
    np.fill_diagonal(Dw, np.inf)
    Dpi = Dp.copy()
    np.fill_diagonal(Dpi, np.inf)
    agree = sum(1 for i in range(n) if np.argmin(Dw[i]) == np.argmin(Dpi[i]))
    say(f"最近傍の一致率: {agree}/{n} = {agree / n * 100:.0f}%")
    say("  （波形が最も近い相手 == パラメータが最も近い相手。低いほど逆問題が不安定）")
    say()

    # --- 保存
    with open(os.path.join(args.out_dir, "pairwise_distances.csv"),
              "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["file_i", "file_j", "pitch_i", "width_i", "depth_i",
                     "pitch_j", "width_j", "depth_j",
                     "d_param", "d_cos", "d_shape", "d_spec"])
        for i, j in zip(*iu):
            wr.writerow([names[i], names[j],
                         P[i, 0], P[i, 1], P[i, 2], P[j, 0], P[j, 1], P[j, 2],
                         f"{Dp[i, j]:.6f}", f"{Dcos[i, j]:.6f}",
                         f"{Dshape[i, j]:.6f}", f"{Dspec[i, j]:.6f}"])

    # 図1: パラメータ距離 vs 波形距離（この解析の中心）
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=True)
    for ax, (k, D) in zip(axes, metrics.items()):
        ax.scatter(Dp[iu], D[iu], s=12, alpha=0.45, edgecolors="none")
        fl = floor_s if k == "d_spec" else floor_t
        if fl is not None:
            ax.axhline(fl, color="crimson", ls="--", lw=1.4,
                       label=f"実験ノイズ床 {fl:.3f}")
            ax.legend(fontsize=9)
        ax.set_xlabel("パラメータ距離（正規化）")
        ax.set_ylabel(f"{k} [rad]")
        ax.set_title(k)
        ax.grid(alpha=0.3)
    fig.suptitle("パラメータ距離 vs 波形距離 — 右下（パラメータは遠いのに波形が近い）が縮退")
    fig.tight_layout()
    fig.savefig(os.path.join(args.out_dir, "scatter_param_vs_wave.png"), dpi=140)
    plt.close(fig)

    # 図2: 距離行列
    order = np.lexsort((P[:, 1], P[:, 2], P[:, 0]))  # pitch → depth → width
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(Dcos[np.ix_(order, order)], cmap="viridis")
    ax.set_title("d_cos 距離行列（pitch → depth → width 順）")
    fig.colorbar(im, ax=ax, label="角距離 [rad]")
    fig.tight_layout()
    fig.savefig(os.path.join(args.out_dir, "distance_matrix.png"), dpi=140)
    plt.close(fig)

    # 図3: 軸ごとの感度
    for nm, j in AXES:
        recs = sensitivity(P, Dcos, j)
        if not recs:
            continue
        fig, ax = plt.subplots(figsize=(7, 5))
        for r in recs:
            ax.plot([r["p_from"] / 100, r["p_to"] / 100], [0, r["dist"]],
                    marker="o", ms=3, alpha=0.5)
        if floor_t is not None:
            ax.axhline(floor_t, color="crimson", ls="--", lw=1.4, label="実験ノイズ床")
            ax.legend()
        ax.set_xlabel(f"{nm} [mm]")
        ax.set_ylabel("隣接条件との d_cos [rad]")
        ax.set_title(f"{nm} を 1 段階動かしたときの波形変化")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(args.out_dir, f"sensitivity_{nm}.png"), dpi=140)
        plt.close(fig)

    with open(os.path.join(args.out_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    say(f"出力: {args.out_dir}/")


if __name__ == "__main__":
    main()
