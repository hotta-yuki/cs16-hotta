"""掃引の進捗を表示する。いつ実行してもよく、走行中の計算には触らない。

    python vscode/surrogate/progress.py
    python vscode/surrogate/progress.py --watch     # 60 秒ごとに更新
    python vscode/surrogate/progress.py --markdown  # Notion 用の本文を出力

Notion の進捗ページ（callas さんのスペース、非公開）:
https://app.notion.com/p/40567fce91ed81a99c06fbea9744746e

Notion 側は自動更新されない。--markdown の出力を Claude Code 経由で
上のページに貼り直している（MCP 接続が Claude Code 側にあるため、
このスクリプト単体では Notion を書き換えられない）。

出力ファイルの有無を数えるので、ログの文字化けや途中で再起動した場合にも影響
されない。残り時間は直近の完了ファイルのタイムスタンプから出す。
"""

import argparse
import csv
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "vscode", "simulation"))
sys.path.insert(0, HERE)

from naming import SIM_SHAPE, sim_csv_name, smooth_csv_name
# run_design が「計算済み」とみなす場所（既存の 4.7 MHz データ）も見る。
# 試験体の 2 件（p1.25/w25/d20 と p1.25/w15/d10）はそこにしか無く、
# out_dir だけ数えると永久に「残り 2」「次に回る条件」に出続けていた。
from run_design import CHECK_DIRS  # solver は関数内 import なので GPU は不要

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


def collect(out_dir):
    """進捗を数えて dict で返す。表示と Notion 出力で同じ数字を使う。"""
    rows = list(csv.DictReader(open(os.path.join(HERE, "design.csv"), encoding="utf-8")))
    have, times = {}, []
    for r in rows:
        path = os.path.join(out_dir, out_name(r))
        ok = os.path.exists(path)
        if not ok:
            ok = any(os.path.exists(os.path.join(d, out_name(r))) for d in CHECK_DIRS)
        have[id(r)] = ok
        # ペースは掃引で書いたファイルだけから出す（既存データの時刻は無関係）
        if os.path.exists(path) and r["set"] != "reuse":
            times.append(os.path.getmtime(path))
    times.sort()
    recent = [b - a for a, b in zip(times[-11:], times[-10:]) if 60 < b - a < 3600]
    per = sum(recent) / len(recent) if recent else 8.4 * 60

    phases = []
    total_left = 0
    for ph in sorted({int(r["phase"]) for r in rows}):
        sub = [r for r in rows if int(r["phase"]) == ph]
        done = sum(have[id(r)] for r in sub)
        left = len(sub) - done
        if ph != 9:
            total_left += left
        phases.append({"phase": ph, "name": PHASE_NAME.get(ph, ""), "done": done,
                       "total": len(sub), "left": left,
                       "eta_h": None if ph == 9 or left == 0 else left * per / 3600})

    running = [r for r in rows if not have[id(r)]]
    nxt = min(running, key=lambda r: (int(r["phase"]), int(r["order"]))) if running else None
    # 最後に出力されたファイルから、いま計算が動いているかを推定する
    stale_min = (time.time() - times[-1]) / 60 if times else None
    return {
        "rows": rows, "phases": phases, "per": per, "total_left": total_left,
        "done_all": sum(have.values()), "n_all": len(rows), "next": nxt,
        "eta_abs": time.time() + total_left * per, "stale_min": stale_min,
    }


