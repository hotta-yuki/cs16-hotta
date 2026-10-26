"""ラテン超方格法でシミュレーション条件（pitch / width / depth）を決める。

README の 3.・4. に対応する。出力は `design.csv` で、1 行が 1 条件。

    python vscode/surrogate/make_lhs_design.py

生成する集合（`set` 列）:

    reuse    既に計算済みで、箱の中に入っている条件。追加コスト 0 で学習に使える
    train    学習用に新しく振る LHS
    test     精度評価用の LHS。別シードで、train と重複しない（README 4.）
    specimen 試験体と同じ条件。実験データとの直接比較用。学習には使わない
    isorms   同じ RMS 粗さで (width, depth) だけ変える検証用。pitch は 1.50 mm 固定

`isorms` の意図: 試験体 48 件は duty 比 r=w/p が 0.12-0.20 にしか無く、
σ=h*sqrt(r(1-r)) の sqrt 部分が 0.325-0.400 とほぼ一定。つまり実験試料の中では
RMS と深さがほとんど共線で、w と h を分離できない。等 RMS で (w,h) を振った波形が
実験ノイズを超えて違うかどうかは、本番の掃引（約 28 時間）に入る前に確かめる価値が
ある。違わなければ逆問題が不良設定で、サロゲートの精度では解決できない。
"""

import argparse
import csv
import math
import os
import re
import sys

import numpy as np
from scipy.stats import qmc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_space import (BOX_CELLS, BOX_MM, MESH_MM, make_condition,
                          realized_mm, rms_um)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

N_TRAIN = 180
N_TEST = 50
SEED_TRAIN = 20261026
SEED_TEST = 20261027
ISORMS_PITCH_MM = 1.50
ISORMS_SIGMA_UM = 40.0
MINUTES_PER_RUN = 7.4   # 実測値。README の 2.5 分は誤り


