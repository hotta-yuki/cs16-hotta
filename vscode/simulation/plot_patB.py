import sourse_new_2 as s2
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import glob
import pandas as pd
import numpy as np

"""
vscode\simulation\data\patB_csv 内の実験データを読み込み、
平均波形および FFT スペクトル（個別・平均）をプロットするスクリプト。
切り出し範囲（窓関数）の可視化機能付き。
"""

# =============================================================================
# 設定
# =============================================================================
data_dir = os.path.join("vscode", "simulation", "data", "patB_csv")  
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
        waveform = (volts - bias).values
        all_waveforms.append(waveform)
        
        # FFT スペクトルの算出
        # s2.left, s2.right は sourse_new_2.py で定義されている (1024, 3072)
        cut_wave = s2.kiritori2(waveform, s2.left, s2.right)
        yf, freq = s2.make_fftdata(cut_wave, s2.exp_dt)
        all_yf.append(yf)

    # 1. 平均波形のプロットと切り出し範囲の可視化
    print("Plotting average waveform with window visualization...")
    mean_waveform = np.mean(all_waveforms, axis=0)
    
    # 窓の範囲を特定 (平均波形のピークを基準とする)
    peak_idx = np.nanargmax(mean_waveform)
    start_idx = peak_idx - s2.left
    end_idx = peak_idx + s2.right
    
    plt.figure(figsize=(10, 6))
    # ユーザーが index を参照しやすいため x 軸を index に変更
    plt.plot(mean_waveform, color='blue', label="平均波形")
    
    # 切り出し範囲を垂直線で表示
    plt.axvline(start_idx, color='red', linestyle='--', label=f"窓開始: {start_idx}")
    plt.axvline(end_idx, color='red', linestyle='--', label=f"窓終了: {end_idx}")
    
    plt.title("Average Waveform and FFT Window (patB)")
    plt.xlabel("Index")
    plt.ylabel("Amplitude [V]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    waveform_path = os.path.join(output_dir, "exp_waveform_patB.png")
    plt.savefig(waveform_path)
    plt.close()
    print(f"Saved average waveform with window to {waveform_path}")

    # 2. FFT スペクトルのプロット (個別 + 平均)
    print("Plotting FFT spectra...")
    plt.figure(figsize=(10, 6))
    for yf in all_yf:
        plt.plot(freq, yf, alpha=0.3, linewidth=0.5)

    mean_yf = np.mean(all_yf, axis=0)
    plt.plot(freq, mean_yf, color='black', linewidth=2, label="Average Spectrum")

    plt.xlim(2e6, 8e6)  # 2 - 8 MHz
    plt.title("Individual and Average FFT Spectra (patB)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    
    fft_path = os.path.join(output_dir, "exp_fft_individual_patB.png")
    plt.savefig(fft_path)
    plt.close()
    print(f"Saved FFT plot to {fft_path}")

    print(f"Window Summary: Index {start_idx} to {end_idx} (Total {end_idx - start_idx} points)")
    print("Done.")
