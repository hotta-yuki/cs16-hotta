import sourse_new_2 as s2
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import glob
import pandas as pd
import numpy as np
import argparse

"""
指定されたディレクトリ内の実験データを読み込み、
波形（インデックス6000まで）および FFT スペクトルをプロットするスクリプト。
sourse_new_2.py の信号処理関数を利用します。
"""

# =============================================================================
# 設定
# =============================================================================
parser = argparse.ArgumentParser(description="Plot waveforms and FFT spectra from experimental data.")
parser.add_argument("--data_dir", type=str, default=os.path.join("vscode", "simulation", "data", "patA_csv"), help="Data directory containing CSV files")
parser.add_argument("--output_dir", type=str, default="tmp_output", help="Output directory for plots")
args = parser.parse_args()

# データが格納されているディレクトリ
data_dir = args.data_dir
output_dir = args.output_dir
pattern_name = os.path.basename(os.path.normpath(data_dir))

os.makedirs(output_dir, exist_ok=True)

# =============================================================================
# メイン処理
# =============================================================================

print(f"Loading data from {data_dir}...")
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

if not csv_files:
    print(f"Error: No CSV files found in {data_dir}")
else:
    all_waveforms = []
    all_yf = []
    
    print("Processing individual files...")
    for i, csv_file in enumerate(csv_files):
        # データ読み込み
        try:
            df = pd.read_csv(csv_file, header=None, skiprows=2)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, header=None, skiprows=2, encoding='SHIFT-JIS')
        
        # 列 1 が電圧データ (6000までにカット)
        volts = df.iloc[:6000, 1].astype(float)
        # バイアス除去 (最頻値を引く)
        bias = volts.mode().iloc[0]
        waveform = (volts - bias).values
        all_waveforms.append(waveform)
        
        # FFT スペクトルの算出 (sourse_new_2 の関数を使用)
        # 波形のピーク付近を切り出す
        cut_wave = s2.kiritori2(waveform, s2.left, s2.right)
        yf, freq = s2.make_fftdata(cut_wave, s2.exp_dt)
        all_yf.append(yf)

    # 1. 時間軸波形のプロット (インデックス6000まで)
    print("Plotting time-domain waveforms...")
    plt.figure(figsize=(10, 6))
    for wf in all_waveforms:
        plt.plot(wf, color='gray', alpha=0.1, linewidth=0.5)
    
    mean_waveform = np.mean(all_waveforms, axis=0)
    plt.plot(mean_waveform, color='black', linewidth=1.5, label="平均波形")
    
    plt.xlim(0, 6000)
    plt.title(f"Experimental Waveforms ({pattern_name})")
    plt.xlabel("Index")
    plt.ylabel("Amplitude [V]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    waveform_save_path = os.path.join(output_dir, f"exp_waveform_{pattern_name}.png")
    plt.savefig(waveform_save_path)
    plt.close()
    print(f"Saved waveform plot to {waveform_save_path}")

    # 2. FFT スペクトルのプロット (個別 + 平均)
    print("Plotting FFT spectra...")
    plt.figure(figsize=(10, 6))
    for yf in all_yf:
        plt.plot(freq, yf, alpha=0.3, linewidth=0.5)

    mean_yf = np.mean(all_yf, axis=0)
    plt.plot(freq, mean_yf, color='black', linewidth=2, label="Average Spectrum")

    # グラフ設定
    plt.xlim(2e6, 8e6)  # 2 - 8 MHz
    plt.title(f"Individual and Average FFT Spectra ({pattern_name})")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    
    fft_save_path = os.path.join(output_dir, f"exp_fft_individual_{pattern_name}.png")
    plt.savefig(fft_save_path)
    plt.close()
    print(f"Saved individual FFT plot to {fft_save_path}")

    print("Done.")
