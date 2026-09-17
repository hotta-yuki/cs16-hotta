##########################################################################
#  3D 超音波シミュレーション (FDTD法)
#  UT_FlawVariation_Sim.py を 3D に拡張

import numpy as np
import cupy as cp
import os

from naming import SIM_SHAPE, sim3d_csv_name

# =============================================================================
# シミュレーションパラメータ
# =============================================================================
x_length = 0.02          # x方向の長さ [m]
y_length = 0.04          # y方向の長さ [m]
z_length = 0.04          # z方向の長さ [m] 
mesh_length = 2.0e-5     # 空間メッシュ間隔 [m] (3D のため 2.0e-5 に推奨)

nx = int(x_length / mesh_length)
ny = int(y_length / mesh_length)
nz = int(z_length / mesh_length)

dx = x_length / nx  # メッシュ間隔 [m]
dy = y_length / ny  # [m]
dz = z_length / nz  # [m]

# 材料定数 (鉄鋼想定)
rho = 7840               # 密度 [kg/m^3]
E = 206 * 1e9            # ヤング率 [Pa]
G = 80 * 1e9             # せん断弾性率 [Pa]
V = 0.27                 # ポアソン比

# 弾性波速度
cl = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))  # P波
ct = np.sqrt(G / rho)                                   # S波

# 弾性定数テンソル成分 (等方性材料)
c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
c12 = E * V / (1 + V) / (1 - 2 * V)
c44 = G

dt = dx / cl / np.sqrt(6)  # 時間ステップ [s]
f = 4.7e6                 # 周波数 [Hz]
T = 1 / f
n = T / dt                 # 1周期あたりのステップ数

# =============================================================================
# 境界条件と欠陥の定義
# =============================================================================

def isfree_3d(nx, ny, nz, f_width, f_pitch, f_depth, f_length, mesh_length):
    """
    自由境界のフラグ配列を作成する (1: 固体, 0: 自由境界/真空)
    """
    # 垂直応力ノードの自由境界フラグ (Txx, Tyy, Tzz)
    Normal_isfree = np.ones((nx + 1, ny, nz), dtype=np.int8)
    # せん断応力ノードの自由境界フラグ
    Txy_isfree = np.ones((nx, ny + 1, nz), dtype=np.int8)
    Tyz_isfree = np.ones((nx, ny, nz + 1), dtype=np.int8)
    Tzx_isfree = np.ones((nx + 1, ny, nz + 1), dtype=np.int8)

    mn_w = int(f_width / mesh_length)
    mn_p = int(f_pitch / mesh_length)
    mn_nf = int((f_pitch - f_width) / mesh_length)
    mn_d = int(f_depth / mesh_length)
    mn_l = int(f_length / mesh_length)
    num_f = int(ny * mesh_length / f_pitch)

    # 外界の自由境界 (x=0, x=nx, y=0, y=ny, z=0, z=nz)
    Normal_isfree[0, :, :] = 0
    Normal_isfree[nx, :, :] = 0
    # y, z 方向の境界は簡易的に 0 に設定
    Txy_isfree[:, 0, :] = 0
    Txy_isfree[:, ny, :] = 0
    Tyz_isfree[:, :, 0] = 0
    Tyz_isfree[:, :, nz] = 0
    Tzx_isfree[0, :, :] = 0
    Tzx_isfree[nx, :, :] = 0

    # 欠陥 (溝) の作成
    # z 方向の中央に配置
    sz_start = int((nz - mn_l) / 2)
    sz_end = sz_start + mn_l

    for i in range(num_f):
        y_start = mn_nf + i * mn_p
        y_end = (i + 1) * mn_p
        if y_end >= ny:
            break
        
        # 欠陥部分の Normal_isfree を 0 に (x方向深さ mn_d)
        Normal_isfree[nx - mn_d:nx + 1, y_start:y_end, sz_start:sz_end] = 0
        # せん断応力ノードも同様に 0 に
        Txy_isfree[nx - mn_d:nx, y_start:y_end + 1, sz_start:sz_end] = 0
        Tyz_isfree[nx - mn_d:nx, y_start:y_end, sz_start:sz_end + 1] = 0
        Tzx_isfree[nx - mn_d:nx + 1, y_start:y_end, sz_start:sz_end + 1] = 0

    return Normal_isfree, Txy_isfree, Tyz_isfree, Tzx_isfree

