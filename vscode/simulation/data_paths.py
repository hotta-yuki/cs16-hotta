"""データの置き場所を解決する。

データはコードとは別のリポジトリ **lab-data** で管理している（再現できるが再現に時間が
かかるため、計算結果そのものを履歴に残す）。理由と構成は `AGENTS.md` 11章と
lab-data 側の `README.md`。

探索順は次のとおり。最初に見つかったものを使う。

1. 環境変数 ``LAB_DATA_DIR``（データリポジトリを別の場所に置いた場合）
2. 本体リポジトリ内の作業コピー（Windows 機。Google Drive のバックアップも兼ねている）
3. 本体リポジトリの**隣**に clone した ``lab-data/``（Mac 側は通常こちら）

2 を 3 より先に見るのは、シミュレーションの出力先が本体リポジトリ内の ``tmp_output/``
だからで、回した直後のデータをそのまま読めるようにするため。2 と 3 の同期は
``scripts/sync_data_repo.py`` が行う。
"""

import os
from pathlib import Path

# このファイルは <repo>/vscode/simulation/ にある
REPO_ROOT = Path(__file__).resolve().parents[2]

# データリポジトリ内の場所 -> 本体リポジトリ内の作業コピーの場所
_LAYOUT = {
    "experiment": REPO_ROOT / "vscode" / "simulation" / "data",
    "simulation/sim": REPO_ROOT / "tmp_output" / "sim",
    "simulation/sim_csv": REPO_ROOT / "tmp_output" / "sim_csv",
    "plots/comparison_plots": REPO_ROOT / "tmp_output" / "comparison_plots",
    "plots/plots_simulation_fft": REPO_ROOT / "tmp_output" / "plots_simulation_fft",
    "plots/plots_simulation_waveform": REPO_ROOT / "tmp_output" / "plots_simulation_waveform",
}


def data_repo_root():
    """データリポジトリ ``lab-data`` の場所。見つからなければ None。"""
    env = os.environ.get("LAB_DATA_DIR")
    if env:
        p = Path(env).expanduser()
        return p if p.is_dir() else None
    sibling = REPO_ROOT.parent / "lab-data"
    return sibling if sibling.is_dir() else None


def resolve(kind, must_exist=True):
    """``_LAYOUT`` のキーを実在するディレクトリに解決する。

    例) ``resolve("experiment")`` -> 実験データのディレクトリ

    ``must_exist=False`` なら、存在しなくても書き込み先として
    本体リポジトリ内の作業コピーのパスを返す（新規に作る場合に使う）。
    """
    if kind not in _LAYOUT:
        raise KeyError(f"未知のデータ種別: {kind}（有効: {sorted(_LAYOUT)}）")

    local = _LAYOUT[kind]
    if local.is_dir():
        return local

    root = data_repo_root()
    if root is not None and (root / kind).is_dir():
        return root / kind

    if must_exist:
        raise FileNotFoundError(
            f"{kind} が見つかりません。探した場所:\n"
            f"  - {local}\n"
            f"  - {(root / kind) if root else '(lab-data が見つからない)'}\n"
            f"データリポジトリを本体の隣に clone するか、環境変数 LAB_DATA_DIR を "
            f"設定してください。手順は AGENTS.md 11章。"
        )
    return local


def experiment_dir(must_exist=True):
    """実験データ（``ex_data/``・``ex_index.csv``・``patA``〜``patC`` など）。"""
    return resolve("experiment", must_exist)


def sim_csv_dir(must_exist=True):
    """シミュレーション出力 CSV（``sim_csv``）。"""
    return resolve("simulation/sim_csv", must_exist)


def sim_dir(must_exist=True):
    """シミュレーション出力 CSV（``sim``）。"""
    return resolve("simulation/sim", must_exist)


if __name__ == "__main__":
    print(f"本体リポジトリ : {REPO_ROOT}")
    print(f"データリポジトリ: {data_repo_root() or '(見つからない)'}")
    for k in _LAYOUT:
        try:
            print(f"  {k:32s} -> {resolve(k)}")
        except FileNotFoundError:
            print(f"  {k:32s} -> (無し)")
