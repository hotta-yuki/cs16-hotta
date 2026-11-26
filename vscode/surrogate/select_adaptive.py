"""適応的サンプリング（README 8）: GPR の苦手な領域に足す FDTD の点を選ぶ。

    python vscode/surrogate/select_adaptive.py              # 図と候補の一覧を出すだけ（design.csv は触らない）
    python vscode/surrogate/select_adaptive.py --write      # 確認後、design.csv に set=adapt1 で追記

その後の計算:
    python vscode/surrogate/run_design.py --set adapt1

選び方
------
1. 候補の箱（既定 p 1.22-1.38, w 0.15-0.40, d 0.15-0.30 mm）のメッシュ格子点をすべて候補にする。
   p を試験体の範囲（1.25-）より少し外まで取るのは、設計の箱の端 p < 1.25 も誤差が大きく、
   端が弱いと p = 1.25 付近の予測も引きずられるため。広げすぎると GPR の不確かさが最大になる
   箱の端（p 1.20, d 0.32）に点が集まり、試験体の範囲の外を計算することになる（1.20-1.40 で試して 8 点が p 1.20 に寄った）。
   design.csv の全条件（train / test / test_spec など）と計算済み出力は候補から外す。
2. 各候補に「予想される誤差」をつける
       sigma_D = ||sd(R) |D_smooth| || / ||R_pred D_smooth||    GPR の予測標準偏差を eps_D と同じ尺度にしたもの
       loo_loc = 近い学習点 k 個の LOO 誤差 eps_D の距離重みつき平均
       score   = max(sigma_D, loo_loc)
   sigma_D は 2 倍しない。誤差のノルムは 232 個の特徴量の和なので、||sd|| そのものが
   予想される ||誤差|| の大きさになる（LOO での比を summary に出して確認する）。
   sigma だけにしないのは、この領域では GPR が不確かさを小さく見積もっている
   （実験条件での ±2σ 被覆率が約 0.7）ため。LOO の実測誤差で補う。
3. score の高い順に、学習点と選んだ点から距離 r 以上離れたものだけを取る（貪欲法）。
   距離は GPR の入力空間（(1/p, w/p, d) を [0,1] に正規化）で測る。
   r は 0.12 から始め、N 点取れなければ 0.85 倍ずつ縮める。
   test / test_spec の点は選ぶときに一切使わない（評価の独立性を保つため）。

出力（vscode/surrogate/tmp_output/gpr/<model>/adaptive/）
    summary.txt     選んだ点と、選ぶ前の予想誤差
    selected.csv    選んだ点（セル数・mm・score・sigma_D・loo_loc）
    error_map.png   試験体の範囲の予想誤差の地図（(p, d) 面と (p, w) 面、もう 1 変数は最大値）と選んだ点
    selected.png    候補の箱の中の学習点と選んだ点（3 つの 2 変数面）
"""

import argparse
import csv
import itertools
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
from matplotlib.patches import Rectangle
try:
    import japanize_matplotlib  # noqa: F401
except ImportError:
    pass

from design_space import make_condition, realized_mm, rms_um
from matplotlib.colors import LinearSegmentedColormap
from featurize import _style
from make_lhs_design import MINUTES_PER_RUN, existing_conditions, load_specimens, to_cells
from order_design import farthest_point_order
from train_gpr import KEYS, errors, normalize, to_R

