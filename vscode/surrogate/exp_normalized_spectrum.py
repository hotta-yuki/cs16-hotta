"""実験波形の正規化スペクトル R_exp = D_exp / D_exp,flat を作る。

    python vscode/surrogate/exp_normalized_spectrum.py

シミュレーション側の R = D / D_smooth（plot_complex_spectrum.py）と同じ手順・同じ図の書式で、
分母を実験の平滑面にしたもの。送信パルス・探触子・接触の共通部分が割り算で消え、
きず面の反射特性だけが残るので、シミュレーションの R と直接比べられる。

データ
----
- 平滑面: vscode/simulation/data/ex_flat/scope_4〜9 の 6 本（FLAT_IDX）。
  scope_0〜3 は振幅が約 1/4（0.13-0.16 V、他は 0.51-0.60 V）でピークも 70 ns 遅く、
  測定条件が違うので使わない（2026-11-12 ユーザー判断）
- きず面: vscode/simulation/data/ex_data/ と ex_index.csv の 18 条件（各 10〜20 本）

手順
----
1. 切り出しは featurize.cut（kiritori2 と同じ。ピークは正の最大）。実験には平滑面の
   シミュレーション t0 が使えないので --peak smooth は使わない。代わりに各条件の
   t0 のばらつきを summary.txt に出して、ピークの取り違えが無いかを確認する
2. 複素スペクトルは plot_complex_spectrum.complex_fft と同じ（fft_N 点、位相原点 t0）
3. D_flat は 6 本の複素スペクトルの平均（各本を自分の t0 で揃えてあるので位相が揃っている）
4. 条件ごとに R_i = D_i / D_flat（1 本ずつ）と、R_mean = mean(D_i) / D_flat を出す

注意: 平滑面（2026-11-05 測定）ときず面（2026-06 測定）は別の日の測定で、接触状態が
違えば |R| 全体に定数倍がかかる。形（周波数依存・位相）は比べられるが、絶対値の比較は
この倍率込みで読む。

出力（vscode/surrogate/tmp_output/features/exp_ex_index/complex_spectrum/）
    waveform/<name>_waveform.png       切り出した波形（全本を重ね、平均を太線）
    spectrum_png/<name>_complex.png    D の実部・虚部・|D|（平均）
    spectrum_csv/<name>_complex.csv    周波数 [Hz], 実部, 虚部（平均、2-8 MHz）
    spectrum_norm_png/<name>_norm.png  R_mean の実部・虚部・|R|（1 本ずつを薄く重ねる）
    spectrum_norm_csv/<name>_norm.csv  周波数 [Hz], R_mean の実部, 虚部（2-8 MHz）
    compare_sim_png/<name>_compare.png 同じ寸法のシミュレーションの R と重ねた図（あれば）
    flat_reference.png                 平滑面 6 本の波形と D
    complex_spectra.npz                全件まとめ
    summary.txt                        条件ごとの本数・t0・ばらつき
<name> は exp_pitch<p>_width<w>_depth<d>（naming.mm_code）。平滑面は exp_flat。
"""

import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "simulation"))

import featurize as f
import plot_complex_spectrum as pcs
from data_paths import experiment_dir
from naming import SIM_SHAPE, mm_code, sim_csv_name, smooth_csv_name
from run_design import CHECK_DIRS

SIM = os.path.join(HERE, "tmp_output")
EXP = str(experiment_dir())
FLAT_DIR = os.path.join(EXP, "ex_flat")
FLAT_IDX = range(4, 10)      # scope_4〜9（上の docstring 参照）
OUT = os.path.join(SIM, "features", "exp_ex_index", "complex_spectrum")

FMIN, FMAX = pcs.fft_freq_min, pcs.fft_freq_max
C_RE, C_IM = f.C_RE, f.C_IM


def load_group(paths):
    """スコープ CSV を読んで切り出し、(t0 の配列, 切り出し波形の配列, 複素スペクトルの配列, freq)。"""
    T0, S, D = [], [], []
    for p in paths:
        t0, seg, _ = f.cut(*f.load_scope(p))
        yf, freq = pcs.complex_fft(seg)
        T0.append(t0); S.append(seg); D.append(yf)
    return np.array(T0), np.array(S), np.array(D), freq


