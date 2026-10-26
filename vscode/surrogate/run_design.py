"""`design.csv` の条件を順に FDTD で回す。

`loop_UT_sim.py` は `simdata.csv` の値リストを `itertools.product` で総当たりに
するので、ラテン超方格法のような**点のリスト**は表現できない。こちらはリストを
そのまま回す。リポジトリルートから実行すること（AGENTS.md 6章）。

    python vscode/surrogate/run_design.py --set isorms
    python vscode/surrogate/run_design.py --set specimen train test

既に出力がある条件は飛ばす。判定は `loop_UT_sim.py` と同じ 3 ディレクトリを見る。
"""

import argparse
import csv
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "vscode", "simulation"))

from naming import SIM_SHAPE, sim_csv_name

CHECK_DIRS = [
    os.path.join(REPO_ROOT, "tmp_output", "sim"),
    os.path.join(REPO_ROOT, "tmp_output", "sim_csv"),
    os.path.join(REPO_ROOT, "data", "simdata_out"),
]

# 実行順。安い確認を先に済ませてから本番の掃引に入る（README 6.・8.）
DEFAULT_ORDER = ["isorms", "specimen", "train", "test"]


def already_done(p_m, w_m, d_m, extra_dirs=()):
    fn = sim_csv_name(SIM_SHAPE, p_m, w_m, d_m)
    for d in list(extra_dirs) + CHECK_DIRS:
        path = os.path.join(d, fn)
        if os.path.exists(path):
            return path
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", default=os.path.join(HERE, "design.csv"))
    ap.add_argument("--set", nargs="+", default=DEFAULT_ORDER,
                    help="回す集合。既定は " + " ".join(DEFAULT_ORDER))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="先頭 N 件だけ回す")
    ap.add_argument("--out-dir", default=os.path.join(HERE, "tmp_output"),
                    help="波形 CSV の出力先。既定は vscode/surrogate/tmp_output")
    args = ap.parse_args()

    with open(args.design, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    order = {name: i for i, name in enumerate(args.set)}
    todo = [r for r in rows if r["set"] in order]
    todo.sort(key=lambda r: order[r["set"]])
    if args.limit:
        todo = todo[:args.limit]

    os.makedirs(args.out_dir, exist_ok=True)
    print(f"出力先: {args.out_dir}")
    if not args.dry_run:
        import UT_FlawVariation_Sim as sim

    t0 = time.time()
    ran = 0
    for i, r in enumerate(todo, 1):
        # [m] 値は design.csv に repr で入っている。これは「切り捨て離散化を通しても
        # 狙ったセル数になる」よう ulp 単位で調整済みなので、丸め直さないこと。
        p_m, w_m, d_m = float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"])
        tag = f"[{i}/{len(todo)}] {r['set']:8s} p={r['pitch_mm']} w={r['width_mm']} d={r['depth_mm']}"
        hit = already_done(p_m, w_m, d_m, [args.out_dir])
        if hit:
            print(f"{tag} skip ({os.path.basename(os.path.dirname(hit))})")
            continue
        if args.dry_run:
            print(f"{tag} RUN -> {sim_csv_name(SIM_SHAPE, p_m, w_m, d_m)}")
            continue
        print(f"{tag} running...", flush=True)
        sim.run_simulation(f_width=w_m, f_pitch=p_m, f_depth=d_m,
                           output_dir=args.out_dir)
        ran += 1
        el = time.time() - t0
        print(f"{tag} done ({el / ran / 60:.1f} 分/件、経過 {el / 3600:.1f} 時間)", flush=True)


if __name__ == "__main__":
    main()
