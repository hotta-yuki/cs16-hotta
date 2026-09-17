"""本体リポジトリの作業コピーと、データリポジトリ lab-data を同期する。

データはコードとは別のリポジトリで管理している（理由と構成は AGENTS.md 11章）。
実体は2か所にある。

* 本体リポジトリ内の作業コピー … スクリプトが読み書きする場所。Google Drive 同期の
  対象なので、ここに置いてあること自体がバックアップにもなっている
* lab-data … git で履歴を残す場所。Drive の外に置く（Drive 内に .git を置くと同期の
  ロックで壊れるため）

この2つを行き来させるのがこのスクリプト。どちらへ流すかは --to で指定する。

    python scripts/sync_data_repo.py --to repo    # 作業コピー -> lab-data（計算した後）
    python scripts/sync_data_repo.py --to work    # lab-data -> 作業コピー（pull した後）

既定では**上書きと追加だけ**を行い、相手側にしか無いファイルは消さずに報告する。
消してよいと分かっている場合だけ --delete を付ける。--dry-run で確認できる。
"""

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vscode" / "simulation"))
import data_paths  # noqa: E402


def _pairs():
    """(データリポジトリ側の相対パス, 作業コピー側の絶対パス) を返す。"""
    return sorted(data_paths._LAYOUT.items())


# Excel のロックファイルと OS の生成物は同期しない（lab-data 側の .gitignore とも揃えてある）
def _ignored(p):
    return p.name.startswith("~$") or p.name in {".DS_Store", "Thumbs.db"} or "__pycache__" in p.parts


def _files(root):
    if not root.is_dir():
        return {}
    return {p.relative_to(root): p for p in root.rglob("*") if p.is_file() and not _ignored(p)}


def sync(src_root, dst_root, dry_run, delete):
    """src_root -> dst_root。(コピー数, 削除候補数) を返す。"""
    src_files, dst_files = _files(src_root), _files(dst_root)
    copied = removed = 0

    for rel, s in sorted(src_files.items()):
        d = dst_root / rel
        if d.exists() and filecmp.cmp(s, d, shallow=True):
            continue
        print(f"    {'[dry] ' if dry_run else ''}copy  {rel}")
        if not dry_run:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
        copied += 1

    extra = sorted(set(dst_files) - set(src_files))
    for rel in extra:
        if delete:
            print(f"    {'[dry] ' if dry_run else ''}delete {rel}")
            if not dry_run:
                (dst_root / rel).unlink()
            removed += 1
        else:
            print(f"    残存（送り元に無い。消すなら --delete）: {rel}")
    return copied, len(extra) if not delete else removed


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to", choices=["repo", "work"], required=True,
                    help="repo: 作業コピー -> lab-data / work: lab-data -> 作業コピー")
    ap.add_argument("--dry-run", action="store_true", help="実際には書き込まない")
    ap.add_argument("--delete", action="store_true",
                    help="送り元に無いファイルを送り先から削除する（既定は残す）")
    ap.add_argument("--commit", metavar="MESSAGE", default=None,
                    help="--to repo のとき、同期後に lab-data でコミットする（push はしない）")
    args = ap.parse_args()

    repo_root = data_paths.data_repo_root()
    if repo_root is None:
        sys.exit("lab-data が見つかりません。本体リポジトリの隣に clone するか、"
                 "環境変数 LAB_DATA_DIR を設定してください（AGENTS.md 11章）。")
    print(f"本体リポジトリ : {data_paths.REPO_ROOT}")
    print(f"データリポジトリ: {repo_root}")
    print(f"向き           : {'作業コピー -> lab-data' if args.to == 'repo' else 'lab-data -> 作業コピー'}\n")

    total_copied = total_extra = 0
    for kind, work_dir in _pairs():
        data_dir = repo_root / kind
        src, dst = (work_dir, data_dir) if args.to == "repo" else (data_dir, work_dir)
        if not src.is_dir():
            print(f"  skip {kind}（送り元が無い: {src}）")
            continue
        print(f"  {kind}")
        c, e = sync(src, dst, args.dry_run, args.delete)
        print(f"    -> コピー {c} 件 / 送り元に無いもの {e} 件")
        total_copied += c
        total_extra += e

    print(f"\n合計: コピー {total_copied} 件 / 送り元に無いもの {total_extra} 件")

    if args.commit and args.to == "repo" and not args.dry_run:
        subprocess.run(["git", "add", "-A"], cwd=repo_root, check=True)
        r = subprocess.run(["git", "commit", "-m", args.commit], cwd=repo_root)
        if r.returncode == 0:
            print("lab-data でコミットしました。push はしていません。")
        else:
            print("コミットする変更はありませんでした。")
    elif args.commit:
        print("--commit は --to repo のときだけ、かつ --dry-run でないときだけ有効です。")


if __name__ == "__main__":
    main()
