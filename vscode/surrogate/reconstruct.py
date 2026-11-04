"""README 6. テストデータの圧縮・復元誤差を実験のノイズレベルと比べる。

    python vscode/surrogate/reconstruct.py                    # train 60 点の PCA × test 20 点
    python vscode/surrogate/reconstruct.py --train train_ph1 --set test --phase 2

先に featurize.py で学習側の PCA（features/<train>/features.npz）を作っておくこと。

比べる量
--------
実験には平滑面の測定が無く R = D / D_smooth を作れない。そこで両者とも
「窓をかけた main wave の複素スペクトル D の相対誤差」に揃える。

    復元誤差   eps_rec(J) = ||(R_rec - R) D_smooth|| / ||R D_smooth||
    ノイズ     eps_noise  = ||D_i - D_mean|| / ||D_mean||   （同一条件の繰り返し測定）

どちらも同じ帯域・同じ窓・同じ t0 の決め方で計算する（featurize.py の関数を使う）。
参考に Notion Step 8 の形（きず由来の変化に対する比）も出す。

    eps_flaw(J) = ||y_rec - y|| / ||y - y_smooth||     （y_smooth は R = 1）

出力（vscode/surrogate/tmp_output/features/step6_<train>_<test>/）
    summary.txt       J ごとの誤差とノイズ（まずこれを読む）
    recon_error.png   J に対する復元誤差とノイズ床
    recon_per_sample.png  採用 J での test 各点の誤差
    noise_groups.csv  実験の条件ごとのばらつき
"""

import argparse
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
try:
    import japanize_matplotlib  # noqa: F401  日本語ラベル用
except ImportError:
    pass

from featurize import C_IM, C_RE, GRID, _style, load_scope, load_wave, spectrum
from run_design import out_name

EXP_DIR = os.path.join(HERE, "..", "simulation", "data", "ex_data")
EXP_INDEX = os.path.join(HERE, "..", "simulation", "data", "ex_index.csv")
J_MAX = 40