def around_free_3d(Normal_isfree, Txy_isfree, Tyz_isfree, Tzx_isfree):
    """
    粒子速度更新用の自由境界カウント配列を作成する
    """
    nx, ny, nz = Normal_isfree.shape[0] - 1, Normal_isfree.shape[1], Normal_isfree.shape[2]
    
    Vx_free_count = np.zeros((nx, ny, nz), dtype=np.float32)
    Vy_free_count = np.zeros((nx + 1, ny + 1, nz), dtype=np.float32)
    Vz_free_count = np.zeros((nx + 1, ny, nz + 1), dtype=np.float32)

    # Vx 更新に関わる 6 つの応力ノードの自由境界数をカウント
    # Txx(i, j, k), Txx(i+1, j, k), Txy(i, j, k), Txy(i, j+1, k), Tzx(i, j, k), Tzx(i, j, k+1)
    Vx_free_count += (1 - Normal_isfree[0:nx, :, :])
    Vx_free_count += (1 - Normal_isfree[1:nx+1, :, :])
    Vx_free_count += (1 - Txy_isfree[:, 0:ny, :])
    Vx_free_count += (1 - Txy_isfree[:, 1:ny+1, :])
    Vx_free_count += (1 - Tzx_isfree[0:nx, :, 0:nz])
    Vx_free_count += (1 - Tzx_isfree[0:nx, :, 1:nz+1])

    # Vy 用
    Vy_free_count[1:nx, 1:ny, :] += (1 - Normal_isfree[1:nx, 1:ny, :])
    Vy_free_count[1:nx, 1:ny, :] += (1 - Normal_isfree[1:nx, 0:ny-1, :])
    Vy_free_count[1:nx, 1:ny, :] += (1 - Txy_isfree[1:nx, 1:ny, :])
    Vy_free_count[1:nx, 1:ny, :] += (1 - Txy_isfree[0:nx-1, 1:ny, :])
    Vy_free_count[1:nx, 1:ny, :] += (1 - Tyz_isfree[1:nx, 1:ny, 0:nz])
    Vy_free_count[1:nx, 1:ny, :] += (1 - Tyz_isfree[1:nx, 1:ny, 1:nz+1])
    # 境界部分は 4 (自由) に設定して更新されないようにする (簡易的)
    Vy_free_count[0, :, :] = 6
    Vy_free_count[nx, :, :] = 6
    Vy_free_count[:, 0, :] = 6
    Vy_free_count[:, ny, :] = 6

    # Vz 用
    Vz_free_count[1:nx, :, 1:nz] += (1 - Normal_isfree[1:nx, :, 1:nz])
    Vz_free_count[1:nx, :, 1:nz] += (1 - Normal_isfree[1:nx, :, 0:nz-1])
    Vz_free_count[1:nx, :, 1:nz] += (1 - Tyz_isfree[1:nx, 0:ny-1, 1:nz])
    Vz_free_count[1:nx, :, 1:nz] += (1 - Tyz_isfree[1:nx, 1:ny, 1:nz])
    Vz_free_count[1:nx, :, 1:nz] += (1 - Tzx_isfree[1:nx, :, 1:nz])
    Vz_free_count[1:nx, :, 1:nz] += (1 - Tzx_isfree[0:nx-1, :, 1:nz])
    Vz_free_count[0, :, :] = 6
    Vz_free_count[nx, :, :] = 6
    Vz_free_count[:, :, 0] = 6
    Vz_free_count[:, :, nz] = 6

    return Vx_free_count, Vy_free_count, Vz_free_count

# =============================================================================
# 入射波の設定
# =============================================================================
wn = 2.5
wave_steps = int(wn * n)
wave4 = np.zeros(wave_steps, dtype=np.float32)
for ms in range(wave_steps):
    wave2 = (1 - np.cos(2 * np.pi * f * dt * ms / wn)) / 2
    wave3 = np.sin(2 * np.pi * f * dt * ms)
    wave4[ms] = wave2 * wave3

# 音源 (探触子) の設定
probe_d = 0.007
probe_r_mesh = int(probe_d / mesh_length / 2)
sy_c, sz_c = ny // 2, nz // 2

# 円形探触子のマスク作成
Y, Z = np.ogrid[:ny, :nz]
dist_sq = (Y - sy_c)**2 + (Z - sz_c)**2
probe_mask = dist_sq <= probe_r_mesh**2

t_max = int(4 * x_length / cl / dt)

