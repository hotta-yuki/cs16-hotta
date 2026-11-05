"""教師データ（train phase 1、60 点）の複素スペクトルを 1 ファイルずつ作る。

    python vscode/surrogate/plot_complex_spectrum.py
    python vscode/surrogate/plot_complex_spectrum.py --set test --phase 2

vscode/simulation/plot_simdata.py と同じ流れ・同じ図の書式で作る。違いは 2 点だけ。

- 切り出しは正しいピーク（平滑面の t0 に最も近い正の山、featurize.cut(t_ref=...)）。
  kiritori2 の正の最大は p=1.14 w=0.48 d=0.30 mm で後続波に乗り 0.6 us ずれる
- FFT は make_fftdata と同じ fft_N 点・同じ正規化（/ (fft_N/2)）だが、絶対値を取らず
  複素数のまま残す。位相の原点は t0（ピーク）に置く。make_fftdata のように前後に
  均等にゼロを足すと原点が配列先頭になり、位相が周波数に比例して大きく回って
  実部・虚部が細かく振動する

出力（vscode/surrogate/tmp_output/features/<set>_ph<phase>_refpeak/complex_spectrum/）
    waveform/<name>_waveform.png   切り出した波形（plot_simdata.py と同じ書式）
    spectrum_png/<name>_complex.png  複素スペクトルの実部・虚部・振幅
    spectrum_csv/<name>_complex.csv  周波数 [Hz], 実部, 虚部（2-8 MHz）
    spectrum_norm_png/<name>_norm.png  平滑面で正規化した R = D / D_smooth の実部・虚部・|R|
    spectrum_norm_csv/<name>_norm.csv  周波数 [Hz], R の実部, 虚部（2-8 MHz）
    complex_spectra.npz            全件まとめ（names, params_mm, freq, D, R）

平滑面自身の R は定義上 1 + 0j になる（確認用にそのまま出力する）。
"""

import argparse
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import featurize as f
from run_design import out_name

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "tmp_output")

# plot_simdata.py と同じ表示範囲
fft_freq_min = 2000000
fft_freq_max = 8000000
waveform_ylim_min = -1.5
waveform_ylim_max = 1.5
fft_ylim_min = -0.06
fft_ylim_max = 0.06
# 正規化スペクトル R は 1 前後（教師 60 点で |R| = 0.06-1.42）
norm_ylim_min = -1.5
norm_ylim_max = 1.5


