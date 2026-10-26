"""
dataio.py — 実験 CSV / シミュレーション CSV の読み込みとデータセット作成
=============================================================
ファイルを読む処理はここに集約する。図は描かない（plotting.py の担当）。
パスは config.py（環境変数 LAB_DOC_ROOT で差し替え可）。

【ファイルの読み込み先】
    実験データ  : Experiment_Data/<Shape>/<pitch>_<depth>/*.csv
    シミュデータ: Simulation_Data/<Shape>/<shape>_cupy_pitch<p>_depth<d>.csv

【パラメータのコード規則】
    pitch, depth はすべて整数で value[mm] × 100
    例) pitch=125 → 1.25 mm, depth=20 → 0.20 mm
"""

import glob
import os
import re

import numpy as np
import pandas as pd

from config import (
    depth_index_all, exp_base_dir, exp_dt, left, right,
    sim_base_dir, target_shape,
)
from signal_utils import (
    interpolate_sim, interpolate_sim_one, kiritori2, make_data, make_fftdata,
)

# 平滑面（参照）のシミュレーション波形
SMOOTH_SIM_CSV = os.path.join(sim_base_dir, "Smooth", "smooth_cupy_pitch125_depth0.csv")

# シミュレーション波形の先頭スキップ点数（入射パルスを避ける）
SIM_SKIP = 8000


def sim_csv_path(pitch, depth):
    """シミュレーション CSV のパスを組み立てる。"""
    return os.path.join(
        sim_base_dir, target_shape,
        f"{target_shape.lower()}_cupy_pitch{pitch}_depth{depth}.csv")


# =============================================================================
# シミュレーションデータの読み込み
# =============================================================================

def simu_data_import(filenames):
    """
    シミュレーション CSV を複数読み込み、参照(平滑面)を 0 行目として縦に結合して返す。

    Parameters
    ----------
    filenames : list[str]  Simulation_Data/<target_shape>/ 以下のファイル名リスト

    Returns
    -------
    ndarray  shape = (1 + len(filenames), 時系列点数)
             0 行目 = 平滑面 (参照)
    """
    # 参照として平滑面データを最初に読み込む
    data0 = np.loadtxt(SMOOTH_SIM_CSV)
    data_set_raw = data0
    for filename in filenames:
        data = np.loadtxt(os.path.join(sim_base_dir, target_shape, filename))
        print(filename)
        data_set_raw = np.vstack([data_set_raw, data])
    return data_set_raw


def extract_numbers(filename):
    """
    ファイル名の文字列から pitch と depth の数値を正規表現で取得する。
    例) "kusabi_cupy_pitch200_depth20.csv" → (200, 20)

    Parameters
    ----------
    filename : str

    Returns
    -------
    pitch : int or None
    depth : int or None
    """
    pitch_match = re.search(r'pitch(\d+)', filename)
    depth_match = re.search(r'depth(\d+)', filename)
    pitch = int(pitch_match.group(1)) if pitch_match else None
    depth = int(depth_match.group(1)) if depth_match else None
    return pitch, depth


def make_dataset_sim(filenames, a1):
    """
    シミュレーション CSV を複数読み込み、正規化スペクトルの 2D 配列を返す。
    0 行目 (平滑面) を参照として各行を正規化する。

    Parameters
    ----------
    filenames : list[str]  ファイル名リスト
    a1        : int        波形のスキップ点数

    Returns
    -------
    data_set : ndarray  shape = (len(filenames), 周波数点数)
    freq     : ndarray  対応する周波数軸 [Hz]
    """
    data_set_raw = interpolate_sim(simu_data_import(filenames))
    data_test, freq = make_data(data_set_raw[0], data_set_raw[0], a1)
    data_set = np.zeros((data_set_raw.shape[0] - 1, len(data_test)))
    for i in range(data_set_raw.shape[0] - 1):
        print(i)
        data_set[i], freq = make_data(data_set_raw[0], data_set_raw[i + 1], a1)
    return data_set, freq


# =============================================================================
# 実験データの読み込み
# =============================================================================

