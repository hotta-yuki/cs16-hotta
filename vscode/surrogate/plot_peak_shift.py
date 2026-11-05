"""kiritori2 のピーク（正の最大）がずれる波形と、正しいピークで切った場合の比較図。

    python vscode/surrogate/plot_peak_shift.py

p=1.14 w=0.48 d=0.30 mm では正の最大が後続の波（7.93 us）にあり、窓が底面エコーから
外れる。溝の間の平らな部分は平滑面と同じ高さなので、そこからの正反射は平滑面の
エコーと同じ時刻に届く。そこで「平滑面の t0 に最も近い正の山」を正しいピークとする。

図の書式は vscode/simulation/plot_simdata.py に倣う（切り出した波形のみ、
切り出し開始からの相対時刻、縦軸 ±1.5 固定、1 図 1 波形）。

出力: vscode/surrogate/tmp_output/features/train_ph1/peak_shift_{a,b,c}.png
    a  ピークが正しく取れている例（kiritori2）
    b  ピークがずれた例（kiritori2）
    c  b と同じ波形を正しいピークで切った場合
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import featurize as f

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "tmp_output")
OUT_DIR = os.path.join(SIM, "features", "train_ph1")

SMOOTH = "smooth_cupy_pitch200_depth0.csv"
GOOD = "kukei_cupy_pitch196_width50_depth18.csv"    # window.png の 2 段目と同じ代表例
SHIFTED = f.WINDOW_HARD_CASE                        # p=1.14 w=0.48 d=0.30 mm

# plot_simdata.py と同じ縦軸の固定範囲
WAVEFORM_YLIM = (-1.5, 1.5)


def cut_at(t, w, t0):
    """kiritori2 と同じ左右点数で、指定した t0 を中心に切る。"""
    k = int(np.argmin(np.abs(t - t0)))
    return w[k - f.LEFT:k + f.RIGHT]


def nearest_positive_peak(t, w, t_ref):
    """t_ref に最も近い正の極大の時刻。"""
    i = np.arange(1, len(w) - 1)
    pk = i[(w[i] > w[i - 1]) & (w[i] >= w[i + 1]) & (w[i] > 0.2 * w.max())]
    return t[pk[np.argmin(np.abs(t[pk] - t_ref))]]


def plot_waveform(sliced_waveform, title, path):
    """plot_simdata.py の波形プロットと同じ書式。"""
    plt.figure(figsize=(8, 4))
    x_axis = np.arange(len(sliced_waveform)) * f.EXP_DT * 1e6
    plt.plot(x_axis, sliced_waveform)
    plt.title(title)
    plt.xlabel('Time [us] (from cut start)')
    plt.ylabel('Amplitude')
    plt.ylim(*WAVEFORM_YLIM)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main():
    ts, ws = f.load_wave(os.path.join(SIM, SMOOTH))
    t0s = f.cut(ts, ws)[0]
    tg, wg = f.load_wave(os.path.join(SIM, GOOD))
    tb, wb = f.load_wave(os.path.join(SIM, SHIFTED))
    t0b = f.cut(tb, wb)[0]
    t_ok = nearest_positive_peak(tb, wb, t0s)

    plot_waveform(f.cut(tg, wg)[1], f"{GOOD} - Waveform",
                  os.path.join(OUT_DIR, "peak_shift_a.png"))
    plot_waveform(f.cut(tb, wb)[1], f"{SHIFTED} - Waveform",
                  os.path.join(OUT_DIR, "peak_shift_b.png"))
    plot_waveform(cut_at(tb, wb, t_ok), f"{SHIFTED} - Waveform (corrected peak)",
                  os.path.join(OUT_DIR, "peak_shift_c.png"))

    print(f"正しいピーク t0 = {t_ok*1e6:.3f} us（kiritori2 は {t0b*1e6:.3f} us、平滑面 {t0s*1e6:.3f} us）")
    print(f"出力: {OUT_DIR}\\peak_shift_{{a,b,c}}.png")


if __name__ == "__main__":
    main()
