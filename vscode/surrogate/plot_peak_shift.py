"""kiritori2 のピーク（正の最大）がずれる波形と、正しいピークで切った場合の比較図。

    python vscode/surrogate/plot_peak_shift.py

p=1.14 w=0.48 d=0.30 mm では正の最大が後続の波（7.93 us）にあり、窓が底面エコーから
外れる。溝の間の平らな部分は平滑面と同じ高さなので、そこからの正反射は平滑面の
エコーと同じ時刻に届く。そこで「平滑面の t0 に最も近い正の山」を正しいピークとする。
図は波形のみ（(a) 正しく取れている例、(b) ずれた例、(c) 正しいピークで切った例）。

出力: vscode/surrogate/tmp_output/features/train_ph1/peak_shift.png
"""

import os

import numpy as np

import featurize as f

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "tmp_output")
OUT = os.path.join(SIM, "features", "train_ph1", "peak_shift.png")

SMOOTH = "smooth_cupy_pitch200_depth0.csv"
GOOD = "kukei_cupy_pitch196_width50_depth18.csv"    # window.png の 2 段目と同じ代表例
SHIFTED = f.WINDOW_HARD_CASE                        # p=1.14 w=0.48 d=0.30 mm


def cut_at(t, w, t0):
    """kiritori2 と同じ左右点数で、指定した t0 を中心に切る。"""
    k = int(np.argmin(np.abs(t - t0)))
    seg = w[k - f.LEFT:k + f.RIGHT]
    return t[k], seg, (np.arange(len(seg)) - f.LEFT) * f.EXP_DT


def nearest_positive_peak(t, w, t_ref):
    """t_ref に最も近い正の極大の時刻。"""
    i = np.arange(1, len(w) - 1)
    pk = i[(w[i] > w[i - 1]) & (w[i] >= w[i + 1]) & (w[i] > 0.2 * w.max())]
    return t[pk[np.argmin(np.abs(t[pk] - t_ref))]]


def main():
    plt = f.plt
    ts, ws = f.load_wave(os.path.join(SIM, SMOOTH))
    t0s = f.cut(ts, ws)[0]

    tg, wg = f.load_wave(os.path.join(SIM, GOOD))
    tb, wb = f.load_wave(os.path.join(SIM, SHIFTED))
    t_ok = nearest_positive_peak(tb, wb, t0s)

    rows = [
        ("(a) ピークが正しく取れている例  p=1.96 w=0.50 d=0.18 mm（kiritori2）", tg, wg, f.cut(tg, wg)),
        ("(b) ピークがずれた例  p=1.14 w=0.48 d=0.30 mm（kiritori2、正の最大）", tb, wb, f.cut(tb, wb)),
        ("(c) 同じ波形を正しいピークで切った場合（平滑面の t0 に最も近い正の山）", tb, wb, cut_at(tb, wb, t_ok)),
    ]

    fig, axs = plt.subplots(3, 1, figsize=(11, 9), layout="constrained")
    xlim = (6.4, 10.0)
    for ax, (title, t, w, (t0, seg, tau)) in zip(axs, rows):
        lo, hi = t0 + tau[0], t0 + tau[-1]
        z = (t >= xlim[0] * 1e-6) & (t <= xlim[1] * 1e-6)
        ax.axvspan(lo * 1e6, hi * 1e6, color=f.GRID, alpha=0.6, linewidth=0)
        ax.plot(ts[z] * 1e6, ws[z], color="#52514e", linewidth=0.8, linestyle=":", label="平滑面")
        ax.plot(t[z] * 1e6, w[z], color=f.C_RE, linewidth=1.0, label="波形")
        ax.plot((t0 + tau) * 1e6, seg, color=f.C_IM, linewidth=1.2, label="切り出し")
        ax.axvline(t0s * 1e6, color="#52514e", linewidth=1, linestyle=":")
        ax.axvline(t0 * 1e6, color="#0b0b0b", linewidth=1.2, linestyle="--")
        ax.text(t0 * 1e6, ax.get_ylim()[1] * 0.92, f" t0 = {t0*1e6:.3f} us", va="top", color="#0b0b0b")
        ax.set_xlim(*xlim)
        ax.set_title(f"{title}　窓 {lo*1e6:.2f}-{hi*1e6:.2f} us", loc="left")
        ax.set_ylabel("振幅")
        f._style(ax)
    axs[0].legend(frameon=False, loc="upper right", ncol=3)
    axs[2].set_xlabel("時刻 [us]（点線は平滑面の t0 = %.3f us）" % (t0s * 1e6))

    fig.savefig(OUT, dpi=150)
    print(f"正しいピーク t0 = {t_ok*1e6:.3f} us（kiritori2 は {rows[1][3][0]*1e6:.3f} us、平滑面 {t0s*1e6:.3f} us）")
    print(f"出力: {OUT}")


if __name__ == "__main__":
    main()
