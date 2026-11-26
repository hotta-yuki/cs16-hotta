"""band_rmse.py の結果（rmse_points.csv）から、学習点 1 組・テスト 1 組だけの図を描き直す。

band_rmse.py は 180 点と 200 点、test と test_spec を並べて描くが、報告では
200 点・test_spec（試験体の範囲の 80 点）だけを論じる（2026-11-26 ユーザーの依頼）。
GPR を学習し直さず、保存済みの点ごとの RMSE だけから描く（数秒で終わる）。

    python band_rmse_plot.py                        # 200 点 / test_spec
    python band_rmse_plot.py --train 180 --set test

出力（tmp_output/gpr/band_rmse/）:
    rmse_vs_params_full_<N>.png  full で学習・評価。pitch / depth / width ごとの RMSE
    band_matrix_<N>.png          学習帯域 x 評価帯域の RMSE 中央値
（--set が test_spec 以外のときはファイル名の末尾に _<set> が付く）
"""
import argparse
import csv
import os

import numpy as np

from band_rmse import C180, C200, PLOT_AXES, SEQ, plt
from featurize import _style

HERE = os.path.dirname(os.path.abspath(__file__))
BANDS = ["full", "-6dB", "-10dB", "low", "high"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="200", choices=["180", "200"])
    ap.add_argument("--set", default="test_spec", choices=["test_spec", "test"])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()
    out = os.path.join(args.sim_dir, "gpr", "band_rmse")
    col = C200 if args.train == "200" else C180
    suffix = args.train + ("" if args.set == "test_spec" else f"_{args.set}")

    rows = [r for r in csv.DictReader(open(os.path.join(out, "rmse_points.csv"), encoding="utf-8"))
            if r["train_points"] == args.train and r["set"] == args.set]
    n = len({r["name"] for r in rows})

    # ---- full / full を p, d, w に対して
    ff = [r for r in rows if r["train_band"] == "full" and r["eval_band"] == "full"]
    P = np.array([[float(r["pitch_mm"]), float(r["width_mm"]), float(r["depth_mm"])] for r in ff])
    y = np.array([float(r["rmse"]) for r in ff])

    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True, constrained_layout=True)
    for ax, (name, k, label) in zip(axs, PLOT_AXES):
        ax.scatter(P[:, k], y, s=20, color=col, alpha=0.75, lw=0, zorder=2)
        ax.set_xlabel(label)
        ax.set_ylim(0, 1.1 * y.max())
        _style(ax)
    axs[0].set_ylabel("RMSE of R")
    fig.savefig(os.path.join(out, f"rmse_vs_params_full_{suffix}.png"), dpi=150)
    plt.close(fig)

    # ---- 学習帯域 x 評価帯域
    M = np.full((len(BANDS), len(BANDS)), np.nan)
    for b in BANDS:
        for e in BANDS:
            v = [float(r["rmse"]) for r in rows if r["train_band"] == b and r["eval_band"] == e]
            if v:
                M[BANDS.index(b), BANDS.index(e)] = np.median(v)
    vmax = np.nanmax(M)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    im = ax.imshow(M, cmap=SEQ, vmin=0, vmax=vmax)
    for a in range(len(BANDS)):
        for c in range(len(BANDS)):
            v = M[a, c]
            if np.isfinite(v):
                ax.text(c, a, f"{v:.3f}", ha="center", va="center", fontsize=9,
                        color="white" if v > 0.6 * vmax else "#1f1e1c")
    ax.set_xticks(range(len(BANDS)), BANDS)
    ax.set_yticks(range(len(BANDS)), BANDS)
    ax.set_xlabel("評価帯域")
    ax.set_ylabel("学習帯域")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="RMSE 中央値（空欄 = 学習帯域の外）")
    fig.savefig(os.path.join(out, f"band_matrix_{suffix}.png"), dpi=150, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

    # 本文用の数値
    print(f"{args.train} 点 / {args.set}（{n} 点）の中央値（行 = 学習、列 = 評価）")
    for b in BANDS:
        print(f"  {b:6s} " + "  ".join("  -   " if np.isnan(v) else f"{v:.4f}" for v in M[BANDS.index(b)]))
    for name, k, label in PLOT_AXES:
        x = P[:, k]
        edges = np.linspace(x.min(), x.max(), 5)
        print(label, "  ".join(
            f"{a:.2f}-{bb:.2f}: {np.median(y[(x >= a) & ((x <= bb) if bb == edges[-1] else (x < bb))]):.4f}"
            for a, bb in zip(edges[:-1], edges[1:])))
    print(f"出力: {out}")


if __name__ == "__main__":
    main()
