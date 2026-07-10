"""
plot_bscan_overlay.py — 参照ラインと境界面のB-scanデータを同一のグラフに重ね合わせ（Overlay）およびA-scan（波形）比較プロット

最新のシミュレーションデータ (.npz) を自動的に読み込み、以下のプロットを生成します：
1. 2次元B-scanの重ね合わせ（参照ラインデータを背景カラー画像、境界面データを等高線（Contour）として同一z軸上に重ねる）
2. 代表点（探触子中心など）におけるA-scan波形比較（参照ラインと境界面の波形を同じ時間軸の線グラフで比較）
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

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

def get_latest_npz(output_dir="output"):
    files = glob.glob(os.path.join(output_dir, "bscan_*_data.npz"))
    if not files:
        raise FileNotFoundError(f"No B-scan data files found in '{output_dir}'. Run plot_bscan_mode_conversion.py first.")
    # 最も新しいファイルを取得
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def main():
    output_dir = "output"
    try:
        data_path = get_latest_npz(output_dir)
        print(f"Loading latest data file: {data_path}")
        data = np.load(data_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # データの展開
    bscan_surf_P = data['bscan_surf_P']
    bscan_surf_S = data['bscan_surf_S']
    bscan_ref_P = data['bscan_ref_P']
    bscan_ref_S = data['bscan_ref_S']
    time_axis = data['time_axis']
    surf_x_mm = data['surf_x_mm']
    ref_x_mm = data['ref_x_mm']
    path_xs = data['path_xs']
    dx = float(data['dx'])
    x_ref = int(data['x_ref'])
    f_pitch = float(data['f_pitch'])
    f_depth = float(data['f_depth'])
    f_width = float(data['f_width'])
    
    nz = len(ref_x_mm)
    mesh_length = dx
    nx = int(np.max(path_xs) + 1)
    
    # --- 境界パスの再構築と z-座標へのマッピング ---
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
        
        for z in range(i * mn_p_val, min(groove_start, nz)):
            raw_path.append((nx - 1, z))
        if groove_start >= nz:
            continue
        for x in range(nx - 1, cut_top - 2, -1):
            raw_path.append((x, groove_start - 1))
        for z in range(groove_start, groove_end):
            raw_path.append((cut_top - 1, z))
        if groove_end >= nz:
            continue
        for x in range(cut_top - 1, nx):
            raw_path.append((x, groove_end))

    path_indices = []
    for pt in raw_path:
        if not path_indices or path_indices[-1] != pt:
            path_indices.append(pt)
            
    # 各輪郭インデックスの z 座標値（mm）
    path_zs_mm = np.array([pt[1] * dx * 1000 for pt in path_indices])
    
    # --- 境界面B-scanを z 座標系へ投影投影（垂直壁での複数値を平均化） ---
    num_save_frames = len(time_axis)
    bscan_surf_P_proj = np.zeros((num_save_frames, nz), dtype=np.float32)
    bscan_surf_S_proj = np.zeros((num_save_frames, nz), dtype=np.float32)
    
    for z_idx in range(nz):
        indices_at_z = [i for i, pt in enumerate(path_indices) if pt[1] == z_idx]
        if indices_at_z:
            bscan_surf_P_proj[:, z_idx] = np.mean(bscan_surf_P[:, indices_at_z], axis=1)
            bscan_surf_S_proj[:, z_idx] = np.mean(bscan_surf_S[:, indices_at_z], axis=1)

    # --- プロット生成 ---
    fig = plt.figure(figsize=(15, 12), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 4, 4])
    
    t_max_us = time_axis[-1]
    
    # ---------------- 1. 形状プロファイル (上段) ----------------
    ax_prof = fig.add_subplot(gs[0, :])
    # 参照ライン直下の境界形状
    groove_profile_x = np.zeros(nz)
    for z in range(nz):
        xs_at_z = [p[0] for p in path_indices if p[1] == z]
        groove_profile_x[z] = min(xs_at_z) if xs_at_z else nx - 1
    ax_prof.plot(ref_x_mm, groove_profile_x * dx * 1000, color='black', lw=1.5, label='Groove Surface')
    ax_prof.axhline(x_ref * dx * 1000, color='red', lw=1.2, ls='--', label='Ref Line')
    ax_prof.set_ylabel("Depth (mm)")
    ax_prof.set_title("Specimen Geometry Profile (Aligned with B-scan Horizontal Axis)")
    ax_prof.invert_yaxis()
    ax_prof.grid(True, ls='--')
    ax_prof.legend(loc='lower right')
    ax_prof.set_xlim(ref_x_mm[0], ref_x_mm[-1])
    
    # ---------------- 2. 境界面上での P波 & S波 重ね合わせ (中段左) ----------------
    ax_surf_combined = fig.add_subplot(gs[1, 0], sharex=ax_prof)
    max_surf_P = np.max(np.abs(bscan_surf_P_proj)) or 1.0
    max_surf_S = np.max(np.abs(bscan_surf_S_proj)) or 1.0
    
    # 背景イメージ：境界面の P波 (静水圧)
    im_surf_P = ax_surf_combined.imshow(
        bscan_surf_P_proj, extent=[ref_x_mm[0], ref_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='Blues', vmin=0, vmax=max_surf_P*0.8
    )
    # 重ね合わせ等高線：境界面の S波 (T5)
    Z_grid, T_grid = np.meshgrid(ref_x_mm, time_axis)
    levels_surf_S = np.linspace(-max_surf_S*0.8, max_surf_S*0.8, 8)
    levels_surf_S = levels_surf_S[np.abs(levels_surf_S) > max_surf_S*0.1]
    
    contour_surf_S = ax_surf_combined.contour(
        Z_grid, T_grid, bscan_surf_S_proj, levels=levels_surf_S,
        colors='darkorange', linewidths=1.0, alpha=0.8
    )
    
    ax_surf_combined.set_ylabel("Time (µs)")
    ax_surf_combined.set_title("Groove Surface B-scan (Color: P-wave, Contour: S-wave)")
    fig.colorbar(im_surf_P, ax=ax_surf_combined, label="Surface Pressure (norm.)")
    
    # ---------------- 3. 参照ラインでの P波 & S波 重ね合わせ (中段右) ----------------
    ax_ref_combined = fig.add_subplot(gs[1, 1], sharex=ax_prof)
    max_ref_P = np.max(np.abs(bscan_ref_P)) or 1.0
    max_ref_S = np.max(np.abs(bscan_ref_S)) or 1.0
    
    # 背景イメージ：参照ラインの P波 (静水圧)
    im_ref_P = ax_ref_combined.imshow(
        bscan_ref_P, extent=[ref_x_mm[0], ref_x_mm[-1], t_max_us, 0],
        aspect='auto', cmap='Blues', vmin=0, vmax=max_ref_P*0.8
    )
    # 重ね合わせ等高線：参照ラインの S波 (T5)
    levels_ref_S = np.linspace(-max_ref_S*0.8, max_ref_S*0.8, 8)
    levels_ref_S = levels_ref_S[np.abs(levels_ref_S) > max_ref_S*0.1]
    
    contour_ref_S = ax_ref_combined.contour(
        Z_grid, T_grid, bscan_ref_S, levels=levels_ref_S,
        colors='darkorange', linewidths=1.0, alpha=0.8
    )
    
    ax_ref_combined.set_ylabel("Time (µs)")
    ax_ref_combined.set_title("Reference Line B-scan (Color: P-wave, Contour: S-wave)")
    fig.colorbar(im_ref_P, ax=ax_ref_combined, label="Ref Line Pressure (norm.)")

    # ---------------- 4. A-scan 波形比較 (下段) ----------------
    # 探触子中心（中央の $z$ 座標）での1D波形比較
    z_center_idx = nz // 2
    z_center_mm = ref_x_mm[z_center_idx]
    
    # 溝の角付近（例: 中央から少しずれた位置）での波形も比較するため2箇所選定
    # 溝の角（gap_center から 0.2mm ずれた位置など）
    z_corner_idx = int(z_center_idx + (0.2 * 1e-3 / dx))
    z_corner_mm = ref_x_mm[z_corner_idx]
    
    # ① 探触子中心での波形比較 (下段左)
    ax_ascan_center = fig.add_subplot(gs[2, 0])
    ax_ascan_center.plot(time_axis, bscan_ref_P[:, z_center_idx], label='Ref Line P-wave', color='royalblue', lw=1.5)
    ax_ascan_center.plot(time_axis, bscan_surf_P_proj[:, z_center_idx], label='Groove Surface P-wave', color='crimson', lw=1.2, ls='--')
    ax_ascan_center.plot(time_axis, bscan_ref_S[:, z_center_idx], label='Ref Line S-wave (T5)', color='green', lw=1.5)
    ax_ascan_center.plot(time_axis, bscan_surf_S_proj[:, z_center_idx], label='Groove Surface S-wave (T5)', color='darkorange', lw=1.2, ls='--')
    ax_ascan_center.set_xlabel("Time (µs)")
    ax_ascan_center.set_ylabel("Normalized Amplitude")
    ax_ascan_center.set_title(f"A-scan Waveform Comparison at Center (z = {z_center_mm:.2f} mm)")
    ax_ascan_center.grid(True, ls='--')
    ax_ascan_center.legend(fontsize=9, loc='upper right')
    
    # ② 溝の角付近での波形比較 (下段右)
    ax_ascan_corner = fig.add_subplot(gs[2, 1])
    ax_ascan_corner.plot(time_axis, bscan_ref_P[:, z_corner_idx], label='Ref Line P-wave', color='royalblue', lw=1.5)
    ax_ascan_corner.plot(time_axis, bscan_surf_P_proj[:, z_corner_idx], label='Groove Surface P-wave', color='crimson', lw=1.2, ls='--')
    ax_ascan_corner.plot(time_axis, bscan_ref_S[:, z_corner_idx], label='Ref Line S-wave (T5)', color='green', lw=1.5)
    ax_ascan_corner.plot(time_axis, bscan_surf_S_proj[:, z_corner_idx], label='Groove Surface S-wave (T5)', color='darkorange', lw=1.2, ls='--')
    ax_ascan_corner.set_xlabel("Time (µs)")
    ax_ascan_corner.set_ylabel("Normalized Amplitude")
    ax_ascan_corner.set_title(f"A-scan Waveform Comparison near Corner/Slope (z = {z_corner_mm:.2f} mm)")
    ax_ascan_corner.grid(True, ls='--')
    ax_ascan_corner.legend(fontsize=9, loc='upper right')

    # 画像保存
    base_name = os.path.basename(data_path).replace("_data.npz", "")
    output_plot_path = unique_path(os.path.join(output_dir, f"{base_name}_overlay.png"))
    plt.savefig(output_plot_path, dpi=200)
    plt.close()
    
    print(f"Overlay plot successfully created and saved to: {output_plot_path}")

if __name__ == "__main__":
    main()