def experimental_noise(freq):
    """繰り返し測定の相対ばらつき。条件ごとの中央値と全体の分布を返す。"""
    # ex_index.csv は BOM 付き。utf-8-sig で開かないと 1 列目の名前が壊れる
    with open(EXP_INDEX, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.reader(fh) if r and r[0].strip()][1:]

    groups, eps_all = [], []
    for r in rows:
        s, e = int(r[0]), int(r[1])
        D = []
        for i in range(s, e + 1):
            p = os.path.join(EXP_DIR, f"scope_{i}.csv")
            if os.path.isfile(p):
                D.append(spectrum(*load_scope(p), freq))
        if len(D) < 2:
            continue
        D = np.array(D)
        Dm = D.mean(axis=0)
        eps = np.linalg.norm(D - Dm, axis=1) / np.linalg.norm(Dm)
        # 平均に自分が入っている分だけ小さく出るので sqrt(n/(n-1)) で補正する
        eps *= np.sqrt(len(D) / (len(D) - 1))
        groups.append({"pitch": r[2], "depth": r[3], "width": r[4], "n": len(D),
                       "median": float(np.median(eps)), "max": float(eps.max())})
        eps_all.extend(eps)
    return groups, np.array(eps_all)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="train_ph1", help="features/ の下の学習側サブディレクトリ")
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=["test"])
    ap.add_argument("--phase", nargs="+", type=int, default=[2])
    ap.add_argument("--sim-dir", default=os.path.join(HERE, "tmp_output"))
    args = ap.parse_args()

    feat_dir = os.path.join(args.sim_dir, "features")
    z = np.load(os.path.join(feat_dir, args.train, "features.npz"))
    freq, X_ref = z["freq"], z["X_ref"]
    mean, comps, ratio = z["pca_mean"], z["pca_components"], z["pca_ratio"]
    K = len(freq)

    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    sel = [r for r in rows if r["set"] in args.set and int(r["phase"]) in args.phase]
    names, P, Y = [], [], []
    for r in sel:
        fn = out_name(r, float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"]))
        if fn in set(z["names"]):
            raise SystemExit(f"{fn} が学習側にも入っている")
        R = spectrum(*load_wave(os.path.join(args.sim_dir, fn)), freq) / X_ref
        names.append(fn)
        P.append([float(r[k + "_m"]) * 1e3 for k in ("pitch", "width", "depth")])
        Y.append(np.concatenate([R.real, R.imag]))
    P, Y = np.array(P), np.array(Y)
    R = Y[:, :K] + 1j * Y[:, K:]
    y_smooth = np.concatenate([np.ones(K), np.zeros(K)])

    Js = np.arange(1, min(J_MAX, len(comps)) + 1)
    eps_rec = np.zeros((len(Js), len(Y)))
    eps_flaw = np.zeros_like(eps_rec)
    for a, J in enumerate(Js):
        V = comps[:J]
        Yr = mean + (Y - mean) @ V.T @ V
        Rr = Yr[:, :K] + 1j * Yr[:, K:]
        eps_rec[a] = np.linalg.norm((Rr - R) * X_ref, axis=1) / np.linalg.norm(R * X_ref, axis=1)
        eps_flaw[a] = np.linalg.norm(Yr - Y, axis=1) / np.linalg.norm(Y - y_smooth, axis=1)

    groups, eps_n = experimental_noise(freq)
    n_med, n_p05 = float(np.median(eps_n)), float(np.percentile(eps_n, 5))
    J99 = int(np.searchsorted(np.cumsum(ratio), 0.99) + 1)

    # ノイズの中央値を、test の全点（max）と中央値が下回る最小の J
    def first_below(curve):
        idx = np.nonzero(curve < n_med)[0]
        return int(Js[idx[0]]) if len(idx) else None
    J_med = first_below(np.median(eps_rec, axis=1))
    J_all = first_below(eps_rec.max(axis=1))

    out = os.path.join(feat_dir, f"step6_{args.train}_{'_'.join(args.set)}_ph{''.join(map(str, args.phase))}")
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "noise_groups.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(groups[0]))
        w.writeheader()
        w.writerows(groups)

    # 図 1: J に対する復元誤差
    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    ax.axhspan(n_p05, n_med, color=GRID, alpha=0.6, linewidth=0)
    ax.axhline(n_med, color="#52514e", linestyle="--", linewidth=1)
    ax.text(Js[-1], n_med, f" 実験ノイズ 中央値 {n_med:.3f}", va="bottom", ha="right", color="#0b0b0b")
    ax.text(Js[-1], n_p05, f" 5% 点 {n_p05:.3f}", va="top", ha="right", color="#52514e")
    ax.plot(Js, np.median(eps_rec, axis=1), color=C_RE, linewidth=2, marker="o", markersize=4,
            label=f"test {len(Y)} 点の中央値")
    ax.plot(Js, eps_rec.max(axis=1), color=C_IM, linewidth=2, marker="o", markersize=4,
            label=f"test {len(Y)} 点の最大")
    ax.axvline(J99, color="#52514e", linewidth=1, linestyle=":")
    ax.text(J99, eps_rec.max(), f" 寄与率 99%（J={J99}）",
            color="#52514e", va="top")
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("主成分の数 J")
    ax.set_ylabel("相対誤差 ||D_rec - D|| / ||D||")
    ax.set_title(f"圧縮・復元誤差（学習 {args.train}、評価 {' '.join(args.set)} phase {' '.join(map(str, args.phase))}）")
    ax.legend(frameon=False, loc="lower left")
    _style(ax)
    fig.savefig(os.path.join(out, "recon_error.png"), dpi=150)
    plt.close(fig)

    # 図 2: J99 での各点の誤差
    a = J99 - 1
    order = np.argsort(eps_rec[a])[::-1]
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    ax.barh(np.arange(len(Y)), eps_rec[a, order], color=C_RE, height=0.7)
    ax.axvline(n_med, color="#52514e", linestyle="--", linewidth=1)
    ax.set_yticks(np.arange(len(Y)))
    ax.set_yticklabels([f"p={P[i,0]:.2f} w={P[i,1]:.2f} d={P[i,2]:.2f}" for i in order])
    ax.invert_yaxis()
    ax.set_xlabel(f"相対誤差（J = {J99}）。破線は実験ノイズ中央値")
    _style(ax)
    fig.savefig(os.path.join(out, "recon_per_sample.png"), dpi=150)
    plt.close(fig)

    lines = [
        f"学習: {args.train}（{len(z['names'])} 点）  評価: {' '.join(args.set)} phase {' '.join(map(str, args.phase))}（{len(Y)} 点）",
        f"実験ノイズ（{len(groups)} 条件、{len(eps_n)} 波形）: 中央値 {n_med:.4f}, 5% 点 {n_p05:.4f}, 95% 点 {np.percentile(eps_n, 95):.4f}",
        f"累積寄与率 99% の J = {J99}",
        f"test の中央値がノイズ中央値を下回る最小の J = {J_med}",
        f"test の全点がノイズ中央値を下回る最小の J = {J_all}",
        "",
        "  J   寄与率累積[%]  eps_rec 中央値   最大     eps_flaw 中央値   最大",
    ]
    cum = np.cumsum(ratio)
    for a, J in enumerate(Js):
        lines.append(f"{J:3d}  {cum[J-1]*100:10.3f}   {np.median(eps_rec[a]):9.4f}  {eps_rec[a].max():8.4f}"
                     f"   {np.median(eps_flaw[a]):10.4f}  {eps_flaw[a].max():8.4f}")
    lines += ["", f"J = {J99} での各点（eps_rec の大きい順）"]
    for i in np.argsort(eps_rec[J99 - 1])[::-1]:
        lines.append(f"  {names[i]:45s} eps_rec {eps_rec[J99-1, i]:.4f}  eps_flaw {eps_flaw[J99-1, i]:.4f}")
    text = "\n".join(lines)
    with open(os.path.join(out, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    print(f"\n出力: {out}")


if __name__ == "__main__":
    main()
