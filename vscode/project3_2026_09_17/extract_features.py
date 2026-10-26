"""
extract_features.py — シミュレーション波形から特徴量を抽出して CSV にまとめる

入力は既定で config.SIM_OUT_DIR（lab/tmp_output/sim）。
別の場所を見たいときは --input-dir で指定する。
"""

import argparse
import glob
import os
import re

import numpy as np
import pandas as pd

from config import SIM_OUT_DIR, TMP_OUTPUT_DIR, dt as SIM_DT, left, right, search_offset
from naming import SIM_SHAPE
from signal_utils import kiritori2, make_fftdata


def parse_cli_args(argv=None):
    parser = argparse.ArgumentParser(
        description="シミュレーション波形 CSV から特徴量を抽出する。")
    parser.add_argument("--input-dir", default=SIM_OUT_DIR,
                        help="波形 CSV のあるフォルダ（既定: lab/tmp_output/sim）")
    parser.add_argument("--output", default=os.path.join(TMP_OUTPUT_DIR,
                                                         "simulation_features.csv"),
                        help="特徴量 CSV の出力先")
    parser.add_argument("--offset", type=int, default=search_offset,
                        help="波形の先頭スキップ点数（入射パルスを避ける）")
    return parser.parse_args(argv)


def extract_params(filename):
    """
    ファイル名から pitch, width, depth のコードを抽出する。

    コードは値[mm] × 100 (AGENTS.md 7章)。小数コードがあるため int 決め打ちにしない。
    例: kukei_cupy_pitch125_width15_depth12.5.csv -> (125, 15, 12.5)
    """
    def _code(key):
        # depth12.5 のような小数コードを取りこぼさないこと。
        # r'depth(\d+)' だと "12" だけ拾って depth 0.12 と区別できなくなる。
        m = re.search(key + r'(\d+(?:\.\d+)?)', filename)
        if m is None:
            raise ValueError(f"{key} がファイル名にない: {filename}")
        v = float(m.group(1))
        return int(v) if v.is_integer() else v

    return _code('pitch'), _code('width'), _code('depth')

def calculate_features(waveform, dt):
    """
    波形から特徴量を計算する。
    """
    # 時間領域の特徴
    max_amp = np.max(np.abs(waveform))
    p2p = np.max(waveform) - np.min(waveform)
    energy = np.sum(waveform**2)
    rms = np.sqrt(np.mean(waveform**2))

    # FFT (signal_utils の関数を使用)
    # ここでは生のシミュレーション時間ステップ dt を使用する想定
    # もし比較のために実験サンプリングレートに合わせるなら補間が必要だが、
    # 単純な特徴抽出なら生データでも可。
    mag, freq = make_fftdata(waveform, dt)

    # 2MHz - 10MHz の範囲で特徴を抽出
    mask = (freq >= 2e6) & (freq <= 10e6)
    mag_band = mag[mask]
    freq_band = freq[mask]

    peak_freq = freq_band[np.argmax(mag_band)]
    centroid_freq = np.sum(freq_band * mag_band) / np.sum(mag_band)

    # -6dB 帯域幅の簡易計算
    peak_mag = np.max(mag_band)
    threshold = peak_mag / 2.0
    within_threshold = freq_band[mag_band >= threshold]
    if len(within_threshold) > 0:
        bandwidth_6dB = np.max(within_threshold) - np.min(within_threshold)
    else:
        bandwidth_6dB = 0

    return {
        'max_amplitude': max_amp,
        'peak_to_peak': p2p,
        'energy': energy,
        'rms': rms,
        'peak_frequency': peak_freq,
        'centroid_frequency': centroid_freq,
        'bandwidth_6dB': bandwidth_6dB
    }

def main(argv=None):
    args = parse_cli_args(argv)
    input_dir = args.input_dir
    output_file = args.output

    # 命名規則は AGENTS.md 7章。<shape>_cupy_pitch..._width..._depth....csv
    csv_files = glob.glob(os.path.join(input_dir, f'{SIM_SHAPE.lower()}_cupy_*.csv'))
    if not csv_files:
        print(f"No files found in {input_dir}")
        return

    results = []

    # シミュレーションの dt は config.dt（= dx / cl / sqrt(6)）
    sim_dt = SIM_DT
    print(f"Input dir: {input_dir}")
    print(f"Using simulation dt: {sim_dt}")

    for csv_path in sorted(csv_files):
        filename = os.path.basename(csv_path)
        print(f"Processing {filename}...")

        try:
            pitch, width, depth = extract_params(filename)
            df = pd.read_csv(csv_path, header=None)
            waveform = df.iloc[:, 0].values

            # 初期パルス等を避けるためのオフセット（config.search_offset）
            offset = args.offset
            if len(waveform) > offset:
                sliced_waveform = kiritori2(waveform[offset:], left, right)
            else:
                sliced_waveform = waveform

            features = calculate_features(sliced_waveform, sim_dt)

            row = {
                'filename': filename,
                'pitch': pitch,
                'depth': depth,
                'width': width
            }
            row.update(features)
            results.append(row)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if results:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False)
        print(f"\nFeature extraction completed. Results saved to {output_file}")
    else:
        print("No features extracted.")

if __name__ == "__main__":
    main()
