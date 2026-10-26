"""design.csv に実行順（`order`）と段階（`phase`）を付ける。

LHS は「n 点そろって初めて一様」な設計なので、180 点用に振った点の**先頭 60 点**を
取っても空間充填にならない。そこで farthest-point traversal（既に選んだ点から
いちばん遠い点を貪欲に足す）で並べ替える。こうすると**どこで打ち切っても**
先頭 k 点がその k 点なりに一様になり、学習曲線（60 → 100 → 180 点）を途中で
評価できる。

phase は実行の段階。安く結論が出るものを先に置く。

    0  isorms  5 件   逆問題が識別可能かの判定（README 6. の前提確認）
    1  train   60 件  まず 60 点で検討する
    2  test    20 件  その 60 点を評価するための最小限のテストデータ
    3  specimen 42 件 試験体との直接比較
    4  train   120 件 残り（学習曲線の 100 点・180 点）
    5  test    30 件  残り

    python vscode/surrogate/order_design.py
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from design_space import BOX_CELLS

N_TRAIN_FIRST = 60
N_TEST_FIRST = 20


def unit(rows):
    lo = np.array([BOX_CELLS[k][0] for k in ("pitch", "width", "depth")], float)
    hi = np.array([BOX_CELLS[k][1] for k in ("pitch", "width", "depth")], float)
    x = np.array([[int(r["pitch_cells"]), int(r["width_cells"]), int(r["depth_cells"])]
                  for r in rows], float)
    return (x - lo) / (hi - lo)


def farthest_point_order(rows):
    """先頭 k 点がどの k でも一様になるよう並べ替えた添字を返す。"""
    x = unit(rows)
    # 起点は重心に最も近い点（乱数に依らず決まるように）
    start = int(np.argmin(((x - x.mean(0)) ** 2).sum(1)))
    chosen = [start]
    dmin = np.sqrt(((x - x[start]) ** 2).sum(1))
    dmin[start] = -1.0
    while len(chosen) < len(rows):
        nxt = int(np.argmax(dmin))
        chosen.append(nxt)
        d = np.sqrt(((x - x[nxt]) ** 2).sum(1))
        dmin = np.minimum(dmin, d)
        dmin[nxt] = -1.0
    return chosen


def main():
    path = os.path.join(HERE, "design.csv")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))

    for r in rows:
        r["order"] = 0
        r["phase"] = {"isorms": 0, "specimen": 3, "reuse": 9}.get(r["set"], 0)

    for tag, first, ph_a, ph_b in (("train", N_TRAIN_FIRST, 1, 4),
                                   ("test", N_TEST_FIRST, 2, 5)):
        sub = [r for r in rows if r["set"] == tag]
        for rank, idx in enumerate(farthest_point_order(sub)):
            sub[idx]["order"] = rank
            sub[idx]["phase"] = ph_a if rank < first else ph_b

    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    # 先頭 k 点の一様性を確認する（小さいほど一様 / 大きいほど点が離れている）
    from scipy.stats import qmc
    sub = sorted([r for r in rows if r["set"] == "train"], key=lambda r: r["order"])
    print("train を farthest-point で並べ替えたときの先頭 k 点の質")
    print("   k   discrepancy   最小点間距離")
    for k in (30, 60, 100, 180):
        x = unit(sub[:k])
        d = np.sqrt(((x[:, None, :] - x[None, :, :]) ** 2).sum(-1))
        np.fill_diagonal(d, np.inf)
        print(f"  {k:4d}   {qmc.discrepancy(x):10.5f}   {d.min():10.4f}")
    print("\n（比較）並べ替え前に先頭から素直に 60 点取った場合")
    raw = [r for r in rows if r["set"] == "train"][:60]
    x = unit(raw)
    d = np.sqrt(((x[:, None, :] - x[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    print(f"    60   {qmc.discrepancy(x):10.5f}   {d.min():10.4f}")

    print()
    for ph in range(6):
        sub = [r for r in rows if r["phase"] == ph]
        if sub:
            todo = sum(1 for r in sub if not int(r["done"]))
            print(f"  phase {ph}: {sub[0]['set']:9s} {len(sub):3d} 件 "
                  f"(要計算 {todo:3d}、{todo * 8.3 / 60:5.1f} 時間)")


if __name__ == "__main__":
    main()
