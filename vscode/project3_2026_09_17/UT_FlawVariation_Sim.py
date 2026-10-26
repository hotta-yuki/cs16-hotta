##########################################################################
#  シミュレーションを傷のバリエーション全部でやるやつ（2D FDTD）
#
#  物理定数・メッシュ設定は config.py、きずの形状マスクは geometry.py にある。
#  このファイルには FDTD の時間発展だけを置く。
##########################################################################

import os

import numpy as np
import cupy as cp

import geometry
from config import (
    SIM_OUT_DIR, c11, c13, c55, cl, dt, dx, dz, mesh_length, nx, nz,
    f_freq, probe_d, rho, steps_per_period, wn, x_length, z_length,
)
from naming import SIM_SHAPE, sim_csv_name


def make_source_wave():
    """
    送信バースト波形を作る。ハン窓をかけた wn 周期ぶんの正弦波。

    Returns
    -------
    ndarray  1D、長さ int(wn * steps_per_period)
    """
    wave4 = np.zeros(int(wn * steps_per_period), dtype=float)
    for ms in range(len(wave4)):
        envelope = (1 - np.cos(2 * np.pi * f_freq * dt * ms / wn)) / 2
        carrier = np.sin(2 * np.pi * f_freq * dt * ms)
        wave4[ms] = envelope * carrier
    return wave4


def probe_range():
    """
    探触子が占める z 方向のインデックス範囲 [sz_l, sz_r) を返す。
    領域の中央に置く。
    """
    sz = int(nz / 2)
    half = int(probe_d / mesh_length / 2)
    return sz - half, sz + half


def total_steps():
    """計算ステップ数。1往復ちょいの時間。"""
    return int(4 * x_length / cl / dt)


