"""
plot_simdata_compare.py — 条件違いのシミュレーション波形・FFT を重ね書きして比較する

入力は既定で config.SIM_OUT_DIR（lab/tmp_output/sim）。
別の場所を見たいときは --input-dir で指定する。
"""

import argparse
import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import COMPARE_OUT_DIR, SIM_OUT_DIR, exp_dt, left, right, search_offset
from naming import SIM_SHAPE
from signal_utils import kiritori2, make_fftdata

# FFTのプロット範囲
FFT_FREQ_MIN = 2000000
FFT_FREQ_MAX = 10000000


def parse_cli_args(argv=None):
    parser = argparse.ArgumentParser(
        description="シミュレーション波形の比較プロットを作る。")
    parser.add_argument("--input-dir", default=SIM_OUT_DIR,
                        help="波形 CSV のあるフォルダ（既定: lab/tmp_output/sim）")
    parser.add_argument("--output-dir", default=COMPARE_OUT_DIR,
                        help="図の出力先（既定: lab/tmp_output/comparison_plots）")
    parser.add_argument("--offset", type=int, default=search_offset,
                        help="初期パルスを避けるための検索開始オフセット")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_cli_args(argv)
    input_dir = args.input_dir
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # 比較対象のCSVファイルを取得（ソートして順番を固定）
    # 命名規則は AGENTS.md 7章。改名前の旧命名（sim_*.csv）も拾えるようにしておく。
    csv_files = sorted(glob.glob(os.path.join(input_dir, f'{SIM_SHAPE.lower()}_cupy_*.csv'))
                       + glob.glob(os.path.join(input_dir, 'sim_*.csv')))

    if not csv_files:
        print(f"No simulation CSV files found in {input_dir}")
        return 1

    # プロットの初期化
    fig_wave, ax_wave = plt.subplots(figsize=(12, 6))
    fig_fft, ax_fft = plt.subplots(figsize=(12, 6))

    print(f"Found {len(csv_files)} files. Starting comparison plotting...")

    for csv_file in csv_files:
        try:
            # ファイル名からラベルを作成
            # 例: kukei_cupy_pitch125_width15_depth20.csv -> pitch125_width15_depth20
            label = os.path.basename(csv_file).replace('.csv', '')
            for prefix in (f'{SIM_SHAPE.lower()}_cupy_', 'sim_'):
                if label.startswith(prefix):
                    label = label[len(prefix):]
                    break

            df = pd.read_csv(csv_file, header=None)
            waveform = df.iloc[:, 0].values

            # kiritori2 を用いたカット（切り出し幅は config の left / right）
            sliced_waveform = kiritori2(waveform[args.offset:], left, right)

            # 波形のプロット（重ね書き）
            x_axis = np.arange(len(sliced_waveform))
            ax_wave.plot(x_axis, sliced_waveform, label=label, alpha=0.7, linewidth=1)

            # FFTの計算とプロット（重ね書き）
            fft_amp, freq = make_fftdata(sliced_waveform, exp_dt)
            ax_fft.plot(freq, fft_amp, label=label, alpha=0.7, linewidth=1)

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

    # 波形プロットの整形
    ax_wave.set_title("Waveform Comparison")
    ax_wave.set_xlabel("Index")
    ax_wave.set_ylabel("Amplitude")
    ax_wave.grid(True)
    # 凡例が多い場合は外側に配置
    ax_wave.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small',
                   ncol=2 if len(csv_files) > 15 else 1)
    fig_wave.tight_layout()
    fig_wave.savefig(os.path.join(output_dir, 'comparison_waveform.png'))

    # FFTプロットの整形
    ax_fft.set_title("FFT Comparison")
    ax_fft.set_xlabel("Frequency [Hz]")
    ax_fft.set_ylabel("Magnitude")
    ax_fft.set_xlim(FFT_FREQ_MIN, FFT_FREQ_MAX)
    ax_fft.grid(True)
    ax_fft.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small',
                  ncol=2 if len(csv_files) > 15 else 1)
    fig_fft.tight_layout()
    fig_fft.savefig(os.path.join(output_dir, 'comparison_fft.png'))

    plt.close('all')
    print(f"Comparison completed. Plots saved to: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
