"""
sourse_new_2.py — 超音波実験・シミュレーション共通ライブラリ
=============================================================
実験 CSV とシミュレーション CSV を読み込み、FFT スペクトルを
正規化・比較するための関数群。

【基本的な使い方】
    1. target_shape を変更する (★ マーク箇所、65行目付近)
    2. doc_path を自分の PC のパスに変更する (82行目付近)
    3. select_pitch_and_image_exp(pitch, depth_list) を呼び出す

【ファイルの読み込み先】
    実験データ : Experiment_Data/<Shape>/<pitch>_<depth>/*.csv
    シミュ データ: Simulation_Data/<Shape>/<shape>_cupy_pitch<p>_depth<d>.csv

【パラメータのコード規則】
    pitch, depth はすべて整数で value[mm] × 100
    例) pitch=125 → 1.25 mm, depth=20 → 0.20 mm
"""

import numpy as np
from scipy.interpolate import interp1d
import re
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# =============================================================================
# シミュレーションメッシュ設定
# =============================================================================
fft_N = 2 ** 14          # FFT のゼロパディング後の総点数 (16384点)
x_length = 0.02          # シミュレーション領域 x方向 [m]
z_length = 0.04          # シミュレーション領域 z方向 [m]
mesh_length = 1.0e-5     # 空間メッシュ間隔 [m]
nx = int(x_length / mesh_length)   # x方向メッシュ数
nz = int(z_length / mesh_length)   # z方向メッシュ数

dx = x_length / nx       # x方向メッシュ幅 [m]
dz = z_length / nz       # z方向メッシュ幅 [m]

# =============================================================================
# 材料定数 (鉄鋼を想定)
# =============================================================================
rho = 7840               # 密度 [kg/m^3]
E   = 206 * 1e9          # ヤング率 [Pa]
G   = 80  * 1e9          # せん断弾性率 [Pa]
V   = 0.27               # ポアソン比

# 弾性波速度の計算
cl  = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))  # P波 (縦波) 速度 [m/s]
ct  = np.sqrt(G / rho)                                       # S波 (横波) 速度 [m/s]

# 弾性定数テンソル成分
c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
c13 = E * V       / (1 + V) / (1 - 2 * V)
c55 = (c11 - c13) / 2

# =============================================================================
# 時間・切り出し設定
# =============================================================================
dt     = dx / cl / np.sqrt(6)  # シミュレーションの時間ステップ [s] (安定条件から決定)
exp_dt = 0.0005E-06             # 実験のサンプリング間隔 [s] (= 0.5 ns)

# kiritori2 で波形を切り出す際のピーク前後点数
left  = int(2 ** 10)       # ピーク左側に含める点数 (1024点)
right = int((2 ** 10) * 3) # ピーク右側に含める点数 (3072点) → 合計 4096点

# 実験データの切り出し範囲インデックス (使用する関数による)
exp_a1 = 0
exp_a2 = 3730
exp_a3 = 12000

# シミュレーションデータの対応インデックス
sim_a1 = 6000
sim_a2 = 15000
sim_a3 = sim_a2 + exp_a3 - exp_a2

data_size = exp_a3 - exp_a2  # 処理対象の波形長

# =============================================================================
# 各形状で使用可能な pitch / depth の一覧
# =============================================================================
# 実験データが存在する (pitch, depth) の組み合わせ
# ※ Kukei の depth=15 はまだシミュレーションを行っていないため実験データのみ
_depth_exp = {
    "Kukei":   {125: [10, 20],        150: [10, 15, 20], 175: [10, 15, 20], 200: [10, 15, 20]},
    "Sankaku": {125: [10, 15, 20],    150: [10, 15, 20], 175: [10, 15, 20], 200: [10, 15, 20]},
    "Kusabi":  {125: [10, 15, 20],    150: [10, 15, 20], 175: [10, 15, 20], 200: [10, 15, 20]},
    "Ushape":  {125: [12.5, 15, 20],  150: [12.5, 15, 20], 175: [12.5, 15, 20], 200: [12.5, 15, 20]},
}

# シミュレーションデータが存在する (pitch, depth) の組み合わせ
_depth_sim = {
    "Kukei":   {125: [10, 20],        150: [10, 20],       175: [10, 20],       200: [10, 20]},
    "Sankaku": {125: [10, 15, 20],    150: [10, 15, 20],   175: [10, 15, 20],   200: [10, 15, 20]},
    "Kusabi":  {125: [10, 15, 20],    150: [10, 15, 20],   175: [10, 15, 20],   200: [10, 15, 20]},
    "Ushape":  {125: [12.5, 15, 20],  150: [12.5, 15, 20], 175: [12.5, 15, 20], 200: [12.5, 15, 20]},
}

# =============================================================================
# ★ 形状選択 (ここを変更する)
# =============================================================================
target_shape = "Kusabi"  # "Kukei" / "Sankaku" / "Kusabi" / "Ushape"

