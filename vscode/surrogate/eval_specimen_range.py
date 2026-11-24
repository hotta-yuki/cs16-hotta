"""試験体の範囲で、学習済み GPR（train_gpr.py）の予測スペクトルの誤差を評価する。

    python vscode/surrogate/eval_specimen_range.py                       # 既定: invp_duty のモデル
    python vscode/surrogate/eval_specimen_range.py --model train_ph14_first180_refpeak_J17
    python vscode/surrogate/eval_specimen_range.py --set test_spec      # 試験体の範囲だけの 80 点で (A)

試験体の範囲は specimens.csv の kukei 行の最小〜最大（p 1.25-2.00, w 0.15-0.40, d 0.02-0.28 mm）。
設計の箱（p 1.10-2.20, w 0.10-0.50, d 0.02-0.32）の内側にある。

評価は 2 つ
----------
(A) GPR vs FDTD（サロゲートの誤差）
    学習 180 点の LOO と test 50 点のうち、試験体の範囲に入る点だけで集計し、範囲外と比べる。
    誤差の定義は train_gpr.py と同じ
        eps_D = ||(R_pred - R) D_smooth|| / ||R D_smooth||   実験ノイズ（D の繰り返し）と比べる
        eps_R = ||R_pred - R|| / ||R||                       実験 R のばらつきと比べる
(B) 実験の試験体（ex_index.csv の 18 条件のうち試験体の範囲に入るもの）
    同じ寸法で 3 者を比べる。R_exp = mean(D_i) / D_flat（reconstruct.experimental_noise_R と同じ）
        GPR vs FDTD   … サロゲートの誤差（実験条件の点で）
        FDTD vs 実験  … モデル化の誤差（GPR が完璧でも残る分）
        GPR vs 実験   … 逆推定で実際に効く誤差
    平滑面（2026-11-05）ときず面（2026-06）は測定日が違い |R| 全体に倍率がかかりうるので、
    実数倍 a を最適にした後の誤差 eps_R(a) も出す。
    GPR の入力は FDTD が実際に作った寸法（公称値 [m] をメッシュ 10 μm で切り捨てたもの）。

出力（vscode/surrogate/tmp_output/gpr/<model>/specimen_range/）
    summary.txt         まずこれを読む
    points.csv          (A) の点ごとの誤差と範囲内かどうか
    experiment.csv      (B) の条件ごとの誤差
    error_vs_param.png  (A) eps_D を p, w, d に対して。試験体の範囲を網かけ
    exp_abs.png         (B) |R|: 実験・FDTD・GPR(±2σ)
    exp_phase.png       (B) arg R: 同上
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
    import japanize_matplotlib  # noqa: F401
except ImportError:
    pass

from design_space import MESH_M
from featurize import C_IM, C_RE, _style, load_scope, load_wave, spectrum
from naming import SIM_SHAPE, sim_csv_name
from reconstruct import EXP_DIR, EXP_INDEX, FLAT_DIR, FLAT_IDX, experimental_noise, experimental_noise_R
from run_design import CHECK_DIRS
from train_gpr import KEYS, errors, load_set, normalize, to_R

C_EXP = "#3d3c39"
C_BOX = "#efe9dc"


def specimen_box():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "specimens.csv"), encoding="utf-8"))
            if r["kind"] == "kukei" and r["pitch_mm"]]
    P = np.array([[float(r[k + "_mm"]) for k in KEYS] for r in rows])
    return P.min(0), P.max(0), len(P)


def inside(P, lo, hi, tol=1e-9):
    return np.all((P >= lo - tol) & (P <= hi + tol), axis=1)


def stats(e, n):
    if len(e) == 0:
        return "   （点なし）"
    return (f"{len(e):4d} 点  中央値 {np.median(e):.4f}  95%点 {np.percentile(e, 95):.4f}  "
            f"最大 {e.max():.4f}  ノイズ未満 {int((e < n).sum())}/{len(e)}")


def scaled_err(R_exp, R):
    """min_a ||a R_exp - R|| / ||R||（a は実数）と a。"""
    a = np.real(np.vdot(R_exp, R)) / np.real(np.vdot(R_exp, R_exp))
    return np.linalg.norm(a * R_exp - R) / np.linalg.norm(R), a


def find_sim(p, w, d):
    fn = sim_csv_name(SIM_SHAPE, p * 1e-3, w * 1e-3, d * 1e-3)
    for dd in [os.path.join(HERE, "tmp_output")] + CHECK_DIRS:
        if os.path.isfile(os.path.join(dd, fn)):
            return os.path.join(dd, fn)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="train_ph14_first180_refpeak_J17_invp_duty",
                    help="tmp_output/gpr/ の下のモデルのディレクトリ")
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--set", nargs="+", default=["test"],
                    help="(A) のテストに使う design.csv の集合。test_spec = 試験体の範囲だけの 80 点")
    ap.add_argument("--phase", nargs="+", type=int, default=None,
                    help="省略時は test なら 2 5、test_spec なら 6")
    args = ap.parse_args()
    if args.phase is None:
        args.phase = [6] if args.set == ["test_spec"] else [2, 5]

    mdir = os.path.join(args.sim_dir, "gpr", args.model)
    mz = np.load(os.path.join(mdir, "model.npz"))
    jb = joblib.load(os.path.join(mdir, "model.joblib"))
    models, kind, J = jb["models"], jb["inputs"], jb["J"]
    train = args.model.split("_J")[0]
    fz = np.load(os.path.join(args.sim_dir, "features", train, "features.npz"))
    freq, X_ref = fz["freq"], fz["X_ref"]
    t_ref = float(fz["t_ref"]) if "t_ref" in fz.files and np.isfinite(fz["t_ref"]) else None
    K = len(freq)
    mean, V = mz["pca_mean"], mz["pca_components"]
    if not np.allclose(mean, fz["pca_mean"]):
        raise SystemExit("model.npz と features.npz の PCA が一致しない")

    def predict(P):
        U = normalize(P, kind)
        out = [m.predict(U, return_std=True) for m in models]
        Z = np.stack([a for a, _ in out], 1)
        S = np.stack([b for _, b in out], 1)
        Xp = mean + Z @ V
        sd = np.sqrt((S ** 2) @ (V ** 2))
        return to_R(Xp, K), sd[:, :K], sd[:, K:]

    lo, hi, n_spec = specimen_box()
    _, eps_n = experimental_noise(freq)
    nD = float(np.median(eps_n))
    _, _, nR_pair, _ = experimental_noise_R(freq)
    nR = float(np.median(nR_pair))

    out = os.path.join(mdir, "specimen_range" + ("" if args.set == ["test"] else "_" + "_".join(args.set)))
    os.makedirs(out, exist_ok=True)

    # ================= (A) GPR vs FDTD =================
    P_tr, X_tr = fz["params_mm"], fz["X"]
    Z_loo = np.stack([m.loo()[0] for m in models], 1)
    R_tr, R_loo = to_R(X_tr, K), to_R(mean + Z_loo @ V, K)
    eD_loo, eR_loo = errors(R_loo, R_tr, X_ref)

    la = SimpleNamespace(design=os.path.join(HERE, "design.csv"), set=args.set, phase=args.phase,
                         sim_dir=args.sim_dir)
    names_te, P_te, X_te = load_set(la, fz, freq, X_ref, t_ref)
    R_te = to_R(X_te, K)
    R_pr, _, _ = predict(P_te)
    eD_te, eR_te = errors(R_pr, R_te, X_ref)

    in_tr, in_te = inside(P_tr, lo, hi), inside(P_te, lo, hi)
    with open(os.path.join(out, "points.csv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["set", "p_mm", "w_mm", "d_mm", "in_specimen_range", "eps_D", "eps_R"])
        for s, P, m, eD, eR in (("loo", P_tr, in_tr, eD_loo, eR_loo), ("test", P_te, in_te, eD_te, eR_te)):
            for i in range(len(P)):
                wr.writerow([s, *P[i], int(m[i]), f"{eD[i]:.5f}", f"{eR[i]:.5f}"])

    # ================= (B) 実験の試験体 =================
    Df = np.array([spectrum(*load_scope(os.path.join(FLAT_DIR, f"scope_{j}.csv")), freq) for j in FLAT_IDX])
    D_flat = Df.mean(0)
    rows = [r for r in csv.reader(open(EXP_INDEX, encoding="utf-8-sig", newline="")) if r and r[0].strip()][1:]
    exp = []
    for r in rows:
        # ex_index.csv の列順は pitch, depth("dipth"), width
        p, d, w = float(r[2]), float(r[3]), float(r[4])
        nom = np.array([p, w, d])
        if not inside(nom[None], lo, hi)[0]:
            continue
        D = np.array([spectrum(*load_scope(os.path.join(EXP_DIR, f"scope_{i}.csv")), freq)
                      for i in range(int(r[0]), int(r[1]) + 1)
                      if os.path.isfile(os.path.join(EXP_DIR, f"scope_{i}.csv"))])
        Rp = (D[:, None, :] / Df[None, :, :]).reshape(-1, K)      # 平滑面の繰り返しも込み
        R_exp = D.mean(0) / D_flat
        Rpm = Rp.mean(0)
        spread = np.median(np.linalg.norm(Rp - Rpm, axis=1) / np.linalg.norm(Rpm)) * np.sqrt(len(Rp) / (len(Rp) - 1))
        sim = find_sim(p, w, d)
        # FDTD が実際に作る寸法（公称 [m] をメッシュで切り捨て）
        real = np.array([int(v * 1e-3 / MESH_M) * MESH_M * 1e3 for v in nom])
        exp.append(dict(nom=nom, real=real, R_exp=R_exp, n=len(D), spread=spread,
                        R_sim=None if sim is None else spectrum(*load_wave(sim), freq, t_ref) / X_ref))
    if not exp:
        raise SystemExit("試験体の範囲に入る実験条件がない")
    P_ex = np.array([e["real"] for e in exp])
    R_g, sdRe, sdIm = predict(P_ex)
    for i, e in enumerate(exp):
        e["R_gpr"], e["sdRe"], e["sdIm"] = R_g[i], sdRe[i], sdIm[i]
        rel = lambda a, b: float(np.linalg.norm(a - b) / np.linalg.norm(b))
        relD = lambda a, b: float(np.linalg.norm((a - b) * X_ref) / np.linalg.norm(b * X_ref))
        e["gs"] = rel(e["R_gpr"], e["R_sim"]) if e["R_sim"] is not None else np.nan
        e["gsD"] = relD(e["R_gpr"], e["R_sim"]) if e["R_sim"] is not None else np.nan
        e["se"] = rel(e["R_exp"], e["R_sim"]) if e["R_sim"] is not None else np.nan
        e["ge"] = rel(e["R_exp"], e["R_gpr"])
        e["se_a"], e["a_s"] = scaled_err(e["R_exp"], e["R_sim"]) if e["R_sim"] is not None else (np.nan, np.nan)
        e["ge_a"], e["a_g"] = scaled_err(e["R_exp"], e["R_gpr"])
        # GPR と FDTD の差が予測の ±2σ に入る周波数点の割合（実部・虚部）
        if e["R_sim"] is not None:
            dr = e["R_gpr"] - e["R_sim"]
            e["cov"] = float(np.mean(np.r_[np.abs(dr.real) <= 2 * e["sdRe"], np.abs(dr.imag) <= 2 * e["sdIm"]]))
        else:
            e["cov"] = np.nan

    with open(os.path.join(out, "experiment.csv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["p_nom", "w_nom", "d_nom", "p_mesh", "w_mesh", "d_mesh", "n_shots", "exp_spread_R",
                     "eps_R_gpr_vs_fdtd", "eps_D_gpr_vs_fdtd", "cover2s_gpr_vs_fdtd",
                     "eps_R_fdtd_vs_exp", "eps_R_gpr_vs_exp", "eps_R_fdtd_vs_exp_scaled", "a_fdtd",
                     "eps_R_gpr_vs_exp_scaled", "a_gpr"])
        for e in exp:
            wr.writerow([*e["nom"], *np.round(e["real"], 3), e["n"]] + [f"{e[k]:.5f}" for k in
                        ("spread", "gs", "gsD", "cov", "se", "ge", "se_a", "a_s", "ge_a", "a_g")])

    # ================= summary =================
    col = lambda k: np.array([e[k] for e in exp])
    L = [
        f"モデル: {args.model}（入力 {kind}、J = {J}）",
        f"試験体の範囲 [mm]（specimens.csv の kukei {n_spec} 件）: p {lo[0]:.2f}-{hi[0]:.2f}, "
        f"w {lo[1]:.2f}-{hi[1]:.2f}, d {lo[2]:.2f}-{hi[2]:.2f}",
        f"実験ノイズ: D の繰り返し 中央値 {nD:.4f}（eps_D と比べる） / R のばらつき（平滑面込み）中央値 {nR:.4f}（eps_R と比べる）",
        "",
        "==== (A) GPR vs FDTD（eps_D、ノイズ未満は < %.4f）====" % nD,
        f"  LOO  試験体の範囲内   {stats(eD_loo[in_tr], nD)}",
        f"  LOO  範囲外         {stats(eD_loo[~in_tr], nD)}",
        f"  test 試験体の範囲内   {stats(eD_te[in_te], nD)}",
        f"  test 範囲外         {stats(eD_te[~in_te], nD)}",
        f"  合算 試験体の範囲内   {stats(np.r_[eD_loo[in_tr], eD_te[in_te]], nD)}",
        "",
        "==== (A) GPR vs FDTD（eps_R、ノイズ未満は < %.4f）====" % nR,
        f"  LOO  試験体の範囲内   {stats(eR_loo[in_tr], nR)}",
        f"  LOO  範囲外         {stats(eR_loo[~in_tr], nR)}",
        f"  test 試験体の範囲内   {stats(eR_te[in_te], nR)}",
        f"  test 範囲外         {stats(eR_te[~in_te], nR)}",
        f"  合算 試験体の範囲内   {stats(np.r_[eR_loo[in_tr], eR_te[in_te]], nR)}",
        "",
        "  範囲内で eps_D の大きい点（LOO と test、上位 8）",
    ]
    allP = np.r_[P_tr[in_tr], P_te[in_te]]
    allE = np.r_[eD_loo[in_tr], eD_te[in_te]]
    allS = ["loo"] * int(in_tr.sum()) + ["test"] * int(in_te.sum())
    for i in np.argsort(allE)[::-1][:8]:
        L.append(f"    {allS[i]:4s}  p {allP[i,0]:.2f}  w {allP[i,1]:.2f}  d {allP[i,2]:.2f}   eps_D {allE[i]:.4f}")
    L += [
        "",
        f"==== (B) 実験の試験体（ex_index のうち試験体の範囲に入る {len(exp)} 条件。eps はすべて R の相対誤差）====",
        "  GPR の入力はメッシュに刻んだ寸法。exp のばらつき = 平滑面込みの R の繰り返し（条件ごとの中央値）",
        "  cover = GPR−FDTD の差が予測の ±2σ に入った周波数点の割合（実部・虚部、理想 0.95）",
        "  (a) は実数倍 a を最適化した後（測定日の違いによる |R| 全体の倍率を除く）",
        "",
        "   p     w     d   | 本数  expばらつき | GPR-FDTD  cover | FDTD-実験  GPR-実験 | FDTD-実験(a)  GPR-実験(a)   a",
    ]
    for e in exp:
        p, w, d = e["nom"]
        L.append(f"  {p:.2f}  {w:.2f}  {d:.2f} | {e['n']:3d}    {e['spread']:.3f}    |  {e['gs']:.4f}  {e['cov']:.2f}  |"
                 f"  {e['se']:.4f}    {e['ge']:.4f}  |   {e['se_a']:.4f}       {e['ge_a']:.4f}    {e['a_g']:.3f}")
    L += [
        "  " + "-" * 100,
        f"  中央値            {np.nanmedian(col('spread')):.3f}    |  {np.nanmedian(col('gs')):.4f}  {np.nanmedian(col('cov')):.2f}  |"
        f"  {np.nanmedian(col('se')):.4f}    {np.nanmedian(col('ge')):.4f}  |   {np.nanmedian(col('se_a')):.4f}       {np.nanmedian(col('ge_a')):.4f}",
        f"  最大              {np.nanmax(col('spread')):.3f}    |  {np.nanmax(col('gs')):.4f}        |"
        f"  {np.nanmax(col('se')):.4f}    {np.nanmax(col('ge')):.4f}  |   {np.nanmax(col('se_a')):.4f}       {np.nanmax(col('ge_a')):.4f}",
        "",
        f"  GPR-FDTD が実験の R ばらつき中央値 {nR:.3f} 未満: {int((col('gs') < nR).sum())}/{len(exp)}",
        f"  GPR-実験 が各条件の実験ばらつき未満: {int((col('ge') < col('spread')).sum())}/{len(exp)}"
        f"   FDTD-実験: {int((col('se') < col('spread')).sum())}/{len(exp)}",
        "  （ex_index の残り 6 条件は w 0.60・0.80 mm で試験体の範囲・設計の箱の外なので除外）",
    ]
    txt = "\n".join(L)
    open(os.path.join(out, "summary.txt"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)

    # ================= 図 =================
    labels = ("p [mm]", "w [mm]", "d [mm]")
    fig, axs = plt.subplots(1, 3, figsize=(14, 4), layout="constrained", sharey=True)
    for k, ax in enumerate(axs):
        ax.axvspan(lo[k], hi[k], color=C_BOX, zorder=0, label="試験体の範囲")
        # 網かけは 1 軸ぶんの射影なので、3 軸とも範囲内の点を塗りつぶし、範囲外は白抜きにする
        ax.scatter(P_tr[~in_tr, k], eD_loo[~in_tr], s=12, facecolor="none", edgecolor="#b8b7b2",
                   linewidth=0.8, label="LOO 範囲外", zorder=2)
        ax.scatter(P_te[~in_te, k], eD_te[~in_te], s=22, facecolor="none", edgecolor=C_RE,
                   linewidth=1.0, label="test 範囲外", zorder=2)
        ax.scatter(P_tr[in_tr, k], eD_loo[in_tr], s=14, color="#6f6e6a", label="LOO 試験体の範囲内", zorder=3)
        ax.scatter(P_te[in_te, k], eD_te[in_te], s=24, color=C_RE, label="test 試験体の範囲内", zorder=4)
        ax.axhline(nD, color="#52514e", linestyle="--", linewidth=1, label=f"実験ノイズ中央値 {nD:.3f}")
        ax.set_xlabel(labels[k])
        _style(ax)
    axs[0].set_ylabel("eps_D（GPR vs FDTD）")
    axs[0].legend(fontsize=8, loc="upper right")
    fig.suptitle(f"GPR の誤差と試験体の範囲（{args.model}）")
    fig.savefig(os.path.join(out, "error_vs_param.png"), dpi=150)
    plt.close(fig)

    n = len(exp)
    nc = 4
    nr = int(np.ceil(n / nc))
    f_mhz = freq / 1e6
    for what, fname, ylab in (("abs", "exp_abs.png", "|R|"), ("phase", "exp_phase.png", "arg R [rad]")):
        fig, axs = plt.subplots(nr, nc, figsize=(4 * nc, 3 * nr), layout="constrained", sharex=True, squeeze=False)
        for i, e in enumerate(exp):
            ax = axs.flat[i]
            g = e["R_gpr"]
            if what == "abs":
                fx = np.abs
                # |R| の標準偏差（デルタ法）
                s = np.sqrt((g.real * e["sdRe"]) ** 2 + (g.imag * e["sdIm"]) ** 2) / np.abs(g)
            else:
                fx = np.angle
                s = np.sqrt((g.imag * e["sdRe"]) ** 2 + (g.real * e["sdIm"]) ** 2) / np.abs(g) ** 2
            ax.fill_between(f_mhz, fx(g) - 2 * s, fx(g) + 2 * s, color=C_IM, alpha=0.18, linewidth=0, label="GPR ±2σ")
            ax.plot(f_mhz, fx(e["R_exp"]), color=C_EXP, linewidth=1.4, label="実験")
            if e["R_sim"] is not None:
                ax.plot(f_mhz, fx(e["R_sim"]), color=C_RE, linewidth=1.6, label="FDTD")
            ax.plot(f_mhz, fx(g), color=C_IM, linewidth=1.6, linestyle="--", label="GPR")
            p, w, d = e["nom"]
            ax.set_title(f"p {p:.2f} w {w:.2f} d {d:.2f}\nGPR-FDTD {e['gs']:.3f} / GPR-実験 {e['ge']:.3f}", fontsize=9)
            _style(ax)
        for ax in axs.flat[n:]:
            ax.axis("off")
        for ax in axs[-1]:
            ax.set_xlabel("周波数 [MHz]")
        for ax in axs[:, 0]:
            ax.set_ylabel(ylab)
        axs.flat[0].legend(fontsize=8)
        fig.suptitle(f"試験体の条件での R（{ylab}）: 実験・FDTD・GPR")
        fig.savefig(os.path.join(out, fname), dpi=150)
        plt.close(fig)
    print(f"\n出力: {out}")


if __name__ == "__main__":
    main()
