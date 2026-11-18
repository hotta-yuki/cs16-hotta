"""test の全点について、FDTD と GPR の予測をスペクトルと波形で比べる図を作る。

    python vscode/surrogate/plot_gpr_test.py
    python vscode/surrogate/plot_gpr_test.py --model train_ph14_first180_refpeak_J17_invp_duty

先に train_gpr.py で学習済みモデル（tmp_output/gpr/<model>/model.joblib）を作っておくこと。

予測波形の作り方
----------------
GPR が予測するのは解析帯域（2.00–7.75 MHz、0.05 MHz 刻み）の R(f) だけなので、
    D_pred(f) = R_pred(f) · D_smooth(f)
を片側スペクトルとして逆変換し、帯域制限した波形にする。
    w(τ) = 2 Re Σ_f D(f) exp(+2πifτ) Δf          （τ の原点は t0。featurize.spectrum の逆）
周期は 1/Δf = 20 us で、窓の長さ 2.048 us より十分長いので折り返しは起きない。

FDTD 側も同じ帯域で逆変換した波形（帯域制限 FDTD）を作り、これと予測を比べる。
帯域外の成分は GPR がそもそも扱っていないため。切り出したままの FDTD 波形も参考に重ねる。
波形の ±2σ は、係数の予測標準偏差を線形に伝搬したもの（成分間は独立とみなす）。

書式は plot_simdata.py に合わせる（横軸は切り出し開始からの時刻 [us]、縦軸 ±1.5）。

出力（vscode/surrogate/tmp_output/gpr/<model>/test_compare/）
    <test の CSV 名>_compare.png   1 点ごとの図（R の実部・虚部、|R|、波形）
    summary.csv                     各点の誤差（スペクトル eps_D、波形の相対誤差など）
"""

import argparse
import csv
import os
import sys

import joblib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:
    import japanize_matplotlib  # noqa: F401  日本語ラベル用
except ImportError:
    pass

from featurize import C_IM, C_RE, EXP_DT, LEFT, RIGHT, _style, cut, load_wave
from run_design import out_name
from train_gpr import KEYS, normalize

C_RAW = "#b5b3ae"