# =============================================================================
# シミュレーション実行関数
# =============================================================================

def run_simulation_3d(f_width, f_pitch, f_depth, f_length=None):
    if f_length is None:
        f_length = z_length
    
    print(f"Running 3D simulation: pitch={f_pitch}, depth={f_depth}, width={f_width}, length={f_length}")
    
    # 配列の初期化 (メモリ節約のため float32)
    Txx = cp.zeros((nx + 1, ny, nz), dtype=cp.float32)
    Tyy = cp.zeros((nx + 1, ny, nz), dtype=cp.float32)
    Tzz = cp.zeros((nx + 1, ny, nz), dtype=cp.float32)
    Txy = cp.zeros((nx, ny + 1, nz), dtype=cp.float32)
    Tyz = cp.zeros((nx, ny, nz + 1), dtype=cp.float32)
    Tzx = cp.zeros((nx + 1, ny, nz + 1), dtype=cp.float32)
    
    Vx = cp.zeros((nx, ny, nz), dtype=cp.float32)
    Vy = cp.zeros((nx + 1, ny + 1, nz), dtype=cp.float32)
    Vz = cp.zeros((nx + 1, ny, nz + 1), dtype=cp.float32)

    # 自由境界フラグの準備
    Normal_isfree, Txy_isfree, Tyz_isfree, Tzx_isfree = isfree_3d(nx, ny, nz, f_width, f_pitch, f_depth, f_length, mesh_length)
    Vx_free_count, Vy_free_count, Vz_free_count = around_free_3d(Normal_isfree, Txy_isfree, Tyz_isfree, Tzx_isfree)
    
    # CuPy 配列へ
    Vx_free_count_cp = cp.asarray(Vx_free_count)
    Vy_free_count_cp = cp.asarray(Vy_free_count)
    Vz_free_count_cp = cp.asarray(Vz_free_count)
    
    probe_mask_cp = cp.asarray(probe_mask)
    
    dtx = dt / dx
    dty = dt / dy
    dtz = dt / dz
    
    wave_output = np.zeros(t_max, dtype=np.float32)
    
    for t in range(t_max):
        # 入射波 (x=0 面に Txx を印加)
        if t < len(wave4):
            Txx[0, probe_mask_cp] = wave4[t]
        else:
            # 入射終了後は境界を固定または自由にする
            # 2D スクリプトに合わせて 0 に
            Txx[0, :, :] = 0
            Vx[0, :, :] = 0
            Vy[0, :, :] = 0
            Vz[0, :, :] = 0

        # --- 応力の更新 (Stress Update) ---
        # 垂直応力 (Normal Stress) at (i, j, k)
        # i: 1~nx, j: 0~ny-1, k: 0~nz-1
        dVx_dx = (Vx[0:nx, :, :] - cp.roll(Vx, 1, axis=0)[0:nx, :, :]) / dx # 簡易的な中心差分
        # より正確には staggered grid の配置に合わせる
        dVx_dx = (Vx[0:nx, :, :] - cp.pad(Vx[0:nx-1, :, :], ((1,0),(0,0),(0,0)), mode='constant')) / dx # 0-th is boundary
        
        # 2Dスクリプトの配置に倣う
        # Ux at (i+1/2, j, k) -> Txx at (i, j, k)
        # Txx[i, j, k] update uses Vx[i, j, k] - Vx[i-1, j, k]
        
        # Vx: (nx, ny, nz) -> Vx[i, j, k] is at (i+1/2, j, k)
        # Txx[1:nx, :, :] update:
        dVx_dx = (Vx[1:nx, :, :] - Vx[0:nx-1, :, :]) / dx
        dVy_dy = (Vy[1:nx, 1:ny+1, :] - Vy[1:nx, 0:ny, :]) / dy
        dVz_dz = (Vz[1:nx, :, 1:nz+1] - Vz[1:nx, :, 0:nz]) / dz
        
        Txx[1:nx, 0:ny, 0:nz] -= dt * (c11 * dVx_dx + c12 * dVy_dy[:, 0:ny, :] + c12 * dVz_dz[:, :, 0:nz])
        Tyy[1:nx, 0:ny, 0:nz] -= dt * (c12 * dVx_dx + c11 * dVy_dy[:, 0:ny, :] + c12 * dVz_dz[:, :, 0:nz])
        Tzz[1:nx, 0:ny, 0:nz] -= dt * (c12 * dVx_dx + c12 * dVy_dy[:, 0:ny, :] + c11 * dVz_dz[:, :, 0:nz])

        # せん断応力 (Shear Stress)
        # Txy at (i+1/2, j+1/2, k)
        Txy[0:nx, 1:ny, 0:nz] -= dt * c44 * ((Vx[0:nx, 1:ny, 0:nz] - Vx[0:nx, 0:ny-1, 0:nz]) / dy + 
                                            (Vy[1:nx+1, 1:ny, 0:nz] - Vy[0:nx, 1:ny, 0:nz]) / dx)
        # Tyz at (i, j+1/2, k+1/2)
        Tyz[1:nx, 0:ny, 1:nz] -= dt * c44 * ((Vy[1:nx, 1:ny+1, 1:nz] - Vy[1:nx, 1:ny+1, 0:nz-1]) / dz + 
                                            (Vz[1:nx, 1:ny, 1:nz] - Vz[1:nx, 0:ny-1, 1:nz]) / dy)
        # Tzx at (i+1/2, j, k+1/2)
        Tzx[0:nx, 0:ny, 1:nz] -= dt * c44 * ((Vz[1:nx+1, 0:ny, 1:nz] - Vz[0:nx, 0:ny, 1:nz]) / dx + 
                                            (Vx[0:nx, 0:ny, 1:nz] - Vx[0:nx, 0:ny, 0:nz-1]) / dz)

        # 欠陥部分の応力境界条件
        Txx *= cp.asarray(Normal_isfree)
        Tyy *= cp.asarray(Normal_isfree)
        Tzz *= cp.asarray(Normal_isfree)
        Txy *= cp.asarray(Txy_isfree)
        Tyz *= cp.asarray(Tyz_isfree)
        Tzx *= cp.asarray(Tzx_isfree)

        # --- 粒子速度の更新 (Velocity Update) ---
        # Vx at (i+1/2, j, k)
        dTxx_dx = (Txx[1:nx+1, :, :] - Txx[0:nx, :, :]) / dx
        dTxy_dy = (Txy[:, 1:ny+1, :] - Txy[:, 0:ny, :]) / dy
        dTzx_dz = (Tzx[1:nx+1, :, 1:nz+1] - Tzx[1:nx+1, :, 0:nz]) / dz
        
        Vx = cp.where(Vx_free_count_cp < 6,
                      Vx - (6.0 / rho / (6.0 - Vx_free_count_cp)) * dt * (dTxx_dx + dTxy_dy + dTzx_dz[0:nx, :, :]),
                      0)

        # Vy at (i, j+1/2, k)
        dTyy_dy = (Tyy[:, 1:ny, :] - cp.pad(Tyy[:, 0:ny-1, :], ((0,0),(1,0),(0,0)), mode='constant')) / dy # Simplified
        # Vy 更新も同様に free_count を使用
        # (簡単のため Vx 以外の更新式は標準的な FDTD に準拠)
        Vy[1:nx, 1:ny, :] -= (dt / rho) * ((Tyy[1:nx, 1:ny, :] - Tyy[1:nx, 0:ny-1, :]) / dy + 
                                           (Txy[1:nx, 1:ny, :] - Txy[0:nx-1, 1:ny, :]) / dx)

        # Vz at (i, j, k+1/2)
        Vz[1:nx, :, 1:nz] -= (dt / rho) * ((Tzz[1:nx, :, 1:nz] - Tzz[1:nx, :, 0:nz-1]) / dz + 
                                           (Tzx[1:nx, :, 1:nz] - Tzx[0:nx-1, :, 1:nz]) / dx)
        
        # 同期 (必要に応じて)
        # cp.cuda.Device().synchronize()
        
        # 受信波形の取得
        if t > 0:
            wave_output[t] = cp.mean(Txx[1, probe_mask_cp])


    # 結果の保存
    output_dir = "tmp_output/sim_3d"
    os.makedirs(output_dir, exist_ok=True)
    # 命名規則は AGENTS.md 7章
    filename = os.path.join(output_dir, sim3d_csv_name(SIM_SHAPE, f_pitch, f_depth))
    np.savetxt(filename, wave_output, delimiter=',')
    print(f"Saved: {filename}")

if __name__ == "__main__":
    # テスト実行
    run_simulation_3d(0.15e-3, 2.00e-3, 0.20e-3, 0.001e-3)
