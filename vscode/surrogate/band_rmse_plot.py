"""band_rmse.py の結果（rmse_points.csv）から、学習点 1 組だけの図を描き直す。

band_rmse.py は 180 点と 200 点を並べて描くが、報告では 200 点だけを論じることがある。
GPR を学習し直さず、保存済みの点ごとの RMSE だけから描く（数秒で終わる）。

    python band_rmse_plot.py              # 200 点
    python band_rmse_plot.py --train 180

出力（tmp_output/gpr/band_rmse/）:
    rmse_vs_params_full_<N>.png  full で学習・評価。pitch / depth / width ごとの RMSE
    band_matrix_<N>.png          学習帯域 x 評価帯域の RMSE 中央値（test_spec / test）
"""
import argparse
import csv
import os

import numpy as np

from band_rmse import C180, C200, C_BOX, PLOT_AXES, SEQ, plt
from eval_specimen_range import specimen_box
from featurize import _style

HERE = os.path.dirname(os.path.abspath(__file__))
BANDS = ["full", "-6dB", "-10dB", "low", "high"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="200", choices=["180", "200"])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()
    out = os.path.join(args.sim_dir, "gpr", "band_rmse")
    col = C200 if args.train == "200" else C180

    rows = [r for r in csv.DictReader(open(os.path.join(out, "rmse_points.csv"), encoding="utf-8"))
            if r["train_points"] == args.train]

    # ---- full / full を p, d, w に対して
    ff = [r for r in rows if r["train_band"] == "full" and r["eval_band"] == "full"]
    P = np.array([[float(r["pitch_mm"]), float(r["width_mm"]), float(r["depth_mm"])] for r in ff])
    y = np.array([float(r["rmse"]) for r in ff])
    is_spec = np.array([r["set"] == "test_spec" for r in ff])
    spec_lo, spec_hi, _ = specimen_box()

    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True, constrained_layout=True)
    for ax, (name, k, label) in zip(axs, PLOT_AXES):
        ax.axvspan(spec_lo[k], spec_hi[k], color=C_BOX, zorder=0, lw=0,
                   label="試験体の範囲" if name == "pitch" else None)
        x = P[:, k]
        ax.scatter(x[is_spec], y[is_spec], s=18, color=col, alpha=0.6, lw=0,
                   label="test_spec（試験体の範囲、80 点）" if name == "pitch" else None, zorder=2)
        ax.scatter(x[~is_spec], y[~is_spec], s=18, facecolor="none", edgecolor=col, alpha=0.85, lw=1,
                   label="test（設計範囲全体、50 点）" if name == "pitch" else None, zorder=2)
        ax.set_xlabel(label)
        ax.set_ylim(0, 1.05 * y.max())
        _style(ax)
    axs[0].set_ylabel("RMSE of R")
    h, lab = axs[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.0))
    fig.get_layout_engine().set(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(out, f"rmse_vs_params_full_{args.train}.png"), dpi=150)
    plt.close(fig)

    # ---- 学習帯域 x 評価帯域
    M = {s: np.full((len(BANDS), len(BANDS)), np.nan) for s in ("test_spec", "test")}
    for s in M:
        for b in BANDS:
            for e in BANDS:
                v = [float(r["rmse"]) for r in rows
                     if r["set"] == s and r["train_band"] == b and r["eval_band"] == e]
                if v:
                    M[s][BANDS.index(b), BANDS.index(e)] = np.median(v)
    vmax = max(np.nanmax(m) for m in M.values())
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), constrained_layout=True)
    for ax, (s, title) in zip(axs, (("test_spec", "test_spec（試験体の範囲、80 点）"),
                                     ("test", "test（設計範囲全体、50 点）"))):
        im = ax.imshow(M[s], cmap=SEQ, vmin=0, vmax=vmax)
        for a in range(len(BANDS)):
            for c in range(len(BANDS)):
                v = M[s][a, c]
                if np.isfinite(v):
                    ax.text(c, a, f"{v:.3f}", ha="center", va="center", fontsize=9,
                            color="white" if v > 0.6 * vmax else "#1f1e1c")
        ax.set_xticks(range(len(BANDS)), BANDS)
        ax.set_yticks(range(len(BANDS)), BANDS)
        ax.set_xlabel("評価帯域")
        ax.set_ylabel("学習帯域")
        ax.set_title(title, loc="left", fontsize=10)
        ax.tick_params(length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.colorbar(im, ax=axs, shrink=0.8, label="RMSE 中央値（空欄 = 学習帯域の外）")
    fig.savefig(os.path.join(out, f"band_matrix_{args.train}.png"), dpi=150)
    plt.close(fig)

    # 本文用の数値
    print("test_spec の中央値（行 = 学習、列 = 評価）")
    for b in BANDS:
        print(f"  {b:6s} " + "  ".join("  -   " if np.isnan(v) else f"{v:.4f}" for v in M["test_spec"][BANDS.index(b)]))
    for name, k, label in PLOT_AXES:
        x = P[:, k]
        edges = np.linspace(x.min(), x.max(), 5)
        print(label, "  ".join(
            f"{a:.2f}-{bb:.2f}: {np.median(y[(x >= a) & ((x <= bb) if bb == edges[-1] else (x < bb))]):.4f}"
            for a, bb in zip(edges[:-1], edges[1:])))
    print(f"出力: {out}")


if __name__ == "__main__":
    main()