SEQ = LinearSegmentedColormap.from_list("blue_seq_light", ["#f5f8fc", "#86b6ef", "#3987e5", "#184f95", "#0d366b"])
C_TRAIN = "#6f6e6a"
C_SEL = "#eb6834"
PHASE = 7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="train_ph14_adapt1_refpeak_J17_invp_duty")  # 2026-11-26 から 200 点（旧 180 点は train_ph14_first180_refpeak_J17_invp_duty）
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--box", nargs=6, type=float, default=[1.22, 1.38, 0.15, 0.40, 0.15, 0.30],
                    metavar=("P0", "P1", "W0", "W1", "D0", "D1"), help="候補の箱 [mm]")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--k", type=int, default=5, help="loo_loc に使う近傍の学習点の数")
    ap.add_argument("--r0", type=float, default=0.12, help="点どうしの最小距離の初期値（正規化した入力空間）")
    ap.add_argument("--tag", default="adapt1")
    ap.add_argument("--write", action="store_true", help="design.csv に追記する")
    args = ap.parse_args()

    # ---- モデルと学習データ
    mdir = os.path.join(args.sim_dir, "gpr", args.model)
    mz = np.load(os.path.join(mdir, "model.npz"))
    jb = joblib.load(os.path.join(mdir, "model.joblib"))
    models, kind = jb["models"], jb["inputs"]
    fz = np.load(os.path.join(args.sim_dir, "features", args.model.split("_J")[0], "features.npz"))
    X_ref, K = fz["X_ref"], len(fz["freq"])
    mean, V = mz["pca_mean"], mz["pca_components"]
    W = np.abs(X_ref)

    P_tr = fz["params_mm"]
    U_tr = normalize(P_tr, kind)
    Z_loo = np.stack([m.loo()[0] for m in models], 1)
    eD_loo, _ = errors(to_R(mean + Z_loo @ V, K), to_R(fz["X"], K), X_ref)
    S_loo = np.stack([m.loo()[1] for m in models], 1)
    sd_loo = np.sqrt((S_loo ** 2) @ (V ** 2))
    sig_loo = (np.sqrt(((sd_loo[:, :K] * W) ** 2 + (sd_loo[:, K:] * W) ** 2).sum(1))
               / np.linalg.norm(to_R(mean + Z_loo @ V, K) * X_ref, axis=1))

    def predict(P, chunk=20000):
        """予想誤差 sigma_D と loo_loc、score。"""
        sig, loc = [], []
        for s in range(0, len(P), chunk):
            Pc = P[s:s + chunk]
            U = normalize(Pc, kind)
            out = [m.predict(U, return_std=True, include_noise=False) for m in models]
            Z = np.stack([a for a, _ in out], 1)
            S = np.stack([b for _, b in out], 1)
            R = to_R(mean + Z @ V, K)
            sd = np.sqrt((S ** 2) @ (V ** 2))
            num = np.sqrt(((sd[:, :K] * W) ** 2 + (sd[:, K:] * W) ** 2).sum(1))
            sig.append(num / np.linalg.norm(R * X_ref, axis=1))
            dist = np.sqrt(((U[:, None, :] - U_tr[None]) ** 2).sum(-1))
            nn = np.argsort(dist, 1)[:, :args.k]
            dn = np.take_along_axis(dist, nn, 1)
            w = 1.0 / np.maximum(dn, 1e-3)
            loc.append((w * eD_loo[nn]).sum(1) / w.sum(1))
        sig, loc = np.concatenate(sig), np.concatenate(loc)
        return sig, loc, np.maximum(sig, loc)

    # ---- 候補（箱の中の格子点、使用済みを除く）
    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    if args.write and any(r["set"] == args.tag for r in rows):
        raise SystemExit(f"中止: {args.tag} の行が既にある")
    used = {tuple(int(r[k + "_cells"]) for k in KEYS) for r in rows} | existing_conditions()
    b = args.box
    rng = [range(to_cells(b[0]), to_cells(b[1]) + 1), range(to_cells(b[2]), to_cells(b[3]) + 1),
           range(to_cells(b[4]), to_cells(b[5]) + 1)]
    cand = np.array([c for c in itertools.product(*rng) if c not in used])
    Pc = cand / 100.0
    sig_c, loc_c, sc_c = predict(Pc)
    Uc = normalize(Pc, kind)

    # ---- 貪欲に選ぶ（学習点と選んだ点から r 以上離す）
    r = args.r0
    while True:
        chosen, anchors = [], list(U_tr)
        dmin = np.sqrt(((Uc[:, None, :] - U_tr[None]) ** 2).sum(-1)).min(1)
        for i in np.argsort(-sc_c):
            if dmin[i] < r:
                continue
            if chosen and np.sqrt(((Uc[chosen] - Uc[i]) ** 2).sum(1)).min() < r:
                continue
            chosen.append(int(i))
            if len(chosen) == args.n:
                break
        if len(chosen) == args.n or r < 0.01:
            break
        r *= 0.85
    chosen = np.array(chosen)
    if len(chosen) < args.n:
        raise SystemExit(f"{args.n} 点取れなかった（{len(chosen)} 点）")
    sel_cells = cand[chosen]
    dist_tr = np.sqrt(((Uc[chosen][:, None, :] - U_tr[None]) ** 2).sum(-1)).min(1)

    out = os.path.join(mdir, "adaptive")
    os.makedirs(out, exist_ok=True)

    # ---- 試験体の範囲の地図（候補の箱の外側も含めて p は 1.20 から）
    P_spec = np.array([[p, w, d] for _, p, w, d in load_specimens()])
    lo_s, hi_s = P_spec.min(0), P_spec.max(0)
    gp = np.arange(min(to_cells(b[0]), to_cells(lo_s[0])), to_cells(hi_s[0]) + 1)
    gw = np.arange(to_cells(lo_s[1]), to_cells(hi_s[1]) + 1)
    gd = np.arange(to_cells(lo_s[2]), max(to_cells(b[5]), to_cells(hi_s[2])) + 1)
    G = np.array(list(itertools.product(gp, gw, gd))) / 100.0
    sig_g, loc_g, sc_g = predict(G)
    shape = (len(gp), len(gw), len(gd))
    S3 = sc_g.reshape(shape)
    sig3 = sig_g.reshape(shape)

    # ---- summary / csv
    L = [
        f"モデル: {args.model}（入力 {kind}）  学習 {len(P_tr)} 点",
        f"候補の箱 [mm]: p {b[0]:.2f}-{b[1]:.2f}, w {b[2]:.2f}-{b[3]:.2f}, d {b[4]:.2f}-{b[5]:.2f}"
        f"  格子点 {np.prod([len(x) for x in rng])}、使用済みを除いた候補 {len(cand)}",
        f"score = max(sigma_D, loo_loc)（loo_loc は近傍 {args.k} 点の LOO eps_D の距離重みつき平均）",
        f"sigma_D の較正（LOO 180 点）: 実際の eps_D / sigma_D の中央値 {np.median(eD_loo / sig_loo):.2f}"
        f"、eps_D <= sigma_D の割合 {(eD_loo <= sig_loo).mean():.2f}、eps_D <= 2 sigma_D {(eD_loo <= 2 * sig_loo).mean():.2f}",
        f"最小距離 r = {r:.3f}（正規化した入力空間 {kind}）",
        f"選んだ {len(chosen)} 点の計算時間: {len(chosen) * MINUTES_PER_RUN / 60:.1f} 時間",
        "",
        f"候補の箱の中の予想誤差: score 中央値 {np.median(sc_c):.3f} 最大 {sc_c.max():.3f}"
        f"  / sigma_D 中央値 {np.median(sig_c):.3f}  / loo_loc 中央値 {np.median(loc_c):.3f}",
        f"試験体の範囲全体（地図の格子）: score 中央値 {np.median(sc_g):.3f}  実験ノイズ 0.078 を超える割合 "
        f"{(sc_g > 0.078).mean() * 100:.1f}%",
        "",
        "  #    p     w     d   |  score  sigma_D  loo_loc | 最寄り学習点までの距離",
    ]
    with open(os.path.join(out, "selected.csv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["pitch_cells", "width_cells", "depth_cells", "pitch_mm", "width_mm", "depth_mm",
                     "score", "sigma_D", "loo_loc", "dist_train"])
        for n, (i, c, dt) in enumerate(zip(chosen, sel_cells, dist_tr), 1):
            wr.writerow([*c, *(c / 100), f"{sc_c[i]:.4f}", f"{sig_c[i]:.4f}", f"{loc_c[i]:.4f}", f"{dt:.4f}"])
            L.append(f"  {n:2d}  {c[0]/100:.2f}  {c[1]/100:.2f}  {c[2]/100:.2f} |  {sc_c[i]:.3f}   {sig_c[i]:.3f}"
                     f"    {loc_c[i]:.3f}  |  {dt:.3f}")
    txt = "\n".join(L)
    open(os.path.join(out, "summary.txt"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)

    # ---- error_map.png
    in_map = np.all((P_tr >= G.min(0) - 1e-9) & (P_tr <= G.max(0) + 1e-9), 1)
    sel_mm = sel_cells / 100.0
    vmax = float(np.percentile(S3, 99))
    fig, axs = plt.subplots(2, 2, figsize=(13, 9), layout="constrained")
    planes = [((0, 2), 1, "p [mm]", "d [mm]", gp, gd), ((0, 1), 2, "p [mm]", "w [mm]", gp, gw)]
    for row, ((a, c), red, xl, yl, gx, gy) in enumerate(planes):
        for col, (arr, ttl) in enumerate(((S3, "予想誤差 score = max(σ_D, loo_loc)"), (sig3, "GPR の σ_D のみ"))):
            ax = axs[row, col]
            M = arr.max(axis=red)
            im = ax.pcolormesh(gx / 100, gy / 100, M.T, cmap=SEQ, vmin=0, vmax=vmax, shading="nearest")
            cs = ax.contour(gx / 100, gy / 100, M.T, levels=[0.078], colors="#0b0b0b", linewidths=1.0)
            ax.clabel(cs, fmt="0.078", fontsize=8)
            ax.add_patch(Rectangle((lo_s[a], lo_s[c]), hi_s[a] - lo_s[a], hi_s[c] - lo_s[c], fill=False,
                                   edgecolor="#52514e", linestyle="--", linewidth=1.2))
            ax.add_patch(Rectangle((b[2 * a], b[2 * c]), b[2 * a + 1] - b[2 * a], b[2 * c + 1] - b[2 * c],
                                   fill=False, edgecolor=C_SEL, linewidth=1.6))
            ax.scatter(P_tr[in_map, a], P_tr[in_map, c], s=10, color="white", edgecolor=C_TRAIN,
                       linewidth=0.6, label="学習点", zorder=3)
            ax.scatter(sel_mm[:, a], sel_mm[:, c], s=60, marker="*", color=C_SEL, edgecolor="white",
                       linewidth=0.6, label=f"選んだ {len(sel_mm)} 点", zorder=4)
            ax.set_xlabel(xl)
            ax.set_ylabel(yl)
            ax.set_title(f"{ttl}（{'wd'[red - 1] if red else ''} 方向の最大）", fontsize=10)
            fig.colorbar(im, ax=ax, shrink=0.85)
        axs[row, 0].legend(fontsize=8, loc="upper right")
    fig.suptitle("試験体の範囲の予想誤差（破線 = 試験体の範囲、橙の枠 = 候補の箱、黒線 = 実験ノイズ 0.078）")
    fig.savefig(os.path.join(out, "error_map.png"), dpi=150)
    plt.close(fig)

    # ---- selected.png（候補の箱の中）
    in_box = np.all((P_tr >= np.array(b[0::2]) - 1e-9) & (P_tr <= np.array(b[1::2]) + 1e-9), 1)
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), layout="constrained")
    names = ("p [mm]", "w [mm]", "d [mm]")
    for ax, (a, c) in zip(axs, ((0, 2), (0, 1), (1, 2))):
        ax.scatter(Pc[:, a], Pc[:, c], s=3, c=sc_c, cmap=SEQ, vmin=0, vmax=vmax, alpha=0.25, linewidth=0)
        ax.scatter(P_tr[in_box, a], P_tr[in_box, c], s=40, color="white", edgecolor=C_TRAIN, linewidth=1.2,
                   label=f"学習点（箱の中 {int(in_box.sum())} 点）", zorder=3)
        sc = ax.scatter(sel_mm[:, a], sel_mm[:, c], s=110, marker="*", c=sc_c[chosen], cmap=SEQ, vmin=0, vmax=vmax,
                        edgecolor=C_SEL, linewidth=1.2, label="選んだ点（色 = score）", zorder=4)
        for n, (x, y) in enumerate(zip(sel_mm[:, a], sel_mm[:, c]), 1):
            ax.annotate(str(n), (x, y), xytext=(4, 4), textcoords="offset points", fontsize=7, color="#3d3c39")
        ax.set_xlabel(names[a])
        ax.set_ylabel(names[c])
        _style(ax)
    axs[0].legend(fontsize=8)
    fig.colorbar(sc, ax=axs, shrink=0.85, label="score")
    fig.suptitle("候補の箱の中の学習点と選んだ点（背景の点 = 候補、色 = 予想誤差）")
    fig.savefig(os.path.join(out, "selected.png"), dpi=150)
    plt.close(fig)
    print(f"\n出力: {out}")

    # ---- design.csv に追記
    if not args.write:
        print("design.csv は変更していない。追記するなら --write を付けて再実行")
        return
    fields = list(rows[0].keys())
    add = []
    for c_p, c_w, c_d in sel_cells.tolist():
        p_m, w_m, d_m = make_condition(c_p, c_w, c_d)
        add.append({
            "set": args.tag, "shape": "Kukei", "label": "",
            "pitch_mm": realized_mm(c_p), "width_mm": realized_mm(c_w), "depth_mm": realized_mm(c_d),
            "pitch_cells": c_p, "width_cells": c_w, "depth_cells": c_d,
            "duty": round(c_w / c_p, 6), "rms_um": round(rms_um(c_p, c_w, c_d), 4),
            "pitch_m": repr(p_m), "width_m": repr(w_m), "depth_m": repr(d_m),
            "done": 0, "order": 0, "phase": PHASE,
        })
    for rank, idx in enumerate(farthest_point_order(add)):
        add[idx]["order"] = rank
    with open(args.design, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=fields).writerows([{k: r.get(k, "") for k in fields} for r in add])
    print(f"追記: {args.design}（set={args.tag}, phase {PHASE}, {len(add)} 件）")


if __name__ == "__main__":
    main()
