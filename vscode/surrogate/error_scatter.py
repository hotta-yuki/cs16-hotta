"""GPR の誤差 eps_D を p, w, d ごとの散布図にする（どの領域が苦手かを見る）。

全域（full）で学習した GPR を test_spec（試験体の範囲の 80 点）で評価し、
    error_pairs.png        p-d / p-w / w-d の平面に点を置き、eps_D を色で示す（ノイズ超えは輪で囲む）
    error_vs_param_bands.png  評価帯域（full / -6dB / -10dB / low / high）ごとに eps_D を p, w, d に対して
を描く。eps_D の和は評価帯域の周波数点だけでとり、実験ノイズも同じ帯域で計算し直す
（band_error_plot.py と同じ）。

    python error_scatter.py                # 200 点モデル
    python error_scatter.py --model train_ph14_first180_refpeak_J17_invp_duty

出力: tmp_output/gpr/<model>/specimen_range_<set>/
"""
import argparse
import os
import sys
from types import SimpleNamespace

import joblib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

from band_rmse import SEQ, bands_from_ref, mask_of
from eval_specimen_range import plt
from featurize import C_RE, _style
from reconstruct import experimental_noise
from train_gpr import load_set, normalize, to_R

INK = "#1f1e1c"
LABELS = {0: "p [mm]", 1: "w [mm]", 2: "d [mm]"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="train_ph14_adapt1_refpeak_J17_invp_duty")
    ap.add_argument("--set", default="test_spec")
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()
    phase = [6] if args.set == "test_spec" else [2, 5]

    mdir = os.path.join(args.sim_dir, "gpr", args.model)
    mz = np.load(os.path.join(mdir, "model.npz"))
    jb = joblib.load(os.path.join(mdir, "model.joblib"))
    fz = np.load(os.path.join(args.sim_dir, "features", args.model.split("_J")[0], "features.npz"))
    freq, X_ref = fz["freq"], fz["X_ref"]
    t_ref = float(fz["t_ref"]) if "t_ref" in fz.files and np.isfinite(fz["t_ref"]) else None
    K = len(freq)

    la = SimpleNamespace(design=os.path.join(HERE, "design.csv"), set=[args.set], phase=phase,
                         sim_dir=args.sim_dir)
    _, P, X = load_set(la, fz, freq, X_ref, t_ref)
    R = to_R(X, K)
    Z = np.stack([g.predict(normalize(P, jb["inputs"])) for g in jb["models"]], 1)
    Rp = to_R(mz["pca_mean"] + Z @ mz["pca_components"], K)
    E, D = (Rp - R) * X_ref, R * X_ref

    bands = bands_from_ref(freq, X_ref)
    res = {}
    for b, rng in bands.items():
        m = mask_of(freq, rng)
        e = np.linalg.norm(E[:, m], axis=1) / np.linalg.norm(D[:, m], axis=1)
        n = float(np.median(experimental_noise(freq[m])[1]))
        res[b] = (e, n, rng)

    out = os.path.join(mdir, f"specimen_range_{args.set}")
    os.makedirs(out, exist_ok=True)

    # ---- 2 次元の散布図（full）
    e, n, _ = res["full"]
    over = e >= n
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.3), layout="constrained")
    for ax, (i, j) in zip(axs, [(0, 2), (0, 1), (1, 2)]):
        order = np.argsort(e)                      # 誤差の大きい点を上に描く
        sc = ax.scatter(P[order, i], P[order, j], c=e[order], cmap=SEQ, vmin=0, vmax=e.max(),
                        s=46, edgecolors="white", linewidths=0.6, zorder=2)
        ax.scatter(P[over, i], P[over, j], s=150, facecolors="none", edgecolors=INK, linewidths=1.4,
                   zorder=3, label=f"実験ノイズ {n:.3f} 以上")
        ax.set_xlabel(LABELS[i])
        ax.set_ylabel(LABELS[j])
        _style(ax)
    if over.any():
        axs[0].legend(fontsize=8, loc="upper right")
    fig.colorbar(sc, ax=axs, shrink=0.85, label="eps_D（GPR vs FDTD）")
    fig.suptitle(f"GPRの誤差の分布（全域で学習・評価、{args.set} {len(P)} 点）")
    fig.savefig(os.path.join(out, "error_pairs.png"), dpi=150)
    plt.close(fig)

    # ---- 評価帯域ごとの 1 次元散布図
    names = list(bands)
    ymax = 1.1 * max(max(r[0].max(), r[1]) for r in res.values())
    fig, axs = plt.subplots(len(names), 3, figsize=(13, 2.5 * len(names)), sharey=True,
                            layout="constrained")
    for row, b in zip(axs, names):
        e, n, (lo, hi) = res[b]
        for k, ax in enumerate(row):
            ax.scatter(P[:, k], e, s=16, color=C_RE, zorder=3)
            ax.axhline(n, color="#52514e", linestyle="--", linewidth=1)
            ax.set_ylim(0, ymax)
            _style(ax)
            if b == names[-1]:
                ax.set_xlabel(LABELS[k])
        row[0].set_ylabel("eps_D")
        row[0].set_title(f"評価 {b}（{lo / 1e6:.2f}-{hi / 1e6:.2f} MHz）  中央値 {np.median(e):.3f}  "
                         f"最大 {e.max():.3f}  破線 = 同じ帯域の実験ノイズ {n:.3f}  "
                         f"ノイズ未満 {int((e < n).sum())}/{len(e)}", loc="left", fontsize=9)
    fig.suptitle(f"評価帯域ごとの GPR の誤差（全域で学習、{args.set} {len(P)} 点）")
    fig.savefig(os.path.join(out, "error_vs_param_bands.png"), dpi=130)
    plt.close(fig)

    for b in names:
        e, n, (lo, hi) = res[b]
        i = int(np.argmax(e))
        print(f"{b:6s} {lo / 1e6:.2f}-{hi / 1e6:.2f}  中央値 {np.median(e):.4f}  95% {np.percentile(e, 95):.4f}  "
              f"最大 {e.max():.4f}（p {P[i, 0]:.2f} w {P[i, 1]:.2f} d {P[i, 2]:.2f}）  ノイズ {n:.4f}  "
              f"未満 {int((e < n).sum())}/{len(e)}")
    print(f"出力: {out}")


if __name__ == "__main__":
    main()