def complex_fft(seg):
    """make_fftdata と同じ点数・正規化の複素スペクトル。位相の原点は t0（seg の LEFT 点目）。"""
    fft_N = f.sn2.fft_N
    data_fft = np.zeros(fft_N)
    data_fft[:len(seg)] = seg
    data_fft = np.roll(data_fft, -f.LEFT)     # t0 を配列の先頭（時刻 0）に回す
    yf = np.fft.rfft(data_fft) / (fft_N / 2)
    freq = np.fft.rfftfreq(fft_N, d=f.EXP_DT)
    return yf, freq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", nargs="+", default=["train"])
    ap.add_argument("--phase", nargs="+", type=int, default=[1])
    args = ap.parse_args()

    rows = list(csv.DictReader(open(os.path.join(HERE, "design.csv"), encoding="utf-8")))
    ref = [r for r in rows if r["set"] == "smooth"][0]
    sel = [r for r in rows if r["set"] in args.set and int(r["phase"]) in args.phase]

    def name_of(r):
        return out_name(r, float(r["pitch_m"]), float(r["width_m"]), float(r["depth_m"]))

    tag = "_".join(args.set) + "_ph" + "".join(map(str, args.phase)) + "_refpeak"
    out = os.path.join(SIM, "features", tag, "complex_spectrum")
    output_dir_waveform = os.path.join(out, "waveform")
    output_dir_fft = os.path.join(out, "spectrum_png")
    output_dir_csv = os.path.join(out, "spectrum_csv")
    output_dir_norm = os.path.join(out, "spectrum_norm_png")
    output_dir_norm_csv = os.path.join(out, "spectrum_norm_csv")
    for d in (output_dir_waveform, output_dir_fft, output_dir_csv, output_dir_norm, output_dir_norm_csv):
        os.makedirs(d, exist_ok=True)

    # 正しいピークの基準 = 平滑面の t0（平滑面自身は kiritori2 で問題なく取れる）
    t_ref = f.cut(*f.load_wave(os.path.join(SIM, name_of(ref))))[0]

    names, params, spectra, norm_spectra = [], [], [], []
    D_smooth = None
    for r in [ref] + sel:   # 先頭が平滑面。そのスペクトルを D_smooth として以降の正規化に使う
        csv_file = name_of(r)
        t, waveform = f.load_wave(os.path.join(SIM, csv_file))   # exp_dt に補間済み
        t0, sliced_waveform, _ = f.cut(t, waveform, t_ref)

        # 波形のプロット（plot_simdata.py と同じ）
        plt.figure(figsize=(8, 4))
        x_axis = np.arange(len(sliced_waveform)) * f.EXP_DT * 1e6
        plt.plot(x_axis, sliced_waveform)
        plt.title(f"{csv_file} - Waveform")
        plt.xlabel('Time [us] (from cut start)')
        plt.ylabel('Amplitude')
        plt.ylim(waveform_ylim_min, waveform_ylim_max)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir_waveform, csv_file.replace('.csv', '_waveform.png')))
        plt.close()

        # 複素スペクトルのプロット（plot_simdata.py の FFT と同じ軸・範囲。振幅は ±|D| で包絡を示す）
        yf, freq = complex_fft(sliced_waveform)
        plt.figure(figsize=(8, 4))
        plt.plot(freq, yf.real, label='Real')
        plt.plot(freq, yf.imag, label='Imag')
        plt.plot(freq, np.abs(yf), color='gray', linestyle='--', linewidth=1, label='|D|')
        plt.title(f"{csv_file} - Complex spectrum")
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Spectrum')
        plt.xlim(fft_freq_min, fft_freq_max)
        plt.ylim(fft_ylim_min, fft_ylim_max)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir_fft, csv_file.replace('.csv', '_complex.png')))
        plt.close()

        band = (freq >= fft_freq_min) & (freq <= fft_freq_max)
        np.savetxt(os.path.join(output_dir_csv, csv_file.replace('.csv', '_complex.csv')),
                   np.column_stack([freq[band], yf.real[band], yf.imag[band]]),
                   delimiter=",", header="freq_Hz,real,imag", comments="")

        # 平滑面で正規化した複素スペクトル R = D / D_smooth
        if D_smooth is None:
            D_smooth = yf
        R = yf / D_smooth
        plt.figure(figsize=(8, 4))
        plt.plot(freq[band], R.real[band], label='Real')
        plt.plot(freq[band], R.imag[band], label='Imag')
        plt.plot(freq[band], np.abs(R[band]), color='gray', linestyle='--', linewidth=1, label='|R|')
        plt.title(f"{csv_file} - Normalized spectrum (D / D_smooth)")
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Normalized spectrum')
        plt.xlim(fft_freq_min, fft_freq_max)
        plt.ylim(norm_ylim_min, norm_ylim_max)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir_norm, csv_file.replace('.csv', '_norm.png')))
        plt.close()
        np.savetxt(os.path.join(output_dir_norm_csv, csv_file.replace('.csv', '_norm.csv')),
                   np.column_stack([freq[band], R.real[band], R.imag[band]]),
                   delimiter=",", header="freq_Hz,real,imag", comments="")

        names.append(csv_file)
        params.append([float(r[k + "_m"]) * 1e3 for k in ("pitch", "width", "depth")])
        spectra.append(yf[band])
        norm_spectra.append(R[band])
        print(f"{csv_file}: t0 = {t0*1e6:.3f} us")

    np.savez(os.path.join(out, "complex_spectra.npz"),
             names=np.array(names), params_mm=np.array(params),
             freq=freq[band], D=np.array(spectra), R=np.array(norm_spectra), t_ref=t_ref)
    print(f"Processed {len(names)} files（先頭は平滑面）. Output: {out}")


if __name__ == "__main__":
    main()
