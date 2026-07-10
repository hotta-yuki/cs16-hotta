import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys

# sourse_new_2のインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sourse_new_2 as sn2

input_dir = 'vscode\\simulation\\tmp'
output_dir_waveform = 'tmp_output/plots_simulation_waveform'
output_dir_fft = 'tmp_output/plots_simulation_fft'

os.makedirs(output_dir_waveform, exist_ok=True)
os.makedirs(output_dir_fft, exist_ok=True)

csv_files = glob.glob(os.path.join(input_dir, 'sim_*.csv'))

# 初期パルスを避けるための検索開始オフセット
search_offset = 8000

# FFTのプロット範囲（200kHzから10MHz）
fft_freq_min = 2000000
fft_freq_max = 10000000

# 縦軸の固定範囲
waveform_ylim_min = -1.5
waveform_ylim_max = 1.5
fft_ylim_min = 0
fft_ylim_max = 0.04

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file, header=None)
        waveform = df.iloc[:, 0].values
        
        # kiritori2 を用いたカット
        # sourse_new_2 の定数 (left, right) を使用
        sliced_waveform = sn2.kiritori2(waveform[search_offset:], sn2.left, sn2.right)
            
        # 波形のプロット（インデックス対電圧）
        plt.figure(figsize=(8, 4))
        x_axis = np.arange(len(sliced_waveform))
        plt.plot(x_axis, sliced_waveform)
        plt.title(f"{os.path.basename(csv_file)} - Waveform")
        plt.xlabel('Index')
        plt.ylabel('Amplitude')
        plt.ylim(waveform_ylim_min, waveform_ylim_max)
        plt.grid(True)
        
        waveform_output_filename = os.path.basename(csv_file).replace('.csv', '_waveform.png')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir_waveform, waveform_output_filename))
        plt.close()
        
        # FFTのプロット
        plt.figure(figsize=(8, 4))
        fft_amp, freq = sn2.make_fftdata(sliced_waveform, sn2.exp_dt)
        plt.plot(freq, fft_amp)
        plt.title(f"{os.path.basename(csv_file)} - FFT")
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Magnitude')
        plt.xlim(fft_freq_min, fft_freq_max)
        plt.ylim(fft_ylim_min, fft_ylim_max)
        plt.grid(True)
        
        fft_output_filename = os.path.basename(csv_file).replace('.csv', '_fft.png')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir_fft, fft_output_filename))
        plt.close()
        
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

print(f"Processed {len(csv_files)} files. Waveform plots saved to {output_dir_waveform}. FFT plots saved to {output_dir_fft}.")
