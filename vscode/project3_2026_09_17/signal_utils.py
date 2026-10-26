"""
signal_utils.py — 波形の切り出し・FFT・補間・帯域抽出
=============================================================
ファイルを読まない、図を描かない、純粋な信号処理だけを置く。
定数は config.py から取る。

元は sourse_new_2.py に I/O・作図と一緒に入っていた。
"""

import numpy as np
from scipy.interpolate import interp1d

from config import cl, dt, exp_dt, fft_N, left, right


# =============================================================================
# 波形処理ユーティリティ
# =============================================================================

def kiritori2(data_sumple, left, right):
    """
    波形のピーク付近を切り出す。

    ピーク位置を中心に左 left 点・右 right 点を取り出す。
    配列端でピークが近い場合はゼロパディングで補完する。

    Parameters
    ----------
    data_sumple : ndarray  切り出し対象の 1D 波形
    left        : int      ピーク左側の点数
    right       : int      ピーク右側の点数

    Returns
    -------
    ndarray  長さ (left + right) の切り出し波形

    テール波のまわりの波形を切り出すために, この関数を使う。
    """
    L_target    = left + right                    # 目標の切り出し長
    datamaxhere = np.nanargmax(data_sumple)       # ピーク位置のインデックス
    datamaxstart = datamaxhere - left
    datamaxend   = datamaxhere + right
    cut_data = data_sumple[datamaxstart:datamaxend]

    if len(cut_data) != L_target:
        # 配列端に近い場合は長さが足りないのでゼロで埋める
        padding_needed = L_target - len(cut_data)
        if padding_needed > 0:
            return np.pad(cut_data, (0, padding_needed), mode='constant')
        else:
            return cut_data[:L_target]   # 万が一長すぎる場合は切り捨て
    print(f"cut_data.shape: {cut_data.shape}")
    return cut_data


def make_fftdata(data, dt_sumple):
    """
    1D 波形に対してゼロパディング付き FFT を行い、振幅スペクトルと周波数軸を返す。

    fft_N 点になるようにゼロパディングし、rfft で計算する。
    rfft を使うため返り値の長さは fft_N//2 + 1 点になる点に注意。
    (sourse_2.py の fft とは配列長が異なる)

    Parameters
    ----------
    data      : ndarray  入力波形 (長さ ≤ fft_N)
    dt_sumple : float    サンプリング間隔 [s]

    Returns
    -------
    magnitude : ndarray  振幅スペクトル (長さ fft_N//2 + 1)
    freq      : ndarray  周波数軸 [Hz]  (長さ fft_N//2 + 1)
    """
    howmanyzero = fft_N - len(data)
    # 前後均等にゼロを挿入して fft_N 点に揃える
    data_fft = np.concatenate(
        [np.zeros(int(howmanyzero / 2)), data, np.zeros(int(howmanyzero / 2))], 0)
    yf   = np.fft.rfft(data_fft) / (fft_N / 2)      # 正規化した片側スペクトル
    freq = np.fft.rfftfreq(fft_N, d=dt_sumple)       # 対応する周波数軸
    return np.abs(yf), freq


# =============================================================================
# 補間 (シミュレーション時間刻み ⇔ 実験サンプリング間隔)
# =============================================================================

def interpolate_sim(data_set_raw):
    """
    シミュレーション時系列 (dt 刻み) を実験のサンプリング間隔 (exp_dt) に補間する。
    複数波形 (2D 配列) を一括処理する。

    Parameters
    ----------
    data_set_raw : ndarray  shape = (N波形, シミュ時系列点数)

    Returns
    -------
    ndarray  shape = (N波形, 補間後点数)  各行が exp_dt 刻みの波形
    """
    sim_t     = np.arange(0, len(data_set_raw[0]) * dt, dt)
    sim_t_new = np.arange(0, (len(data_set_raw[0]) - 1) * dt, exp_dt)
    data_set_raw_new = np.zeros((data_set_raw.shape[0], len(sim_t_new)))
    for i in range(data_set_raw.shape[0]):
        func = interp1d(sim_t, data_set_raw[i], kind='cubic')
        data_set_raw_new[i] = func(sim_t_new)
    return data_set_raw_new


