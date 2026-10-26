"""
config.py — プロジェクト共通の設定値（2D）
=============================================================
FDTD シミュレーション・解析・可視化のすべてのスクリプトが
ここから定数を読む。**物理定数やメッシュ設定をここ以外に書かないこと。**

以前は同じ定数が UT_FlawVariation_Sim.py / kukei_ani.py / sourse_new_2.py に
別々に書かれており、片方だけ直すと波形とアニメーションで dt がずれた。

【値を変えるとき】
    材料・メッシュ・周波数     → このファイルの該当セクション
    データの置き場所           → 環境変数 LAB_DOC_ROOT（下の「パス」参照）
    解析対象の形状             → naming.py の SIM_SHAPE

※ 3D 版 (UT_FlawVariation_Sim_3d.py) は mesh_length が異なるため、
  このファイルは参照していない（3D は独自に定数を持つ）。
"""

import os

import numpy as np

from naming import SIM_SHAPE

# =============================================================================
# 解析対象の形状
# =============================================================================
# naming.SIM_SHAPE が唯一の定義。sourse_new_2 の target_shape はこれの別名。
target_shape = SIM_SHAPE

# =============================================================================
# 計算領域・メッシュ
# =============================================================================
x_length = 0.02          # x方向（深さ方向）の長さ [m]
z_length = 0.04          # z方向（表面に沿う方向）の長さ [m]
mesh_length = 1.0e-5     # 空間メッシュ間隔 [m]

# ★要判断★ int() は切り捨て。0.02 / 1.0e-5 は浮動小数点では 1999.9999999999998 に
# なるので nx = 2000 ではなく **1999** になる。その結果
#     dx = 0.02 / 1999 = 1.0005e-5 [m]  (mesh_length と 0.05% ずれる)
#     dt = dx / cl / sqrt(6)            (この dx を通じて同じだけずれる)
# となる。これまでの FDTD 出力 CSV はすべて nx=1999 で計算されている。
#
# ここを int(round(...)) にすると nx=2000・dx=1.0e-5 ちょうどになり、
# 物理的にはそちらが正しい。ただし dt が変わるので**過去の出力と比較できなくなる**。
# 既存データを守るため、いまは従来どおり int() のままにしてある。
# 作り直す覚悟ができたら、この 2 行を int(round(...)) に変えるだけでよい。
#
# 旧 kukei_ani.py だけが int(round(...)) を使っており、アニメーションは
# nx=2000・dt が 0.05% 違う条件で計算されていた（今は本体に合わせて 1999）。
nx = int(x_length / mesh_length)   # x方向メッシュ数 → 1999
nz = int(z_length / mesh_length)   # z方向メッシュ数 → 3999

dx = x_length / nx       # x方向メッシュ幅 [m]
dz = z_length / nz       # z方向メッシュ幅 [m]

# =============================================================================
# 材料定数（鉄鋼を想定）
# =============================================================================
rho = 7840               # 密度 [kg/m^3]
E   = 206 * 1e9          # ヤング率 [Pa]
G   = 80 * 1e9           # せん断弾性率 [Pa]
V   = 0.27               # ポアソン比

cl = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))  # P波（縦波）速度 [m/s]
ct = np.sqrt(G / rho)                                    # S波（横波）速度 [m/s]

# 弾性定数テンソル成分
c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
c13 = E * V       / (1 + V) / (1 - 2 * V)
c55 = (c11 - c13) / 2

# =============================================================================
# 時間刻み・送信波
# =============================================================================
dt = dx / cl / np.sqrt(6)   # FDTD の時間ステップ [s]（安定条件から決定）

f_freq = 4.7e6              # 送信周波数 [Hz]
wave_period = 1 / f_freq    # 周期 [s]
wavelength  = cl / f_freq   # 波長 [m]
wavenumber  = 1 / wavelength   # 波数 [1/m]
steps_per_period = wave_period / dt   # 1周期あたりの離散点数
wn = 2.5                    # 送信バーストの波数（何周期分の波を送るか）