pitch_list      = [125, 150, 175, 200]
depth_index_all = _depth_exp[target_shape]   # 実験データの depth 一覧 (辞書)
depth_sim_all   = _depth_sim[target_shape]   # シミュレーションデータの depth 一覧 (辞書)

# pitch ごとの depth リスト (よく使う変数として展開)
depth_125 = depth_index_all[125]
depth_150 = depth_index_all[150]
depth_175 = depth_index_all[175]
depth_200 = depth_index_all[200]

rough_list  = {p: len(depth_index_all[p]) for p in pitch_list}  # pitch ごとの depth 数
depth_index = {0: 0, **{p: len(depth_index_all[p]) for p in pitch_list}}  # pitch→depth数 (0は平滑)

# =============================================================================
# パス設定 (自分の PC に合わせて変更)
# =============================================================================
doc_path     = r"C:/Users/cs16/Roughness/project4"   # 研究室 PC
# doc_path   = r"C:/Users/local6021/python_projects/Roughness/project4"  # 自宅 PC
sim_base_dir = os.path.join(doc_path, "Simulation_Data")   # シミュレーション CSV の親フォルダ
exp_base_dir = os.path.join(doc_path, "Experiment_Data")   # 実験 CSV の親フォルダ
output_dir   = os.path.join(doc_path, "tmp_output")        # 図の保存先


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
# シミュレーションデータの読み込み・補間
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
    data0 = np.loadtxt(
        os.path.join(sim_base_dir, "Smooth", "smooth_cupy_pitch125_depth0.csv"))
    data_set_raw = data0
    for filename in filenames:
        data = np.loadtxt(os.path.join(sim_base_dir, target_shape, filename))
        print(filename)
        data_set_raw = np.vstack([data_set_raw, data])
    return data_set_raw


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


# =============================================================================
# データセット作成 (正規化スペクトル)
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
    sim_data_ref = np.loadtxt(
        os.path.join(sim_base_dir, "Smooth", "smooth_cupy_pitch125_depth0.csv"))
    yf_ref, freq_ref = make_fftdata(
        kiritori2(interpolate_sim_one(sim_data_ref)[8000:], left, right), exp_dt)

    # 各 depth のシミュレーション FFT を計算
    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(os.path.join(
            sim_base_dir, target_shape,
            f"{target_shape.lower()}_cupy_pitch{pitch}_depth{depth_list[i]}.csv"))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[8000:], left, right), exp_dt)

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
    sim_data_ref = np.loadtxt(
        os.path.join(sim_base_dir, "Smooth", "smooth_cupy_pitch125_depth0.csv"))
    yf_ref, freq_ref = make_fftdata(
        kiritori2(interpolate_sim_one(sim_data_ref)[8000:], left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(os.path.join(
            sim_base_dir, target_shape,
            f"{target_shape.lower()}_cupy_pitch{pitch}_depth{depth_list[i]}.csv"))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[8000:], left, right), exp_dt)

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


# =============================================================================
# 周波数帯域抽出 (2D 版)
# =============================================================================

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
# 誤差評価 (シミュレーション vs 実験の比較用)
# =============================================================================

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


# =============================================================================
# 波数軸 FFT (周波数軸→波数軸に変換したい場合)
# =============================================================================

def make_fftdata_wavy(data, dt_sample, wave_speed=cl, wavenumber_type='standard'):
    """
    FFT を計算し、周波数軸を波数軸に変換して返す。
    周波数スペクトルを波数スペクトルとして表示したい場合に使う。

    Parameters
    ----------
    data           : ndarray  入力波形
    dt_sample      : float    サンプリング間隔 [s]
    wave_speed     : float    波速 [m/s] (デフォルト = cl, P 波速度)
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


def select_pitch_and_image_wavy(pitch, depth_list):
    """
    シミュレーションデータを波数軸で正規化 FFT plot する。

    Parameters
    ----------
    pitch      : int
    depth_list : list[int]
    """
    sim_data_ref = np.loadtxt(
        os.path.join(sim_base_dir, "Smooth", "smooth_cupy_pitch125_depth0.csv"))
    yf_ref, freq_ref = make_fftdata_wavy(
        kiritori2(interpolate_sim_one(sim_data_ref)[8000:], left, right), exp_dt)

    sim_data = np.zeros((len(depth_list), len(sim_data_ref)))
    yf       = np.zeros((len(depth_list), len(yf_ref)))
    freq     = np.zeros((len(depth_list), len(freq_ref)))
    for i in range(len(depth_list)):
        sim_data[i] = np.loadtxt(os.path.join(
            sim_base_dir, target_shape,
            f"{target_shape.lower()}_cupy_pitch{pitch}_depth{depth_list[i]}.csv"))
        yf[i], freq[i] = make_fftdata(
            kiritori2(interpolate_sim_one(sim_data[i])[8000:], left, right), exp_dt)

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


# =============================================================================
# 波形の前半・後半分割 FFT
# =============================================================================

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