def existing_conditions():
    """計算済みの条件をセル数の組で返す。ファイル名の公称値をセル数に直す。"""
    found = set()
    for sub in ("tmp_output/sim", "tmp_output/sim_csv", "data/simdata_out"):
        d = os.path.join(REPO_ROOT, sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            m = re.search(r"pitch([0-9.]+?)_width([0-9.]+?)_depth([0-9]+(?:\.[0-9]+)?)", fn)
            if not m:
                continue
            # ファイル名のコードは「mm×100」。既存データは切り捨てで計算されている
            # ので、公称 mm ではなく int() を通したセル数が実際の形状。
            found.add(tuple(int(float(c) / 100 * 1e-3 / 1.0e-5) for c in m.groups()))
    return found


def load_specimens():
    path = os.path.join(HERE, "specimens.csv")
    out = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["kind"] != "kukei":
                continue
            out.append((row["group"] + "#" + row["id"],
                        float(row["pitch_mm"]), float(row["width_mm"]), float(row["depth_mm"])))
    return out


def to_cells(mm):
    return int(round(mm / MESH_MM))


def lhs_cells(n, seed):
    """箱の中に n 点の LHS を振り、セル数の整数格子に落とす。

    整数格子に落とすと層化が多少崩れる。特に depth はセル数で 2-32 の 31 水準しか
    無いので、n=180 では 1 水準あたり約 6 点が重なる。メッシュ 0.01 mm である以上
    これ以上は細かくできないので、深さ方向の分解能は 0.01 mm が上限と割り切る。
    """
    sampler = qmc.LatinHypercube(d=3, scramble=True, optimization="random-cd", seed=seed)
    u = sampler.random(n)
    cols = []
    for i, key in enumerate(("pitch", "width", "depth")):
        lo, hi = BOX_CELLS[key]
        # u in [0,1) -> lo..hi の整数。層の境界で切るので marginal は一様
        cols.append(lo + np.floor(u[:, i] * (hi - lo + 1)).astype(int).clip(0, hi - lo))
    return [tuple(int(c[i]) for c in cols) for i in range(n)]


def build(n, seed, exclude):
    """重複を除いて n 点そろえる。足りない分はシードを変えて継ぎ足す。"""
    out, seen = [], set(exclude)
    attempt = 0
    while len(out) < n and attempt < 50:
        for cond in lhs_cells(n - len(out) if attempt else n, seed + attempt * 1000):
            if cond in seen:
                continue
            seen.add(cond)
            out.append(cond)
            if len(out) == n:
                break
        attempt += 1
    return out


def isorms_set():
    """pitch 固定・RMS 固定で width を振り、depth を逆算する。"""
    c_p = to_cells(ISORMS_PITCH_MM)
    out = []
    lo_w, hi_w = BOX_CELLS["width"]
    lo_d, hi_d = BOX_CELLS["depth"]
    for c_w in np.linspace(lo_w, hi_w, 5).round().astype(int):
        r = c_w / c_p
        h_mm = ISORMS_SIGMA_UM / math.sqrt(r * (1 - r)) / 1e3
        c_d = to_cells(h_mm)
        if not (lo_d <= c_d <= hi_d):
            continue
        out.append((c_p, int(c_w), c_d))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "design.csv"))
    args = ap.parse_args()

    done = existing_conditions()
    specimens = load_specimens()

    rows = []
    seen = set()

    def add(tag, cond, label=""):
        if cond in seen:
            return False
        seen.add(cond)
        c_p, c_w, c_d = cond
        p_m, w_m, d_m = make_condition(c_p, c_w, c_d)   # ここで離散化を検算
        rows.append({
            "set": tag, "label": label,
            "pitch_mm": realized_mm(c_p), "width_mm": realized_mm(c_w), "depth_mm": realized_mm(c_d),
            "pitch_cells": c_p, "width_cells": c_w, "depth_cells": c_d,
            "duty": round(c_w / c_p, 6), "rms_um": round(rms_um(c_p, c_w, c_d), 4),
            "pitch_m": repr(p_m), "width_m": repr(w_m), "depth_m": repr(d_m),
            "done": int(cond in done),
        })
        return True

    # specimen を先に入れる。LHS 側がこれを避けるようにして、評価用と学習用を分ける
    outside = []
    for name, p, w, h in specimens:
        cond = (to_cells(p), to_cells(w), to_cells(h))
        for key, c in zip(("pitch", "width", "depth"), cond):
            lo, hi = BOX_CELLS[key]
            if not (lo <= c <= hi):
                outside.append((name, key))
        add("specimen", cond, name)

    for cond in isorms_set():
        add("isorms", cond, f"sigma{ISORMS_SIGMA_UM:.0f}um")

    # 既存の計算済み条件のうち箱の中にあるものは、追加コスト 0 で学習に使える。
    # LHS は整数格子上の一様乱択なので、既存の格子点と偶然一致することはまず無い
    # (141,081 通りに対し既存は 127 件)。明示的に拾わないと 56 件が無駄になる。
    for cond in sorted(done):
        if all(BOX_CELLS[k][0] <= c <= BOX_CELLS[k][1]
               for k, c in zip(("pitch", "width", "depth"), cond)):
            add("reuse", cond)
    for cond in build(N_TRAIN, SEED_TRAIN, seen):
        add("train", cond)
    for cond in build(N_TEST, SEED_TEST, seen):
        add("test", cond)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    # ---- 要約 ----
    print(f"書き出し: {args.out}")
    print(f"箱 [mm]: " + ", ".join(f"{k} {lo}-{hi}" for k, (lo, hi) in BOX_MM.items()))
    print(f"箱 [cells]: " + ", ".join(f"{k} {lo}-{hi}" for k, (lo, hi) in BOX_CELLS.items()))
    levels = [hi - lo + 1 for lo, hi in BOX_CELLS.values()]
    print(f"量子化後の設計空間: {levels[0]} x {levels[1]} x {levels[2]} = {np.prod(levels):,} 通り")
    if outside:
        print(f"警告: 箱の外に出た試験体: {outside}")
    print()
    for tag in ("specimen", "isorms", "reuse", "train", "test"):
        sub = [r for r in rows if r["set"] == tag]
        nd = sum(r["done"] for r in sub)
        todo = len(sub) - nd
        print(f"  {tag:9s} {len(sub):4d} 件  計算済み {nd:3d}  要計算 {todo:3d}"
              f"  ({todo * MINUTES_PER_RUN / 60:5.1f} 時間)")
    todo_all = sum(1 - r["done"] for r in rows)
    print(f"  {'合計':9s} {len(rows):4d} 件                 要計算 {todo_all:3d}"
          f"  ({todo_all * MINUTES_PER_RUN / 60:5.1f} 時間)")
    print()
    n_fit = sum(r["set"] in ("reuse", "train") for r in rows)
    print(f"\n  学習に使える点数: {n_fit} (reuse + train)")
    lhs = np.array([[r["pitch_cells"], r["width_cells"], r["depth_cells"]]
                    for r in rows if r["set"] == "train"], dtype=float)
    lo = np.array([BOX_CELLS[k][0] for k in ("pitch", "width", "depth")], dtype=float)
    hi = np.array([BOX_CELLS[k][1] for k in ("pitch", "width", "depth")], dtype=float)
    unit = (lhs - lo) / (hi - lo)
    print(f"train の discrepancy (CD, 小さいほど一様): {qmc.discrepancy(unit):.5f}")
    d2 = np.sqrt(((unit[:, None, :] - unit[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(d2, np.inf)
    print(f"train の最小点間距離 (maximin): {d2.min():.4f}")
    print(f"train の depth 水準数: {len(set(lhs[:, 2]))} / {levels[2]}")
    print(f"train の duty 比の範囲: {min(r['duty'] for r in rows if r['set']=='train'):.3f}"
          f" - {max(r['duty'] for r in rows if r['set']=='train'):.3f}")
    rms_all = [r["rms_um"] for r in rows if r["set"] == "train"]
    print(f"train の RMS 範囲: {min(rms_all):.1f} - {max(rms_all):.1f} um"
          f" (試験体は 6.6 - 92.6 um)")


if __name__ == "__main__":
    main()
