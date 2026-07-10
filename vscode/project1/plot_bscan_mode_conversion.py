"""
plot_bscan_mode_conversion.py — 境界面におけるモード変換の時空間クロスセクション（B-scan）可視化

FDTDシミュレーションを実行し、以下の2つのラインにおける縦波（圧力 P = -(T1+T3)/2）および横波（せん断応力 T5）のB-scanをプロットします：
1. 矩形溝の凹凸に沿った境界パス（境界での直接的なモード変換と表面波の伝搬）
2. 境界面の少し上に位置する平坦な参照ライン（入射波と、反射・モード変換されて戻る波の分離）
"""

import os
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

# CuPy と NumPy のフォールバック設定
try:
    import cupy as cp
    use_gpu = True
    print("Using GPU (CuPy)")
except ImportError:
    import numpy as cp
    use_gpu = False
    print("Using CPU (NumPy)")

def to_np(arr):
    if use_gpu:
        return cp.asnumpy(arr)
    return arr

def unique_path(path: str) -> str:
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(path)
    k = 2
    while True:
        cand = f"{root}_v{k}{ext}"
        if not os.path.exists(cand):
            return cand
        k += 1

def build_kukei_masks(nx, nz, f_width, f_pitch, f_depth, mesh_length):
    """矩形溝の自由境界マスクを生成"""
    mn_w   = max(1, int(round(f_width  / mesh_length)))
    mn_p   = max(mn_w + 1, int(round(f_pitch  / mesh_length)))
    mn_gap = mn_p - mn_w
    mn_d   = max(1, int(round(f_depth  / mesh_length)))

    if mn_w >= mn_p:
        raise ValueError("f_width を f_pitch より小さくしてください。")

    t13_isfree = np.ones((nx + 1, nz), dtype=np.float32)
    t5_isfree  = np.ones((nx,     nz + 1), dtype=np.float32)

    t13_isfree[0,  :] = 0.0
    t13_isfree[nx, :] = 0.0
    t5_isfree[:,   0] = 0.0
    t5_isfree[:,  nz] = 0.0

    cut_top   = max(0, nx - mn_d)
    num_pitch = int(np.ceil(nz / mn_p))

    for i in range(num_pitch):
        groove_start = i * mn_p + mn_gap
        groove_end   = min(i * mn_p + mn_p, nz)
        if groove_start >= nz or groove_end <= groove_start:
            continue
        t5_isfree[cut_top:nx, groove_start:groove_end] = 0.0
        t13_end = max(groove_start, groove_end - 1)
        if t13_end > groove_start:
            t13_isfree[cut_top:nx + 1, groove_start:t13_end] = 0.0

    return t13_isfree, t5_isfree

def around_free_vectorized(t13_isfree, t5_isfree, nx, nz):
    """自由境界近傍のカウント"""
    ux_free_count = (
        (t13_isfree[0:nx,   :] == 0).astype(np.float32)
        + (t13_isfree[1:nx+1, :] == 0).astype(np.float32)
        + (t5_isfree[:,  0:nz]  == 0).astype(np.float32)
        + (t5_isfree[:, 1:nz+1] == 0).astype(np.float32)
    )

    uz_free_count = np.zeros((nx + 1, nz + 1), dtype=np.float32)
    bd = np.zeros_like(uz_free_count, dtype=bool)
    bd[0, :] = True; bd[nx, :] = True
    bd[:, 0] = True; bd[:,  nz] = True
    uz_free_count[bd] += 1.0

    uz_free_count[:,   1:] += (t13_isfree == 0)
    uz_free_count[:,  :nz] += (t13_isfree == 0)
    uz_free_count[1:,   :] += (t5_isfree  == 0)
    uz_free_count[:nx,  :] += (t5_isfree  == 0)

    d1 = np.ones_like(uz_free_count, dtype=bool); d1[:,  1:] = (t13_isfree == 0)
    d2 = np.ones_like(uz_free_count, dtype=bool); d2[:, :nz] = (t13_isfree == 0)
    d3 = np.ones_like(uz_free_count, dtype=bool); d3[1:,  :] = (t5_isfree  == 0)
    d4 = np.ones_like(uz_free_count, dtype=bool); d4[:nx, :] = (t5_isfree  == 0)
    uz_free_count[d1 & d2 & d3 & d4] = 4.0

    return ux_free_count, uz_free_count

