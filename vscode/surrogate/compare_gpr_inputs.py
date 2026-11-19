"""GPR の入力の取り方 3 通りで、test の予測（推定値）を比べる図を作る。

    python vscode/surrogate/compare_gpr_inputs.py

比べるモデル（先に train_gpr.py --inputs <kind> で作っておくこと）
    pwd        (p, w, d)
    invp       (1/p, w, d)
    invp_duty  (1/p, w/p, d)

出力（vscode/surrogate/tmp_output/gpr/compare_inputs_<train>_J<J>/）。1 図 1 パネル
    eps_points.png          test 各点の eps_D（(p, w, d) の誤差の大きい順に並べる）
    eps_vs_pitch.png        eps_D とピッチ
    eps_cdf.png             eps_D の累積分布（左上にあるほどよい）
    eps_pwd_vs_invp_duty.png  点ごとの eps_D を (p, w, d) と (1/p, w/p, d) で比べた散布図
    parity_z<j>.png         z_j の予測値と真値（j = 1..6）
    summary.csv             各点・各入力の eps_D
    spectra/Re|Im|absR/<test の CSV 名>_<Re|Im|absR>.png
                            test 各点の R を FDTD・(p, w, d)・(1/p, w/p, d) で重ねた図
"""

import argparse
import csv
import os
import sys
from types import SimpleNamespace

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

from featurize import C_IM, C_RE, _style
from reconstruct import experimental_noise
from train_gpr import errors, load_set, normalize, to_R

