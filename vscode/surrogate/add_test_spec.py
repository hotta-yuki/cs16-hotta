"""試験体の範囲だけに振ったテスト点（set = test_spec）を design.csv に追記する。

    python vscode/surrogate/add_test_spec.py              # 80 点を追記
    python vscode/surrogate/add_test_spec.py --dry-run    # 書き込まずに中身を見る

その後の計算:
    python vscode/surrogate/run_design.py --set test_spec

なぜ足すか（2026-11-24）
----------------------
元の test 50 点は設計の箱（p 1.10-2.20, w 0.10-0.50, d 0.02-0.32）全体の LHS なので、
試験体の範囲（p 1.25-2.00, w 0.15-0.40, d 0.02-0.28）に入るのは 16 点しかない。
逆推定を実際に使うのは試験体の範囲なので、そこだけで LHS を振り直したテストを用意する。

- 範囲は specimens.csv の kukei 行の最小〜最大をセル数に直したもの
- design.csv にある全条件（train / test / reuse / specimen / isorms）と計算済みの出力に
  重ならないようにする（学習点がテストに混ざるのを防ぐ）
- 既存の行は書き換えない。追記するだけ。order は farthest-point 順（途中で止めても一様）、phase は 6
"""

import argparse
import csv
import os
import sys

import numpy as np
from scipy.stats import qmc

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from design_space import make_condition, realized_mm, rms_um
from make_lhs_design import MINUTES_PER_RUN, existing_conditions, load_specimens, to_cells
from order_design import farthest_point_order

TAG = "test_spec"
PHASE = 6
N = 80
SEED = 20261124
KEYS = ("pitch", "width", "depth")


def specimen_box_cells():
    P = np.array([[p, w, d] for _, p, w, d in load_specimens()], float)
    return [(to_cells(lo), to_cells(hi)) for lo, hi in zip(P.min(0), P.max(0))]


def lhs_in_box(n, seed, box):
    """make_lhs_design.lhs_cells と同じ作り方で、任意の箱に n 点。"""
    u = qmc.LatinHypercube(d=3, scramble=True, optimization="random-cd", seed=seed).random(n)
    cols = [lo + np.floor(u[:, i] * (hi - lo + 1)).astype(int).clip(0, hi - lo)
            for i, (lo, hi) in enumerate(box)]
    return [tuple(int(c[i]) for c in cols) for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--n", type=int, default=N)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.design, encoding="utf-8")))
    if any(r["set"] == TAG for r in rows):
        raise SystemExit(f"中止: {TAG} の行が既にある（二重に追記しない）")
    fields = list(rows[0].keys())

    box = specimen_box_cells()
    used = {tuple(int(r[k + "_cells"]) for k in KEYS) for r in rows} | existing_conditions()

    new, seen, attempt = [], set(used), 0
    while len(new) < args.n and attempt < 50:
        for cond in lhs_in_box(args.n if attempt == 0 else args.n - len(new), args.seed + attempt * 1000, box):
            if cond not in seen and len(new) < args.n:
                seen.add(cond)
                new.append(cond)
        attempt += 1

    add = []
    for c_p, c_w, c_d in new:
        p_m, w_m, d_m = make_condition(c_p, c_w, c_d)
        add.append({
            "set": TAG, "shape": "Kukei", "label": "",
            "pitch_mm": realized_mm(c_p), "width_mm": realized_mm(c_w), "depth_mm": realized_mm(c_d),
            "pitch_cells": c_p, "width_cells": c_w, "depth_cells": c_d,
            "duty": round(c_w / c_p, 6), "rms_um": round(rms_um(c_p, c_w, c_d), 4),
            "pitch_m": repr(p_m), "width_m": repr(w_m), "depth_m": repr(d_m),
            "done": 0, "order": 0, "phase": PHASE,
        })
    for rank, idx in enumerate(farthest_point_order(add)):
        add[idx]["order"] = rank

    x = np.array([[r[k + "_cells"] for k in KEYS] for r in add], float)
    lo, hi = np.array(box, float).T
    u = (x - lo) / (hi - lo)
    d = np.sqrt(((u[:, None] - u[None]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    print(f"試験体の範囲 [cells]: " + ", ".join(f"{k} {a}-{b}" for k, (a, b) in zip(KEYS, box)))
    print(f"{TAG}: {len(add)} 点（seed {args.seed}、継ぎ足し {attempt - 1} 回）  "
          f"discrepancy {qmc.discrepancy(u):.5f}  最小点間距離 {d.min():.4f}")
    for k, col in zip(KEYS, x.T):
        print(f"  {k:5s} {col.min() / 100:.2f}-{col.max() / 100:.2f} mm  水準数 {len(set(col))}")
    print(f"計算時間の見積り: {len(add) * MINUTES_PER_RUN / 60:.1f} 時間（{MINUTES_PER_RUN} 分/件）")
    if args.dry_run:
        return
    with open(args.design, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=fields).writerows([{k: r.get(k, "") for k in fields} for r in add])
    print(f"追記: {args.design}")


if __name__ == "__main__":
    main()