def parse_args():
    parser = argparse.ArgumentParser(description="Mode conversion B-scan visualization.")
    parser.add_argument("--pitch-mm", type=float, default=2.00, help="Groove pitch in mm")
    parser.add_argument("--depth-mm", type=float, default=0.15, help="Groove depth in mm")
    parser.add_argument("--width-mm", type=float, default=0.40, help="Groove width in mm")
    parser.add_argument("--probe-width-mm", type=float, default=7.00, help="Probe aperture in mm")
    parser.add_argument("--x-length-mm", type=float, default=6.00, help="Specimen height in mm")
    parser.add_argument("--z-length-mm", type=float, default=20.00, help="Specimen width in mm")
    parser.add_argument("--save-interval", type=int, default=2, help="Temporal sampling interval for B-scan")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--t-max-factor", type=float, default=2.0, help="Factor to calculate simulation duration (duration = factor * travel_time)")
    parser.add_argument("--show", action="store_true", help="Display plot window after simulation")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # パラメータ設定
    f_pitch = args.pitch_mm * 1e-3
    f_depth = args.depth_mm * 1e-3
    f_width = args.width_mm * 1e-3
    probe_d = args.probe_width_mm * 1e-3
    x_length = args.x_length_mm * 1e-3
    z_length = args.z_length_mm * 1e-3
    save_interval = args.save_interval
    output_dir = args.output_dir
    
    mesh_length = 1.0e-5  # 10 um
    nx = int(round(x_length / mesh_length))
    nz = int(round(z_length / mesh_length))
    dx = x_length / nx
    dz = z_length / nz
    
    # 物理パラメータ
    rho = 7840
    E   = 206e9
    G   = 80e9
    V   = 0.27
    cl  = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))
    c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
    c13 = E * V       / (1 + V) / (1 - 2 * V)
    c55 = (c11 - c13) / 2
    dt  = (dx / cl / np.sqrt(6)) / 4
    
    f_freq = 4.7e6
    
    # シミュレーションステップ数設定 (P波が往復する時間 + アルファ)
    t_max_steps = int(args.t_max_factor * x_length / cl / dt)
    
    print(f"--- Simulation Setup ---")
    print(f"Specimen Size : Height={args.x_length_mm:.2f}mm, Width={args.z_length_mm:.2f}mm")
    print(f"Groove Params : Pitch={args.pitch_mm:.3f}mm, Depth={args.depth_mm:.3f}mm, Width={args.width_mm:.3f}mm")
    print(f"Grid Size     : nx={nx}, nz={nz} (mesh={mesh_length*1e6:.1f}um)")
    print(f"Time Step     : dt={dt*1e9:.3f}ns (Total Steps={t_max_steps})")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # --- マスク生成 ---
    t13_isfree_np, t5_isfree_np = build_kukei_masks(nx, nz, f_width, f_pitch, f_depth, mesh_length)
    ux_free_np,   uz_free_np   = around_free_vectorized(t13_isfree_np, t5_isfree_np, nx, nz)
    
    T13_isfree  = cp.asarray(t13_isfree_np)
    T5_isfree   = cp.asarray(t5_isfree_np)
    Ux_free_cnt = cp.asarray(ux_free_np)
    Uz_free_cnt = cp.asarray(uz_free_np)
    
    # --- 境界パス（凹凸に沿う表面）のインデックス生成 ---
    mn_p_val   = int(round(f_pitch / mesh_length))
    mn_w_val   = int(round(f_width  / mesh_length))
    mn_gap_val = mn_p_val - mn_w_val
    mn_d_val   = int(round(f_depth  / mesh_length))
    cut_top    = max(0, nx - mn_d_val)
    num_pitch  = int(np.ceil(nz / mn_p_val))
    
    raw_path = []
    for i in range(num_pitch):
        groove_start = i * mn_p_val + mn_gap_val
        groove_end   = min(i * mn_p_val + mn_p_val, nz)
        
        # 1. 底面平坦部 (左)
        for z in range(i * mn_p_val, min(groove_start, nz)):
            raw_path.append((nx - 1, z))
            
        if groove_start >= nz:
            continue
            
        # 2. 左壁 (上る)
        for x in range(nx - 1, cut_top - 2, -1):
            raw_path.append((x, groove_start - 1))
            
        # 3. 溝の底 (最奥)
        for z in range(groove_start, groove_end):
            raw_path.append((cut_top - 1, z))
            
        if groove_end >= nz:
            continue
            
        # 4. 右壁 (下る)
        for x in range(cut_top - 1, nx):
            raw_path.append((x, groove_end))

    # 重複する隣接点をユニーク化
    path_indices = []
    for pt in raw_path:
        if not path_indices or path_indices[-1] != pt:
            path_indices.append(pt)
            
    # 累積物理距離の計算
    path_distances = [0.0]
    total_dist = 0.0
    for idx in range(1, len(path_indices)):
        p1 = path_indices[idx - 1]
        p2 = path_indices[idx]
        dist = np.sqrt(((p2[0] - p1[0]) * dx) ** 2 + ((p2[1] - p1[1]) * dz) ** 2)
        total_dist += dist
        path_distances.append(total_dist)
    path_distances = np.array(path_distances)
    
    # 境界パス座標をGPU/CPU用に配列化
    path_xs_cp = cp.array([p[0] for p in path_indices])
    path_zs_cp = cp.array([p[1] for p in path_indices])
    
    # --- 平坦参照ラインのインデックス生成 (溝の最深部より4メッシュ上) ---
    x_ref = cut_top - 4
    if x_ref < 0:
        raise ValueError("x-length-mm is too small relative to depth-mm.")
    ref_zs_cp = cp.arange(nz)
    ref_xs_cp = cp.full(nz, x_ref)
    ref_distances = np.arange(nz) * dz
    
    # B-scanデータ記録用配列
    num_save_frames = int(np.ceil(t_max_steps / save_interval))
    
    # 1. 境界パス上のデータ
    bscan_surf_P = np.zeros((num_save_frames, len(path_indices)), dtype=np.float32)
    bscan_surf_S = np.zeros((num_save_frames, len(path_indices)), dtype=np.float32)
    
    # 2. 参照ライン上のデータ
    bscan_ref_P = np.zeros((num_save_frames, nz), dtype=np.float32)
    bscan_ref_S = np.zeros((num_save_frames, nz), dtype=np.float32)
    
    # --- FDTD 配列確保 ---
    T1 = cp.zeros((nx + 1, nz),     dtype=cp.float32)
    T3 = cp.zeros((nx + 1, nz),     dtype=cp.float32)
    T5 = cp.zeros((nx,     nz + 1), dtype=cp.float32)
    Ux = cp.zeros((nx,     nz),     dtype=cp.float32)
    Uz = cp.zeros((nx + 1, nz + 1), dtype=cp.float32)
    
    dtx = dt / dx
    dtz = dt / dz
    
    # --- 入射波形生成 ---
    wn = 2.5
    n_period = (1.0 / f_freq) / dt
    wave4 = np.zeros(int(wn * n_period), dtype=float)
    for ms in range(len(wave4)):
        wave4[ms] = (
            (1 - np.cos(2 * np.pi * f_freq * dt * ms / wn)) / 2
            * np.sin(2 * np.pi * f_freq * dt * ms)
        )
        
    # --- 探触子セル範囲計算 ---
    sz = nz // 2
    probe_cells = max(1, min(nz, int(round(probe_d / mesh_length))))
    sz_l = max(0, sz - probe_cells // 2)
    sz_r = min(nz, sz_l + probe_cells)
    
    # --- シミュレーションループ ---
    start_time = time.time()
    print("Running Simulation & extracting B-scans...")
    
    for t_i in range(t_max_steps):
        if t_i % 500 == 0:
            print(f"Step {t_i}/{t_max_steps} ({t_i / t_max_steps:.1%})")
            
        # 境界条件
        T5[:nx, 0] = 0.0;  T5[:nx, nz] = 0.0
        T3[0,  :] = 0.0;   T3[nx,  :] = 0.0
        T1[nx, :] = 0.0
        T1[0, 0] = 0.0; T3[0, 0] = 0.0; T5[0, 0] = 0.0
        
        Uz[1:nx, 0]  -= (4.0 / rho) * dtx *   T3[1:nx, 0]
        Uz[1:nx, nz] -= (4.0 / rho) * dtx * (-T3[1:nx, nz - 1])
        Uz[nx, 1:nz] -= (4.0 / rho) * dtx * (-T5[nx - 1, 1:nz])
        
        T1[1:nx, :] -= dtx * (c11 * (Ux[1:nx, :] - Ux[0:nx-1, :])
                               + c13 * (Uz[1:nx, 1:] - Uz[1:nx, :-1]))
        T3[1:nx, :] -= dtx * (c13 * (Ux[1:nx, :] - Ux[0:nx-1, :])
                               + c11 * (Uz[1:nx, 1:] - Uz[1:nx, :-1]))
        T5[:, 1:nz] -= dtx * c55 * (Ux[:, 1:] - Ux[:, :-1]
                                     + Uz[1:, 1:nz] - Uz[:-1, 1:nz])
        
        T1[T13_isfree == 0] = 0.0
        T3[T13_isfree == 0] = 0.0
        T5[T5_isfree[:nx, :] == 0] = 0.0
        
        if t_i < len(wave4):
            T1[0, sz_l:sz_r] = wave4[t_i]
        else:
            Uz[0, sz_l:sz_r] = 0.0
            Ux[0, sz_l:sz_r] = 0.0
            T1[0, :] = 0.0
            T5[0, :] = 0.0
            
        # ゼロ除算警告（RuntimeWarning）を回避するため、分母が0になる部分をダミー値（1.0）にする安全な除算用配列を作成
        denom_ux = 4.0 - Ux_free_cnt
        denom_ux_safe = cp.where(denom_ux == 0, 1.0, denom_ux)
        Ux[:nx, :nz] = cp.where(
            Ux_free_cnt < 4.0,
            Ux - (4.0 / rho / denom_ux_safe) * dtx
            * (T1[1:nx+1, :] - T1[:nx, :] + T5[:, 1:nz+1] - T5[:, :nz]),
            0.0,
        )
        
        denom_uz = 4.0 - Uz_free_cnt[1:nx, 1:nz]
        denom_uz_safe = cp.where(denom_uz == 0, 1.0, denom_uz)
        Uz[1:nx, 1:nz] = cp.where(
            Uz_free_cnt[1:nx, 1:nz] < 4.0,
            Uz[1:nx, 1:nz] - (4.0 / rho / denom_uz_safe) * dtz
            * (T3[1:nx, 1:nz] - T3[1:nx, :nz-1]
               + T5[1:nx, 1:nz] - T5[:nx-1, 1:nz]),
            0.0,
        )
        
        # B-scanデータのサンプリング
        if t_i % save_interval == 0:
            frame_idx = t_i // save_interval
            
            # 圧力 P = -(T1+T3)/2 (縦波プロキシ)
            P_cp = -(T1 + T3) / 2.0
            
            # 1. 境界パス上のサンプリング
            P_surf = P_cp[path_xs_cp, path_zs_cp]
            T5_surf = T5[cp.clip(path_xs_cp, 0, nx - 1), cp.clip(path_zs_cp, 0, nz)]
            
            bscan_surf_P[frame_idx] = to_np(P_surf)
            bscan_surf_S[frame_idx] = to_np(T5_surf)
            
            # 2. 平坦参照ライン上のサンプリング
            P_ref = P_cp[ref_xs_cp, ref_zs_cp]
            T5_ref = T5[cp.clip(ref_xs_cp, 0, nx - 1), ref_zs_cp]
            
            bscan_ref_P[frame_idx] = to_np(P_ref)
            bscan_ref_S[frame_idx] = to_np(T5_ref)
            
        if use_gpu and t_i % 1000 == 0:
            cp.cuda.Device().synchronize()
            
    print(f"Simulation completed in {time.time() - start_time:.1f} s")
    
    # --- 可視化プロット生成 ---
    print("Generating B-scan comparison plots...")
    
    t_max_us = (t_max_steps * dt) * 1e6
    time_axis = np.linspace(0, t_max_us, num_save_frames)
    
    # 最大振幅で正規化 (カラーバー範囲調整用)
    max_surf_P = np.max(np.abs(bscan_surf_P)) or 1.0
    max_surf_S = np.max(np.abs(bscan_surf_S)) or 1.0
    max_ref_P  = np.max(np.abs(bscan_ref_P))  or 1.0
    max_ref_S  = np.max(np.abs(bscan_ref_S))  or 1.0
    
    fig = plt.figure(figsize=(14, 10), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 4, 4])
    
    # --- 共通のX軸として距離 (mm) を定義 ---
    surf_x_mm = path_distances * 1000
    ref_x_mm = ref_distances * 1000
    
    # ---------------- 1. 形状プロファイル表示 (最上段) ----------------
    ax_prof_surf = fig.add_subplot(gs[0, 0])
    path_xs_np = to_np(path_xs_cp)
    ax_prof_surf.plot(surf_x_mm, path_xs_np * dx * 1000, color='black', lw=1.5)
    ax_prof_surf.set_ylabel("Depth (mm)")
    ax_prof_surf.set_title("Boundary Contour Profile")
    ax_prof_surf.invert_yaxis()  # 深さ方向を下向きに
    ax_prof_surf.grid(True, ls='--')
    ax_prof_surf.set_xlim(surf_x_mm[0], surf_x_mm[-1])
    
    ax_prof_ref = fig.add_subplot(gs[0, 1])
    # 参照ライン直下の実際の境界形状を参考用にプロット
    groove_profile_x = np.zeros(nz)
    for z in range(nz):
        # z位置における境界のx座標を探す
        xs_at_z = [p[0] for p in path_indices if p[1] == z]
        groove_profile_x[z] = min(xs_at_z) if xs_at_z else nx - 1
    ax_prof_ref.plot(ref_x_mm, groove_profile_x * dx * 1000, color='black', lw=1.5, ls='-')
    ax_prof_ref.axhline(x_ref * dx * 1000, color='red', lw=1.2, ls='--', label='Ref Line')
    ax_prof_ref.set_ylabel("Depth (mm)")
    ax_prof_ref.set_title("Specimen Boundary (with Ref Line Location)")
    ax_prof_ref.invert_yaxis()
    ax_prof_ref.grid(True, ls='--')
    ax_prof_ref.legend(loc='lower right', fontsize=8)
    ax_prof_ref.set_xlim(ref_x_mm[0], ref_x_mm[-1])
    
    # ---------------- 2. 境界パス上の B-scan ----------------
    ax_surf_P = fig.add_subplot(gs[1, 0], sharex=ax_prof_surf)
    im_surf_P = ax_surf_P.imshow(
        bscan_surf_P, extent=[surf_x_mm[0], surf_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='RdBu_r', vmin=-max_surf_P*0.8, vmax=max_surf_P*0.8
    )
    ax_surf_P.set_ylabel("Time (µs)")
    ax_surf_P.set_title("Boundary B-scan: P-wave (Pressure)")
    fig.colorbar(im_surf_P, ax=ax_surf_P, label="Pressure (norm.)")
    
    ax_surf_S = fig.add_subplot(gs[2, 0], sharex=ax_prof_surf)
    im_surf_S = ax_surf_S.imshow(
        bscan_surf_S, extent=[surf_x_mm[0], surf_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='PRGn', vmin=-max_surf_S*0.8, vmax=max_surf_S*0.8
    )
    ax_surf_S.set_xlabel("Contour Position (mm)")
    ax_surf_S.set_ylabel("Time (µs)")
    ax_surf_S.set_title("Boundary B-scan: S-wave (Shear Stress T5)")
    fig.colorbar(im_surf_S, ax=ax_surf_S, label="Stress T5 (norm.)")
    
    # ---------------- 3. 平坦参照ライン上の B-scan ----------------
    ax_ref_P = fig.add_subplot(gs[1, 1], sharex=ax_prof_ref)
    im_ref_P = ax_ref_P.imshow(
        bscan_ref_P, extent=[ref_x_mm[0], ref_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='RdBu_r', vmin=-max_ref_P*0.8, vmax=max_ref_P*0.8
    )
    ax_ref_P.set_ylabel("Time (µs)")
    ax_ref_P.set_title("Reference Line B-scan: P-wave (Pressure)")
    fig.colorbar(im_ref_P, ax=ax_ref_P, label="Pressure (norm.)")
    
    ax_ref_S = fig.add_subplot(gs[2, 1], sharex=ax_prof_ref)
    im_ref_S = ax_ref_S.imshow(
        bscan_ref_S, extent=[ref_x_mm[0], ref_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='PRGn', vmin=-max_ref_S*0.8, vmax=max_ref_S*0.8
    )
    ax_ref_S.set_xlabel("Horizontal Position Z (mm)")
    ax_ref_S.set_ylabel("Time (µs)")
    ax_ref_S.set_title("Reference Line B-scan: S-wave (Shear Stress T5)")
    fig.colorbar(im_ref_S, ax=ax_ref_S, label="Stress T5 (norm.)")
    
    # 保存ファイル名の構築
    base_label = f"bscan_pitch{int(round(f_pitch * 1e5))}_depth{int(round(f_depth * 1e5))}_width{int(round(f_width * 1e5))}"
    plot_path = unique_path(os.path.join(output_dir, f"{base_label}.png"))
    data_path = unique_path(os.path.join(output_dir, f"{base_label}_data.npz"))
    
    plt.savefig(plot_path, dpi=200)
    print(f"B-scan plot saved: {plot_path}")
    
    # データ保存
    np.savez_compressed(
        data_path,
        bscan_surf_P=bscan_surf_P,
        bscan_surf_S=bscan_surf_S,
        bscan_ref_P=bscan_ref_P,
        bscan_ref_S=bscan_ref_S,
        time_axis=time_axis,
        surf_x_mm=surf_x_mm,
        ref_x_mm=ref_x_mm,
        path_xs=path_xs_np,
        dx=dx,
        x_ref=x_ref,
        f_pitch=f_pitch,
        f_depth=f_depth,
        f_width=f_width
    )
    print(f"B-scan data saved: {data_path}")
    
    if args.show:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    main()