def rel_spread(D, band):
    """1 本ずつの平均からのずれ ||D_i - D_mean|| / ||D_mean||（reconstruct.py と同じ補正つき）。"""
    Dm = D.mean(axis=0)
    e = np.linalg.norm(D[:, band] - Dm[band], axis=1) / np.linalg.norm(Dm[band])
    return e * np.sqrt(len(D) / (len(D) - 1))


def plot_waveform(path, title, S):
    x = np.arange(S.shape[1]) * f.EXP_DT * 1e6
    plt.figure(figsize=(8, 4))
    for s in S:
        plt.plot(x, s, color="#b8b7b2", linewidth=0.6)
    plt.plot(x, S.mean(axis=0), color=C_RE, linewidth=1.4, label=f"平均（{len(S)} 本）")
    plt.title(f"{title} - Waveform")
    plt.xlabel("Time [us] (from cut start)")
    plt.ylabel("Amplitude [V]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_complex(path, title, freq, D, ylim):
    plt.figure(figsize=(8, 4))
    plt.plot(freq, D.real, label="Real")
    plt.plot(freq, D.imag, label="Imag")
    plt.plot(freq, np.abs(D), color="gray", linestyle="--", linewidth=1, label="|D|")
    plt.title(f"{title} - Complex spectrum")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum")
    plt.xlim(FMIN, FMAX)
    plt.ylim(-ylim, ylim)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_norm(path, title, freq, band, R_each, R_mean):
    plt.figure(figsize=(8, 4))
    for R in R_each:   # 1 本ずつは薄く（ばらつきの目安）
        plt.plot(freq[band], R.real[band], color=C_RE, alpha=0.15, linewidth=0.7)
        plt.plot(freq[band], R.imag[band], color=C_IM, alpha=0.15, linewidth=0.7)
    plt.plot(freq[band], R_mean.real[band], color=C_RE, label="Real")
    plt.plot(freq[band], R_mean.imag[band], color=C_IM, label="Imag")
    plt.plot(freq[band], np.abs(R_mean[band]), color="gray", linestyle="--", linewidth=1, label="|R|")
    plt.title(f"{title} - Normalized spectrum (D / D_flat)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Normalized spectrum")
    plt.xlim(FMIN, FMAX)
    plt.ylim(pcs.norm_ylim_min, pcs.norm_ylim_max)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_compare(path, title, freq, band, R_exp, R_sim):
    """実験（実線）とシミュレーション（破線）の R を重ねる。"""
    fig, axs = plt.subplots(1, 2, figsize=(13, 4), layout="constrained")
    axs[0].plot(freq[band], R_exp.real[band], color=C_RE, label="Real 実験")
    axs[0].plot(freq[band], R_sim.real[band], color=C_RE, linestyle="--", label="Real シミュレーション")
    axs[0].plot(freq[band], R_exp.imag[band], color=C_IM, label="Imag 実験")
    axs[0].plot(freq[band], R_sim.imag[band], color=C_IM, linestyle="--", label="Imag シミュレーション")
    axs[0].set_ylim(pcs.norm_ylim_min, pcs.norm_ylim_max)
    axs[0].set_ylabel("Normalized spectrum")
    axs[1].plot(freq[band], np.abs(R_exp[band]), color="#52514e", label="|R| 実験")
    axs[1].plot(freq[band], np.abs(R_sim[band]), color="#52514e", linestyle="--", label="|R| シミュレーション")
    axs[1].set_ylim(0, pcs.norm_ylim_max)
    axs[1].set_ylabel("|R|")
    for ax in axs:
        ax.set_xlim(FMIN, FMAX)
        ax.set_xlabel("Frequency [Hz]")
        ax.grid(True)
        ax.legend(fontsize=8)
    fig.suptitle(f"{title} - R 実験 vs シミュレーション")
    fig.savefig(path)
    plt.close(fig)


def sim_R(p_mm, w_mm, d_mm, D_smooth_sim, t_ref):
    """同じ寸法のシミュレーションがあれば、その R（plot_complex_spectrum と同じ正しいピーク）。"""
    # 掃引の出力に無ければ、run_design が「計算済み」とみなす既存の出力も見る
    # （ex_index の 18 条件は昔の simdata.csv 掃引でほぼ計算済み）
    fn = sim_csv_name(SIM_SHAPE, p_mm * 1e-3, w_mm * 1e-3, d_mm * 1e-3)
    path = next((p for p in [os.path.join(d, fn) for d in [SIM] + CHECK_DIRS] if os.path.isfile(p)), None)
    if path is None:
        return None
    _, seg, _ = f.cut(*f.load_wave(path), t_ref)
    yf, _ = pcs.complex_fft(seg)
    return yf / D_smooth_sim


def main():
    subdirs = {k: os.path.join(OUT, k) for k in
               ("waveform", "spectrum_png", "spectrum_csv", "spectrum_norm_png",
                "spectrum_norm_csv", "compare_sim_png")}
    for d in subdirs.values():
        os.makedirs(d, exist_ok=True)

    # ---- 平滑面（分母）
    flat_paths = [os.path.join(FLAT_DIR, f"scope_{i}.csv") for i in FLAT_IDX]
    T0f, Sf, Df, freq = load_group(flat_paths)
    band = (freq >= FMIN) & (freq <= FMAX)
    D_flat = Df.mean(axis=0)
    flat_spread = rel_spread(Df, band)

    fig, axs = plt.subplots(1, 2, figsize=(13, 4), layout="constrained")
    x = np.arange(Sf.shape[1]) * f.EXP_DT * 1e6
    for i, s in zip(FLAT_IDX, Sf):
        axs[0].plot(x, s, linewidth=0.7, label=f"scope_{i}")
    axs[0].set_xlabel("Time [us] (from cut start)")
    axs[0].set_ylabel("Amplitude [V]")
    for D in Df:
        axs[1].plot(freq[band], np.abs(D[band]), color="#b8b7b2", linewidth=0.7)
    axs[1].plot(freq[band], np.abs(D_flat[band]), color=C_RE, linewidth=1.6, label="|D_flat|（6 本の平均）")
    axs[1].set_xlabel("Frequency [Hz]")
    axs[1].set_ylabel("|D|")
    for ax in axs:
        ax.grid(True)
        ax.legend(fontsize=8)
    fig.suptitle("実験の平滑面 ex_flat scope_4〜9")
    fig.savefig(os.path.join(OUT, "flat_reference.png"))
    plt.close(fig)

    ylim = 1.2 * np.abs(D_flat[band]).max()   # D の縦軸。実験は [V] なのでシミュレーションの ±0.06 は使わない
    plot_waveform(os.path.join(subdirs["waveform"], "exp_flat_waveform.png"), "exp_flat", Sf)
    plot_complex(os.path.join(subdirs["spectrum_png"], "exp_flat_complex.png"), "exp_flat", freq, D_flat, ylim)
    np.savetxt(os.path.join(subdirs["spectrum_csv"], "exp_flat_complex.csv"),
               np.column_stack([freq[band], D_flat.real[band], D_flat.imag[band]]),
               delimiter=",", header="freq_Hz,real,imag", comments="")

    # シミュレーションの平滑面（比較図用）
    t_s, w_s = f.load_wave(os.path.join(SIM, smooth_csv_name(2.0e-3)))
    t_ref, seg_s, _ = f.cut(t_s, w_s)
    D_smooth_sim, _ = pcs.complex_fft(seg_s)

    # ---- きず面
    with open(os.path.join(EXP, "ex_index.csv"), encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.reader(fh) if r and r[0].strip()][1:]

    names, params, n_used, R_means, D_means = [], [], [], [], []
    lines = []
    for r in rows:
        s, e = int(r[0]), int(r[1])
        p_mm, d_mm, w_mm = float(r[2]), float(r[3]), float(r[4])   # 列順は pitch, depth, width
        paths = [os.path.join(EXP, "ex_data", f"scope_{i}.csv") for i in range(s, e + 1)]
        paths = [p for p in paths if os.path.isfile(p)]
        if not paths:
            continue
        name = f"exp_pitch{mm_code(p_mm)}_width{mm_code(w_mm)}_depth{mm_code(d_mm)}"
        T0, S, D, _ = load_group(paths)
        D_mean = D.mean(axis=0)
        R_each = D / D_flat
        R_mean = D_mean / D_flat

        plot_waveform(os.path.join(subdirs["waveform"], f"{name}_waveform.png"), name, S)
        plot_complex(os.path.join(subdirs["spectrum_png"], f"{name}_complex.png"), name, freq, D_mean, ylim)
        np.savetxt(os.path.join(subdirs["spectrum_csv"], f"{name}_complex.csv"),
                   np.column_stack([freq[band], D_mean.real[band], D_mean.imag[band]]),
                   delimiter=",", header="freq_Hz,real,imag", comments="")
        plot_norm(os.path.join(subdirs["spectrum_norm_png"], f"{name}_norm.png"), name, freq, band, R_each, R_mean)
        np.savetxt(os.path.join(subdirs["spectrum_norm_csv"], f"{name}_norm.csv"),
                   np.column_stack([freq[band], R_mean.real[band], R_mean.imag[band]]),
                   delimiter=",", header="freq_Hz,real,imag", comments="")

        Rs = sim_R(p_mm, w_mm, d_mm, D_smooth_sim, t_ref)
        diff = "      -"
        if Rs is not None:
            plot_compare(os.path.join(subdirs["compare_sim_png"], f"{name}_compare.png"), name, freq, band, R_mean, Rs)
            diff = f"{np.linalg.norm((R_mean - Rs)[band]) / np.linalg.norm(Rs[band]):7.3f}"

        spread = rel_spread(D, band)
        lines.append(f"{name:<34} {len(paths):3d}  {T0.min()*1e6:6.3f}-{T0.max()*1e6:6.3f}  "
                     f"{np.median(spread):6.3f}  {np.abs(R_mean[band]).mean():6.3f}  {diff}")
        names.append(name); params.append([p_mm, w_mm, d_mm]); n_used.append(len(paths))
        R_means.append(R_mean[band]); D_means.append(D_mean[band])
        print(f"{name}: {len(paths)} 本, t0 = {T0.min()*1e6:.3f}-{T0.max()*1e6:.3f} us")

    np.savez(os.path.join(OUT, "complex_spectra.npz"),
             names=np.array(names), params_mm=np.array(params), n=np.array(n_used),
             freq=freq[band], D=np.array(D_means), R=np.array(R_means),
             D_flat=D_flat[band], flat_idx=np.array(list(FLAT_IDX)), t0_flat=T0f)

    head = [
        "実験の正規化スペクトル R_exp = mean(D_i) / D_flat",
        f"平滑面: ex_flat scope_{FLAT_IDX[0]}〜{FLAT_IDX[-1]}（{len(FLAT_IDX)} 本）  "
        f"t0 = {T0f.min()*1e6:.3f}-{T0f.max()*1e6:.3f} us  ばらつき中央値 {np.median(flat_spread):.3f}",
        f"帯域: {FMIN/1e6:.2f}-{FMAX/1e6:.2f} MHz（{band.sum()} 点）, 切り出し kiritori2（正の最大）",
        "ばらつき = ||D_i - D_mean|| / ||D_mean|| * sqrt(n/(n-1)) の中央値",
        "sim との差 = ||R_exp - R_sim|| / ||R_sim||（同じ寸法のシミュレーションがある条件のみ）",
        "",
        f"{'条件':<34} {'本数':>3}  {'t0 [us]':^13}  {'ばらつき':>6}  {'平均|R|':>6}  {'simとの差':>7}",
    ]
    text = "\n".join(head + lines)
    with open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    print(f"\n出力: {OUT}")


if __name__ == "__main__":
    main()