def interpolate_sim_one(data_set_raw):
    """
    シミュレーション時系列 1 波形を実験サンプリング間隔 (exp_dt) に補間する。

    Parameters
    ----------
    data_set_raw : ndarray  1D、シミュ時系列点数

    Returns
    -------
    ndarray  1D、exp_dt 刻みに補間された波形
    """
    sim_t     = np.arange(0, len(data_set_raw) * dt, dt)
    sim_t_new = np.arange(0, (len(data_set_raw) - 1) * dt, exp_dt)
    data_set_raw_new = np.zeros((data_set_raw.shape[0], len(sim_t_new)))
    func = interp1d(sim_t, data_set_raw, kind='cubic')
    data_set_raw_new = func(sim_t_new)
    return data_set_raw_new


def interpolate_sim_one_inverse(data_set_raw):
    """
    実験サンプリング間隔 (exp_dt) の波形をシミュレーション時間刻み (dt) に逆補間する。
    先頭の NaN 区間はスキップして有効データのみ補間する。

    Parameters
    ----------
    data_set_raw : ndarray  1D、exp_dt 刻みの波形 (先頭に NaN を含んでもよい)

    Returns
    -------
    ndarray  1D、dt 刻みに補間された波形
    """
    first_valid = np.where(~np.isnan(data_set_raw))[0][0]  # 最初の有効インデックス
    valid_data  = data_set_raw[first_valid:]
    sim_t     = np.arange(first_valid * exp_dt, len(data_set_raw) * exp_dt, exp_dt)
    sim_t_new = np.arange(first_valid * exp_dt, (len(data_set_raw) - 1) * exp_dt, dt)
    func = interp1d(sim_t, valid_data, kind='cubic')
    data_set_raw_new = func(sim_t_new)
    return data_set_raw_new


# =============================================================================
# 周波数帯域抽出
# =============================================================================

def extract_frequency_band(freq, fft_data, freq_min, freq_max):
    """
    1D FFT スペクトルから指定した周波数帯のデータだけを切り出す。

    Parameters
    ----------
    freq     : ndarray  周波数軸 [Hz]
    fft_data : ndarray  振幅スペクトル (freq と同じ長さ)
    freq_min : float    下限周波数 [Hz]
    freq_max : float    上限周波数 [Hz]

    Returns
    -------
    fft_band  : ndarray  切り出した振幅スペクトル
    freq_band : ndarray  切り出した周波数軸
    """
    mask      = (freq >= freq_min) & (freq <= freq_max)
    freq_band = freq[mask]
    fft_band  = fft_data[mask]
    return fft_band, freq_band


def extract_frequency_band_2d(freq, fft_data_2d, freq_min, freq_max):
    """
    2D FFT スペクトル (複数波形) から指定周波数帯のデータを切り出す。

    Parameters
    ----------
    freq        : ndarray  周波数軸 [Hz]、長さ M
    fft_data_2d : ndarray  shape = (N波形, M)
    freq_min    : float    下限周波数 [Hz]
    freq_max    : float    上限周波数 [Hz]

    Returns
    -------
    fft_band_2d : ndarray  shape = (N波形, 帯域内点数)
    freq_band   : ndarray  切り出した周波数軸
    """
    mask        = (freq >= freq_min) & (freq <= freq_max)
    freq_band   = freq[mask]
    fft_band_2d = fft_data_2d[:, mask]   # 列方向 (周波数方向) にマスク
    return fft_band_2d, freq_band


# =============================================================================
# 正規化スペクトル
# =============================================================================

def make_data(data0, data, a1):
    """
    参照波形 data0 で正規化した振幅スペクトル (2–8 MHz 帯) を返す。

    Parameters
    ----------
    data0 : ndarray  参照波形 (平滑面など)
    data  : ndarray  対象波形
    a1    : int      波形の先頭を何点スキップするか

    Returns
    -------
    normalized_amp : ndarray  2–8 MHz 帯の正規化振幅
    freq_band      : ndarray  対応する周波数軸 [Hz]
    """
    wave  = kiritori2(data[a1:],  left, right)
    wave0 = kiritori2(data0[a1:], left, right)
    fft_data,  freq = make_fftdata(wave,  exp_dt)
    fft_data0, freq = make_fftdata(wave0, exp_dt)
    # 2–8 MHz 帯に絞って正規化
    amp,  freq_band = extract_frequency_band(freq, fft_data,  2e6, 8e6)
    amp0, _         = extract_frequency_band(freq, fft_data0, 2e6, 8e6)
    return amp / amp0, freq_band