VARIANTS = [("pwd", "(p, w, d)", C_IM, "s"),
            ("invp", "(1/p, w, d)", "#3f9a5c", "^"),
            ("invp_duty", "(1/p, w/p, d)", C_RE, "o")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="train_ph14_first180_refpeak")
    ap.add_argument("--J", type=int, default=17)
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=["test"])
    ap.add_argument("--phase", nargs="+", type=int, default=[2, 5])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()

    gdir = os.path.join(args.sim_dir, "gpr")
    zf = np.load(os.path.join(args.sim_dir, "features", args.train, "features.npz"))
    freq, X_ref = zf["freq"], zf["X_ref"]
    t_ref = float(zf["t_ref"]) if "t_ref" in zf.files and np.isfinite(zf["t_ref"]) else None
    K, J = len(freq), args.J
    mean, V = zf["pca_mean"], zf["pca_components"][:J]

    la = SimpleNamespace(design=args.design, set=args.set, phase=args.phase, sim_dir=args.sim_dir)
    names, P_te, X_te = load_set(la, zf, freq, X_ref, t_ref)
    Z_te = (X_te - mean) @ V.T
    R_te = to_R(X_te, K)

    res = {}
    for kind, lab, _, _ in VARIANTS:
        sub = f"{args.train}_J{J}" + ("" if kind == "pwd" else f"_{kind}")
        d = joblib.load(os.path.join(gdir, sub, "model.joblib"))
        assert d["inputs"] == kind and d["J"] == J
        U = normalize(P_te, kind)
        pr = [m.predict(U, return_std=True) for m in d["models"]]
        Zp = np.stack([a for a, _ in pr], 1)
        Sp = np.stack([b for _, b in pr], 1)
        eD, _ = errors(to_R(mean + Zp @ V, K), R_te, X_ref)
        res[kind] = {"Z": Zp, "S": Sp, "eD": eD}
        print(f"  {lab:14s} eps_D 中央値 {np.median(eD):.4f}  最大 {eD.max():.4f}")

    _, eps_n = experimental_noise(freq)
    n_med = float(np.median(eps_n))

    out = os.path.join(gdir, f"compare_inputs_{args.train}_J{J}")
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "summary.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "pitch_mm", "width_mm", "depth_mm"] + [f"eps_D_{k}" for k, *_ in VARIANTS])
        for i in np.argsort(res["pwd"]["eD"])[::-1]:
            w.writerow([names[i], *P_te[i]] + [round(float(res[k]["eD"][i]), 5) for k, *_ in VARIANTS])

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(os.path.join(out, name), dpi=150)
        plt.close(fig)

    def noise_line(ax, horizontal=True):
        f = ax.axhline if horizontal else ax.axvline
        f(n_med, color="#52514e", linestyle="--", linewidth=1, label=f"実験ノイズ中央値 {n_med:.3f}")

    # ---- 1. 点ごとの eps_D
    order = np.argsort(res["pwd"]["eD"])[::-1]
    x = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for kind, lab, c, mk in VARIANTS:
        ax.plot(x, res[kind]["eD"][order], linestyle="none", marker=mk, markersize=5, color=c, label=lab)
    noise_line(ax)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f"p{P_te[i,0]:.2f} w{P_te[i,1]:.2f} d{P_te[i,2]:.2f}" for i in order],
                       rotation=90, fontsize=6)
    ax.set_ylabel("eps_D")
    ax.set_title("test 各点の誤差（(p, w, d) の誤差の大きい順）")
    ax.legend(frameon=False, fontsize=8)
    _style(ax)
    save(fig, "eps_points.png")

    # ---- 2. eps_D とピッチ
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for kind, lab, c, mk in VARIANTS:
        ax.scatter(P_te[:, 0], res[kind]["eD"], marker=mk, s=22, color=c, label=lab, alpha=0.85)
    noise_line(ax)
    ax.set_yscale("log")
    ax.set_xlabel("pitch [mm]")
    ax.set_ylabel("eps_D")
    ax.set_title("ピッチと誤差")
    ax.legend(frameon=False, fontsize=8)
    _style(ax)
    save(fig, "eps_vs_pitch.png")

    # ---- 3. 累積分布
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for kind, lab, c, _ in VARIANTS:
        e = np.sort(res[kind]["eD"])
        ax.step(e, np.arange(1, len(e) + 1) / len(e), where="post", color=c, linewidth=2,
                label=f"{lab}  中央値 {np.median(e):.3f} / 最大 {e.max():.3f}")
    noise_line(ax, horizontal=False)
    ax.set_xscale("log")
    ax.set_xlabel("eps_D")
    ax.set_ylabel("累積割合")
    ax.set_title("test 50 点の誤差の累積分布（左上にあるほどよい）")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    _style(ax)
    save(fig, "eps_cdf.png")

    # ---- 4. 点ごとの改善（(p, w, d) vs (1/p, w/p, d)）
    a, b = res["pwd"]["eD"], res["invp_duty"]["eD"]
    fig, ax = plt.subplots(figsize=(6, 6))
    lo, hi = min(a.min(), b.min()) * 0.8, max(a.max(), b.max()) * 1.2
    ax.plot([lo, hi], [lo, hi], color="#52514e", linewidth=1)
    sc = ax.scatter(a, b, c=P_te[:, 0], cmap="viridis", s=30)
    fig.colorbar(sc, ax=ax, label="pitch [mm]")
    ax.axvline(n_med, color="#52514e", linestyle="--", linewidth=1)
    ax.axhline(n_med, color="#52514e", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("eps_D  入力 (p, w, d)")
    ax.set_ylabel("eps_D  入力 (1/p, w/p, d)")
    ax.set_title(f"点ごとの誤差（対角線より下が改善、{int((b < a).sum())}/{len(a)} 点）")
    _style(ax)
    save(fig, "eps_pwd_vs_invp_duty.png")

    # ---- 5. 係数ごとの予測値と真値
    for j in range(min(6, J)):
        fig, ax = plt.subplots(figsize=(6, 6))
        t = Z_te[:, j]
        allv = np.concatenate([t] + [res[k]["Z"][:, j] for k, *_ in VARIANTS])
        lo, hi = allv.min(), allv.max()
        pad = 0.05 * (hi - lo)
        ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#52514e", linewidth=1, linestyle="--")
        for kind, lab, c, mk in VARIANTS:
            zp = res[kind]["Z"][:, j]
            q2 = 1 - ((zp - t) ** 2).sum() / ((t - t.mean()) ** 2).sum()
            ax.scatter(t, zp, marker=mk, s=24, color=c, alpha=0.85, label=f"{lab}  Q2 {q2:.3f}")
        ax.set_xlim(lo - pad, hi + pad)
        ax.set_ylim(lo - pad, hi + pad)
        ax.set_xlabel(f"z{j+1} 真値（FDTD）")
        ax.set_ylabel(f"z{j+1} 予測（GPR）")
        ax.set_title(f"主成分係数 z{j+1} の予測値と真値（test 50 点）")
        ax.legend(frameon=False, fontsize=8, loc="upper left")
        _style(ax)
        save(fig, f"parity_z{j+1}.png")

    # ---- 6. test 各点のスペクトル：FDTD と (p, w, d)・(1/p, w/p, d) の予測（1 図 1 パネル）
    fm = freq / 1e6
    pair = [(k, lab, c) for k, lab, c, _ in VARIANTS if k in ("pwd", "invp_duty")]
    Rp = {k: to_R(mean + res[k]["Z"] @ V, K) for k, *_ in pair}
    Sd = {k: np.sqrt((res[k]["S"] ** 2) @ (V ** 2)) for k, *_ in pair}   # X 空間の ±σ
    sdir = os.path.join(out, "spectra")
    parts = [("Re", "Re R", lambda r: r.real, lambda s: s[:K]),
             ("Im", "Im R", lambda r: r.imag, lambda s: s[K:]),
             ("absR", "|R|", np.abs, None)]
    for sub, *_ in parts:
        os.makedirs(os.path.join(sdir, sub), exist_ok=True)
    for i in range(len(names)):
        base = os.path.splitext(os.path.basename(names[i]))[0]
        head = f"{base}  p={P_te[i,0]:.2f} w={P_te[i,1]:.2f} d={P_te[i,2]:.2f} mm"
        for sub, ylab, f, sdf in parts:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(fm, f(R_te[i]), color="#0b0b0b", linewidth=2, label="FDTD")
            for k, lab, c in pair:
                y = f(Rp[k][i])
                if sdf is not None:
                    s = sdf(Sd[k][i])
                    ax.fill_between(fm, y - 2 * s, y + 2 * s, color=c, alpha=0.15, linewidth=0)
                ax.plot(fm, y, color=c, linewidth=1.4, linestyle="--",
                        label=f"GPR {lab}  eps_D {res[k]['eD'][i]:.3f}")
            ax.set_xlabel("周波数 [MHz]")
            ax.set_ylabel(ylab)
            band = "（帯は ±2σ）" if sdf is not None else ""
            ax.set_title(f"{head}\n{ylab}{band}", fontsize=10)
            ax.legend(frameon=False, fontsize=8)
            _style(ax)
            save(fig, os.path.join("spectra", sub, f"{base}_{sub}.png"))

    print(f"出力: {out}")


if __name__ == "__main__":
    main()
