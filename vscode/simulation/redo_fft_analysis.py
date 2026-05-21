import sourse_new_2 as s2
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
import glob
import pandas as pd
import numpy as np

"""
ユーザー指定の条件で patA, patB の解析をやり直すスクリプト。
条件:
1. 波形全体に対し、幅 2.05 us (4100点) の矩形窓を適用。
   (位置は各波形のピークを中心に、左 1024点、右 3076点とする)
2. データ長が 2^14 (16384点) に達するまで末尾にゼロパディング。
3. FFT を実施。
"""

# =============================================================================
# 設定
# =============================================================================
output_dir = "tmp_output"
os.makedirs(output_dir, exist_ok=True)

# 窓関数の設定 (2.05 us = 4100 points @ 0.5 ns)
WINDOW_WIDTH = 4100
LEFT_OFFSET = 1024
RIGHT_OFFSET = WINDOW_WIDTH - LEFT_OFFSET # 3076

FFT_N = 2**14 # 16384

def process_pattern(pattern_name):
    data_dir = os.path.join("vscode", "simulation", "data", f"{pattern_name}_csv")
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found for {pattern_name}")
        return

    print(f"Processing {pattern_name} ({len(csv_files)} files)...")
    
    all_waveforms = []
    all_windowed_waveforms = []
    all_yf = []
    
    # 窓の範囲を記録用 (最初のファイルで代表)
    first_start, first_end = 0, 0

    for i, csv_file in enumerate(csv_files):
        try:
            df = pd.read_csv(csv_file, header=None, skiprows=2)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, header=None, skiprows=2, encoding='SHIFT-JIS')
        
        volts = df.iloc[:, 1].astype(float)
        bias = volts.mode().iloc[0]
        waveform = (volts - bias).values
        all_waveforms.append(waveform)
        
        # 1. ピーク位置を特定
        peak_idx = np.nanargmax(waveform)
        start_idx = max(0, peak_idx - LEFT_OFFSET)
        end_idx = min(len(waveform), start_idx + WINDOW_WIDTH)
        
        if i == 0:
            first_start, first_end = start_idx, end_idx

        # 2. 矩形窓を適用 (窓の外を0にする)
        waveform_win = np.zeros_like(waveform)
        waveform_win[start_idx:end_idx] = waveform[start_idx:end_idx]
        all_windowed_waveforms.append(waveform_win)
        
        # 3. ゼロパディング (末尾に 16384点になるまで追加)
        padding_needed = FFT_N - len(waveform_win)
        if padding_needed > 0:
            waveform_padded = np.pad(waveform_win, (0, padding_needed), mode='constant')
        else:
            waveform_padded = waveform_win[:FFT_N]
            
        # 4. FFT (正規化: 長さの半分で割る)
        yf = np.fft.rfft(waveform_padded) / (FFT_N / 2)
        all_yf.append(np.abs(yf))

    # 周波数軸
    freq = np.fft.rfftfreq(FFT_N, d=s2.exp_dt)

    # --- プロット ---
    
    # 1. 平均波形と窓の範囲
    print(f"  Plotting waveform for {pattern_name}...")
    mean_waveform = np.mean(all_waveforms, axis=0)
    plt.figure(figsize=(10, 6))
    plt.plot(mean_waveform, label="平均波形", color='blue', alpha=0.7)
    plt.axvline(first_start, color='red', linestyle='--', label=f"窓開始: {first_start}")
    plt.axvline(first_end, color='red', linestyle='--', label=f"窓終了: {first_end}")
    plt.title(f"Average Waveform and FFT Window ({pattern_name})")
    plt.xlabel("Index")
    plt.ylabel("Amplitude [V]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"exp_waveform_{pattern_name}_redo.png"))
    plt.close()

    # 2. FFT スペクトル (個別 + 平均)
    print(f"  Plotting FFT for {pattern_name}...")
    plt.figure(figsize=(10, 6))
    for yf in all_yf:
        plt.plot(freq, yf, alpha=0.3, linewidth=0.5)
    
    mean_yf = np.mean(all_yf, axis=0)
    plt.plot(freq, mean_yf, color='black', linewidth=2, label="Average Spectrum")
    
    plt.xlim(2e6, 8e6)
    plt.title(f"Redone FFT Spectra ({pattern_name})")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"exp_fft_individual_{pattern_name}_redo.png"))
    plt.close()
    
    print(f"  {pattern_name} done. Indices for first file: {first_start} to {first_end}")
    return first_start, first_end

# メイン実行
start_a, end_a = process_pattern("patA")
start_b, end_b = process_pattern("patB")

print("\nSummary of indices (representative):")
print(f"patA: {start_a} to {start_a + WINDOW_WIDTH} (total {WINDOW_WIDTH} pts)")
print(f"patB: {start_b} to {start_b + WINDOW_WIDTH} (total {WINDOW_WIDTH} pts)")
