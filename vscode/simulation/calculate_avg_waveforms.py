import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from naming import SIM_SHAPE, mm_code, sim_csv_name

# 設定
base_dir = r'vscode/simulation/data'
data_dir = os.path.join(base_dir, 'ex_data')
index_file = os.path.join(base_dir, 'ex_index.csv')
avg_dir = os.path.join(base_dir, 'avg_waveforms')
compare_dir = os.path.join(base_dir, 'comparison_plots')
sim_dir = r'tmp_output/sim_csv'

for d in [avg_dir, compare_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

# カット範囲 (秒)
T_START = 5.5e-6
T_END = 9.0e-6

# FFT設定
fft_N = 2**14 # 16384点

# シミュレーション定数
rho = 7840
E = 206e9
V = 0.27
cl = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))
dx = 1.0e-5
SIM_DT = dx / cl / np.sqrt(6)

def load_simulation_data(pitch_mm, depth_mm, width_mm):
    # 命名規則は AGENTS.md 7章（先輩リポジトリと共通）。値は [m] で渡す
    sim_filename = sim_csv_name(SIM_SHAPE, pitch_mm / 1000, width_mm / 1000, depth_mm / 1000)
    sim_path = os.path.join(sim_dir, sim_filename)
    if not os.path.exists(sim_path):
        return None, None
    
    v_sim = np.loadtxt(sim_path) * -1
    t_sim = np.arange(len(v_sim)) * SIM_DT
    return t_sim, v_sim

def align_peaks(t, v_exp, v_sim):
    """
    ピーク位置を合わせるために v_sim をシフトする。
    """
    idx_exp = np.argmax(np.abs(v_exp))
    idx_sim = np.argmax(np.abs(v_sim))
    
    shift = idx_exp - idx_sim
    if shift > 0:
        v_sim_aligned = np.pad(v_sim, (shift, 0), mode='constant')[:len(v_sim)]
    elif shift < 0:
        v_sim_aligned = np.pad(v_sim, (0, -shift), mode='constant')[-shift : -shift + len(v_sim)]
    else:
        v_sim_aligned = v_sim
        
    return v_sim_aligned

# インデックスファイルの読み込み
df_index = pd.read_csv(index_file)

print(f"Processing {len(df_index)} groups...")

for idx, row in df_index.iterrows():
    start = int(row['index_start'])
    end = int(row['index_end'])
    pitch_mm = float(row['pitch (mm)'])
    depth_mm = float(row['dipth (mm)'])
    width_mm = float(row['width (mm)'])

    # グループ名も値[mm]×100 のコードで揃える (AGENTS.md 7章)
    group_name = (f"p{mm_code(pitch_mm)}_w{mm_code(width_mm)}_d{mm_code(depth_mm)}"
                  f"_{start}_{end}")

    # シミュレーションデータの存在確認 (一致する場合のみ処理するため)
    t_sim_raw, v_sim_raw = load_simulation_data(pitch_mm, depth_mm, width_mm)
    if t_sim_raw is None:
        # print(f"Skipping {group_name}: No matching simulation data.")
        continue

    print(f"Processing Comparison: {group_name}")
    
    waveforms = []
    ffts = []
    time_axis = None
    freq_axis = None
    exp_dt = None
    
    # 実験データの収集
    for i in range(start, end + 1):
        file_path = os.path.join(data_dir, f"scope_{i}.csv")
        if not os.path.exists(file_path):
            continue
        try:
            data = pd.read_csv(file_path, encoding='SHIFT-JIS', header=None, skiprows=2)
            t = data.iloc[:, 0].values
            v = data.iloc[:, 1].values
            mask = (t >= T_START) & (t <= T_END)
            t_cut = t[mask]
            v_cut = v[mask]
            if len(v_cut) == 0: continue
            v_mode = pd.Series(v_cut).mode()
            if not v_mode.empty: v_cut = v_cut - v_mode.iloc[0]
            waveforms.append(v_cut)
            if exp_dt is None: exp_dt = t_cut[1] - t_cut[0]
            if time_axis is None: time_axis = t_cut
            
            # FFT (Exp)
            howmanyzero = fft_N - len(v_cut)
            data_fft = np.concatenate([np.zeros(int(howmanyzero / 2)), v_cut, np.zeros(int(howmanyzero / 2) + howmanyzero % 2)], 0)
            yf = np.fft.rfft(data_fft) / (fft_N / 2)
            ffts.append(np.abs(yf))
            if freq_axis is None: freq_axis = np.fft.rfftfreq(fft_N, d=exp_dt)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if waveforms:
        # 実験データ平均
        min_len = min(len(w) for w in waveforms)
        wave_arr = np.array([w[:min_len] for w in waveforms])
        time_axis = time_axis[:min_len]
        avg_wave_exp = wave_arr.mean(axis=0)
        avg_fft_exp = np.array(ffts).mean(axis=0)
        
        # シミュレーション処理
        f_interp = interp1d(t_sim_raw, v_sim_raw, kind='cubic', fill_value="extrapolate")
        avg_wave_sim = f_interp(time_axis)
        
        # ピーク合わせ
        avg_wave_sim_aligned = align_peaks(time_axis, avg_wave_exp, avg_wave_sim)
        
        # FFT (Sim - 合わせた波形から再計算)
        howmanyzero_sim = fft_N - len(avg_wave_sim_aligned)
        data_fft_sim = np.concatenate([np.zeros(int(howmanyzero_sim / 2)), avg_wave_sim_aligned, np.zeros(int(howmanyzero_sim / 2) + howmanyzero_sim % 2)], 0)
        yf_sim = np.fft.rfft(data_fft_sim) / (fft_N / 2)
        avg_fft_sim = np.abs(yf_sim)

        # 保存 (Time/FFT CSV は avg_dir へ)
        pd.DataFrame({'time': time_axis, 'voltage': avg_wave_exp}).to_csv(os.path.join(avg_dir, f"avg_wave_{group_name}.csv"), index=False)
        pd.DataFrame({'frequency': freq_axis, 'amplitude': avg_fft_exp}).to_csv(os.path.join(avg_dir, f"avg_fft_{group_name}.csv"), index=False)

        # プロット (波形比較 - compare_dir)
        plt.figure(figsize=(8, 4))
        plt.plot(time_axis * 1e6, avg_wave_exp, label='Experiment', alpha=0.7)
        scale = np.max(np.abs(avg_wave_exp)) / np.max(np.abs(avg_wave_sim_aligned)) if np.max(np.abs(avg_wave_sim_aligned)) != 0 else 1
        plt.plot(time_axis * 1e6, avg_wave_sim_aligned * scale, label=f'Simulation (aligned & scaled)', linestyle='--', alpha=0.7)
        plt.title(f"Peak Aligned Waveform: {group_name}")
        plt.xlabel("Time (us)")
        plt.ylabel("Voltage / Normalized Sim")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(compare_dir, f"compare_wave_{group_name}.png"))
        plt.close()

        # プロット (FFT比較 - compare_dir)
        plt.figure(figsize=(8, 4))
        plt.plot(freq_axis / 1e6, avg_fft_exp, label='Experiment', alpha=0.7)
        scale_fft = np.max(avg_fft_exp) / np.max(avg_fft_sim) if np.max(avg_fft_sim) != 0 else 1
        plt.plot(freq_axis / 1e6, avg_fft_sim * scale_fft, label=f'Simulation (scaled)', linestyle='--', alpha=0.7)
        plt.title(f"FFT Comparison: {group_name}")
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Amplitude")
        plt.xlim(0, 15)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(compare_dir, f"compare_fft_{group_name}.png"))
        plt.close()

print("Done.")
