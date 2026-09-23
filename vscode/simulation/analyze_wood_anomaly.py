"""音響ウッド異常（acoustic Wood anomaly）の条件を、本研究の鋼／空気の条件で評価する。

背景は Liu の2編：

- J. F. Liu and N. F. Declercq, "Acoustic Wood anomaly in transmitted diffraction
  field", AIP Advances 7, 035116 (2017)
- J. Liu, ロレーヌ大学博士論文 (2018) 第2章・第3章・第5章

いずれも「周期的な凹凸界面に広帯域波が垂直入射すると、古典的回折格子方程式
  c = f Λ / m      (Λ: 凹凸周期, m: 回折次数)
を満たす周波数でバルク波が表面型波へモード変換され、それが凹凸で再回折して
法線方向へ戻り（＝二重モード変換）、直達反射との位相関係でスペクトルの
ディップ／ティップを作る」という描像を与えている。

本スクリプトは2つのことをする。

1. ``predicted_frequencies()``
   本研究の条件（鋼、底面が鋼-空気の自由境界、Λ = 溝ピッチ）で、
   P波・S波・レイリー波それぞれについて異常が予想される周波数を並べる。
   鋼-空気界面ではショルテ／ストーンリー波が存在しないので、実際に効くのは
   レイリー波（Liu 博論 表2-2・2.3.4.2 節）。

2. ``analyze_tail()``
   実験の平均波形を「メインバン（底面エコー）」と「テイル（後続振動）」に
   分け、それぞれの振幅スペクトルを取る。Liu の中心的な主張は
   「異常の原因はテイルであり、メインバンだけを窓で切り出すと異常は消える」
   （2017年論文 図5、博論 図2-5）なので、まず本研究のデータに同じ構造が
   あるかどうかを見る。

出力先は ``tmp_output/wood_anomaly/``。GPU は不要。
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

import data_paths

try:  # 研究室の Windows 機にはあるが Mac には無い
    import japanize_matplotlib  # noqa: F401
except ImportError:
    pass

# --- 材料定数（UT_FlawVariation_Sim.py と同じ値） -------------------------
RHO = 7840.0        # kg/m^3
E = 206e9           # Pa
G = 80e9            # Pa
NU = 0.27           # ポアソン比

C_L = np.sqrt(E / RHO * (1 - NU) / (1 + NU) / (1 - 2 * NU))  # 縦波 (P)
C_T = np.sqrt(G / RHO)                                        # 横波 (S)
# レイリー波速度の近似式（Viktorov）。厳密解との差は 0.1% 程度。
C_R = C_T * (0.862 + 1.14 * NU) / (1 + NU)

F_PROBE = 4.7e6     # 探触子中心周波数 [Hz]（ソルバの送信波と同じ）

OUT_DIR = data_paths.REPO_ROOT / "tmp_output" / "wood_anomaly"


def rayleigh_speed():
    """レイリー波速度 [m/s]。"""
    return C_R


def predicted_frequencies(pitches_mm=(1.25, 2.00), orders=(1, 2, 3, 4)):
    """異常が予想される周波数 f = m c / Λ を返す。

    戻り値は ``{(pitch_mm, mode_name): [f_1, f_2, ...]}``（単位 Hz）。
    """
    table = {}
    for pitch_mm in pitches_mm:
        lam = pitch_mm * 1e-3
        for name, c in (("P", C_L), ("S", C_T), ("Rayleigh", C_R)):
            table[(pitch_mm, name)] = [m * c / lam for m in orders]
    return table


def print_predicted(pitches_mm=(1.25, 2.00), band=(1.0e6, 9.0e6)):
    """予想周波数を表として標準出力に出す。"""
    print(f"鋼: cl = {C_L:.0f} m/s, ct = {C_T:.0f} m/s, cR = {C_R:.0f} m/s")
    print(f"探触子中心周波数 f0 = {F_PROBE / 1e6:.2f} MHz "
          f"(λ_P = {C_L / F_PROBE * 1e3:.3f} mm, λ_S = {C_T / F_PROBE * 1e3:.3f} mm, "
          f"λ_R = {C_R / F_PROBE * 1e3:.3f} mm)")
    print()
    table = predicted_frequencies(pitches_mm)
    for pitch_mm in pitches_mm:
        print(f"--- Λ = {pitch_mm:.2f} mm ---")
        for name in ("P", "S", "Rayleigh"):
            fs = table[(pitch_mm, name)]
            cells = []
            for m, f in enumerate(fs, start=1):
                mark = "*" if band[0] <= f <= band[1] else " "
                cells.append(f"m={m}: {f / 1e6:6.3f}{mark}")
            print(f"  {name:9s} " + "  ".join(cells))
        print()
    print("* = 探触子の帯域内に入る（観測されうる）")


# --- 実験波形のテイル解析 -------------------------------------------------

_NAME_RE = re.compile(r"avg_wave_p(\d+)_w(\d+)_d(\d+)_")


def _parse_name(path):
    """``avg_wave_p200_w40_d20_70_79.csv`` -> (2.00, 0.40, 0.20) [mm]。"""
    m = _NAME_RE.match(Path(path).name)
    if m is None:
        return None
    return tuple(int(g) / 100 for g in m.groups())


def _spectrum(t, v, t0, t1, nfft=65536):
    """[t0, t1) を窓で切り出して振幅スペクトルを返す。"""
    sel = (t >= t0) & (t < t1)
    x = v[sel] - v[sel].mean()
    x = x * np.hanning(len(x))
    dt = float(np.diff(t).mean())
    return np.fft.rfftfreq(nfft, dt), np.abs(np.fft.rfft(x, nfft))


def split_main_and_tail(t, v, tail_margin=0.6e-6):
    """波形をメインバンとテイルに分ける。

    メインバンのピーク位置を包絡線から求め、そこから ``tail_margin`` だけ
    後ろをテイルの開始時刻とする。戻り値は (t_peak, t_tail_start)。
    """
    env = np.abs(v)
    width = max(int(0.05e-6 / float(np.diff(t).mean())), 1)
    smooth = np.convolve(env, np.ones(width) / width, mode="same")
    t_peak = float(t[int(np.argmax(smooth))])
    return t_peak, t_peak + tail_margin


def analyze_tail(save=True):
    """平均波形のメインバン／テイルのスペクトルを比較する。

    戻り値は行のリスト。各行は
    ``(pitch_mm, width_mm, depth_mm, f, X_main, X_tail, X_noise)``。
    """
    import matplotlib
    if save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    avg_dir = data_paths.experiment_dir() / "avg_waveforms"
    files = sorted(avg_dir.glob("avg_wave_*.csv"))
    if not files:
        raise FileNotFoundError(f"平均波形が見つかりません: {avg_dir}")

    rows = []
    for path in files:
        parsed = _parse_name(path)
        if parsed is None:
            continue
        pitch_mm, width_mm, depth_mm = parsed
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        t, v = data[:, 0], data[:, 1]
        t_peak, t_tail = split_main_and_tail(t, v)

        f, x_main = _spectrum(t, v, t_peak - 0.15e-6, t_peak + 0.30e-6)
        _, x_tail = _spectrum(t, v, t_tail, t[-1])
        # エコー到達前の区間を雑音の基準にする
        _, x_noise = _spectrum(t, v, t[0], t_peak - 0.30e-6)
        rows.append((pitch_mm, width_mm, depth_mm, f, x_main, x_tail, x_noise))

    if save:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        _plot_groups(rows, plt)
    return rows


def _plot_groups(rows, plt):
    """ピッチごとに、テイルのスペクトルと予想周波数を重ねた図を書く。"""
    band = (0.5e6, 9.0e6)
    for pitch_mm in sorted({r[0] for r in rows}):
        group = [r for r in rows if r[0] == pitch_mm]
        fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

        for ax, which, title in (
            (axes[0], 4, "Main bang (bottom echo)"),
            (axes[1], 5, "Tail (after the echo)"),
        ):
            for pitch, width, depth, f, *spectra in group:
                sel = (f > band[0]) & (f < band[1])
                x = spectra[which - 4]
                ax.plot(f[sel] / 1e6, x[sel] / x[sel].max(),
                        label=f"w={width:.2f} d={depth:.2f} mm", lw=1.0)
            for m in range(1, 5):
                f_r = m * C_R / (pitch_mm * 1e-3)
                if band[0] < f_r < band[1]:
                    ax.axvline(f_r / 1e6, color="crimson", ls="--", lw=0.9)
                    ax.text(f_r / 1e6, 1.02, f"m={m}", color="crimson",
                            ha="center", fontsize=8)
            ax.axvline(F_PROBE / 1e6, color="gray", ls=":", lw=1.2)
            ax.set_ylabel("normalized amplitude")
            ax.set_title(f"{title}   (pitch = {pitch_mm:.2f} mm)")
            ax.set_ylim(0, 1.1)

        axes[1].set_xlabel("frequency [MHz]")
        axes[1].legend(fontsize=7, ncol=2)
        fig.suptitle(
            f"dashed red: f = m c_R / Λ  (c_R = {C_R:.0f} m/s), "
            f"dotted gray: probe {F_PROBE / 1e6:.1f} MHz", fontsize=9)
        fig.tight_layout()
        code = f"{int(pitch_mm * 100)}"
        out = OUT_DIR / f"tail_spectrum_pitch{code}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"書き出し: {out}")


def tail_to_main_ratio(rows):
    """テイル／メインバンの振幅比と、テイルの信号対雑音比を出す。"""
    band = (1.0e6, 9.0e6)
    out = []
    for pitch, width, depth, f, x_main, x_tail, x_noise in rows:
        sel = (f > band[0]) & (f < band[1])
        out.append((pitch, width, depth,
                    float(x_tail[sel].max() / x_main[sel].max()),
                    float(x_tail[sel].max() / x_noise[sel].max())))
    return out


if __name__ == "__main__":
    print_predicted()
    rows = analyze_tail()
    print()
    print(f"{'pitch':>6}{'width':>7}{'depth':>7}{'tail/main':>11}{'tail SNR':>10}")
    for pitch, width, depth, ratio, snr in tail_to_main_ratio(rows):
        print(f"{pitch:6.2f}{width:7.2f}{depth:7.2f}{ratio:11.3f}{snr:10.1f}")
