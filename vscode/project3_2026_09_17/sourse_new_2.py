"""
sourse_new_2.py — 旧 共通ライブラリ（互換のための薄い中継）
=============================================================
中身は役割ごとに分割した。**新しいコードは分割後のモジュールを直接 import すること。**

    config.py        定数・データ一覧・パス
    signal_utils.py  波形の切り出し・FFT・補間・帯域抽出
    dataio.py        実験 CSV / シミュレーション CSV の読み込み
    metrics.py       RMSE など誤差評価
    plotting.py      正規化 FFT スペクトルの作図

このファイルは `import sourse_new_2 as sn2` と書いてある既存スクリプトが
そのまま動くように、分割後の名前をまとめて再公開しているだけ。
新規に関数を足すときはここではなく、上のどれかに書く。

【基本的な使い方（従来どおり）】
    1. 形状を変える           → naming.py の SIM_SHAPE
    2. データの置き場所を変える → 環境変数 LAB_DOC_ROOT
    3. plotting.select_pitch_and_image_exp(pitch, depth_list) を呼ぶ
"""

# flake8: noqa: F401  (再公開が目的なので未使用 import の警告は無視する)

from config import (
    c11, c13, c55, cl, ct, data_size, depth_125, depth_150, depth_175, depth_200,
    depth_index, depth_index_all, depth_sim_all, doc_path, dt, dx, dz, E,
    exp_a1, exp_a2, exp_a3, exp_base_dir, exp_dt, fft_N, G, left, mesh_length,
    nx, nz, output_dir, pitch_list, rho, right, rough_list, sim_a1, sim_a2,
    sim_a3, sim_base_dir, target_shape, thick, thin, V, x_length, z_length,
)
from dataio import (
    depthrough, extract_numbers, import_data, make_dataset_exp_new,
    make_dataset_exp_y_new, make_dataset_sim, select_exp, select_sim,
    simu_data_import,
)
from metrics import (
    calculate_column_statistics_with_frequency_band,
    calculate_rmse_with_frequency_band,
)
from plotting import (
    select_pitch_and_image, select_pitch_and_image_exp,
    select_pitch_and_image_exp_wavy, select_pitch_and_image_wavy,
)
from signal_utils import (
    extract_frequency_band, extract_frequency_band_2d, interpolate_sim,
    interpolate_sim_one, interpolate_sim_one_inverse, kiritori2, make_data,
    make_fftdata, make_fftdata_main_tale, make_fftdata_wavy,
)
