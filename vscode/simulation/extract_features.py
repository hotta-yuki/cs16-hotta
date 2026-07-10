import pandas as pd
import numpy as np
import os
import glob
import re
import sys

# sourse_new_2のインポート（パスの解決）
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sourse_new_2 as sn2

def extract_params(filename):
    """
    ファイル名からpitch, depth, widthを抽出する。
    例: sim_pitch1250_depth200_width150.csv -> (1250, 200, 150)
    """
    pitch = int(re.search(r'pitch(\d+)', filename).group(1))
    depth = int(re.search(r'depth(\d+)', filename).group(1))
    width = int(re.search(r'width(\d+)', filename).group(1))
    return pitch, depth, width

def calculate_features(waveform, dt):
    """
    波形から特徴量を計算する。
    """
    # 時間領域の特徴
    max_amp = np.max(np.abs(waveform))
    p2p = np.max(waveform) - np.min(waveform)
    energy = np.sum(waveform**2)
    rms = np.sqrt(np.mean(waveform**2))
    
    # FFT (sourse_new_2 の定数・関数を使用)
    # ここでは生のシミュレーション時間ステップ dt を使用する想定
    # もし比較のために実験サンプリングレートに合わせるなら補間が必要だが、
    # 単純な特徴抽出なら生データでも可。
    mag, freq = sn2.make_fftdata(waveform, dt)
    
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

def main():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
    output_file = 'simulation_features.csv'
    
    csv_files = glob.glob(os.path.join(input_dir, 'sim_*.csv'))
    if not csv_files:
        print(f"No files found in {input_dir}")
        return

    results = []
    
    # シミュレーションのdtを取得
    # sourse_new_2.dt は dx / cl / sqrt(6)
    sim_dt = sn2.dt
    print(f"Using simulation dt: {sim_dt}")

    for csv_path in sorted(csv_files):
        filename = os.path.basename(csv_path)
        print(f"Processing {filename}...")
        
        try:
            pitch, depth, width = extract_params(filename)
            df = pd.read_csv(csv_path, header=None)
            waveform = df.iloc[:, 0].values
            
            # 初期パルス等を避けるためのオフセット（sourse_new_2のsim_a1付近を参考に）
            # search_offset = 8000 (plot_simdata_compare.pyより)
            offset = 8000
            if len(waveform) > offset:
                sliced_waveform = sn2.kiritori2(waveform[offset:], sn2.left, sn2.right)
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
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False)
        print(f"\nFeature extraction completed. Results saved to {output_file}")
    else:
        print("No features extracted.")

if __name__ == "__main__":
    main()
