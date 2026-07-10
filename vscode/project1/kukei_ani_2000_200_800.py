"""
kukei_ani.py — 矩形溝 FDTD アニメーション生成・表示

kusabi_ani.py / ushape_ani.py と同形式の NPZ を出力する。
animation_player_for_npz.py でそのまま再生可能。
"""
import numpy as np
import cupy as cp
import os
import argparse
import matplotlib.pyplot as plt
import time
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import animation
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================== 調整パラメータ ==================

DEFAULT_OUTPUT_DIR = "C:\\Users\\cs16\\lab\\vscode\\project1\\output"
DEFAULT_WIDTH_MM = 0.40
DEFAULT_DEPTH_MM = 0.15
DEFAULT_PITCH_MM = 1.25
DEFAULT_PROBE_WIDTH_MM = 7.0
DEFAULT_SAVE_INTERVAL = 10
DEFAULT_GLOBAL_DOWNSAMPLE = 6
DEFAULT_ZOOM_WIDTH_MM = 3.0
DEFAULT_ZOOM_HEIGHT_MM = 0.5


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Generate and view Kukei FDTD animation data."
    )
    parser.add_argument("--pitch-mm", type=float, default=DEFAULT_PITCH_MM)
    parser.add_argument("--depth-mm", type=float, default=DEFAULT_DEPTH_MM)
    parser.add_argument("--width-mm", type=float, default=DEFAULT_WIDTH_MM)
    parser.add_argument("--probe-width-mm", type=float, default=DEFAULT_PROBE_WIDTH_MM)
    parser.add_argument(
        "--probe-full",
        dest="probe_full",
        action="store_true",
        help="Use the full specimen width as probe aperture",
    )
    parser.add_argument(
        "--probe-half",
        dest="probe_half_specimen",
        action="store_true",
        help="Use half the specimen width as probe aperture",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--save-interval", type=int, default=DEFAULT_SAVE_INTERVAL)
    parser.add_argument("--global-downsample", type=int, default=DEFAULT_GLOBAL_DOWNSAMPLE)
    parser.add_argument("--zoom-width-mm", type=float, default=DEFAULT_ZOOM_WIDTH_MM)
    parser.add_argument("--zoom-height-mm", type=float, default=DEFAULT_ZOOM_HEIGHT_MM)
    args, _ = parser.parse_known_args()
    if args.width_mm >= args.pitch_mm:
        parser.error("--width-mm must be smaller than --pitch-mm")
    if args.probe_full and args.probe_half_specimen:
        parser.error("--probe-full and --probe-half cannot be used together")
    if args.save_interval <= 0:
        parser.error("--save-interval must be positive")
    if args.global_downsample <= 0:
        parser.error("--global-downsample must be positive")
    return args


_cli_args = parse_cli_args()

output_dir = _cli_args.output_dir

# 矩形溝パラメータ
f_width = _cli_args.width_mm * 1e-3
f_depth = _cli_args.depth_mm * 1e-3
f_pitch = _cli_args.pitch_mm * 1e-3

# アニメーション保存
save_interval = _cli_args.save_interval
global_downsample = _cli_args.global_downsample

# 拡大表示の設定
zoom_width_mm = _cli_args.zoom_width_mm
zoom_height_mm = _cli_args.zoom_height_mm

# ===================================================


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


def make_base_name(f_pitch_m: float, f_depth_m: float, f_width_m: float, probe_d_m: float,
                   probe_full: bool = False, probe_half_specimen: bool = False) -> str:
    if probe_full:
        psize_label = "psize_full"
    elif probe_half_specimen:
        psize_label = "psize_half"
    else:
        psize_label = f"psize{int(round(probe_d_m * 1e5))}"
    return (
        f"kukei_ani"
        f"_pitch{int(round(f_pitch_m * 1e5))}"
        f"_depth{int(round(f_depth_m * 1e5))}"
        f"_width{int(round(f_width_m * 1e5))}"
        f"_{psize_label}"
    )


# ---------------- 物理パラメータ ----------------
x_length    = 0.02      # [m]
z_length    = 0.04      # [m]
mesh_length = 1.0e-5    # メッシュサイズ [m]

nx = int(round(x_length / mesh_length))
nz = int(round(z_length / mesh_length))
dx = x_length / nx
dz = z_length / nz

rho = 7840
E   = 206e9
G   = 80e9
V   = 0.27
cl  = np.sqrt(E / rho * (1 - V) / (1 + V) / (1 - 2 * V))
c11 = E * (1 - V) / (1 + V) / (1 - 2 * V)
c13 = E * V       / (1 + V) / (1 - 2 * V)
c55 = (c11 - c13) / 2
dt  = (dx / cl / np.sqrt(6)) 

f_freq = 4.7e6

# ---------------- 拡大領域 ROI ----------------
roi_w_idx = int((zoom_width_mm  * 1e-3) / dz)
roi_h_idx = int((zoom_height_mm * 1e-3) / dx)
z_center  = nz // 2
z_start   = max(0,  z_center - roi_w_idx // 2)
z_end     = min(nz, z_center + roi_w_idx // 2)
x_start   = max(0,  nx - roi_h_idx)
x_end     = nx

extent_global = [0, z_length * 1000, x_length * 1000, 0]
zoom_z_min = z_start * dz * 1000
zoom_z_max = z_end   * dz * 1000
zoom_x_min = x_start * dx * 1000
zoom_x_max = x_end   * dx * 1000
extent_zoom = [zoom_z_min, zoom_z_max, zoom_x_max, zoom_x_min]

print(f"ROI Indices: X[{x_start}:{x_end}], Z[{z_start}:{z_end}]")


# ---------------- 矩形溝マスク生成 ----------------
def build_kukei_masks(nx, nz, f_width, f_pitch, f_depth, mesh_length):
    """矩形溝の自由境界マスクを返す。project2 と同じ配置規則を使用。"""
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


# ---------------- 自由境界近傍カウント（ベクトル化版） ----------------
def around_free_vectorized(t13_isfree, t5_isfree, nx, nz):
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


# ---------------- 入射波形 ----------------
wn = 2.5
n_period = (1.0 / f_freq) / dt
wave4 = np.zeros(int(wn * n_period), dtype=float)
for ms in range(len(wave4)):
    wave4[ms] = (
        (1 - np.cos(2 * np.pi * f_freq * dt * ms / wn)) / 2
        * np.sin(2 * np.pi * f_freq * dt * ms)
    )

# ---------------- 探触子設定 ----------------
probe_full = _cli_args.probe_full
probe_half_specimen = _cli_args.probe_half_specimen
if probe_full:
    probe_d = z_length
elif probe_half_specimen:
    probe_d = z_length * 0.5
else:
    probe_d = _cli_args.probe_width_mm * 1e-3  # 探触子開口幅 [m]
sz = nz // 2
probe_cells = max(1, min(nz, int(round(probe_d / mesh_length))))
sz_l = sz - probe_cells // 2
sz_r = sz_l + probe_cells
if sz_l < 0:
    sz_r -= sz_l
    sz_l = 0
if sz_r > nz:
    sz_l = max(0, sz_l - (sz_r - nz))
    sz_r = nz

t_max_steps = int(1.5 * x_length / cl / dt)


# =======================================================================
#               Viewer Class  （kusabi_ani.py と同一インタフェース）
# =======================================================================
class IntegratedViewer:
    def __init__(self, root, g_t1, g_t3, g_t5, z_t1, z_t3, z_t5, time_step, output_dir,
                 extent_global, extent_zoom, roi_rect_mm, base_name,
                 mask_matrix=None, probe_z_l_mm=None, probe_z_r_mm=None,
                 probe_center_mm=None, gap_center_mm=None):
        self.root = root

        max_t1 = np.max(np.abs(g_t1))
        self.g_t1 = g_t1 / max_t1 if max_t1 > 1e-12 else g_t1
        self.z_t1 = z_t1 / max_t1 if max_t1 > 1e-12 else z_t1

        max_t3 = np.max(np.abs(g_t3))
        self.g_t3 = g_t3 / max_t3 if max_t3 > 1e-12 else g_t3
        self.z_t3 = z_t3 / max_t3 if max_t3 > 1e-12 else z_t3

        max_t5 = np.max(np.abs(g_t5))
        self.g_t5 = g_t5 / max_t5 if max_t5 > 1e-12 else g_t5
        self.z_t5 = z_t5 / max_t5 if max_t5 > 1e-12 else z_t5

        self.time_step    = time_step
        self.output_dir   = output_dir
        self.base_name    = base_name
        self.extent_global = extent_global
        self.extent_zoom  = extent_zoom
        self.roi_rect_mm  = roi_rect_mm
        self.mask_matrix  = mask_matrix
        self.probe_z_l_mm   = probe_z_l_mm
        self.probe_z_r_mm   = probe_z_r_mm
        self.probe_center_mm = probe_center_mm
        self.gap_center_mm   = gap_center_mm

        os.makedirs(self.output_dir, exist_ok=True)
        self.n_frames    = self.g_t1.shape[0]
        self.play_running = False
        self.play_job    = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Kukei Simulation Viewer")
        self.root.geometry("1200x800")

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True)

        self.fig = plt.Figure(figsize=(13, 7), dpi=100, layout="constrained")
        gs = self.fig.add_gridspec(2, 3)

        self.ax_g1 = self.fig.add_subplot(gs[0, 0])
        self.ax_g3 = self.fig.add_subplot(gs[0, 1])
        self.ax_g5 = self.fig.add_subplot(gs[0, 2])
        self.ax_z1 = self.fig.add_subplot(gs[1, 0])
        self.ax_z3 = self.fig.add_subplot(gs[1, 1])
        self.ax_z5 = self.fig.add_subplot(gs[1, 2])

        vmin, vmax = -1.0, 1.0

        self.im_g1 = self.ax_g1.imshow(
            self.g_t1[0], cmap="viridis", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="nearest", extent=self.extent_global)
        self.ax_g1.set_title("Global T1"); self.ax_g1.set_ylabel("Depth X (mm)")
        self._add_roi_rect(self.ax_g1)
        self._draw_outline(self.ax_g1, is_zoom=False)

        self.im_g3 = self.ax_g3.imshow(
            self.g_t3[0], cmap="viridis", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="nearest", extent=self.extent_global)
        self.ax_g3.set_title("Global T3")
        self._add_roi_rect(self.ax_g3)
        self._draw_outline(self.ax_g3, is_zoom=False)

        self.im_g5 = self.ax_g5.imshow(
            self.g_t5[0], cmap="viridis", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="nearest", extent=self.extent_global)
        self.ax_g5.set_title("Global T5")
        self._add_roi_rect(self.ax_g5)
        self._draw_outline(self.ax_g5, is_zoom=False)

        # 探触子枠（Global ビューの表面に黄色の矩形で表示）
        _pz_l_mm  = sz_l  * dz * 1000
        _pz_r_mm  = sz_r  * dz * 1000
        _probe_h  = x_length * 1000 * 0.05  # 試験体高さの 5% を視覚的な高さとして使用
        for _ax in (self.ax_g1, self.ax_g3, self.ax_g5):
            _ax.add_patch(Rectangle(
                (_pz_l_mm, 0), _pz_r_mm - _pz_l_mm, _probe_h,
                linewidth=1.5, edgecolor="yellow", facecolor="yellow",
                alpha=0.45, zorder=6, label="探触子",
            ))

        # 探触子中心線（Global + Zoom 全パネル）
        if self.probe_center_mm is not None:
            for _ax in (self.ax_g1, self.ax_g3, self.ax_g5, self.ax_z1, self.ax_z3, self.ax_z5):
                _ax.axvline(self.probe_center_mm, color="cyan", lw=1.5, ls="--",
                            zorder=8, label=f"探触子中心 {self.probe_center_mm:.3f}mm")

        self.im_z1 = self.ax_z1.imshow(
            self.z_t1[0], cmap="RdBu_r", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="bilinear", extent=self.extent_zoom)
        self.ax_z1.set_title("Zoom T1")
        self.ax_z1.set_xlabel("Z (mm)"); self.ax_z1.set_ylabel("Depth X (mm)")
        self._draw_outline(self.ax_z1, is_zoom=True)

        self.im_z3 = self.ax_z3.imshow(
            self.z_t3[0], cmap="RdBu_r", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="bilinear", extent=self.extent_zoom)
        self.ax_z3.set_title("Zoom T3"); self.ax_z3.set_xlabel("Z (mm)")
        self._draw_outline(self.ax_z3, is_zoom=True)

        self.im_z5 = self.ax_z5.imshow(
            self.z_t5[0], cmap="RdBu_r", vmin=vmin, vmax=vmax,
            aspect="auto", interpolation="bilinear", extent=self.extent_zoom)
        self.ax_z5.set_title("Zoom T5"); self.ax_z5.set_xlabel("Z (mm)")
        self._draw_outline(self.ax_z5, is_zoom=True)

        self.fig.colorbar(self.im_z3,
                          ax=[self.ax_g1, self.ax_g3, self.ax_g5, self.ax_z1, self.ax_z3, self.ax_z5],
                          shrink=0.9, aspect=30, label="(norm.)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.Frame(main_frame, relief=tk.RAISED, borderwidth=1)
        ctrl.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=5)

        sl_box = ttk.Frame(ctrl)
        sl_box.pack(fill=tk.X, padx=10, pady=5)
        self.time_label = ttk.Label(sl_box, text="Time: 0.00 µs", width=20)
        self.time_label.pack(side=tk.LEFT)
        self.time_slider = ttk.Scale(sl_box, from_=0, to=self.n_frames - 1,
                                     orient=tk.HORIZONTAL, command=self.on_slider)
        self.time_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        btn = ttk.Frame(ctrl)
        btn.pack(pady=5)
        ttk.Button(btn, text="<< Start",  command=self.rewind).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn, text="< Prev",    command=self.step_back).pack(side=tk.LEFT, padx=5)
        self.btn_play = ttk.Button(btn, text="Play >", command=self.toggle_play)
        self.btn_play.pack(side=tk.LEFT, padx=10)
        ttk.Button(btn, text="Next >",    command=self.step_fwd).pack(side=tk.LEFT, padx=5)

        ttk.Label(btn, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.DoubleVar(value=30.0)
        ttk.Scale(btn, from_=1, to=60, variable=self.speed_var,
                  orient=tk.HORIZONTAL, length=120).pack(side=tk.LEFT)

        ttk.Button(btn, text="Save MP4",       command=self.save_mp4 ).pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(btn, text="Save Data (.npz)", command=self.save_data).pack(side=tk.LEFT, padx=5)

        self.root.after(500, self.toggle_play)

    # ------ 形状輪郭描画 ------
    def _draw_outline(self, ax, is_zoom=False):
        if self.mask_matrix is None:
            return
        mask   = self.mask_matrix[x_start:x_end, z_start:z_end] if is_zoom else self.mask_matrix[0:nx, :]
        extent = self.extent_zoom if is_zoom else self.extent_global
        if np.all(mask == 0) or np.all(mask == 1):
            return
        z_min, z_max, x_bot, x_top = extent
        rows, cols = mask.shape
        dz_px = (z_max - z_min) / cols
        dx_px = (x_bot - x_top) / rows
        lw = 1.0 if is_zoom else 0.5

        dh = np.diff(mask, axis=1)
        ri, ci = np.where(dh != 0)
        if len(ri):
            ax.vlines(z_min + (ci + 1) * dz_px,
                      x_top + ri * dx_px, x_top + (ri + 1) * dx_px,
                      colors="black", linewidths=lw, zorder=3)

        dv = np.diff(mask, axis=0)
        ri, ci = np.where(dv != 0)
        if len(ri):
            ax.hlines(x_top + (ri + 1) * dx_px,
                      z_min + ci * dz_px, z_min + (ci + 1) * dz_px,
                      colors="black", linewidths=lw, zorder=3)

    def _add_roi_rect(self, ax):
        rz, rx, rw, rh = self.roi_rect_mm
        ax.add_patch(Rectangle((rz, rx), rw, rh,
                                linewidth=1.5, edgecolor="red", facecolor="none"))

    # ------ フレーム更新 ------
    def update_frame(self, frame_idx):
        frame_idx = int(np.clip(frame_idx, 0, self.n_frames - 1))
        self.im_g1.set_array(self.g_t1[frame_idx])
        self.im_g3.set_array(self.g_t3[frame_idx])
        self.im_g5.set_array(self.g_t5[frame_idx])
        self.im_z1.set_array(self.z_t1[frame_idx])
        self.im_z3.set_array(self.z_t3[frame_idx])
        self.im_z5.set_array(self.z_t5[frame_idx])
        self.time_label.config(text=f"Time: {frame_idx * self.time_step * 1e6:.2f} µs")
        self.canvas.draw_idle()

    def on_slider(self, val):
        self.update_frame(float(val))

    # ------ 再生制御 ------
    def toggle_play(self):
        if self.play_running:
            self.play_running = False
            self.btn_play.config(text="Play >")
            if self.play_job:
                self.root.after_cancel(self.play_job)
                self.play_job = None
        else:
            self.play_running = True
            self.btn_play.config(text="Pause ||")
            self._loop()

    def _loop(self):
        if not self.play_running:
            return
        nf   = (int(self.time_slider.get()) + 1) % self.n_frames
        self.time_slider.set(nf)
        self.update_frame(nf)
        delay = int(1000 / max(1e-9, self.speed_var.get()))
        self.play_job = self.root.after(delay, self._loop)

    def rewind(self):
        self.play_running = False; self.btn_play.config(text="Play >")
        self.time_slider.set(0);   self.update_frame(0)

    def step_back(self):
        self.play_running = False; self.btn_play.config(text="Play >")
        c = self.time_slider.get(); self.time_slider.set(c - 1); self.update_frame(c - 1)

    def step_fwd(self):
        self.play_running = False; self.btn_play.config(text="Play >")
        c = self.time_slider.get(); self.time_slider.set(c + 1); self.update_frame(c + 1)

    # ------ 保存 ------
    def save_mp4(self):
        if self.play_running:
            self.toggle_play()
        fps      = int(np.clip(self.speed_var.get(), 1, 60))
        mp4_path = unique_path(os.path.join(self.output_dir, f"{self.base_name}.mp4"))
        gif_path = unique_path(os.path.join(self.output_dir, f"{self.base_name}.gif"))

        def _upd(i):
            self.im_g1.set_array(self.g_t1[i])
            self.im_g3.set_array(self.g_t3[i])
            self.im_g5.set_array(self.g_t5[i])
            self.im_z1.set_array(self.z_t1[i])
            self.im_z3.set_array(self.z_t3[i])
            self.im_z5.set_array(self.z_t5[i])
            self.time_label.config(text=f"Time: {i * self.time_step * 1e6:.2f} µs")
            return [self.im_g1, self.im_g3, self.im_g5, self.im_z1, self.im_z3, self.im_z5]

        ani = animation.FuncAnimation(self.fig, _upd, frames=self.n_frames,
                                      interval=1000 / fps, blit=False)
        try:
            if animation.writers.is_available("ffmpeg"):
                ani.save(mp4_path, writer=animation.FFMpegWriter(fps=fps, bitrate=1800), dpi=100)
                messagebox.showinfo("Saved", f"MP4を保存しました:\n{mp4_path}")
            else:
                ani.save(gif_path, writer=animation.PillowWriter(fps=fps), dpi=100)
                messagebox.showwarning("Saved (GIF)", f"ffmpeg が見つからないため GIF で保存:\n{gif_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"保存に失敗:\n{e}")

    def save_data(self):
        if self.play_running:
            self.toggle_play()
        path = unique_path(os.path.join(self.output_dir, f"{self.base_name}_data.npz"))
        try:
            save_kwargs = dict(
                g_t1=self.g_t1, g_t3=self.g_t3, g_t5=self.g_t5,
                z_t1=self.z_t1, z_t3=self.z_t3, z_t5=self.z_t5,
                time_step=self.time_step,
                extent_global=self.extent_global,
                extent_zoom=self.extent_zoom,
                roi_rect_mm=self.roi_rect_mm,
                base_name=self.base_name,
                mask_matrix=self.mask_matrix,
                f_pitch=np.array(f_pitch),
                f_width=np.array(f_width),
                f_depth=np.array(f_depth),
                probe_width=np.array(probe_d),
                probe_full=np.array(probe_full),
                probe_half_specimen=np.array(probe_half_specimen),
            )
            if self.probe_z_l_mm is not None:
                save_kwargs["probe_z_l_mm"] = self.probe_z_l_mm
            if self.probe_z_r_mm is not None:
                save_kwargs["probe_z_r_mm"] = self.probe_z_r_mm
            if self.probe_center_mm is not None:
                save_kwargs["probe_center_mm"] = self.probe_center_mm
            if self.gap_center_mm is not None:
                save_kwargs["gap_center_mm"] = self.gap_center_mm
            np.savez_compressed(path, **save_kwargs)
            messagebox.showinfo("Saved", f"NPZを保存しました:\n{path}")
            print(f"NPZを保存しました: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"保存に失敗:\n{e}")
            traceback.print_exc()


# =======================================================================
#               Main Simulation
# =======================================================================
def main():
    base_name = make_base_name(f_pitch, f_depth, f_width, probe_d, probe_full, probe_half_specimen)
    print(f"pitch={f_pitch*1e3:.3f}mm  depth={f_depth*1e3:.3f}mm  width={f_width*1e3:.3f}mm")
    print(f"save_interval={save_interval}  global_downsample={global_downsample}")
    print(f"output_dir: {output_dir}")
    print(f"base_name : {base_name}")

    os.makedirs(output_dir, exist_ok=True)

    # --- マスク生成 ---
    t13_isfree_np, t5_isfree_np = build_kukei_masks(nx, nz, f_width, f_pitch, f_depth, mesh_length)
    ux_free_np,   uz_free_np   = around_free_vectorized(t13_isfree_np, t5_isfree_np, nx, nz)

    T13_isfree  = cp.asarray(t13_isfree_np)
    T5_isfree   = cp.asarray(t5_isfree_np)
    Ux_free_cnt = cp.asarray(ux_free_np)
    Uz_free_cnt = cp.asarray(uz_free_np)

    # --- FDTD 配列確保 ---
    T1 = cp.zeros((nx + 1, nz),     dtype=cp.float32)
    T3 = cp.zeros((nx + 1, nz),     dtype=cp.float32)
    T5 = cp.zeros((nx,     nz + 1), dtype=cp.float32)
    Ux = cp.zeros((nx,     nz),     dtype=cp.float32)
    Uz = cp.zeros((nx + 1, nz + 1), dtype=cp.float32)

    dtx = dt / dx
    dtz = dt / dz

    # --- フレームリスト ---
    g_frames_t1, g_frames_t3, g_frames_t5 = [], [], []
    z_frames_t1, z_frames_t3, z_frames_t5 = [], [], []

    start_time = time.time()
    print(f"Running Simulation... ({t_max_steps} steps)")

    for t_i in range(t_max_steps):
        if t_i % 500 == 0:
            print(f"{t_i}/{t_max_steps} ({t_i / t_max_steps:.1%})")

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

        Ux[:nx, :nz] = cp.where(
            Ux_free_cnt < 4.0,
            Ux - (4.0 / rho / (4.0 - Ux_free_cnt)) * dtx
            * (T1[1:nx+1, :] - T1[:nx, :] + T5[:, 1:nz+1] - T5[:, :nz]),
            0.0,
        )
        Uz[1:nx, 1:nz] = cp.where(
            Uz_free_cnt[1:nx, 1:nz] < 4.0,
            Uz[1:nx, 1:nz] - (4.0 / rho / (4.0 - Uz_free_cnt[1:nx, 1:nz])) * dtz
            * (T3[1:nx, 1:nz] - T3[1:nx, :nz-1]
               + T5[1:nx, 1:nz] - T5[:nx-1, 1:nz]),
            0.0,
        )

        # フレーム保存
        if t_i % save_interval == 0:
            f1 = cp.asnumpy(T1[:nx, :])
            g_frames_t1.append(f1[::global_downsample, ::global_downsample].astype(np.float32))
            z_frames_t1.append(f1[x_start:x_end, z_start:z_end].astype(np.float32))

            f3 = cp.asnumpy(T3[:nx, :])
            g_frames_t3.append(f3[::global_downsample, ::global_downsample].astype(np.float32))
            z_frames_t3.append(f3[x_start:x_end, z_start:z_end].astype(np.float32))

            f5 = cp.asnumpy(T5[:nx, :nz])
            g_frames_t5.append(f5[::global_downsample, ::global_downsample].astype(np.float32))
            z_frames_t5.append(f5[x_start:x_end, z_start:z_end].astype(np.float32))

        if t_i % 1000 == 0:
            cp.cuda.Device().synchronize()

    print(f"Done. {time.time() - start_time:.1f} s")

    if not g_frames_t1:
        print("フレームがキャプチャされませんでした。")
        return

    g1 = np.array(g_frames_t1); g3 = np.array(g_frames_t3); g5 = np.array(g_frames_t5)
    z1 = np.array(z_frames_t1); z3 = np.array(z_frames_t3); z5 = np.array(z_frames_t5)

    roi_rect_mm = (
        zoom_z_min, zoom_x_min,
        zoom_z_max - zoom_z_min,
        zoom_x_max - zoom_x_min,
    )

    # 探触子中心 と 最近傍すきま中心 の計算
    # gap_center は alignment_target_z("gap_center", ...) と同じ定義:
    #   gap_left_wall  = pitch_start - 1
    #   gap_right_wall = groove_start - 1 = pitch_start + mn_gap - 1
    #   gap_center     = (gap_left_wall + gap_right_wall) / 2
    mn_p_val  = int(round(f_pitch / mesh_length))
    mn_w_val  = int(round(f_width  / mesh_length))
    mn_gap_val = mn_p_val - mn_w_val
    probe_center_mm_val = sz * dz * 1000
    _pitch_i_near = sz // mn_p_val
    _gc_candidates = []
    for _pi in range(max(0, _pitch_i_near - 1), min(int(np.ceil(nz / mn_p_val)) + 1, _pitch_i_near + 3)):
        _gap_lw = _pi * mn_p_val - 1
        _gap_rw = _pi * mn_p_val + mn_gap_val - 1
        _gc = (_gap_lw + _gap_rw) / 2.0
        if 0 <= _gc < nz:
            _gc_candidates.append((abs(_gc - sz), _gc))
    if _gc_candidates:
        gap_center_mm_val = min(_gc_candidates)[1] * dz * 1000
    else:
        gap_center_mm_val = probe_center_mm_val
    _diff_um = abs(probe_center_mm_val - gap_center_mm_val) * 1000
    print(f"探触子中心: {probe_center_mm_val:.4f} mm  "
          f"すきま中心(最近接): {gap_center_mm_val:.4f} mm  "
          f"ずれ: {_diff_um:.1f} µm")

    try:
        root = tk.Tk()
        IntegratedViewer(
            root=root,
            g_t1=g1, g_t3=g3, g_t5=g5, z_t1=z1, z_t3=z3, z_t5=z5,
            time_step=dt * save_interval,
            output_dir=output_dir,
            extent_global=extent_global,
            extent_zoom=extent_zoom,
            roi_rect_mm=roi_rect_mm,
            base_name=base_name,
            mask_matrix=t13_isfree_np,
            probe_z_l_mm=sz_l * dz * 1000,
            probe_z_r_mm=sz_r * dz * 1000,
            probe_center_mm=probe_center_mm_val,
            gap_center_mm=gap_center_mm_val,
        )
        root.mainloop()
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