def markdown(out_dir):
    """Notion 用の本文を組み立てる（Notion-flavored Markdown）。"""
    st = collect(out_dir)
    pct = 100 * st["done_all"] / st["n_all"]
    # 直近の出力が per の 2.5 倍より古ければ、掃引が止まっている可能性が高い
    alive = st["stale_min"] is not None and st["stale_min"] * 60 < st["per"] * 2.5
    if st["total_left"] == 0:
        icon, state = "✅", "完了"
    elif alive:
        icon, state = "🟢", "実行中"
    else:
        icon, state = "🔴", f"停止している可能性（最後の出力から {st['stale_min']:.0f} 分）"

    out = []
    out.append(f'<callout icon="{icon}" color="{"green_bg" if alive or st["total_left"] == 0 else "red_bg"}">')
    out.append(f"**{state}** ・ {st['done_all']} / {st['n_all']} 件 ({pct:.1f}%) ・ "
               f"ペース {st['per'] / 60:.1f} 分/件")
    out.append("")
    out.append(f"残り {st['total_left']} 件 = {st['total_left'] * st['per'] / 3600:.1f} 時間"
               f"（完了予定 {time.strftime('%m/%d %H:%M', time.localtime(st['eta_abs']))}）"
               if st["total_left"] else "すべての条件が揃いました。")
    out.append("</callout>")
    out.append("")
    out.append(f"最終更新 {time.strftime('%Y-%m-%d %H:%M')}")
    out.append("")
    out.append("## 段階ごとの進捗")
    out.append("")
    out.append("| phase | 内容 | 進捗 | 完了 | 残り | 残り時間 |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for p in st["phases"]:
        filled = int(10 * p["done"] / p["total"])
        bar = "█" * filled + "░" * (10 - filled)
        eta = "—" if p["eta_h"] is None else f"{p['eta_h']:.1f} h"
        # PHASE_NAME は端末表示用に空白で桁を揃えてあるので、表では区切りに直す
        name = re.sub(r"\s{2,}", " — ", p["name"])
        out.append(f"| {p['phase']} | {name} | {bar} | {p['done']}/{p['total']} | {p['left']} | {eta} |")
    out.append("")
    if st["next"]:
        n = st["next"]
        out.append(f"次に回る条件: `{n['set']}` pitch {n['pitch_mm']} mm / "
                   f"width {n['width_mm']} mm / depth {n['depth_mm']} mm")
        out.append("")
    # phase 1+2 が揃った時点が最初の節目（学習曲線の 1 点目）。見落とさないよう目立たせる
    ph = {p["phase"]: p for p in st["phases"]}
    if ph.get(1, {}).get("left") == 0 and ph.get(2, {}).get("left") == 0:
        out.append('<callout icon="🎯" color="blue_bg">')
        out.append("**train 60 点 + test 20 点が揃った。** 残りの計算を待たずに "
                   "README 5.（特徴量化と PCA）以降へ進める。学習曲線の 1 点目。")
        out.append("")
        out.append("学習に使えるのは train 60 点。reuse 53 点は depth 0.10–0.20 の格子なので、"
                   "混ぜずに別立てで評価したほうが切り分けやすい。")
        out.append("</callout>")
        out.append("")
    out.append("## 見かた")
    out.append("")
    out.append("- **phase 1 + 2 が終われば** train 60 点 + test 20 点が揃い、"
               "最初の精度評価ができる（学習曲線の 1 点目）")
    out.append("- **phase 9 (reuse)** は既に計算済みのデータを流用したもので、計算時間はかからない")
    out.append("- 出力は `lab/vscode/surrogate/tmp_output/`、1 条件 = CSV 1 本")
    out.append("")
    out.append("## 手元での操作")
    out.append("")
    out.append("````")
    out.append("python vscode/surrogate/progress.py       # 進捗を見る")
    out.append("python vscode/surrogate/run_design.py     # 再開（済んだ条件は飛ばす）")
    out.append("````")
    out.append("")
    out.append("<callout icon=\"⚠️\" color=\"yellow_bg\">")
    # cron ジョブ ID はセッションごとに変わるので書かない
    out.append("Claude Code のセッションから 30 分ごとに貼り直している。"
               "**セッションを閉じると更新も止まる**（掃引自体も一緒に落ちる）。"
               "上のバナーが 🔴 なら掃引が止まっている。")
    out.append("</callout>")
    return chr(10).join(out)


def report(out_dir):
    st = collect(out_dir)
    per = st["per"]

    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}   出力先: {out_dir}")
    print(f"{'phase':<34}  {'完了':>8}  {'残り':>5}  {'残り時間':>9}")
    print("-" * 64)
    for p in st["phases"]:
        done, total, left = p["done"], p["total"], p["left"]
        bar = "#" * int(20 * done / total) + "." * (20 - int(20 * done / total))
        eta = "-" if p["eta_h"] is None else f"{p['eta_h']:6.1f} h"
        print(f"{p['phase']} {p['name']:<32}{bar} {done:3d}/{total:<3d} {left:5d}  {eta:>9}")
    print("-" * 64)
    print(f"全体 {st['done_all']}/{st['n_all']} 件   ペース {per / 60:.1f} 分/件   "
          f"残り {st['total_left']} 件 = {st['total_left'] * per / 3600:.1f} 時間"
          f"（完了予定 {time.strftime('%m/%d %H:%M', time.localtime(st['eta_abs']))}）")

    nxt = st["next"]
    if nxt:
        print(f"次に回る条件: {nxt['set']} p={nxt['pitch_mm']} w={nxt['width_mm']} d={nxt['depth_mm']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(HERE, "tmp_output"))
    ap.add_argument("--watch", action="store_true", help="60 秒ごとに更新する")
    ap.add_argument("--markdown", action="store_true",
                    help="Notion 用の本文を出力する（表示はしない）")
    args = ap.parse_args()
    if args.markdown:
        sys.stdout.reconfigure(encoding="utf-8")
        print(markdown(args.out_dir))
        return
    while True:
        report(args.out_dir)
        if not args.watch:
            return
        time.sleep(60)
        print()


if __name__ == "__main__":
    main()
