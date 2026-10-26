"""掃引の進捗を表示する。いつ実行してもよく、走行中の計算には触らない。

    python vscode/surrogate/progress.py
    python vscode/surrogate/progress.py --watch     # 60 秒ごとに更新

出力ファイルの有無を数えるので、ログの文字化けや途中で再起動した場合にも影響
されない。残り時間は直近の完了ファイルのタイムスタンプから出す。
"""

import argparse
import csv
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "vscode", "simulation"))
sys.path.insert(0, HERE)

from naming import SIM_SHAPE, sim_csv_name, smooth_csv_name

PHASE_NAME = {
    0: "isorms + 平滑面  識別可能性の判定",
    1: "train 60 点      まず 60 点で検討",
    2: "test 20 点       その評価用",
    3: "specimen 42 件   試験体との直接比較",
    4: "train 残り 120   学習曲線 100 / 180 点",
    5: "test 残り 30     最終評価",
    9: "reuse 53 件      計算済み（流用）",
}


def out_name(r):
    p, w, d = float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"])
    if r.get("shape") == "Smooth":
        return smooth_csv_name(p)
    return sim_csv_name(SIM_SHAPE, p, w, d)


def report(out_dir):
    rows = list(csv.DictReader(open(os.path.join(HERE, "design.csv"), encoding="utf-8")))
    have, times = {}, []
    for r in rows:
        path = os.path.join(out_dir, out_name(r))
        ok = os.path.exists(path)
        have[id(r)] = ok
        if ok and r["set"] != "reuse":
            times.append(os.path.getmtime(path))
    times.sort()

    # 直近 10 件の間隔から 1 件あたりの所要時間を出す（起動直後の偏りを避ける）
    recent = [b - a for a, b in zip(times[-11:], times[-10:]) if 60 < b - a < 3600]
    per = sum(recent) / len(recent) if recent else 8.4 * 60

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}   出力先: {out_dir}")
    print(f"{'phase':<34}  {'完了':>8}  {'残り':>5}  {'残り時間':>9}")
    print("-" * 64)
    total_left = 0
    for ph in sorted({int(r["phase"]) for r in rows}):
        sub = [r for r in rows if int(r["phase"]) == ph]
        done = sum(have[id(r)] for r in sub)
        left = len(sub) - done
        if ph != 9:
            total_left += left
        bar = "#" * int(20 * done / len(sub)) + "." * (20 - int(20 * done / len(sub)))
        eta = "-" if ph == 9 or left == 0 else f"{left * per / 3600:6.1f} h"
        print(f"{ph} {PHASE_NAME.get(ph, ''):<32}{bar} {done:3d}/{len(sub):<3d} {left:5d}  {eta:>9}")
    print("-" * 64)
    done_all = sum(have.values())
    print(f"全体 {done_all}/{len(rows)} 件   ペース {per / 60:.1f} 分/件   "
          f"残り {total_left} 件 = {total_left * per / 3600:.1f} 時間"
          f"（完了予定 {time.strftime('%m/%d %H:%M', time.localtime(time.time() + total_left * per))}）")

    running = [r for r in rows if not have[id(r)]]
    if running:
        nxt = min(running, key=lambda r: (int(r["phase"]), int(r["order"])))
        print(f"次に回る条件: {nxt['set']} p={nxt['pitch_mm']} w={nxt['width_mm']} d={nxt['depth_mm']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--watch", action="store_true", help="60 秒ごとに更新する")
    args = ap.parse_args()
    while True:
        report(args.out_dir)
        if not args.watch:
            return
        time.sleep(60)
        print()


if __name__ == "__main__":
    main()
