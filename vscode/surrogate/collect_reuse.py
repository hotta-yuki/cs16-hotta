"""既存の計算済み CSV を、サロゲート用の出力先に実現値の名前で集める。

既存データのファイル名は**公称値**（pitch125 = 1.25 mm）だが、FDTD が実際に
作った形状は `int()` 切り捨てのせいで 124 セル = 1.24 mm。サロゲートの教師ラベル
は実現値なので、名前もそちらに合わせてコピーする（再計算は不要、AGENTS.md 11章の
「再現できるが再現に時間がかかる」データをそのまま使う）。

    python vscode/surrogate/collect_reuse.py
"""

import csv
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "vscode", "simulation"))
sys.path.insert(0, HERE)

from naming import SIM_SHAPE, sim_csv_name
from design_space import MESH_M

SRC_DIRS = ["tmp_output/sim", "tmp_output/sim_csv", "data/simdata_out"]


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tmp_output")
    os.makedirs(out_dir, exist_ok=True)

    design = {}
    with open(os.path.join(HERE, "design.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (int(r["pitch_cells"]), int(r["width_cells"]), int(r["depth_cells"]))
            design[key] = r

    copied = skipped = unused = 0
    for sub in SRC_DIRS:
        d = os.path.join(REPO_ROOT, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            m = re.search(r"pitch([0-9.]+?)_width([0-9.]+?)_depth([0-9]+(?:\.[0-9]+)?)", fn)
            if not m:
                continue
            cells = tuple(int(float(c) / 100 * 1e-3 / MESH_M) for c in m.groups())
            row = design.get(cells)
            if row is None:
                unused += 1
                continue
            dst_name = sim_csv_name(SIM_SHAPE,
                                    float(row["pitch_m"]), float(row["width_m"]), float(row["depth_m"]))
            dst = os.path.join(out_dir, dst_name)
            if os.path.exists(dst):
                skipped += 1
                continue
            shutil.copy2(os.path.join(d, fn), dst)
            note = "" if fn == dst_name else f"  (公称 {fn} -> 実現値 {dst_name})"
            print(f"{row['set']:8s} {dst_name}{note}")
            copied += 1

    print(f"\nコピー {copied} 件 / 既にあった {skipped} 件 / 設計外のため未使用 {unused} 件")
    print(f"出力先: {out_dir}")


if __name__ == "__main__":
    main()
