"""波形をメインバンとテイルに切り分けて FFT する。

Liu の2編（2017年 AIP Advances / 2018年 博士論文）の中心的な主張は
「周期凹凸からの反射でスペクトル異常を作っているのは直達エコー（メインバン）
ではなく、遅れて届く後続振動（テイル）である。メインバンだけを窓で切り出すと
異常は消える」というもの（2017年論文 図5、博論 図2-5）。

そこでこのモジュールは、1本の波形を

    送信  |  静穏  |  メインバン  |  テイル
    ------+--------+-------------+---------------->  t

に分け、メインバンとテイルそれぞれの振幅スペクトルを出す。
シミュレーション出力（時間軸なしの CSV）と実験の平均波形（time,voltage の CSV）の
どちらも読める。

使い方
------
リポジトリルートから::

    # 1条件だけ見る
    python vscode/simulation/tail_fft.py --pitch 2.00 --depth 0.20 --width 0.40

    # 見つかった全条件をまとめて処理して集計 CSV を書く
    python vscode/simulation/tail_fft.py --all

    # 実験の平均波形を対象にする
    python vscode/simulation/tail_fft.py --all --source experiment

出力は ``tmp_output/wood_anomaly/``。GPU は不要。
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import numpy as np

import data_paths

try:  # 研究室の Windows 機にはあるが Mac には無い
    import japanize_matplotlib  # noqa: F401
    _JP = True
except ImportError:
    _JP = False

# --- ソルバと同じ定数（UT_FlawVariation_Sim.py） -------------------------
RHO = 7840.0
E = 206e9
G = 80e9
NU = 0.27
MESH = 1.0e-5          # 格子間隔 [m]

C_L = np.sqrt(E / RHO * (1 - NU) / (1 + NU) / (1 - 2 * NU))   # 縦波
C_T = np.sqrt(G / RHO)                                         # 横波
C_R = C_T * (0.862 + 1.14 * NU) / (1 + NU)                     # レイリー波（Viktorov 近似）

DT_SIM = MESH / C_L / np.sqrt(6)   # ソルバの時間刻み [s]
F_SRC = 4.7e6                      # 送信波の中心周波数 [Hz]。探触子の実測値ではない
SRC_CYCLES = 2.5                   # 送信波の波数（ハン窓つき正弦波）
SRC_LEN = SRC_CYCLES / F_SRC       # 送信波の長さ [s] = 0.532 us

PLATE_THICKNESS = 0.02             # x_length [m]
ECHO_TIME = 2 * PLATE_THICKNESS / C_L   # 底面エコーの往復時間 [s] = 6.98 us

OUT_DIR = data_paths.REPO_ROOT / "tmp_output" / "wood_anomaly"

# シミュレーション出力の2つの命名に対応する
#   旧: sim_pitch1250_depth200_width400.csv      （値[mm] x 1000）
#   新: kukei_cupy_pitch125_width40_depth20.csv  （値[mm] x 100。AGENTS.md 7章）
_RE_OLD = re.compile(r"sim_pitch(\d+)_depth(\d+)_width(\d+)\.csv$")
_RE_NEW = re.compile(r"_cupy_pitch([\d.]+)_width([\d.]+)_depth([\d.]+)\.csv$")
_RE_EXP = re.compile(r"avg_wave_p(\d+)_w(\d+)_d(\d+)_")


def parse_params(path):
    """ファイル名から (pitch, depth, width) [mm] を取り出す。

    対応していない名前なら None を返す。
    """
    name = Path(path).name
    m = _RE_OLD.search(name)
    if m:
        p, d, w = (int(x) / 1000 for x in m.groups())
        return p, d, w
    m = _RE_NEW.search(name)
    if m:
        p, w, d = (float(x) / 100 for x in m.groups())
        return p, d, w
    m = _RE_EXP.match(name)
    if m:
        p, w, d = (int(x) / 100 for x in m.groups())
        return p, d, w
    return None


def load_waveform(path):
    """波形を (t, v) で返す。

    シミュレーション出力は時間軸を持たない1列の CSV なので、
    ソルバと同じ ``DT_SIM`` から時間軸を作る。
    実験の平均波形は ``time,voltage`` の2列なのでそのまま読む。
    """
    path = Path(path)
    with path.open() as fh:
        head = fh.readline()
    if "," in head and "time" in head.lower():
        a = np.loadtxt(path, delimiter=",", skiprows=1)
        return a[:, 0], a[:, 1]
    v = np.loadtxt(path, delimiter=",")
    v = np.atleast_1d(v).ravel()
    return np.arange(len(v)) * DT_SIM, v


def find_echo(t, v, skip=None):
    """底面エコーのピーク時刻を返す。

    送信波そのものを拾わないよう、先頭 ``skip`` 秒を除外して探す。
    既定は送信波の長さの2倍（シミュレーションでは 1.06 us）。
    実験波形は収録が echo の手前から始まっているので、
    先頭が送信波でなければそのまま最大値を取る。
    """
    if skip is None:
        # 送信波は t=0 から出る。収録がそれより後から始まっている波形
        # （実験のスコープ CSV は 5.5 us 付近から）には送信波が入っていないので
        # スキップしない。ここを一律に 2*SRC_LEN にすると、実験波形では
        # エコー本体を飛び越して後続振動の山を拾ってしまう。
        skip = 2 * SRC_LEN if t[0] < SRC_LEN else 0.0
    dt = float(np.diff(t).mean())
    width = max(int(0.05e-6 / dt), 1)
    env = np.convolve(np.abs(v), np.ones(width) / width, mode="same")
    i0 = int(np.searchsorted(t, t[0] + skip))
    if i0 >= len(t) - 1:
        i0 = 0
    return float(t[i0 + int(np.argmax(env[i0:]))])


def split(t, v, t_echo=None, margin=None):
    """波形を (メインバン, テイル) の時間区間に切る。

    メインバンは「エコーのピーク ± 送信波の長さ」、テイルはその後ろ全部。
    送信波より短いメインバンはありえないので、窓幅の根拠をそこに置いている。

    Returns
    -------
    (t0_main, t1_main), (t0_tail, t1_tail)
    """
    if t_echo is None:
        t_echo = find_echo(t, v)
    if margin is None:
        margin = SRC_LEN
    main = (t_echo - 0.3 * margin, t_echo + 0.7 * margin)
    tail = (t_echo + 1.2 * margin, float(t[-1]))
    return main, tail


def spectrum(t, v, window, nfft=1 << 16):
    """区間 ``window`` を Hann 窓で切り出して振幅スペクトルを返す。

    Returns
    -------
    f : ndarray    周波数 [Hz]
    X : ndarray    振幅
    res : float    この窓長で得られる周波数分解能 [Hz]（= 1/窓長）
    """
    t0, t1 = window
    sel = (t >= t0) & (t < t1)
    if sel.sum() < 8:
        raise ValueError(f"窓が短すぎます: {t0*1e6:.3f}-{t1*1e6:.3f} us")
    x = v[sel] - v[sel].mean()
    x = x * np.hanning(len(x))
    dt = float(np.diff(t).mean())
    f = np.fft.rfftfreq(nfft, dt)
    return f, np.abs(np.fft.rfft(x, nfft)), 1.0 / (len(x) * dt)


def predicted(pitch_mm, orders=(1, 2, 3, 4, 5, 6), c=C_R, fmax=9e6):
    """レイリー波の予測異常周波数 f = m c / Λ [Hz] を返す。"""
    out = [m * c / (pitch_mm * 1e-3) for m in orders]
    return [x for x in out if x <= fmax]


def analyze(path, nfft=1 << 16):
    """1本の波形を処理して結果を dict で返す。"""
    t, v = load_waveform(path)
    t_echo = find_echo(t, v)
    w_main, w_tail = split(t, v, t_echo)
    f, x_main, res_main = spectrum(t, v, w_main, nfft)
    _, x_tail, res_tail = spectrum(t, v, w_tail, nfft)

    band = (f > 0.8e6) & (f < 9.0e6)
    sel_main = (t >= w_main[0]) & (t < w_main[1])
    sel_tail = (t >= w_tail[0]) & (t < w_tail[1])
    main_pk = float(np.abs(v[sel_main]).max())
    tail_rms = float(np.sqrt(np.mean(v[sel_tail] ** 2)))

    params = parse_params(path)
    return dict(
        path=str(path), params=params,
        t=t, v=v, t_echo=t_echo, window_main=w_main, window_tail=w_tail,
        f=f, x_main=x_main, x_tail=x_tail, band=band,
        res_main=res_main, res_tail=res_tail,
        main_peak=main_pk, tail_rms=tail_rms, ratio=tail_rms / main_pk,
        f_peak_tail=float(f[band][int(np.argmax(x_tail[band]))]),
    )


# --- 図 -------------------------------------------------------------------

def plot(r, out_path=None):
    """1条件ぶんの図（波形＋2つのスペクトル）を書き出す。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t, v = r["t"], r["v"]
    fig, ax = plt.subplots(2, 1, figsize=(8.5, 6.4),
                           gridspec_kw=dict(height_ratios=[1, 1.25], hspace=.32))

    ax[0].plot(t * 1e6, v / np.abs(v).max(), lw=.5, color="#444")
    for w, c, lab in ((r["window_main"], "#2f5d9e", "main bang"),
                      (r["window_tail"], "#a86a14", "tail")):
        ax[0].axvspan(w[0] * 1e6, w[1] * 1e6, color=c, alpha=.14, lw=0)
        ax[0].text((w[0] + w[1]) / 2 * 1e6, 1.08, lab, ha="center",
                   fontsize=8.5, color=c)
    ax[0].axvline(r["t_echo"] * 1e6, color="#b03a3a", lw=.9, ls="--")
    ax[0].set_xlabel("Time [us]"); ax[0].set_ylabel("Normalized")
    ax[0].set_ylim(-1.2, 1.25)

    f, b = r["f"], r["band"]
    for key, c, lab, res in (("x_main", "#2f5d9e", "main bang", r["res_main"]),
                             ("x_tail", "#a86a14", "tail", r["res_tail"])):
        x = r[key][b]
        ax[1].plot(f[b] / 1e6, x / x.max(), lw=1.4, color=c,
                   label=f"{lab}  (resolution {res/1e6:.3f} MHz)")
    if r["params"]:
        for m, fa in enumerate(predicted(r["params"][0]), start=1):
            ax[1].axvline(fa / 1e6, color="#b03a3a", lw=.8, ls=":")
            ax[1].text(fa / 1e6, 1.03, f"m{m}", ha="center", fontsize=7,
                       color="#b03a3a")
    ax[1].set_xlabel("Frequency [MHz]"); ax[1].set_ylabel("Normalized")
    ax[1].set_ylim(0, 1.12); ax[1].legend(fontsize=8)

    if r["params"]:
        p, d, w = r["params"]
        title = f"pitch {p:.2f} / depth {d:.3f} / width {w:.2f} mm"
    else:
        title = Path(r["path"]).name
    fig.suptitle(title + f"    tail/main = {r['ratio']:.4f}", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    if out_path is None:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUT_DIR / (Path(r["path"]).stem + "_split.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


# --- まとめて処理 ---------------------------------------------------------

def iter_files(source="simulation"):
    """対象の波形ファイルを列挙する。"""
    if source == "simulation":
        d = data_paths.sim_csv_dir()
        return sorted(p for p in d.glob("*.csv") if parse_params(p))
    d = data_paths.experiment_dir() / "avg_waveforms"
    return sorted(d.glob("avg_wave_*.csv"))


def run_all(source="simulation", make_plots=False):
    """全条件を処理して集計 CSV を書く。"""
    files = iter_files(source)
    if not files:
        raise FileNotFoundError(f"波形が見つかりません（source={source}）")

    rows = []
    for path in files:
        r = analyze(path)
        p, d, w = r["params"] if r["params"] else (None, None, None)
        nearest = ""
        if p:
            fs = predicted(p)
            if fs:
                i = int(np.argmin([abs(r["f_peak_tail"] - x) for x in fs]))
                nearest = f"m={i+1} ({abs(r['f_peak_tail']-fs[i])/fs[i]*100:.1f}%)"
        rows.append(dict(
            file=Path(path).name, pitch_mm=p, depth_mm=d, width_mm=w,
            echo_us=round(r["t_echo"] * 1e6, 4),
            main_peak=round(r["main_peak"], 6),
            tail_rms=round(r["tail_rms"], 6),
            ratio=round(r["ratio"], 6),
            tail_peak_MHz=round(r["f_peak_tail"] / 1e6, 4),
            tail_resolution_MHz=round(r["res_tail"] / 1e6, 4),
            nearest_order=nearest,
        ))
        if make_plots:
            plot(r)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"split_fft_{source}.csv"
    with out.open("w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wtr.writeheader()
        wtr.writerows(rows)
    return rows, out


def _find_one(pitch, depth, width):
    """指定した条件のファイルを1つ探す。"""
    for path in iter_files("simulation"):
        pr = parse_params(path)
        if pr and np.allclose(pr, (pitch, depth, width), atol=1e-6):
            return path
    raise FileNotFoundError(
        f"pitch={pitch} depth={depth} width={width} のファイルが見つかりません")


def main():
    ap = argparse.ArgumentParser(
        description="波形をメインバンとテイルに切り分けて FFT する")
    ap.add_argument("--source", choices=("simulation", "experiment"),
                    default="simulation", help="対象（既定: simulation）")
    ap.add_argument("--all", action="store_true", help="全条件を処理して集計 CSV を書く")
    ap.add_argument("--plots", action="store_true", help="--all のときに図も全部書く")
    ap.add_argument("--pitch", type=float, help="ピッチ [mm]")
    ap.add_argument("--depth", type=float, help="深さ [mm]")
    ap.add_argument("--width", type=float, help="幅 [mm]")
    ap.add_argument("--file", help="ファイルを直接指定する")
    args = ap.parse_args()

    if not _JP:
        print("注意: japanize_matplotlib が無いため図のラベルは英語になります\n")

    if args.all:
        rows, out = run_all(args.source, make_plots=args.plots)
        hdr = (f"{'pitch':>6}{'depth':>7}{'width':>7}{'echo[us]':>10}"
               f"{'main':>9}{'tailRMS':>10}{'ratio':>9}"
               f"{'tailPk[MHz]':>13}  最寄次数")
        print(hdr)
        for r in rows:
            print(f"{r['pitch_mm']:6.2f}{r['depth_mm']:7.3f}{r['width_mm']:7.2f}"
                  f"{r['echo_us']:10.3f}{r['main_peak']:9.4f}{r['tail_rms']:10.5f}"
                  f"{r['ratio']:9.4f}{r['tail_peak_MHz']:13.2f}  {r['nearest_order']}")
        print(f"\n周波数分解能（テイル窓）: {rows[0]['tail_resolution_MHz']:.3f} MHz")
        print(f"集計: {out}")
        return

    if args.file:
        path = Path(args.file)
    elif None not in (args.pitch, args.depth, args.width):
        path = _find_one(args.pitch, args.depth, args.width)
    else:
        ap.error("--all か、--pitch/--depth/--width か、--file を指定してください")

    r = analyze(path)
    print(f"ファイル    : {Path(path).name}")
    if r["params"]:
        print(f"条件        : pitch {r['params'][0]:.2f} / "
              f"depth {r['params'][1]:.3f} / width {r['params'][2]:.2f} mm")
    print(f"エコー到達  : {r['t_echo']*1e6:.3f} us "
          f"（理論値 {ECHO_TIME*1e6:.3f} us）")
    print(f"メインバン窓: {r['window_main'][0]*1e6:.3f} – {r['window_main'][1]*1e6:.3f} us"
          f"   分解能 {r['res_main']/1e6:.3f} MHz")
    print(f"テイル窓    : {r['window_tail'][0]*1e6:.3f} – {r['window_tail'][1]*1e6:.3f} us"
          f"   分解能 {r['res_tail']/1e6:.3f} MHz")
    print(f"メインバン最大: {r['main_peak']:.5f}")
    print(f"テイル RMS    : {r['tail_rms']:.6f}")
    print(f"テイル/メイン : {r['ratio']:.5f}")
    print(f"テイルの主ピーク: {r['f_peak_tail']/1e6:.3f} MHz")
    if r["params"]:
        fs = predicted(r["params"][0])
        print("予測異常周波数: " + ", ".join(
            f"m{i+1}={x/1e6:.3f}" for i, x in enumerate(fs)))
    print(f"\n図: {plot(r)}")


if __name__ == "__main__":
    main()
