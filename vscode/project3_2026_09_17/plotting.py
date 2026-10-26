"""
plotting.py — 正規化 FFT スペクトルの作図
=============================================================
データの読み込みは dataio.py、計算は signal_utils.py。
ここは「描いて保存する」だけを受け持つ。

【よく使う関数】
    select_pitch_and_image_exp(pitch, depth_list)   実験データ  ★メイン
    select_pitch_and_image(pitch, depth_list)       シミュレーション
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from config import cl, exp_dt, left, output_dir, right
from dataio import SIM_SKIP, SMOOTH_SIM_CSV, import_data, sim_csv_path
from signal_utils import (
    interpolate_sim_one, kiritori2, make_fftdata, make_fftdata_wavy,
)


# =============================================================================
# FFT スペクトルの可視化・保存 (シミュレーション)
# =============================================================================

def select_pitch_and_image(pitch, depth_list):
    """
    シミュレーションデータの正規化 FFT スペクトルをまとめて plot し EPS 保存する。
    各 depth を 1 枚のグラフに重ねて描画する。

    Parameters
    ----------
    pitch      : int        ピッチコード
    depth_list : list[int]  depth コードのリスト (例: [10, 15, 20])
    """
    # 参照 (平滑面) の FFT
    sim_data_ref = np.loadtxt(SMOOTH_SIM_CSV)
    yf_ref, freq_ref = make_fftdata(
        kiritori2(interpolate_sim_one(sim_data_ref)[SIM_SKIP:], left, right), exp_dt)

    # 各 depth のシミュレーション FFT を計算
    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(sim_csv_path(pitch, depth_list[i]))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[SIM_SKIP:], left, right), exp_dt)

    # plot
    plt.rcParams["font.size"] = 16
    plt.figure()
    for i in range(len(depth_list)):
        plt.plot(freq_ref, yf[i] / yf_ref, label=f"d:{int(depth_list[i])/100} mm")
    plt.xlim(2000000, 8000000)
    plt.ylim(0, 1.7)
    plt.ylabel("Normalized amplitude", fontsize=17)
    plt.xlabel("Frequency [Hz]",       fontsize=17)
    plt.legend(ncol=2, loc='upper left', fontsize=18)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"sim_yfs_{pitch}.eps"), format="eps", dpi=300)
    plt.show()


# =============================================================================
# FFT スペクトルの可視化・保存 (実験データ) ★ メインで使う関数
# =============================================================================

def select_pitch_and_image_exp(pitch, depth_list):
    """
    実験データの正規化 FFT スペクトルをまとめて plot し EPS 保存する。
    各 depth を 1 枚のグラフに重ねて描画する。

    Parameters
    ----------
    pitch      : int          ピッチコード (例: 200)
    depth_list : list[float]  depth コードのリスト (例: [10, 15, 20])

    使用例
    ------
    select_pitch_and_image_exp(200, [10, 15, 20])
    """
    # 参照 (平滑面) の FFT
    sim_data_ref, _ = import_data(0, 0)
    yf_ref, freq_ref = make_fftdata(kiritori2(sim_data_ref, left, right), exp_dt)

    # 各 depth の実験 FFT を計算
    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i], _ = import_data(pitch, depth_list[i])
        yf[i], freq[i] = make_fftdata(kiritori2(sim_data[i], left, right), exp_dt)

    # plot
    plt.rcParams["font.size"] = 16
    plt.figure()
    for i in range(len(depth_list)):
        plt.plot(freq_ref, yf[i] / yf_ref, label=f"d:{depth_list[i]/100} mm")
    plt.xlim(2000000, 8000000)
    plt.ylim(0, 1.7)
    plt.ylabel("Normalized amplitude", fontsize=17)
    plt.xlabel("Frequency [Hz]",       fontsize=17)
    plt.legend(ncol=2, loc='upper left', fontsize=18)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"exp_yfs_{pitch}.eps"), format="eps", dpi=300)
    plt.show()


# =============================================================================
# 波数軸での可視化
# =============================================================================

def select_pitch_and_image_wavy(pitch, depth_list):
    """
    シミュレーションデータを波数軸で正規化 FFT plot する。

    Parameters
    ----------
    pitch      : int
    depth_list : list[int]
    """
    sim_data_ref = np.loadtxt(SMOOTH_SIM_CSV)
    yf_ref, freq_ref = make_fftdata_wavy(
        kiritori2(interpolate_sim_one(sim_data_ref)[SIM_SKIP:], left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(sim_csv_path(pitch, depth_list[i]))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[SIM_SKIP:], left, right), exp_dt)

    plt.rcParams["font.size"] = 14
    plt.figure()
    for i in range(len(depth_list)):
        plt.plot(freq_ref, yf[i] / yf_ref, label=f"d:{int(depth_list[i])/100} mm")
    plt.xlim(2000000 / cl, 8000000 / cl)
    plt.ylim(0, 1.5)
    plt.ylabel("Normalized amplitude")
    plt.xlabel("Wave number m^-1")
    plt.legend()
    plt.tight_layout()
    plt.show()


def select_pitch_and_image_exp_wavy(pitch, depth_list):
    """
    実験データを波数軸で正規化 FFT plot する。

    Parameters
    ----------
    pitch      : int
    depth_list : list[float]

    注意
    ----
    参照 (yf_ref) は make_fftdata_wavy で波数軸を計算しているが、
    各 depth の yf は make_fftdata (rfft) で計算している。
    x 軸に freq_ref (波数) を使っているため、yf との長さが合わない場合がある。
    """
    sim_data_ref, _ = import_data(0, 0)
    yf_ref, freq_ref = make_fftdata_wavy(kiritori2(sim_data_ref, left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i], _ = import_data(pitch, depth_list[i])
        yf[i], freq[i] = make_fftdata(kiritori2(sim_data[i], left, right), exp_dt)

    plt.rcParams["font.size"] = 14
    plt.figure()
    for i in range(len(depth_list)):
        plt.plot(freq_ref, yf[i] / yf_ref, label=f"d:{depth_list[i]/100} mm")
    plt.xlim(2000000 / cl, 8000000 / cl)
    plt.ylim(0, 1.5)
    plt.ylabel("Normalized amplitude")
    plt.xlabel("Wave number m^-1")
    plt.legend()
    plt.tight_layout()
    plt.show()
