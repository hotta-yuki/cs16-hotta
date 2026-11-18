"""README 7–8. 主成分係数ごとにガウス過程回帰を学習し、R に戻して精度を評価する。

    python vscode/surrogate/train_gpr.py                         # train 180 点、J = 17、test 50 点
    python vscode/surrogate/train_gpr.py --inputs pwd            # 入力を (p, w, d) のままにする（比較用）
    python vscode/surrogate/train_gpr.py --J 18
    python vscode/surrogate/train_gpr.py --train train_ph1_refpeak --phase 2

先に featurize.py で学習側の PCA（features/<train>/features.npz）を作っておくこと。

手順
----
1. 入力 θ = (p, w, d) [mm] を (1/p, w/p, d) に変換し、設計の箱（design_space.BOX_MM）の
   範囲で [0, 1] に正規化する。値は design.csv の実寸法（メッシュに刻んだ後。公称値ではない）。
   変換する理由: 回折の条件 sinθ = mλ/p は 1/p で効き、p が小さい側ほど応答が速く変わる。
   (p, w, d) のままだと test の誤差 最大 0.332 / 中央値 0.038 だったのが、(1/p, w/p, d) で
   最大 0.200 / 中央値 0.028 に下がった（2026-11-17、train 180 点・J = 17・test 50 点）
2. 学習データの特徴量 X を PCA の上位 J 成分に射影し、係数 z_1..z_J を得る
3. z_j ごとに GPR（Matérn 5/2、p, w, d ごとの長さスケール ARD、ノイズ項）を 1 本ずつ学習。
   中身は scikit-learn の GaussianProcessRegressor（gpr.py が包んでいる）
4. 予測した係数を PCA の逆変換で R に戻し、真の R（射影する前）と比べる
   - 学習データの一点抜き交差検証（LOO。ハイパーパラメータは全点で決めたものに固定）
   - test（学習に使っていない LHS 点）
   誤差は reconstruct.py（README 6）と同じ 2 通り
     eps_D = ||(R_pred - R) D_smooth|| / ||R D_smooth||   実験ノイズ（D の繰り返し）と比べる
     eps_R = ||R_pred - R|| / ||R||                       実験 R のばらつきと比べる
   PCA の打ち切り誤差（J 成分で復元しただけの誤差）も並べ、回帰の誤差と分けて見る

出力（vscode/surrogate/tmp_output/gpr/<train>_J<J>[_<inputs>]/。pwd のときは接尾辞なし）
    summary.txt       まずこれを読む。長さスケール、誤差、ノイズとの比較、点ごとの誤差
    model.joblib      逆推定（README 9）で使う学習済みモデル（sklearn の GPR 17 本。joblib.load で読む）
    model.npz         同じモデルのハイパーパラメータと PCA・正規化の情報（sklearn なしでも読める控え）
    parity.png        test の z_j 予測 vs 真値（上位 6 成分、誤差棒は ±2σ）
    error_points.png  test 各点の eps_D と PCA 打ち切り誤差、実験ノイズ
    error_region.png  (p, w, d) ごとの誤差の分布（LOO 180 点と test）
    lengthscale.png   成分ごとの長さスケール（短いほどその変数に敏感）
    examples.png      test の誤差 最小・中央・最大の 3 点の R（予測 ±2σ と真値）
"""

import argparse
import csv
import os
import sys
import time

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

from design_space import BOX_MM
from featurize import C_IM, C_RE, GRID, _style, load_wave, spectrum
from gpr import GPR
from reconstruct import experimental_noise, experimental_noise_R
from run_design import out_name

KEYS = ("pitch", "width", "depth")
SYM = ("p", "w", "d")
LO = np.array([BOX_MM[k][0] for k in KEYS])
HI = np.array([BOX_MM[k][1] for k in KEYS])
C_LOO = "#9a9893"


# 入力の変数変換。回折の条件 sinθ = mλ/p は 1/p で効くので、p が小さい側ほど
# 同じ Δp で応答が速く変わる。1/p に直すと長さスケール 1 つで扱いやすくなるはず
INPUTS = {
    "pwd":       (("p", "w", "d"),     lambda P: P),
    "invp":      (("1/p", "w", "d"),   lambda P: np.c_[1 / P[:, 0], P[:, 1], P[:, 2]]),
    "invp_duty": (("1/p", "w/p", "d"), lambda P: np.c_[1 / P[:, 0], P[:, 1] / P[:, 0], P[:, 2]]),
}


