"""教師データの点数を変えた PCA の累積寄与率を 1 枚に重ねる（学習曲線・報告用）。

    python vscode/surrogate/plot_pca_compare.py                 # 60 点と 180 点
    python vscode/surrogate/plot_pca_compare.py --n 60 100 160 180

先に featurize.py --set train --phase 1 4 --first N --peak smooth で各 N の
features/train_ph14_first<N>_refpeak/features.npz を作っておくこと。

出力: vscode/surrogate/tmp_output/features/pca_compare/pca_cumulative_<N...>.png
"""

import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import featurize as f   # 図の書式（色・日本語フォント）を揃える
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

FEAT = os.path.join(HERE, "tmp_output", "features")
COLORS = {60: f.C_IM, 100: "#86b6ef", 160: "#3987e5", 180: f.C_RE}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", nargs="+", type=int, default=[60, 180])
    ap.add_argument("--jmax", type=int, default=25)
    args = ap.parse_args()

    fig, ax = plt.subplots(figsize=(7, 4.5), layout="constrained")
    for n in args.n:
        z = np.load(os.path.join(FEAT, f"train_ph14_first{n}_refpeak", "features.npz"))
        cum = np.cumsum(z["pca_ratio"])[:args.jmax] * 100
        J99 = int(np.searchsorted(cum, 99.0) + 1)
        k = np.arange(1, len(cum) + 1)
        ax.plot(k, cum, marker="o", markersize=4, linewidth=2, color=COLORS.get(n, "#52514e"),
                label=f"教師データ {n} 点（99% は J = {J99}）")
        ax.plot([J99], [cum[J99 - 1]], marker="o", markersize=9, markerfacecolor="none",
                color=COLORS.get(n, "#52514e"))
    ax.axhline(99, color="#52514e", linestyle="--", linewidth=1)
    ax.text(1, 99, "99%", va="bottom", ha="left", color="#52514e")
    ax.set_xlim(0.5, args.jmax + 0.5)
    ax.set_ylim(50, 100.5)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("主成分の数 J")
    ax.set_ylabel("累積寄与率 [%]")
    ax.legend(frameon=False, loc="lower right")
    f._style(ax)

    # 90-100% の拡大（差が見えるのはこの範囲）
    ins = ax.inset_axes([0.42, 0.30, 0.55, 0.38])
    for n in args.n:
        z = np.load(os.path.join(FEAT, f"train_ph14_first{n}_refpeak", "features.npz"))
        cum = np.cumsum(z["pca_ratio"])[:args.jmax] * 100
        ins.plot(np.arange(1, len(cum) + 1), cum, marker="o", markersize=3, linewidth=1.5,
                 color=COLORS.get(n, "#52514e"))
    ins.axhline(99, color="#52514e", linestyle="--", linewidth=0.8)
    ins.set_xlim(9.5, 21.5)
    ins.set_ylim(94, 100.2)
    ins.xaxis.set_major_locator(MaxNLocator(integer=True))
    ins.tick_params(labelsize=8)
    f._style(ins)

    out = os.path.join(FEAT, "pca_compare")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "pca_cumulative_" + "_".join(map(str, args.n)) + ".png")
    fig.savefig(path, dpi=150)
    print(path)


if __name__ == "__main__":
    main()