# =============================================================================
# 波数軸 FFT / 前半・後半分割 FFT
# =============================================================================

def make_fftdata_wavy(data, dt_sample, wave_speed=cl, wavenumber_type='standard'):
    """
    FFT を計算し、周波数軸を波数軸に変換して返す。
    周波数スペクトルを波数スペクトルとして表示したい場合に使う。

    Parameters
    ----------
    data           : ndarray  入力波形
    dt_sample      : float    サンプリング間隔 [s]
    wave_speed     : float    波速 [m/s] (デフォルト = config.cl, P波速度)
    wavenumber_type: str      'standard' → k = f/c [1/m]
                              'angular'  → k = 2πf/c [rad/m]

    Returns
    -------
    magnitude : ndarray  振幅スペクトル
    k_values  : ndarray  波数軸 [1/m] または [rad/m]

    注意
    ----
    こちらは fft (全点) を使うため返り値の長さは fft_N 点。
    make_fftdata (rfft) と混在させると配列長が合わないので注意。
    """
    howmanyzero = fft_N - len(data)
    data_fft    = np.concatenate(
        [np.zeros(int(howmanyzero / 2)), data, np.zeros(int(howmanyzero / 2))], 0)
    yf   = np.fft.fft(data_fft) / (fft_N / 2)
    freq = np.linspace(0, 1.0 / dt_sample, fft_N)   # 周波数軸

    # 周波数 → 波数に変換
    if wavenumber_type == 'angular':
        k_values = 2 * np.pi * freq / wave_speed   # 角波数 [rad/m]
    else:
        k_values = freq / wave_speed                # 標準波数 [1/m]

    return np.abs(yf), k_values


def make_fftdata_main_tale(data, dt, boader):
    """
    波形を「全体」「前半 (main)」「後半 (tale)」の 3 つに分割して FFT を計算する。
    入射波と反射波を分けて周波数成分を比較したい場合に使う。

    Parameters
    ----------
    data   : ndarray  1D 波形
    dt     : float    サンプリング間隔 [s]
    boader : int      前半と後半の境界インデックス

    Returns
    -------
    yf   : ndarray  shape = (3, fft_N)  [全体, 前半, 後半] の振幅スペクトル
    freq : ndarray  shape = (3, fft_N)  対応する周波数軸 (3 行とも同じ値)
    """
    yf, freq = np.zeros((3, fft_N)), np.zeros((3, fft_N))

    # 全体
    howmanyzero0 = fft_N - len(data)
    data_fft0    = np.concatenate(
        [np.zeros(int(howmanyzero0 / 2)), data, np.zeros(int(howmanyzero0 / 2))], 0)
    yf0   = np.fft.fft(data_fft0) / (fft_N / 2)
    freq1 = np.linspace(0, 1.0 / dt, fft_N)

    # 前半 (main: boader まで)
    howmanyzero1 = fft_N - len(data[:boader])
    data_fft1    = np.concatenate(
        [np.zeros(int(howmanyzero1 / 2)), data[:boader], np.zeros(int(howmanyzero1 / 2))], 0)
    yf1 = np.fft.fft(data_fft1) / (fft_N / 2)

    # 後半 (tale: boader 以降)
    howmanyzero2 = fft_N - len(data[boader:])
    data_fft2    = np.concatenate(
        [np.zeros(int(howmanyzero2 / 2)), data[boader:], np.zeros(int(howmanyzero2 / 2))], 0)
    yf2 = np.fft.fft(data_fft2) / (fft_N / 2)

    yf[0],   freq[0] = np.abs(yf0), freq1
    yf[1],   freq[1] = np.abs(yf1), freq1
    yf[2],   freq[2] = np.abs(yf2), freq1
    return yf, freq
