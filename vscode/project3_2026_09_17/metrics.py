"""
metrics.py — シミュレーションと実験の一致度の評価
=============================================================
指定した周波数帯で 2 つのスペクトル群を突き合わせ、誤差を数値で出す。
"""

import numpy as np

from signal_utils import extract_frequency_band_2d


def calculate_rmse_with_frequency_band(freq, array1, array2, freq_min, freq_max):
    """
    指定周波数帯で 2 つの 2D スペクトル配列の行ごと RMSE を計算する。
    シミュレーションと実験の一致度を周波数帯単位で評価するために使う。

    Parameters
    ----------
    freq     : ndarray  周波数軸 [Hz]
    array1   : ndarray  shape = (N, M)  1 つ目のスペクトル群
    array2   : ndarray  shape = (N, M)  2 つ目のスペクトル群
    freq_min : float    下限周波数 [Hz]
    freq_max : float    上限周波数 [Hz]

    Returns
    -------
    row_rmse      : ndarray  shape = (N,)  行 (depth) ごとの RMSE
    masked_array1 : ndarray  マスク後の array1
    masked_array2 : ndarray  マスク後の array2
    freq_band     : ndarray  マスク後の周波数軸
    """
    if array1.shape != array2.shape:
        raise ValueError("両方の配列は同じ形状である必要があります")

    masked_array1, freq_band = extract_frequency_band_2d(freq, array1, freq_min, freq_max)
    masked_array2, _         = extract_frequency_band_2d(freq, array2, freq_min, freq_max)

    squared_diff     = np.square(masked_array1 - masked_array2)
    mean_squared_diff = np.mean(squared_diff, axis=1)   # 行ごとの平均二乗誤差
    row_rmse         = np.sqrt(mean_squared_diff)
    return row_rmse, masked_array1, masked_array2, freq_band


def calculate_column_statistics_with_frequency_band(freq, array1, array2, freq_min, freq_max):
    """
    指定周波数帯で列 (周波数ポイント) ごとの誤差統計を計算する。
    どの周波数で実験とシミュレーションがずれているかを詳しく調べるために使う。

    Parameters
    ----------
    freq     : ndarray  周波数軸 [Hz]
    array1   : ndarray  shape = (N, M)
    array2   : ndarray  shape = (N, M)
    freq_min : float    下限周波数 [Hz]
    freq_max : float    上限周波数 [Hz]

    Returns
    -------
    stats         : dict    列ごとの誤差統計 (rmse, max_error, min_error,
                            mean_error, median_error, std_error,
                            max_rmse_column_index, max_rmse_frequency)
    masked_array1 : ndarray
    masked_array2 : ndarray
    freq_band     : ndarray
    """
    if array1.shape != array2.shape:
        raise ValueError("両方の配列は同じ形状である必要があります")

    masked_array1, freq_band = extract_frequency_band_2d(freq, array1, freq_min, freq_max)
    masked_array2, _         = extract_frequency_band_2d(freq, array2, freq_min, freq_max)

    # 列ごとの RMSE
    squared_diff      = np.square(masked_array1 - masked_array2)
    mean_squared_diff = np.mean(squared_diff, axis=0)
    column_rmse       = np.sqrt(mean_squared_diff)

    abs_diff = np.abs(masked_array1 - masked_array2)

    stats = {
        'rmse':         column_rmse,
        'max_error':    np.max(abs_diff,    axis=0),
        'min_error':    np.min(abs_diff,    axis=0),
        'mean_error':   np.mean(abs_diff,   axis=0),
        'median_error': np.median(abs_diff, axis=0),
        'std_error':    np.std(abs_diff,    axis=0),
    }

    # RMSE が最大になる周波数ポイントの情報
    max_rmse_index = np.argmax(column_rmse)
    stats['max_rmse_column_index'] = max_rmse_index
    stats['max_rmse_frequency']    = freq_band[max_rmse_index]

    return stats, masked_array1, masked_array2, freq_band
