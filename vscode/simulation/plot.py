import sourse_new_2 as s2
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import glob
import pandas as pd
import numpy as np

from data_paths import experiment_dir

"""
vscode\simulation\data\patC_csv 内の実験データを読み込み、
平均波形および FFT スペクトル（個別・平均）をプロットするスクリプト。
"""

# =============================================================================
# 設定
# =============================================================================
data_dir = os.path.join(experiment_dir(), "patC_csv")  # 場所は data_paths.py が解決
output_dir = "tmp_output"
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
        try:
            df = pd.read_csv(csv_file, header=None, skiprows=2)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, header=None, skiprows=2, encoding='SHIFT-JIS')
        
        volts = df.iloc[:, 1].astype(float)
        bias = volts.mode().iloc[0]
        # インデックス6000まででカット
        waveform = (volts - bias).iloc[:6000].values
        all_waveforms.append(waveform)
        
        # FFT スペクトルの算出
        cut_wave = s2.kiritori2(waveform, s2.left, s2.right)
        yf, freq = s2.make_fftdata(cut_wave, s2.exp_dt)
        all_yf.append(yf)

    # 1. 時間軸波形のプロット
    print("Plotting waveforms...")
    mean_waveform = np.mean(all_waveforms, axis=0)
    
    plt.figure(figsize=(10, 6))
    
    # 平均波形のみを表示
    plt.plot(mean_waveform, color='black', linewidth=1.5, label="平均波形")
    
    plt.title("Average Waveform (patC)")
    plt.xlabel("Index")
    plt.ylabel("Amplitude [V]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    waveform_path = os.path.join(output_dir, "exp_waveform_patC.png")
    plt.savefig(waveform_path)
    plt.close()
    print(f"Saved waveform plot to {waveform_path}")

    # 2. FFT スペクトルのプロット (個別 + 平均)
    print("Plotting FFT spectra...")
    plt.figure(figsize=(10, 6))
    for yf in all_yf:
        plt.plot(freq, yf, alpha=0.3, linewidth=0.5)

    mean_yf = np.mean(all_yf, axis=0)
    plt.plot(freq, mean_yf, color='black', linewidth=2, label="Average Spectrum")

    plt.xlim(2e6, 8e6)  # 2 - 8 MHz
    plt.title("Individual and Average FFT Spectra (patC)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [V]")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    
    fft_path = os.path.join(output_dir, "exp_fft_individual_patC.png")
    plt.savefig(fft_path)
    plt.close()
    print(f"Saved FFT plot to {fft_path}")

    print("Done.")
