import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys

# sourse_new_2のインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sourse_new_2 as sn2
from naming import SIM_SHAPE

input_dir = 'C:\\Users\\cs16\\lab\\vscode\\simulation\\tmp'
output_dir = 'tmp_output/comparison_plots'
os.makedirs(output_dir, exist_ok=True)

# 比較対象のCSVファイルを取得（ソートして順番を固定）
csv_files = sorted(glob.glob(os.path.join(input_dir, 'sim_*.csv')))

if not csv_files:
    print(f"No simulation CSV files found in {input_dir}")
    sys.exit()

# 初期パルスを避けるための検索開始オフセット
search_offset = 8000

# FFTのプロット範囲
fft_freq_min = 2000000
fft_freq_max = 10000000

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
        
        # kiritori2 を用いたカット
        # sourse_new_2 の定数 (left, right) を使用
        sliced_waveform = sn2.kiritori2(waveform[search_offset:], sn2.left, sn2.right)
            
        # 波形のプロット（重ね書き）
        x_axis = np.arange(len(sliced_waveform))
        ax_wave.plot(x_axis, sliced_waveform, label=label, alpha=0.7, linewidth=1)
        
        # FFTの計算とプロット（重ね書き）
        fft_amp, freq = sn2.make_fftdata(sliced_waveform, sn2.exp_dt)
        ax_fft.plot(freq, fft_amp, label=label, alpha=0.7, linewidth=1)
        
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

# 波形プロットの整形
ax_wave.set_title("Waveform Comparison")
ax_wave.set_xlabel("Index")
ax_wave.set_ylabel("Amplitude")
ax_wave.grid(True)
# 凡例が多い場合は外側に配置
ax_wave.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2 if len(csv_files) > 15 else 1)
fig_wave.tight_layout()
fig_wave.savefig(os.path.join(output_dir, 'comparison_waveform.png'))

# FFTプロットの整形
ax_fft.set_title("FFT Comparison")
ax_fft.set_xlabel("Frequency [Hz]")
ax_fft.set_ylabel("Magnitude")
ax_fft.set_xlim(fft_freq_min, fft_freq_max)
ax_fft.grid(True)
ax_fft.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2 if len(csv_files) > 15 else 1)
fig_fft.tight_layout()
fig_fft.savefig(os.path.join(output_dir, 'comparison_fft.png'))

plt.close('all')
print(f"Comparison completed. Plots saved to: {output_dir}")
