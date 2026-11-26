"""試験体の範囲のテストデータ（test_spec 80 点）の周波数成分を描く。

    spectrum_<set>.png   (a) |D(f)| を p で色分け（灰の破線 = 平滑面 |X_ref|）
                         (b) |D(f)| を d で色分け
                         (c) |R(f)| = |D / X_ref| を p で色分け
                         (d) GPR の誤差の周波数分布 |D_GPR - D_FDTD|(f) / rms_f|D_FDTD|
                             （80 点の中央値と 10-90% の範囲、low / high の帯域も示す）

    spectra/Re|Im|absR/D<eps_D 順位>_R<eps_R 順位>_<CSV 名>_<Re|Im|absR>.png
                         順位は 200 点モデルで 1 = 誤差最大（名前順 = eps_D の悪い順）
                         点ごとに FDTD と GPR（180 点・200 点）の R を重ねる（Re / Im は ±2σ の帯つき）。
                         compare_gpr_inputs.py の spectra/ と同じ形

D は FDTD の溝ありのスペクトル（R * X_ref）。値は全域（2.00-7.75 MHz）の特徴量のもの。

    python spectrum_test_spec.py                 # 200 点モデル / test_spec
    python spectrum_test_spec.py --set test

出力: tmp_output/gpr/<model>/specimen_range_<set>/spectrum_<set>.png
"""
import argparse
import os
import sys
from types import SimpleNamespace

import joblib
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

from band_rmse import bands_from_ref
from eval_specimen_range import plt
from featurize import C_RE, SEQ, _style
from train_gpr import load_set, normalize, to_R