def box_of(kind):
    """変換後の入力の範囲。設計の箱 BOX_MM の 8 隅を変換して取る（学習点に依らない）。"""
    corners = np.array(np.meshgrid(*zip(LO, HI))).reshape(3, -1).T
    T = INPUTS[kind][1](corners)
    return T.min(0), T.max(0)


def normalize(P_mm, kind="pwd"):
    lo, hi = box_of(kind)
    return (INPUTS[kind][1](np.asarray(P_mm, float)) - lo) / (hi - lo)


def to_R(Xf, K):
    return Xf[..., :K] + 1j * Xf[..., K:]


def errors(Rp, R, X_ref):
    eD = np.linalg.norm((Rp - R) * X_ref, axis=1) / np.linalg.norm(R * X_ref, axis=1)
    eR = np.linalg.norm(Rp - R, axis=1) / np.linalg.norm(R, axis=1)
    return eD, eR


def load_set(args, z, freq, X_ref, t_ref):
    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    sel = [r for r in rows if r["set"] in args.set and int(r["phase"]) in args.phase]
    train_names = set(z["names"])
    names, P, Y = [], [], []
    for r in sel:
        fn = out_name(r, float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"]))
        if fn in train_names:
            raise SystemExit(f"{fn} が学習側にも入っている")
        R = spectrum(*load_wave(os.path.join(args.sim_dir, fn)), freq, t_ref) / X_ref
        names.append(fn)
        P.append([float(r[k + "_mm"]) for k in KEYS])
        Y.append(np.concatenate([R.real, R.imag]))
    return names, np.array(P), np.array(Y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="train_ph14_first180_refpeak",
                    help="features/ の下の学習側サブディレクトリ")
    ap.add_argument("--J", type=int, default=17, help="主成分の数（README 6 で決めた値）")
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=["test"])
    ap.add_argument("--phase", nargs="+", type=int, default=[2, 5])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--inputs", choices=list(INPUTS), default="invp_duty",
                    help="GPR の入力。pwd = (p, w, d)、invp = (1/p, w, d)、invp_duty = (1/p, w/p, d)")
    ap.add_argument("--restarts", type=int, default=8, help="ハイパーパラメータ最適化の初期値の数 - 1")
    args = ap.parse_args()

    z = np.load(os.path.join(args.sim_dir, "features", args.train, "features.npz"))
    freq, X_ref = z["freq"], z["X_ref"]
    t_ref = float(z["t_ref"]) if "t_ref" in z.files and np.isfinite(z["t_ref"]) else None
    K, J = len(freq), args.J
    mean, V = z["pca_mean"], z["pca_components"][:J]
    ratio = z["pca_ratio"]

    # ---- 学習データ
    P_tr, X_tr = z["params_mm"], z["X"]
    U_tr = normalize(P_tr, args.inputs)
    Z_tr = (X_tr - mean) @ V.T
    if U_tr.min() < -1e-9 or U_tr.max() > 1 + 1e-9:
        raise SystemExit("学習点が設計の箱の外にある")

    # ---- 評価データ
    names_te, P_te, X_te = load_set(args, z, freq, X_ref, t_ref)
    U_te = normalize(P_te, args.inputs)
    Z_te = (X_te - mean) @ V.T

    # ---- 学習
    t0 = time.time()
    models = []
    for j in range(J):
        models.append(GPR(n_restarts=args.restarts, seed=j).fit(U_tr, Z_tr[:, j]))
        m = models[-1]
        print(f"  z{j+1:<2d} ell = {m.ell[0]:7.3f} {m.ell[1]:7.3f} {m.ell[2]:7.3f}"
              f"  sf2 {m.sf2:8.3f}  sn2 {m.sn2:.2e}", flush=True)
    t_fit = time.time() - t0

    loo = [m.loo() for m in models]
    Z_loo = np.stack([a for a, _ in loo], 1)
    pred = [m.predict(U_te, return_std=True) for m in models]
    Z_pr = np.stack([a for a, _ in pred], 1)
    S_pr = np.stack([b for _, b in pred], 1)       # sklearn の既定（ノイズ項 sn2 込み）
    S_pr_f = np.stack([m.predict(U_te, return_std=True, include_noise=False)[1] for m in models], 1)

    R_tr, R_te = to_R(X_tr, K), to_R(X_te, K)
    R_loo = to_R(mean + Z_loo @ V, K)
    R_pr = to_R(mean + Z_pr @ V, K)
    R_trunc_te = to_R(mean + Z_te @ V, K)          # J 成分で復元しただけ（回帰の誤差なし）
    R_trunc_tr = to_R(mean + Z_tr @ V, K)
    sd_R = np.sqrt((S_pr ** 2) @ (V ** 2))          # 特徴量ごとの予測標準偏差（成分間は独立とみなす）

    eD_loo, eR_loo = errors(R_loo, R_tr, X_ref)
    eD_te, eR_te = errors(R_pr, R_te, X_ref)
    eD_tr_te, eR_tr_te = errors(R_trunc_te, R_te, X_ref)
    eD_tr_tr, _ = errors(R_trunc_tr, R_tr, X_ref)

    # ---- 実験ノイズ
    _, eps_n = experimental_noise(freq)
    n_med = float(np.median(eps_n))
    _, nR_fixed, nR_pair, _ = experimental_noise_R(freq)
    nRp = float(np.median(nR_pair))

    # ---- 係数ごとの予測精度（test）
    q2 = 1 - ((Z_pr - Z_te) ** 2).sum(0) / ((Z_te - Z_te.mean(0)) ** 2).sum(0)
    q2_loo = 1 - ((Z_loo - Z_tr) ** 2).sum(0) / ((Z_tr - Z_tr.mean(0)) ** 2).sum(0)
    cover = (np.abs(Z_pr - Z_te) <= 2 * S_pr).mean(0)
    cover_f = (np.abs(Z_pr - Z_te) <= 2 * S_pr_f).mean(0)

    suffix = "" if args.inputs == "pwd" else f"_{args.inputs}"
    out = os.path.join(args.sim_dir, "gpr", f"{args.train}_J{J}{suffix}")
    os.makedirs(out, exist_ok=True)

    np.savez(os.path.join(out, "model.npz"),
             J=J, freq=freq, X_ref=X_ref, t_ref=np.nan if t_ref is None else t_ref,
             pca_mean=mean, pca_components=V, box_lo=LO, box_hi=HI, param_names=np.array(KEYS), inputs=args.inputs,
             input_lo=box_of(args.inputs)[0], input_hi=box_of(args.inputs)[1],
             U_train=U_tr, P_train_mm=P_tr,
             ell=np.stack([m.ell for m in models]), sf2=np.array([m.sf2 for m in models]),
             sn2=np.array([m.sn2 for m in models]), y_mean=np.array([m.y_mean for m in models]),
             y_std=np.array([m.y_std for m in models]), alpha=np.stack([m.alpha for m in models]))
    # sklearn の学習済みモデル本体（逆推定ではこちらを読めば predict がそのまま使える）
    joblib.dump({"models": models, "inputs": args.inputs, "J": J}, os.path.join(out, "model.joblib"))

    # ---- summary.txt
    def frac_below(e, lv):
        return f"{int((e < lv).sum())}/{len(e)}"

    L = [
        f"学習: {args.train}（{len(U_tr)} 点）  評価: {' '.join(args.set)} phase "
        f"{' '.join(map(str, args.phase))}（{len(U_te)} 点）  J = {J}（累積寄与率 {np.cumsum(ratio)[J-1]*100:.3f}%）",
        f"設計の箱 [mm]: " + ", ".join(f"{s} {lo:.2f}-{hi:.2f}" for s, lo, hi in zip(SYM, LO, HI)),
        f"GPR の入力: {args.inputs} = ({', '.join(INPUTS[args.inputs][0])})、それぞれ箱の範囲で [0, 1] に正規化",
        f"学習時間 {t_fit:.1f} s（{J} 本、初期値 {args.restarts + 1} 個ずつ）",
        "",
        f"実験ノイズ  D の繰り返し: 中央値 {n_med:.4f}   R のばらつき（平滑面の繰り返し込み）: 中央値 {nRp:.4f}",
        "",
        "---- 誤差（R に戻して比較。真値は射影前の R）----",
        "                         eps_D 中央値   95%点     最大   ノイズ未満   eps_R 中央値    最大   ノイズ未満",
    ]
    for lab, eD, eR in (("LOO（train）", eD_loo, eR_loo),
                        ("test GPR", eD_te, eR_te),
                        ("test PCA 打ち切りのみ", eD_tr_te, eR_tr_te)):
        L.append(f"  {lab:22s} {np.median(eD):10.4f} {np.percentile(eD, 95):8.4f} {eD.max():8.4f}"
                 f"   {frac_below(eD, n_med):>7s}     {np.median(eR):10.4f} {eR.max():8.4f}   {frac_below(eR, nRp):>7s}")
    L += ["", "---- 係数ごとの GPR ----",
          f"  入力は ({', '.join(INPUTS[args.inputs][0])})。長さスケールは [0,1] 正規化での値と、元の単位に直した値"
          "（= 値 × 範囲の幅）。短いほどその変数に敏感。",
          "  上限 100 に張り付いた変数は、その成分にはほぼ効いていない。",
          "  Q2 = 1 - Σ(予測誤差)^2 / Σ(偏差)^2。cover = |誤差| <= 2σ に入った test 点の割合（理想 0.95）",
          "  cover は sklearn の σ（ノイズ項込み）、cover_f は潜在関数 f の σ（ノイズ項なし）で数えたもの",
          "",
          "   j  寄与率[%]   ell_1   ell_2   ell_3  |  元の単位 ell_1 ell_2 ell_3  |  sn2/sf2    Q2_LOO  Q2_test  cover  cover_f"]
    for j, m in enumerate(models):
        lm = m.ell * (box_of(args.inputs)[1] - box_of(args.inputs)[0])
        flag = " *" if m.at_bound else ""
        L.append(f"  {j+1:2d}  {ratio[j]*100:8.3f}  {m.ell[0]:6.3f}  {m.ell[1]:6.3f}  {m.ell[2]:6.3f}  |"
                 f"  {lm[0]:8.3f}  {lm[1]:8.3f}  {lm[2]:8.3f}  |  {m.sn2/m.sf2:.1e}  {q2_loo[j]:7.3f}  {q2[j]:7.3f}"
                 f"  {cover[j]:5.2f}  {cover_f[j]:5.2f}{flag}")
    L.append("  * は探索範囲の端に張り付いたハイパーパラメータがある成分")
    L += ["", "---- test 各点（eps_D の大きい順）----",
          "  ファイル                                      p      w      d     eps_D   打ち切り  eps_R"]
    for i in np.argsort(eD_te)[::-1]:
        L.append(f"  {names_te[i]:44s} {P_te[i,0]:.2f}  {P_te[i,1]:.2f}  {P_te[i,2]:.2f}"
                 f"   {eD_te[i]:.4f}   {eD_tr_te[i]:.4f}   {eR_te[i]:.4f}")
    L += ["", "---- LOO で誤差の大きい学習点（上位 10）----"]
    for i in np.argsort(eD_loo)[::-1][:10]:
        L.append(f"  {str(z['names'][i]):44s} {P_tr[i,0]:.2f}  {P_tr[i,1]:.2f}  {P_tr[i,2]:.2f}"
                 f"   {eD_loo[i]:.4f}   打ち切り {eD_tr_tr[i]:.4f}")
    text = "\n".join(L)
    with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)

    # ---- 図: parity
    nshow = min(6, J)
    fig, axs = plt.subplots(2, 3, figsize=(12, 7.5), layout="constrained")
    for j, ax in enumerate(axs.flat[:nshow]):
        lo, hi = min(Z_te[:, j].min(), Z_pr[:, j].min()), max(Z_te[:, j].max(), Z_pr[:, j].max())
        ax.plot([lo, hi], [lo, hi], color="#52514e", linewidth=1, linestyle="--")
        ax.scatter(Z_tr[:, j], Z_loo[:, j], s=10, color=C_LOO, label="LOO（train）", zorder=2)
        ax.errorbar(Z_te[:, j], Z_pr[:, j], yerr=2 * S_pr[:, j], fmt="o", markersize=4, color=C_RE,
                    ecolor=C_RE, elinewidth=0.8, alpha=0.9, label="test（±2σ）", zorder=3)
        ax.set_title(f"z{j+1}（寄与率 {ratio[j]*100:.1f}%）  Q2 test {q2[j]:.3f}")
        ax.set_xlabel("真値")
        ax.set_ylabel("予測")
        _style(ax)
    axs.flat[0].legend(frameon=False, loc="upper left")
    fig.savefig(os.path.join(out, "parity.png"), dpi=150)
    plt.close(fig)

    # ---- 図: test 各点の誤差
    order = np.argsort(eD_te)[::-1]
    fig, ax = plt.subplots(figsize=(9, max(5, 0.22 * len(order))), layout="constrained")
    y = np.arange(len(order))
    ax.barh(y, eD_te[order], color=C_RE, height=0.7, label="GPR")
    ax.scatter(eD_tr_te[order], y, color=C_IM, s=14, zorder=3, label="PCA 打ち切りのみ")
    ax.axvline(n_med, color="#52514e", linestyle="--", linewidth=1, label=f"実験ノイズ中央値 {n_med:.3f}")
    ax.set_yticks(y)
    ax.set_yticklabels([f"p={P_te[i,0]:.2f} w={P_te[i,1]:.2f} d={P_te[i,2]:.2f}" for i in order], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("相対誤差 ||(R_pred - R) D_smooth|| / ||R D_smooth||")
    ax.set_title(f"test 各点の誤差（J = {J}）")
    ax.legend(frameon=False, loc="lower right")
    _style(ax)
    fig.savefig(os.path.join(out, "error_points.png"), dpi=150)
    plt.close(fig)

    # ---- 図: 領域ごとの誤差
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2), layout="constrained", sharey=True)
    for k, ax in enumerate(axs):
        ax.scatter(P_tr[:, k], eD_loo, s=12, color=C_LOO, label="LOO（train）")
        ax.scatter(P_te[:, k], eD_te, s=18, color=C_RE, label="test")
        ax.axhline(n_med, color="#52514e", linestyle="--", linewidth=1)
        ax.set_xlabel(f"{KEYS[k]} [mm]")
        ax.set_yscale("log")
        _style(ax)
    axs[0].set_ylabel("eps_D")
    axs[0].legend(frameon=False)
    fig.suptitle(f"パラメータごとの誤差（破線は実験ノイズ中央値 {n_med:.3f}）")
    fig.savefig(os.path.join(out, "error_region.png"), dpi=150)
    plt.close(fig)

    # ---- 図: 長さスケール
    ell = np.stack([m.ell for m in models])
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    js = np.arange(1, J + 1)
    for k, c in zip(range(3), (C_RE, C_IM, "#3f9a5c")):
        ax.plot(js, ell[:, k], marker="o", markersize=4, linewidth=1.5, color=c, label=INPUTS[args.inputs][0][k])
    ax.set_yscale("log")
    ax.set_xlabel("主成分 j")
    ax.set_ylabel("長さスケール（[0,1] 正規化）")
    ax.set_title("長さスケール（小さいほどその変数で係数が速く変わる）")
    ax.set_xticks(js)
    ax.legend(frameon=False)
    _style(ax)
    fig.savefig(os.path.join(out, "lengthscale.png"), dpi=150)
    plt.close(fig)

    # ---- 図: 例（誤差 最小・中央・最大）
    o = np.argsort(eD_te)
    picks = [("最小", o[0]), ("中央", o[len(o) // 2]), ("最大", o[-1])]
    fm = freq / 1e6
    fig, axs = plt.subplots(3, 2, figsize=(12, 9), layout="constrained")
    for row, (lab, i) in enumerate(picks):
        rp, rt = R_pr[i], R_te[i]
        sr, si = sd_R[i, :K], sd_R[i, K:]
        a = axs[row, 0]
        a.fill_between(fm, rp.real - 2 * sr, rp.real + 2 * sr, color=C_RE, alpha=0.2, linewidth=0)
        a.fill_between(fm, rp.imag - 2 * si, rp.imag + 2 * si, color=C_IM, alpha=0.2, linewidth=0)
        a.plot(fm, rt.real, color=C_RE, linewidth=2, label="Re 真値")
        a.plot(fm, rp.real, color=C_RE, linewidth=1.2, linestyle="--", label="Re 予測")
        a.plot(fm, rt.imag, color=C_IM, linewidth=2, label="Im 真値")
        a.plot(fm, rp.imag, color=C_IM, linewidth=1.2, linestyle="--", label="Im 予測")
        a.set_title(f"誤差{lab}: p={P_te[i,0]:.2f} w={P_te[i,1]:.2f} d={P_te[i,2]:.2f} mm"
                    f"（eps_D {eD_te[i]:.3f}）")
        a.set_ylabel("R")
        _style(a)
        b = axs[row, 1]
        b.plot(fm, np.abs(rt), color="#0b0b0b", linewidth=2, label="|R| 真値")
        b.plot(fm, np.abs(rp), color="#0b0b0b", linewidth=1.2, linestyle="--", label="|R| 予測")
        b.set_ylabel("|R|")
        _style(b)
    axs[0, 0].legend(frameon=False, ncol=2, fontsize=8)
    axs[0, 1].legend(frameon=False, fontsize=8)
    for a in axs[-1]:
        a.set_xlabel("周波数 [MHz]")
    fig.savefig(os.path.join(out, "examples.png"), dpi=150)
    plt.close(fig)

    print(f"\n出力: {out}")


if __name__ == "__main__":
    main()
