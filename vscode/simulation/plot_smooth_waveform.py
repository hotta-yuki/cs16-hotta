import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# sourse_new_2 などの共通設定をインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sourse_new_2 as sn2

def main():
    # 日本語フォントの設定（japanize_matplotlibがあれば使用）
    try:
        import japanize_matplotlib
    except ImportError:
        pass

    csv_path = os.path.join("tmp_output", "cupy_pitch200_depth0.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    # 波形データ読み込み
    wave = np.loadtxt(csv_path, delimiter=',')
    
    # 時間軸の計算 [s] および [μs]
    # dt は sourse_new_2 のシミュレーション時間ステップ
    dt = sn2.dt
    t_us = np.arange(len(wave)) * dt * 1e6
    
    print(f"Total time steps: {len(wave)}")
    print(f"Time step dt = {dt*1e9:.4f} ns")
    print(f"Total simulation time: {t_us[-1]:.3f} μs")

    # B1反射波 (1回目の底面反射波) の探索範囲: index 7000 〜 13000 付近 (約 5.0 μs 〜 9.0 μs)
    search_start = 7000
    search_end = 13000
    b1_region = wave[search_start:search_end]
    
    # ピーク位置 (B1 反射波の最大値インデックス)
    peak_idx_local = np.argmax(np.abs(b1_region))
    peak_idx_global = search_start + peak_idx_local
    peak_time_us = t_us[peak_idx_global]
    
    print(f"B1 Echo Peak Index: {peak_idx_global}")
    print(f"B1 Echo Arrival Time: {peak_time_us:.3f} μs")
    print(f"B1 Echo Max Amplitude: {wave[peak_idx_global]:.6f}")

    # B1 反射波の切り出し (kiritori2 使用)
    left_pts = sn2.left   # 1024 点
    right_pts = sn2.right # 3072 点
    
    b1_cut = sn2.kiritori2(wave[search_start:search_end], left_pts, right_pts)
    t_b1_cut_us = np.arange(-left_pts, right_pts) * dt * 1e6  # ピーク相対時間 [μs]

    # FFT スペクトル計算
    fft_amp, freq = sn2.make_fftdata(b1_cut, dt)
    freq_mhz = freq / 1e6  # 周波数 [MHz]
    
    # ピーク周波数の特定 (2 ~ 8 MHz の範囲で探索)
    mhz_mask = (freq_mhz >= 1.0) & (freq_mhz <= 10.0)
    freq_in_range = freq_mhz[mhz_mask]
    amp_in_range = fft_amp[mhz_mask]
    peak_freq_mhz = freq_in_range[np.argmax(amp_in_range)]
    print(f"B1 Echo Peak Frequency: {peak_freq_mhz:.3f} MHz")

    output_dir = "tmp_output"
    os.makedirs(output_dir, exist_ok=True)

    # 1. 全時間波形のプロット
    plt.figure(figsize=(10, 4.5), dpi=150)
    plt.plot(t_us, wave, color='#1f77b4', linewidth=1.2, label='送信・反射波 (全時間)')
    plt.axvspan(t_us[search_start], t_us[search_end], color='red', alpha=0.15, label='B1反射波 検出ウィンドウ')
    plt.axvline(peak_time_us, color='red', linestyle='--', linewidth=1.0, label=f'B1ピーク ({peak_time_us:.2f} μs)')
    plt.title('Smooth Surface', fontsize=13)
    plt.xlabel('Time [μs]', fontsize=11)
    plt.ylabel('Normalized Stress Amplitude T1', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    full_plot_path = os.path.join(output_dir, "smooth_surface_full_waveform.png")
    plt.savefig(full_plot_path)
    plt.close()
    print(f"Saved: {full_plot_path}")

    # 2. B1 反射波の切り出し波形 (時間軸)
    plt.figure(figsize=(9, 4.5), dpi=150)
    plt.plot(t_b1_cut_us, b1_cut, color='#d62728', linewidth=1.5, label='平滑面 反射波 B1')
    plt.axvline(0, color='black', linestyle=':', alpha=0.7, label='Peak (t=0)')
    plt.title('Smooth Surface', fontsize=13)
    plt.xlabel('Time [μs]', fontsize=11)
    plt.ylabel('Amplitude', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    b1_plot_path = os.path.join(output_dir, "smooth_surface_B1_waveform.png")
    plt.savefig(b1_plot_path)
    plt.close()
    print(f"Saved: {b1_plot_path}")

    # 3. B1 反射波の FFT スペクトル
    plt.figure(figsize=(9, 4.5), dpi=150)
    plt.plot(freq_mhz, fft_amp, color='#2ca02c', linewidth=1.5, label='FFT Spectrum')
    plt.axvline(peak_freq_mhz, color='darkgreen', linestyle='--', label=f'Peak Freq: {peak_freq_mhz:.2f} MHz')
    plt.xlim(0.5, 10.0)
    plt.title('平滑面反射波 (B1) の FFT 周波数スペクトル', fontsize=13)
    plt.xlabel('Frequency [MHz]', fontsize=11)
    plt.ylabel('Spectral Magnitude', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    fft_plot_path = os.path.join(output_dir, "smooth_surface_B1_fft.png")
    plt.savefig(fft_plot_path)
    plt.close()
    print(f"Saved: {fft_plot_path}")

    # 4. 統合サマリープロット (3パネル)
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), dpi=150)
    
    # 上段: 全波形
    axes[0].plot(t_us, wave, color='#1f77b4', linewidth=1.0)
    axes[0].axvspan(t_us[search_start], t_us[search_end], color='red', alpha=0.15, label='B1 Window')
    axes[0].set_title('(a) 全時間波形 (Full Simulation Waveform)', fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Time [μs]', fontsize=10)
    axes[0].set_ylabel('Stress T1', fontsize=10)
    axes[0].grid(True, linestyle=':', alpha=0.6)
    axes[0].legend(loc='upper right')

    # 中段: B1 抽出波形
    axes[1].plot(t_b1_cut_us, b1_cut, color='#d62728', linewidth=1.2)
    axes[1].set_title('(b) 平滑面 底面反射波 B1 (Extracted B1 Waveform)', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Time relative to peak [μs]', fontsize=10)
    axes[1].set_ylabel('Stress T1', fontsize=10)
    axes[1].grid(True, linestyle=':', alpha=0.6)

    # 下段: FFT スペクトル
    axes[2].plot(freq_mhz, fft_amp, color='#2ca02c', linewidth=1.2)
    axes[2].axvline(peak_freq_mhz, color='darkgreen', linestyle='--', label=f'Peak: {peak_freq_mhz:.2f} MHz')
    axes[2].set_xlim(0.5, 10.0)
    axes[2].set_title('(c) B1 反射波の FFT スペクトル (FFT Spectrum of B1)', fontsize=11, fontweight='bold')
    axes[2].set_xlabel('Frequency [MHz]', fontsize=10)
    axes[2].set_ylabel('Magnitude', fontsize=10)
    axes[2].grid(True, linestyle=':', alpha=0.6)
    axes[2].legend(loc='upper right')

    plt.tight_layout()
    summary_plot_path = os.path.join(output_dir, "smooth_surface_summary.png")
    plt.savefig(summary_plot_path)
    plt.close()
    print(f"Saved summary: {summary_plot_path}")

    # B1反射波データ単体を CSV として出力
    b1_csv_path = os.path.join(output_dir, "smooth_surface_B1_waveform.csv")
    np.savetxt(b1_csv_path, b1_cut, delimiter=',', header='B1_Waveform_Amplitude', comments='')
    print(f"Saved B1 CSV: {b1_csv_path}")

if __name__ == "__main__":
    main()
