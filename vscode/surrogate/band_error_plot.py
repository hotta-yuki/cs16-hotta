"""全域（full）で学習した GPR を、一部の周波数帯だけで評価した eps_D を p, w, d に対して描く。

11/26 の進捗報告 Fig. 2（error_vs_param_test.png）と同じ形の図を、評価帯域を変えて作る。

    eps_D(band) = ||(R_pred - R) X_ref||_band / ||R X_ref||_band     （和は帯域内の周波数点だけ）

比べる実験ノイズも同じ帯域で計算し直す（reconstruct.experimental_noise に帯域内の周波数を渡す）。
full の 0.078 をそのまま使うと、帯域ごとに物差しが変わってしまうため。

    python band_error_plot.py --band low           # 200 点モデル / test_spec / low 2.00-4.80 MHz
    python band_error_plot.py --band full          # Fig. 2 と同じ値になることの確認

出力: tmp_output/gpr/<model>/specimen_range_<set>/error_vs_param_eval_<band>.png
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

from band_rmse import bands_from_ref, mask_of
from eval_specimen_range import plt
from featurize import C_RE, _style
from reconstruct import experimental_noise
from train_gpr import load_set, normalize, to_R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="train_ph14_adapt1_refpeak_J17_invp_duty")
    ap.add_argument("--band", default="low", help="full / -6dB / -10dB / low / high")
    ap.add_argument("--set", default="test_spec")
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()
    phase = [6] if args.set == "test_spec" else [2, 5]

    mdir = os.path.join(args.sim_dir, "gpr", args.model)
    mz = np.load(os.path.join(mdir, "model.npz"))
    jb = joblib.load(os.path.join(mdir, "model.joblib"))
    models, kind = jb["models"], jb["inputs"]
    fz = np.load(os.path.join(args.sim_dir, "features", args.model.split("_J")[0], "features.npz"))
    freq, X_ref = fz["freq"], fz["X_ref"]
    t_ref = float(fz["t_ref"]) if "t_ref" in fz.files and np.isfinite(fz["t_ref"]) else None
    K = len(freq)
    mean, V = mz["pca_mean"], mz["pca_components"]

    bands = bands_from_ref(freq, X_ref)
    if args.band not in bands:
        raise SystemExit(f"--band は {list(bands)} のどれか")
    m = mask_of(freq, bands[args.band])
    f_lo, f_hi = bands[args.band]

    la = SimpleNamespace(design=os.path.join(HERE, "design.csv"), set=[args.set], phase=phase,
                         sim_dir=args.sim_dir)
    names, P, X = load_set(la, fz, freq, X_ref, t_ref)
    R = to_R(X, K)
    U = normalize(P, kind)
    Z = np.stack([g.predict(U) for g in models], 1)
    Rp = to_R(mean + Z @ V, K)

    eD = (np.linalg.norm(((Rp - R) * X_ref)[:, m], axis=1)
          / np.linalg.norm((R * X_ref)[:, m], axis=1))
    nD = float(np.median(experimental_noise(freq[m])[1]))

    out = os.path.join(mdir, f"specimen_range_{args.set}")
    os.makedirs(out, exist_ok=True)
    labels = ("p [mm]", "w [mm]", "d [mm]")
    fig, axs = plt.subplots(1, 3, figsize=(14, 4), layout="constrained", sharey=True)
    for k, ax in enumerate(axs):
        ax.scatter(P[:, k], eD, s=24, color=C_RE, label="test", zorder=4)
        ax.axhline(nD, color="#52514e", linestyle="--", linewidth=1, label=f"実験ノイズ中央値 {nD:.3f}")
        ax.set_ylim(0, 1.1 * max(eD.max(), nD))
        ax.set_xlabel(labels[k])
        _style(ax)
    axs[0].set_ylabel("eps_D（GPR vs FDTD）")
    axs[0].legend(fontsize=8, loc="upper right")
    fig.suptitle(f"GPRの誤差（学習 full・評価 {args.band} {f_lo / 1e6:.2f}-{f_hi / 1e6:.2f} MHz）")
    fn = os.path.join(out, f"error_vs_param_eval_{args.band}.png")
    fig.savefig(fn, dpi=150)
    plt.close(fig)

    print(f"モデル {args.model} / {args.set} {len(P)} 点 / 評価 {args.band} "
          f"{f_lo / 1e6:.2f}-{f_hi / 1e6:.2f} MHz（{int(m.sum())} 点）")
    print(f"  eps_D 中央値 {np.median(eD):.4f}  95%点 {np.percentile(eD, 95):.4f}  最大 {eD.max():.4f}")
    print(f"  実験ノイズ（同じ帯域）中央値 {nD:.4f}   ノイズ未満 {int((eD < nD).sum())}/{len(eD)}")
    i = int(np.argmax(eD))
    print(f"  最大の点: p {P[i, 0]:.2f}  w {P[i, 1]:.2f}  d {P[i, 2]:.2f}")
    for k, lab in enumerate(labels):
        x = P[:, k]
        edges = np.linspace(x.min(), x.max(), 5)
        print("  " + lab + "  " + "  ".join(
            f"{a:.2f}-{b:.2f}: {np.median(eD[(x >= a) & ((x <= b) if b == edges[-1] else (x < b))]):.4f}"
            for a, b in zip(edges[:-1], edges[1:])))
    print(f"出力: {fn}")


if __name__ == "__main__":
    main()