def band_wave(D, freq, tau):
    """片側の帯域スペクトル D(f) を τ 上の実波形に戻す。"""
    df = freq[1] - freq[0]
    E = np.exp(2j * np.pi * np.outer(tau, freq))     # (n_tau, n_f)
    return 2 * np.real(E @ D) * df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="train_ph14_first180_refpeak_J17_invp_duty",
                    help="tmp_output/gpr/ の下のモデルのディレクトリ")
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=["test"])
    ap.add_argument("--phase", nargs="+", type=int, default=[2, 5])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()

    mdir = os.path.join(args.sim_dir, "gpr", args.model)
    z = np.load(os.path.join(mdir, "model.npz"))
    d = joblib.load(os.path.join(mdir, "model.joblib"))
    models, inputs = d["models"], d["inputs"]
    freq, X_ref, mean, V = z["freq"], z["X_ref"], z["pca_mean"], z["pca_components"]
    t_ref = float(z["t_ref"]) if np.isfinite(z["t_ref"]) else None
    K = len(freq)
    fm = freq / 1e6

    tau = (np.arange(LEFT + RIGHT) - LEFT) * EXP_DT            # t0 基準
    t_plot = np.arange(LEFT + RIGHT) * EXP_DT * 1e6             # 切り出し開始から [us]
    # 係数 → 波形 の線形写像（平均波形 + Σ z_j · 基底波形_j）
    Vc = V[:, :K] + 1j * V[:, K:]                               # (J, K) 複素の基底
    W_basis = np.stack([band_wave(Vc[j] * X_ref, freq, tau) for j in range(len(V))])
    mean_c = mean[:K] + 1j * mean[K:]
    w_mean = band_wave(mean_c * X_ref, freq, tau)

    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    sel = [r for r in rows if r["set"] in args.set and int(r["phase"]) in args.phase]
    out = os.path.join(mdir, "test_compare")
    os.makedirs(out, exist_ok=True)

    recs = []
    for n, r in enumerate(sel, 1):
        fn = out_name(r, float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"]))
        P = np.array([[float(r[k + "_mm"]) for k in KEYS]])
        t, w = load_wave(os.path.join(args.sim_dir, fn))
        _, seg, tau_seg = cut(t, w, t_ref)
        assert np.allclose(tau_seg, tau)
        E = np.exp(-2j * np.pi * np.outer(freq, tau))
        D_true = E @ seg * EXP_DT
        R_true = D_true / X_ref

        U = normalize(P, inputs)
        pr = [m.predict(U, return_std=True) for m in models]
        zp = np.array([a[0] for a, _ in pr])
        sp = np.array([b[0] for _, b in pr])
        Xp = mean + zp @ V
        R_pred = Xp[:K] + 1j * Xp[K:]
        sd_X = np.sqrt((sp ** 2) @ (V ** 2))
        sd_re, sd_im = sd_X[:K], sd_X[K:]

        w_bl = band_wave(D_true, freq, tau)                     # 帯域制限 FDTD
        w_pr = w_mean + zp @ W_basis                            # = band_wave(R_pred * X_ref)
        sd_w = np.sqrt((sp ** 2) @ (W_basis ** 2))

        eD = np.linalg.norm((R_pred - R_true) * X_ref) / np.linalg.norm(R_true * X_ref)
        ew = np.linalg.norm(w_pr - w_bl) / np.linalg.norm(w_bl)
        eband = np.linalg.norm(w_bl - seg) / np.linalg.norm(seg)  # 帯域で切ったこと自体による差
        recs.append({"file": fn, "pitch_mm": P[0, 0], "width_mm": P[0, 1], "depth_mm": P[0, 2],
                     "eps_D": round(eD, 5), "wave_rel_err": round(ew, 5),
                     "band_limit_err": round(eband, 5)})

        fig = plt.figure(figsize=(13, 8.5), layout="constrained")
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])
        a = fig.add_subplot(gs[0, 0])
        a.fill_between(fm, R_pred.real - 2 * sd_re, R_pred.real + 2 * sd_re, color=C_RE, alpha=0.2, linewidth=0)
        a.fill_between(fm, R_pred.imag - 2 * sd_im, R_pred.imag + 2 * sd_im, color=C_IM, alpha=0.2, linewidth=0)
        a.plot(fm, R_true.real, color=C_RE, linewidth=2, label="Re FDTD")
        a.plot(fm, R_pred.real, color=C_RE, linewidth=1.3, linestyle="--", label="Re GPR")
        a.plot(fm, R_true.imag, color=C_IM, linewidth=2, label="Im FDTD")
        a.plot(fm, R_pred.imag, color=C_IM, linewidth=1.3, linestyle="--", label="Im GPR")
        a.set_xlabel("周波数 [MHz]")
        a.set_ylabel("R = D / D_smooth")
        a.set_title("正規化スペクトル R（実部・虚部、帯は GPR の ±2σ）")
        a.legend(frameon=False, ncol=2, fontsize=9)
        _style(a)

        b = fig.add_subplot(gs[0, 1])
        b.plot(fm, np.abs(R_true), color="#0b0b0b", linewidth=2, label="FDTD")
        b.plot(fm, np.abs(R_pred), color="#0b0b0b", linewidth=1.3, linestyle="--", label="GPR")
        b.set_xlabel("周波数 [MHz]")
        b.set_ylabel("|R|")
        b.set_title("|R|")
        b.legend(frameon=False, fontsize=9)
        _style(b)

        c = fig.add_subplot(gs[1, :])
        c.plot(t_plot, seg, color=C_RAW, linewidth=1, label="FDTD（切り出したまま）")
        c.fill_between(t_plot, w_pr - 2 * sd_w, w_pr + 2 * sd_w, color=C_RE, alpha=0.2, linewidth=0)
        c.plot(t_plot, w_bl, color="#0b0b0b", linewidth=1.6, label="FDTD（2.00–7.75 MHz に帯域制限）")
        c.plot(t_plot, w_pr, color=C_RE, linewidth=1.3, linestyle="--", label="GPR（同じ帯域、帯は ±2σ）")
        c.set_xlabel("Time [us] (from cut start)")
        c.set_ylabel("Amplitude")
        c.set_ylim(-1.5, 1.5)
        c.set_title(f"波形（相対誤差 {ew:.3f}、帯域制限による差 {eband:.3f}）")
        c.legend(frameon=False, fontsize=9, loc="upper right")
        _style(c)

        fig.suptitle(f"{fn}   p={P[0,0]:.2f} w={P[0,1]:.2f} d={P[0,2]:.2f} mm   "
                     f"スペクトル誤差 eps_D = {eD:.3f}", fontsize=12)
        fig.savefig(os.path.join(out, fn.replace(".csv", "_compare.png")), dpi=130)
        plt.close(fig)
        print(f"  [{n:2d}/{len(sel)}] {fn}  eps_D {eD:.4f}  波形 {ew:.4f}", flush=True)

    recs.sort(key=lambda x: -x["eps_D"])
    with open(os.path.join(out, "summary.csv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(recs[0]))
        wr.writeheader()
        wr.writerows(recs)
    eD = np.array([x["eps_D"] for x in recs])
    ew = np.array([x["wave_rel_err"] for x in recs])
    eb = np.array([x["band_limit_err"] for x in recs])
    print(f"\n{len(recs)} 点  eps_D 中央値 {np.median(eD):.4f} 最大 {eD.max():.4f}  "
          f"波形の相対誤差 中央値 {np.median(ew):.4f} 最大 {ew.max():.4f}  "
          f"帯域制限による差 中央値 {np.median(eb):.4f} 最大 {eb.max():.4f}")
    print(f"出力: {out}")


if __name__ == "__main__":
    main()