def run_simulation(f_width, f_pitch, f_depth):
    print(f"Running simulation: pitch={f_pitch}, depth={f_depth}, width={f_width}")

    wave4 = make_source_wave()
    sz_l, sz_r = probe_range()
    t_max = total_steps()

    # きずの深さの離散点数と、各きずが占める z 範囲
    _, _, _, mn_d = geometry.flaw_mesh_counts(f_width, f_pitch, f_depth, mesh_length)

    # ★このループ内の応力ゼロ化は、昔から isfree とは違う領域長で本数を数えていた
    #   （ループ = z_length、isfree = nz * mesh_length）。pitch 1.25mm では
    #   ループのほうが 1 本多い。既存の出力 CSV と同じ結果を保つため、
    #   ここではその昔の数え方をそのまま渡している。
    #   詳しくは geometry.groove_ranges の domain_length の説明を読むこと。
    grooves = geometry.groove_ranges(nz, f_width, f_pitch, mesh_length,
                                     domain_length=z_length)

    #  =======FDTD本体=======
    # 　T1,T3は垂直応力 T5はせん断応力　Ux,Uzは固体粒子速度
    T1 = cp.zeros((nx + 1, nz), dtype=float)
    T3 = cp.zeros((nx + 1, nz), dtype=float)
    T5 = cp.zeros((nx, nz + 1), dtype=float)
    Ux = cp.zeros((nx, nz), dtype=float)
    Uz = cp.zeros((nx + 1, nz + 1), dtype=float)

    dtx = dt / dx
    dtz = dt / dz

    wave = np.zeros(t_max)
    T13_isfree, T5_isfree = geometry.isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length)
    Ux_free_count, Uz_free_count = geometry.around_free(T13_isfree, T5_isfree, nx, nz)

    # cupy用に変換
    Ux_free_count_cp = cp.asarray(Ux_free_count)
    Uz_free_count_cp = cp.asarray(Uz_free_count)

    def zero_stress_in_grooves():
        """きず部分の応力境界条件。時間ループ内で 2 回使う。"""
        for start, end in grooves:
            T5[nx - mn_d:nx, start:end] = 0
            T1[nx - mn_d:nx + 1, start:end - 1] = 0
            T3[nx - mn_d:nx + 1, start:end - 1] = 0

    def update_uz_boundary():
        """横粒子速度の境界条件。時間ループ内で 3 回使う。"""
        Uz[1:nx, 0] = Uz[1:nx, 0] - (4 / rho) * dtx * (T3[1:nx, 0])
        Uz[1:nx, nz] = Uz[1:nx, nz] - (4 / rho) * dtx * (-1 * T3[1:nx, nz - 1])
        Uz[nx, 1:nz] = Uz[nx, 1:nz] - (4 / rho) * dtx * (-1 * T5[nx - 1, 1:nz])

    for t in range(t_max):
        #  入射波
        if t < int(len(wave4)):
            T1[0, sz_l:sz_r] = wave4[t]

        if t >= int(len(wave4)):
            Uz[0, sz_l:sz_r] = 0
            Ux[0, sz_l:sz_r] = 0
            T1[0, 0:nz] = 0
            T5[0, 0:nz] = 0

        #  応力の境界条件
        T5[0:nx, 0] = 0
        T5[0:nx, nz] = 0
        T3[0, 0:nz] = 0
        T1[nx, 0:nz] = 0
        T3[nx, 0:nz] = 0
        T1[0, 0] = 0
        T3[0, 0] = 0
        T5[0, 0] = 0

        update_uz_boundary()
        zero_stress_in_grooves()
        update_uz_boundary()

        #  応力の更新
        T1[1:nx, 0:nz] = T1[1:nx, 0:nz] - dtx * ((c11 * (Ux[1:nx, 0:nz] - Ux[0:nx - 1, 0:nz]))
                                                    + (c13 * (Uz[1:nx, 1:nz + 1] - Uz[1:nx, 0:nz])))

        T3[1:nx, 0:nz] = T3[1:nx, 0:nz] - dtx * ((c13 * (Ux[1:nx, 0:nz] - Ux[0:nx - 1, 0:nz]))
                                                    + (c11 * (Uz[1:nx, 1:nz + 1] - Uz[1:nx, 0:nz])))

        T5[0:nx, 1:nz] = T5[0:nx, 1:nz] - dtx * c55 * (Ux[0:nx, 1:nz] - Ux[0:nx, 0:nz - 1]
                                                        + Uz[1:nx + 1, 1:nz] - Uz[0:nx, 1:nz])

        zero_stress_in_grooves()
        update_uz_boundary()

        #  粒子速度の更新
        # 自由境界に接するノードと接しないノードを組み合わせて粒子速度を更新
        Ux[0:nx, 0:nz] = cp.where(Ux_free_count_cp[0:nx, 0:nz] < 4,
                                    Ux[0:nx, 0:nz] - (4 / rho / (4 - Ux_free_count_cp[0:nx, 0:nz])) * dtx
                                    * (T1[1:nx + 1, 0:nz] - T1[0:nx, 0:nz]
                                        + T5[0:nx, 1: nz + 1] - T5[0:nx, 0: nz]), 0)

        Uz[1:nx, 1:nz] = cp.where(Uz_free_count_cp[1:nx, 1:nz] < 4,
                                    Uz[1:nx, 1:nz] - (4 / rho / (4 - Uz_free_count_cp[1:nx, 1:nz])) * dtz
                                    * (T3[1:nx, 1:nz] - T3[1:nx, 0:nz - 1]
                                        + T5[1:nx, 1:nz] - T5[0:nx - 1, 1:nz]), 0)
        # cp.cuda.Device().synchronize() # ループ毎の同期は重いので外すか検討
        if t > 0:
            wave[t] = cp.mean(T1[1, sz_l:sz_r])

    wave_cpu = cp.asnumpy(wave)

    # 保存先は config.SIM_OUT_DIR（lab/tmp_output/sim）。
    # 実行したディレクトリに関係なく同じ場所に出る。
    os.makedirs(SIM_OUT_DIR, exist_ok=True)

    name = os.path.join(SIM_OUT_DIR, sim_csv_name(SIM_SHAPE, f_pitch, f_width, f_depth))
    np.savetxt(name, wave_cpu, delimiter=',')
    print(f"Saved: {name}")
    return name


if __name__ == "__main__":
    # テスト用実行
    run_simulation(0.15e-3, 2.00e-3, 0.20e-3)