# =============================================================================
# 探触子
# =============================================================================
probe_d = 0.007          # 探触子の開口幅 [m]

# =============================================================================
# 実験データ・FFT の設定
# =============================================================================
fft_N  = 2 ** 14           # FFT のゼロパディング後の総点数 (16384点)
exp_dt = 0.0005E-06        # 実験のサンプリング間隔 [s] (= 0.5 ns)

# kiritori2 で波形を切り出す際のピーク前後点数
thin  = int(2 ** 9)        # 薄いほう (512点)
thick = int(2 ** 10)       # 厚いほう (1024点)
left  = thick              # ピーク左側に含める点数
right = thick * 3          # ピーク右側に含める点数

# 実験データの切り出し範囲インデックス
exp_a1 = 0
exp_a2 = 3730
exp_a3 = 12000

# シミュレーションデータの対応インデックス
sim_a1 = 6000
sim_a2 = 15000
sim_a3 = sim_a2 + exp_a3 - exp_a2

data_size = exp_a3 - exp_a2   # 処理対象の波形長

# シミュレーション波形の先頭スキップ点数（入射パルスを避ける）
search_offset = 8000

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

pitch_list      = [125, 150, 175, 200]
depth_index_all = _depth_exp[target_shape]   # 実験データの depth 一覧 (辞書)
depth_sim_all   = _depth_sim[target_shape]   # シミュレーションデータの depth 一覧 (辞書)

# pitch ごとの depth リスト (よく使う変数として展開)
depth_125 = depth_index_all[125]
depth_150 = depth_index_all[150]
depth_175 = depth_index_all[175]
depth_200 = depth_index_all[200]

rough_list  = {p: len(depth_index_all[p]) for p in pitch_list}   # pitch ごとの depth 数
depth_index = {0: 0, **{p: len(depth_index_all[p]) for p in pitch_list}}  # pitch→depth数 (0は平滑)

# =============================================================================
# パス
# =============================================================================
# 出力先は「スクリプトをどこから実行したか」に依存させない。
# AGENTS.md 11章のとおり lab/tmp_output/ が lab-data と同期される場所なので、
# カレントディレクトリではなくファイル位置を基準に lab/ を求める。
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))          # .../lab/vscode/project3_2026_09_17
REPO_ROOT   = os.path.abspath(os.path.join(PROJECT_DIR, "..", ".."))  # .../lab

# 実験・シミュレーションの元データ置き場。PC ごとに違うので環境変数で差し替える。
#   研究室 PC: 既定値のまま
#   自宅 PC  : setx LAB_DOC_ROOT "C:/Users/local6021/python_projects/Roughness/project4"
# ※ AGENTS.md 9章のとおり、この配下は中身が揃っていないことがある。
doc_path = os.environ.get("LAB_DOC_ROOT", r"C:/Users/cs16/Roughness/project4")

sim_base_dir = os.path.join(doc_path, "Simulation_Data")   # シミュレーション CSV の親フォルダ
exp_base_dir = os.path.join(doc_path, "Experiment_Data")   # 実験 CSV の親フォルダ
output_dir   = os.path.join(doc_path, "tmp_output")        # sourse_new_2 系の図の保存先

# lab/ 配下の作業ディレクトリ（lab-data と同期される。AGENTS.md 11章）
TMP_OUTPUT_DIR  = os.path.join(REPO_ROOT, "tmp_output")
SIM_OUT_DIR     = os.path.join(TMP_OUTPUT_DIR, "sim")                 # FDTD 波形 CSV の出力先
COMPARE_OUT_DIR = os.path.join(TMP_OUTPUT_DIR, "comparison_plots")    # 比較プロットの出力先
ANIM_OUT_DIR    = os.path.join(TMP_OUTPUT_DIR, "animation")           # アニメーションの出力先
DATA_SIM_DIR    = os.path.join(REPO_ROOT, "data", "simdata_out")      # 確定した計算結果の置き場

# バッチ計算のパラメータ表
SIMDATA_CSV = os.path.join(PROJECT_DIR, "simdata.csv")
