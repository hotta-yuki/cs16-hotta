"""
loop_UT_sim.py — simdata.csv のパラメータで 2D FDTD をまとめて回す

出力ずみの条件は飛ばすので、途中で止めても続きから再開できる。
"""

import itertools
import os

import UT_FlawVariation_Sim
from config import DATA_SIM_DIR, SIMDATA_CSV, SIM_OUT_DIR
from naming import SIM_SHAPE, sim_csv_name


def load_simdata(file_path):
    """
    simdata.csv からパラメータを読み込む。
    形式:
    f_width
    val1
    val2
    f_pitch
    val1
    ...
    """
    params = {
        'f_width': [],
        'f_pitch': [],
        'f_depth': []
    }

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return params

    current_key = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line in params:
                current_key = line
            elif current_key:
                try:
                    params[current_key].append(float(line))
                except ValueError:
                    print(f"Warning: Could not parse value '{line}' for {current_key}")

    return params

def main():
    # パラメータ表も出力先も config.py が絶対パスで持っている。
    # どのディレクトリから実行しても同じファイルを読み書きする。
    params = load_simdata(SIMDATA_CSV)

    widths = params['f_width']
    pitches = params['f_pitch']
    depths = params['f_depth']

    print("Parameters loaded:")
    print(f"  f_width: {widths}")
    print(f"  f_pitch: {pitches}")
    print(f"  f_depth: {depths}")

    # 全組み合わせの生成
    combinations = list(itertools.product(widths, pitches, depths))
    total = len(combinations)
    print(f"\nTotal simulations to run: {total}")

    for i, (w, p, d) in enumerate(combinations):
        # ファイル名の生成と存在確認
        # 命名規則は AGENTS.md 7章（先輩リポジトリと共通）
        filename = sim_csv_name(SIM_SHAPE, p, w, d)
        check_paths = [
            os.path.join(SIM_OUT_DIR, filename),
            os.path.join(DATA_SIM_DIR, filename),
        ]

        exists = False
        for path in check_paths:
            if os.path.exists(path):
                print(f"\n[{i+1}/{total}] Skipping: {filename} already exists in {os.path.dirname(path)}")
                exists = True
                break

        if exists:
            continue

        print(f"\n[{i+1}/{total}] Starting simulation...")
        UT_FlawVariation_Sim.run_simulation(f_width=w, f_pitch=p, f_depth=d)

if __name__ == "__main__":
    main()
