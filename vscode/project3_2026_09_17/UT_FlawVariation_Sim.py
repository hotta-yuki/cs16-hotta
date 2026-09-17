##########################################################################
#  シミュレーションを傷のバリエーション全部でやるやつ

import numpy as np
import cupy as cp
import os

from naming import SIM_SHAPE, sim_csv_name

x_length = 0.02  # x方向の長さ m
z_length = 0.04  # z方向の長さ m
mesh_length = 1.0e-5  # m
nx = int(x_length / mesh_length)  # how many mesh
nz = int(z_length / mesh_length)

dx = x_length / nx  # mesh length m
dz = z_length / nz  # m

rho = 7840  # density kg/m^3
E = 206 * 1e9  # young percentage kg/ms^2
G = 80 * 1e9  # stiffness
V = 0.27  # poisson ratio

cl = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))  # P wave
ct = np.sqrt(G / rho)  # S wave
c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
c13 = E * V / (1 + V) / (1 - 2 * V)
c55 = (c11 - c13) / 2

dt = dx / cl / np.sqrt(6)  # time mesh
f = 4.7e6  # frequency
T = 1 / f  # period
lam = cl / f  # lambda
k = 1 / lam  # wave number
n = T / dt  # 波が離散点上で何点か


def isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length):
    T13_isfree = np.ones((nx + 1, nz))
    T5_isfree = np.ones((nx + 1, nz + 1))
    mn_w = int(f_width / mesh_length)  # きずの幅の離散点数
    mn_p = int(f_pitch / mesh_length)  # 1ピッチの離散点数
    mn_nf = int((f_pitch - f_width) / mesh_length)  # きずのない部分の離散点数
    mn_d = int(f_depth / mesh_length)  # きずの深さ方向の離散点数
    num_f = int(nz * mesh_length / f_pitch)  # きずの数
    T13_isfree[0, 0:nz] = 0
    T13_isfree[nx, 0:nz] = 0
    T5_isfree[0:nx, 0] = 0
    T5_isfree[0:nx, nz] = 0
    T5_isfree[nx, 0:nz + 1] = 0

    for i in range(num_f):
        if (i + 1) * mn_p >= nz:
            break
        #  きず部分ゆえに消すとこ
        T5_isfree[nx - mn_d:nx, mn_nf + i * mn_p:(i + 1) * mn_p] = 0
        T13_isfree[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0
    return T13_isfree, T5_isfree


def around_free(T13_isfree, T5_isfree):
    Ux_free_count = np.zeros((nx, nz), dtype=float)
    Uz_free_count = np.zeros((nx + 1, nz + 1), dtype=float)

    for i in range(nx):
        for j in range(nz):
            if T13_isfree[i, j] == 0:
                Ux_free_count[i, j] += 1
            if T13_isfree[i + 1, j] == 0:
                Ux_free_count[i, j] += 1
            if T5_isfree[i, j] == 0:
                Ux_free_count[i, j] += 1
            if T5_isfree[i, j + 1] == 0:
                Ux_free_count[i, j] += 1

    for i in range(nx + 1):
        for j in range(nz + 1):
            if i == 0 or (i == nx and j == 0) or (i == nx and j == nz):
                Uz_free_count[i, j] += 1
            if j == 0 or j == nz:
                Uz_free_count[i, j] += 1
            elif 0 < i and 0 < j:
                if T13_isfree[i, j - 1] == 0:
                    Uz_free_count[i, j] += 1
                if T13_isfree[i, j] == 0:
                    Uz_free_count[i, j] += 1
                if T5_isfree[i - 1, j] == 0:
                    Uz_free_count[i, j] += 1
                if T5_isfree[i, j] == 0:
                    Uz_free_count[i, j] += 1
    return Ux_free_count, Uz_free_count


# =========================================
# 入射波の設定
wn = 2.5  # 波数
wave4 = np.zeros(int(wn * n), dtype=float)
for ms in range(len(wave4)):
    wave2 = (1 - np.cos(2 * np.pi * f * dt * ms / wn)) / 2
    wave3 = np.sin(2 * np.pi * f * dt * ms)
    wave4[ms] = wave2 * wave3
# ==========================================
# 音源の位置
sz = int(nz / 2)
sx = 0
# 探触子の直径 m
probe_d = 0.007
sz_l = sz - int(probe_d / mesh_length / 2)
sz_r = sz + int(probe_d / mesh_length / 2)

t_max = 4 * x_length / cl / dt  # 1往復ちょいの時間

def run_simulation(f_width, f_pitch, f_depth):
    print(f"Running simulation: pitch={f_pitch}, depth={f_depth}, width={f_width}")
    
    #  傷の数
    num_f = int(z_length / f_pitch)
    #  傷の幅の離散点数
    mn_w = int(f_width / mesh_length)
    #  1ピッチの離散点数
    mn_p = int(f_pitch / mesh_length)
    # 傷のない部分の離散点数
    mn_nf = int((f_pitch - f_width) / mesh_length)
    # 傷の深さ方向の離散点数
    mn_d = int(f_depth / mesh_length)

    #  =======FDTD本体=======
    # 　T1,T3は垂直応力 T5はせん断応力　Ux,Uzは固体粒子速度
    T1 = cp.zeros((nx + 1, nz), dtype=float)
    T3 = cp.zeros((nx + 1, nz), dtype=float)
    T5 = cp.zeros((nx, nz + 1), dtype=float)
    Ux = cp.zeros((nx, nz), dtype=float)
    Uz = cp.zeros((nx + 1, nz + 1), dtype=float)

    dtx = dt / dx
    dtz = dt / dz

    wave = np.zeros(int(t_max))
    T13_isfree, T5_isfree = isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length)
    Ux_free_count, Uz_free_count = around_free(T13_isfree, T5_isfree)
    
    # cupy用に変換
    Ux_free_count_cp = cp.asarray(Ux_free_count)
    Uz_free_count_cp = cp.asarray(Uz_free_count)

    for t in range(int(t_max)):
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
        #  横粒子速度の境界条件
        Uz[1:nx, 0] = Uz[1:nx, 0] - (4 / rho) * dtx * (T3[1:nx, 0])
        Uz[1:nx, nz] = Uz[1:nx, nz] - (4 / rho) * dtx * (-1 * T3[1:nx, nz - 1])
        Uz[nx, 1:nz] = Uz[nx, 1:nz] - (4 / rho) * dtx * (-1 * T5[nx - 1, 1:nz])
        #  きず部分の応力境界条件
        for i in range(num_f):
            if (i + 1) * mn_p >= nz:
                break
            #  きず部分ゆえに消すとこ
            T5[nx - mn_d:nx, mn_nf + i * mn_p:(i + 1) * mn_p] = 0
            T1[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0
            T3[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0

        #  横粒子速度の境界条件
        Uz[1:nx, 0] = Uz[1:nx, 0] - (4 / rho) * dtx * (T3[1:nx, 0])
        Uz[1:nx, nz] = Uz[1:nx, nz] - (4 / rho) * dtx * (-1 * T3[1:nx, nz - 1])
        Uz[nx, 1:nz] = Uz[nx, 1:nz] - (4 / rho) * dtx * (-1 * T5[nx - 1, 1:nz])

        #  応力の更新
        T1[1:nx, 0:nz] = T1[1:nx, 0:nz] - dtx * ((c11 * (Ux[1:nx, 0:nz] - Ux[0:nx - 1, 0:nz]))
                                                    + (c13 * (Uz[1:nx, 1:nz + 1] - Uz[1:nx, 0:nz])))

        T3[1:nx, 0:nz] = T3[1:nx, 0:nz] - dtx * ((c13 * (Ux[1:nx, 0:nz] - Ux[0:nx - 1, 0:nz]))
                                                    + (c11 * (Uz[1:nx, 1:nz + 1] - Uz[1:nx, 0:nz])))

        T5[0:nx, 1:nz] = T5[0:nx, 1:nz] - dtx * c55 * (Ux[0:nx, 1:nz] - Ux[0:nx, 0:nz - 1]
                                                        + Uz[1:nx + 1, 1:nz] - Uz[0:nx, 1:nz])
        #  きず部分の応力境界条件
        for i in range(num_f):
            if (i + 1) * mn_p >= nz:
                break
            #  きず部分ゆえに消すとこ
            T5[nx - mn_d:nx, mn_nf + i * mn_p:(i + 1) * mn_p] = 0
            T1[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0
            T3[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0

        #  横粒子速度の境界条件
        Uz[1:nx, 0] = Uz[1:nx, 0] - (4 / rho) * dtx * (T3[1:nx, 0])
        Uz[1:nx, nz] = Uz[1:nx, nz] - (4 / rho) * dtx * (-1 * T3[1:nx, nz - 1])
        Uz[nx, 1:nz] = Uz[nx, 1:nz] - (4 / rho) * dtx * (-1 * T5[nx - 1, 1:nz])
        
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
    
    # 保存先ディレクトリの作成
    output_dir = "tmp_output/sim"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    name = os.path.join(output_dir, sim_csv_name(SIM_SHAPE, f_pitch, f_width, f_depth))
    np.savetxt(name, wave_cpu, delimiter=',')
    print(f"Saved: {name}")

if __name__ == "__main__":
    # テスト用実行
    run_simulation(0.15e-3, 2.00e-3, 0.20e-3)