def import_data(pitch, depth):
    """
    実験 CSV を読み込み、複数ファイルの平均波形と全波形配列を返す。

    CSV は SHIFT-JIS エンコード。先頭 2 行はヘッダとして除去。
    列 0 = 時間, 列 1 = 電圧。各ファイルの最頻値をバイアスとして引く。

    Parameters
    ----------
    pitch : int  ピッチコード (0 のとき平滑面)
    depth : int  深さコード   (0 のとき平滑面)

    Returns
    -------
    data_m   : ndarray  全ファイルの平均波形 (1D)
    data_arr : ndarray  全波形の 2D 配列 shape = (ファイル数, 点数)
    """
    data_tmp0, data_tmp1, data_tmp2 = [], [], []
    data_tmp3, data_tmp4, number_max, data = [], [], [], []

    # フォルダパスの決定
    if pitch == 0 and depth == 0:
        target_dir = os.path.join(exp_base_dir, "Smooth", "0_0")
    else:
        target_dir = os.path.join(exp_base_dir, target_shape, f"{pitch}_{depth}")

    csv_files = glob.glob(os.path.join(target_dir, "*.csv"))
    i = 0
    for csv_file in csv_files:
        print(f"importing : {csv_file}")
        data_tmp0.append(pd.read_csv(csv_file, encoding='SHIFT-JIS', header=None))
        data_tmp1.append(data_tmp0[i].drop(data_tmp0[i].index[[0, 1]]))  # ヘッダ 2行削除
        data_tmp1[i] = data_tmp1[i].astype(float)
        data_tmp2.append(data_tmp1[i].iloc[:, 0])   # 時間列
        data_tmp3.append(data_tmp1[i].iloc[:, 1])   # 電圧列
        number_max.append(data_tmp2[i].count())
        data_tmp4.append([data_tmp3[i].mode().iloc[0]] * number_max[i])  # バイアス (最頻値)
        data.append(data_tmp3[i] - data_tmp4[i])    # バイアス除去済み電圧
        i += 1

    data_arr = np.array(data)
    data_m   = data_arr.mean(0)
    return data_m, data_arr


def depthrough(pitch, rough):
    """
    rough 番号 (0始まりのインデックス) を実際の depth 値に変換する。
    pitch=0 のとき平滑面として 0 を返す。

    Parameters
    ----------
    pitch : int  ピッチコード
    rough : int  depth のインデックス (0, 1, 2, ...)

    Returns
    -------
    float  depth 値 (例: 10, 15, 20, 12.5)
    """
    if pitch == 0:
        return 0
    return depth_index_all[pitch][rough]


def make_dataset_exp_y_new(pitch, rough):
    """
    機械学習用の入力ラベル (pitch/10, depth) を 1×2 の配列で返す。

    Parameters
    ----------
    pitch : int
    rough : int  depth インデックス

    Returns
    -------
    ndarray  shape = (1, 2)  [[pitch/10, depth]]
    """
    depth_set = np.full(1, float(depthrough(pitch, rough)))
    pitch_set = np.full(1, float(pitch))
    return np.column_stack((pitch_set / 10, depth_set))


def make_dataset_exp_new(pitch, depth, a1):
    """
    実験データを 1 条件分読み込み、正規化スペクトルを返す。

    Parameters
    ----------
    pitch : int   ピッチコード
    depth : float 深さコード (整数でも float でも可)
    a1    : int   波形のスキップ点数

    Returns
    -------
    data_set_exp : ndarray  shape = (1, 周波数点数)  正規化振幅スペクトル
    """
    mean,  _  = import_data(pitch, depth)
    mean0, _  = import_data(0, 0)           # 参照 (平滑面)
    data_test_exp, freq = make_data(mean0, mean[0], a1)   # サイズ確認用
    data_set_exp = np.zeros((1, len(data_test_exp)))
    data_set_exp[0], freq = make_data(mean0, mean, a1)
    return data_set_exp


# =============================================================================
# FFT 結果を返すだけの関数 (plot なし、呼び出し元で使う)
# =============================================================================

def select_sim(pitch, depth_list):
    """
    シミュレーション FFT スペクトルと参照を返す (plot なし)。

    Returns
    -------
    freq   : ndarray  shape = (len(depth_list), 周波数点数)
    yf     : ndarray  shape = (len(depth_list), 周波数点数)  各 depth の振幅
    yf_ref : ndarray  参照 (平滑面) の振幅スペクトル
    """
    sim_data_ref = np.loadtxt(SMOOTH_SIM_CSV)
    yf_ref, freq_ref = make_fftdata(
        kiritori2(interpolate_sim_one(sim_data_ref)[SIM_SKIP:], left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(sim_csv_path(pitch, depth_list[i]))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[SIM_SKIP:], left, right), exp_dt)

    return freq, yf, yf_ref


def select_exp(pitch, depth_list):
    """
    実験 FFT スペクトルと参照を返す (plot なし)。

    Returns
    -------
    freq   : ndarray  shape = (len(depth_list), 周波数点数)
    yf     : ndarray  shape = (len(depth_list), 周波数点数)  各 depth の振幅
    yf_ref : ndarray  参照 (平滑面) の振幅スペクトル
    """
    sim_data_ref, _ = import_data(0, 0)
    yf_ref, freq_ref = make_fftdata(kiritori2(sim_data_ref, left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i], _ = import_data(pitch, depth_list[i])
        yf[i], freq[i] = make_fftdata(kiritori2(sim_data[i], left, right), exp_dt)

    return freq, yf, yf_ref
