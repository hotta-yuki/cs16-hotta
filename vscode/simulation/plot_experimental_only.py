import sourse_new_2 as s2
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import numpy as np

"""
vscode\simulation\data\patA 内の実験データのみを読み込み、
波形および FFT スペクトルをプロットするスクリプト。
sourse_new_2.py の信号処理関数を利用します。
"""

# =============================================================================
# 設定
# =============================================================================
# データが格納されているディレクトリ
data_dir = os.path.join("vscode\simulation\data\patA_csv")  

# 保存先
output_dir = "tmp_output"
os.makedirs(output_dir, exist_ok=True)

# =============================================================================
# データ読み込み関数 (sourse_new_2.import_data のロジックを流用)
# =============================================================================
def load_experiment_data(target_dir):
    """
    指定したディレクトリ内の全 CSV ファイルを読み込み、平均波形を返す。
    """
    csv_files = glob.glob(os.path.join(target_dir, "*.csv"))
    if not csv_files:
        print(f"Error: No CSV files found in {target_dir}")
        return None

    all_waveforms = []
    for csv_file in csv_files:
        # print(f"Reading: {os.path.basename(csv_file)}")
        # ヘッダ 2 行をスキップ。sourse_new_2 と同様に Shift-JIS (or UTF-8) で読み込み
        try:
            df = pd.read_csv(csv_file, header=None, skiprows=2)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, header=None, skiprows=2, encoding='SHIFT-JIS')
        
        # 列 1 が電圧データ
        volts = df.iloc[:, 1].astype(float)
        # バイアス除去 (最頻値を引く)
        bias = volts.mode().iloc[0]
        all_waveforms.append(volts - bias)

    # 全ファイルの平均を算出
    data_arr = np.array(all_waveforms)
    mean_waveform = data_arr.mean(0)
    return mean_waveform

# =============================================================================
# メイン処理
# =============================================================================

print(f"Loading data from {data_dir}...")
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

if not csv_files:
    print(f"Error: No CSV files found in {data_dir}")
else:
    plt.figure(figsize=(10, 6))
    
    all_yf = []
    
    print("Processing individual files and performing FFT...")
    for i, csv_file in enumerate(csv_files):
        # データ読み込み
        try:
            df = pd.read_csv(csv_file, header=None, skiprows=2)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, header=None, skiprows=2, encoding='SHIFT-JIS')
        
        volts = df.iloc[:, 1].astype(float)
        bias = volts.mode().iloc[0]
        waveform = volts - bias
        
        # FFT スペクトルの算出 (sourse_new_2 の関数を使用)
        # 波形のピーク付近を切り出す
        cut_wave = s2.kiritori2(waveform, s2.left, s2.right)
        yf, freq = s2.make_fftdata(cut_wave, s2.exp_dt)
        
        all_yf.append(yf)
        
        # 個別スペクトルのプロット (薄い色で描画)
        plt.plot(freq, yf, alpha=0.3, linewidth=0.5)

    # 平均スペクトルの算出とプロット
    mean_yf = np.mean(all_yf, axis=0)
    plt.plot(freq, mean_yf, color='black', linewidth=2, label="Average Spectrum")

    # グラフ設定
    plt.xlim(2e6, 8e6)  # 2 - 8 MHz
    plt.title("Individual and Average FFT Spectra (patA)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, "exp_fft_individual_patA.png")
    plt.savefig(save_path)
    print(f"Saved individual FFT plot to {save_path}")

    plt.show()