GRAY = "#52514e"


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
    fM = freq / 1e6

    la = SimpleNamespace(design=os.path.join(HERE, "design.csv"), set=[args.set], phase=phase,
                         sim_dir=args.sim_dir)
    names, P, X = load_set(la, fz, freq, X_ref, t_ref)
    R = to_R(X, K)
    Z = np.stack([g.predict(normalize(P, jb["inputs"])) for g in jb["models"]], 1)
    Rp = to_R(mz["pca_mean"] + Z @ mz["pca_components"], K)
    D = R * X_ref
    rel = np.abs((Rp - R) * X_ref) / np.sqrt(np.mean(np.abs(D) ** 2, axis=1, keepdims=True))

    fig, axs = plt.subplots(2, 2, figsize=(13, 8.4), layout="constrained")

    def lines(ax, Y, k, label):
        nrm = Normalize(P[:, k].min(), P[:, k].max())
        for i in np.argsort(P[:, k]):
            ax.plot(fM, Y[i], color=SEQ(nrm(P[i, k])), linewidth=0.9, alpha=0.8)
        fig.colorbar(ScalarMappable(nrm, SEQ), ax=ax, label=label, shrink=0.9)

    lines(axs[0, 0], np.abs(D), 0, "p [mm]")
    lines(axs[0, 1], np.abs(D), 2, "d [mm]")
    for ax in axs[0]:
        ax.plot(fM, np.abs(X_ref), color=GRAY, linestyle="--", linewidth=1.4, label="平滑面 |X_ref|")
        ax.set_ylabel("|D(f)|")
        ax.legend(fontsize=8, loc="upper right")
    axs[0, 0].set_title("(a) 溝ありのスペクトル |D| （色 = p）", loc="left", fontsize=10)
    axs[0, 1].set_title("(b) 溝ありのスペクトル |D| （色 = d）", loc="left", fontsize=10)

    lines(axs[1, 0], np.abs(R), 0, "p [mm]")
    axs[1, 0].set_ylabel("|R(f)| = |D / X_ref|")
    axs[1, 0].set_title("(c) 平滑面で割ったスペクトル |R| （色 = p）", loc="left", fontsize=10)

    ax = axs[1, 1]
    q10, q50, q90 = np.percentile(rel, [10, 50, 90], axis=0)
    bands = bands_from_ref(freq, X_ref)
    for b, c in (("low", "#86b6ef"), ("high", "#f2b79a")):
        lo, hi = bands[b]
        ax.axvspan(lo / 1e6, hi / 1e6, color=c, alpha=0.18, lw=0)
        ax.text((lo + hi) / 2e6, 0.97, b, transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=8, color=GRAY)
    ax.fill_between(fM, q10, q90, color=C_RE, alpha=0.25, lw=0, label="10-90%")
    ax.plot(fM, q50, color=C_RE, linewidth=2, label="中央値")
    ax.set_ylim(0, None)
    ax.set_ylabel("|D_GPR - D_FDTD| / rms|D_FDTD|")
    ax.set_title("(d) GPR の誤差の周波数分布", loc="left", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")

    for ax in axs.flat:
        ax.set_xlabel("周波数 [MHz]")
        ax.set_xlim(fM[0], fM[-1])
        _style(ax)
    fig.suptitle(f"テストデータの周波数成分（{args.set} {len(P)} 点、GPR は200点モデル）")

    out = os.path.join(mdir, f"specimen_range_{args.set}")
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f"spectrum_{args.set}.png")
    fig.savefig(fn, dpi=140)
    plt.close(fig)

    # ---- 点ごとのスペクトル（compare_gpr_inputs.py の spectra/ と同じ形）
    #      FDTD と 180 点・200 点の GPR を重ね、Re / Im には ±2σ の帯を付ける
    models = [(m, lab, c) for m, lab, c in (
        ("train_ph14_first180_refpeak_J17_invp_duty", "180点", "#eb6834"),
        (args.model, "200点", "#2a78d6")) if os.path.isdir(os.path.join(args.sim_dir, "gpr", m))]
    pred = {}
    for m, lab, c in models:
        md = os.path.join(args.sim_dir, "gpr", m)
        z2, j2 = np.load(os.path.join(md, "model.npz")), joblib.load(os.path.join(md, "model.joblib"))
        U = normalize(P, j2["inputs"])
        ZS = [g.predict(U, return_std=True) for g in j2["models"]]
        Zm, Zs = np.stack([a for a, _ in ZS], 1), np.stack([b for _, b in ZS], 1)
        V2 = z2["pca_components"]
        Rm = to_R(z2["pca_mean"] + Zm @ V2, K)
        Sd = np.sqrt((Zs ** 2) @ (V2 ** 2))                    # X 空間の ±σ
        eD = np.linalg.norm((Rm - R) * X_ref, axis=1) / np.linalg.norm(D, axis=1)
        eR = np.linalg.norm(Rm - R, axis=1) / np.linalg.norm(R, axis=1)
        pred[m] = (Rm, Sd, eD, eR)
    # ファイル名の先頭に、--model（既定 200 点）での eps_D・eps_R の順位（1 = 最大誤差）を付ける。
    # 名前順に並べると eps_D の悪い順になる
    _, _, eD0, eR0 = pred[args.model]
    rD = np.argsort(-eD0).argsort() + 1
    rR = np.argsort(-eR0).argsort() + 1
    sdir = os.path.join(out, "spectra")
    parts = [("Re", "Re R", lambda r: r.real, lambda s: s[:K]),
             ("Im", "Im R", lambda r: r.imag, lambda s: s[K:]),
             ("absR", "|R|", np.abs, None)]
    for sub, *_ in parts:
        d_sub = os.path.join(sdir, sub)
        os.makedirs(d_sub, exist_ok=True)
        for fn_old in os.listdir(d_sub):           # 順位はモデルで変わるので、前回の図を消してから描く
            if fn_old.endswith(".png"):
                os.remove(os.path.join(d_sub, fn_old))
    for i, name in enumerate(names):
        base = os.path.splitext(os.path.basename(name))[0]
        head = (f"{base}  p={P[i, 0]:.2f} w={P[i, 1]:.2f} d={P[i, 2]:.2f} mm\n"
                f"200点の順位  eps_D {rD[i]}/{len(P)}  eps_R {rR[i]}/{len(P)}（{eR0[i]:.3f}）")
        stem = f"D{rD[i]:02d}_R{rR[i]:02d}_{base}"
        for sub, ylab, f, sdf in parts:
            fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
            ax.plot(fM, f(R[i]), color="#0b0b0b", linewidth=2, label="FDTD")
            for m, lab, c in models:
                Rm, Sd, eD, _ = pred[m]
                y = f(Rm[i])
                if sdf is not None:
                    s = sdf(Sd[i])
                    ax.fill_between(fM, y - 2 * s, y + 2 * s, color=c, alpha=0.15, linewidth=0)
                ax.plot(fM, y, color=c, linewidth=1.4, linestyle="--", label=f"GPR {lab}  eps_D {eD[i]:.3f}")
            ax.set_xlabel("周波数 [MHz]")
            ax.set_ylabel(ylab)
            band = "（帯は ±2σ）" if sdf is not None else ""
            ax.set_title(f"{head}\n{ylab}{band}", fontsize=10)
            ax.legend(frameon=False, fontsize=8)
            _style(ax)
            fig.savefig(os.path.join(sdir, sub, f"{stem}_{sub}.png"), dpi=150)
            plt.close(fig)
    print(f"点ごとのスペクトル: {sdir}（{len(names)} 点 × Re / Im / absR）")
    for m, lab, _ in models:
        print(f"  GPR {lab}: eps_D 中央値 {np.median(pred[m][2]):.4f}")

    k = int(np.argmax(np.abs(X_ref)))
    print(f"{args.set} {len(P)} 点 / {fM[0]:.2f}-{fM[-1]:.2f} MHz（{K} 点）/ X_ref ピーク {fM[k]:.2f} MHz")
    print(f"  誤差の中央値が最大の周波数 {fM[np.argmax(q50)]:.2f} MHz（{q50.max():.4f}）")
    for b in ("low", "high"):
        lo, hi = bands[b]
        m = (freq >= lo) & (freq <= hi)
        print(f"  {b}: 誤差の中央値の平均 {q50[m].mean():.4f}")
    print(f"出力: {fn}")


if __name__ == "__main__":
    main()
