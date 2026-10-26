"""
geometry.py — 矩形きず（溝）の形状マスクと自由境界カウント（2D）
=============================================================
FDTD 本体 (UT_FlawVariation_Sim.py) と可視化 (kukei_ani.py) が
**同じ形状**を計算するための共通モジュール。

以前は両者が別々にマスクを作っており、離散化が int() と int(round()) で
違ううえ自由境界カウントの数え方も別物だった。つまりアニメーションで
見ている形状と、波形を計算した形状が一致する保証がなかった。

ここでの基準は FDTD 本体 (UT_FlawVariation_Sim.py) の実装。
既存の出力 CSV と結果が変わらないよう、離散化も数え方もそちらに合わせてある
（around_free は二重ループを numpy でベクトル化したもので、値は完全に一致する。
  test_geometry.py で元実装との一致を検証している）。

座標の約束
----------
    x (第0軸) : 深さ方向。x = nx 側が探傷面（きずがある面）
    z (第1軸) : 表面に沿う方向
    配列形状  : T13_isfree (nx+1, nz)   T5_isfree (nx+1, nz+1)
                Ux_free_count (nx, nz)  Uz_free_count (nx+1, nz+1)
"""

import numpy as np


def flaw_mesh_counts(f_width, f_pitch, f_depth, mesh_length):
    """
    きずの寸法 [m] を離散点数に変換する。

    Returns
    -------
    mn_w  : int  きずの幅の離散点数
    mn_p  : int  1ピッチの離散点数
    mn_nf : int  きずのない部分（平坦部）の離散点数
    mn_d  : int  きずの深さ方向の離散点数
    """
    mn_w  = int(f_width / mesh_length)
    mn_p  = int(f_pitch / mesh_length)
    mn_nf = int((f_pitch - f_width) / mesh_length)
    mn_d  = int(f_depth / mesh_length)
    return mn_w, mn_p, mn_nf, mn_d


def groove_ranges(nz, f_width, f_pitch, mesh_length, domain_length=None):
    """
    各きず（溝）が占める z 方向のインデックス範囲 [start, end) を列挙する。

    マスク生成と FDTD ループ内の応力ゼロ化で同じ範囲を使うためのヘルパー。
    領域の端にはみ出すきずは含めない（元実装の break と同じ挙動）。

    Parameters
    ----------
    domain_length : float or None
        きずの本数を数えるときの領域長 [m]。
        None なら nz * mesh_length（= isfree が昔から使っている値）。

        ★要注意★ 元のコードは 2 か所でこの値が食い違っていた。
            isfree               : nz * mesh_length = 0.03999 m
            run_simulation のループ: z_length        = 0.04    m
        nz が 3999 で 4000 でないせいで両者が一致しない（config.py の nx/nz の
        コメント参照）。pitch 1.25mm では isfree が 31 本、ループが 32 本となり、
        **マスクが数えていない 32 本目のきずで応力だけがゼロにされていた**。
        pitch 1.5 / 1.75 / 2.0mm では break のおかげで結果は同じ。

        既存の出力 CSV を変えないため、呼び出し側が昔と同じ値を渡して
        昔の挙動をそのまま再現できるようにしてある。
        config.py の nx/nz を int(round(...)) に直せばこのズレ自体が消える。

    Returns
    -------
    list[tuple[int, int]]
    """
    if domain_length is None:
        domain_length = nz * mesh_length

    _, mn_p, mn_nf, _ = flaw_mesh_counts(f_width, f_pitch, 0.0, mesh_length)
    num_f = int(domain_length / f_pitch)   # きずの数

    ranges = []
    for i in range(num_f):
        if (i + 1) * mn_p >= nz:
            break
        ranges.append((mn_nf + i * mn_p, (i + 1) * mn_p))
    return ranges


def isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length):
    """
    自由境界マスクを作る。値 0 が自由境界（応力ゼロ）、1 が内部。

    Returns
    -------
    T13_isfree : ndarray (nx+1, nz)
    T5_isfree  : ndarray (nx+1, nz+1)
    """
    T13_isfree = np.ones((nx + 1, nz))
    T5_isfree = np.ones((nx + 1, nz + 1))
    _, _, _, mn_d = flaw_mesh_counts(f_width, f_pitch, f_depth, mesh_length)

    # 領域外周の自由境界
    T13_isfree[0, 0:nz] = 0
    T13_isfree[nx, 0:nz] = 0
    T5_isfree[0:nx, 0] = 0
    T5_isfree[0:nx, nz] = 0
    T5_isfree[nx, 0:nz + 1] = 0

    # きず部分ゆえに消すとこ
    for start, end in groove_ranges(nz, f_width, f_pitch, mesh_length):
        T5_isfree[nx - mn_d:nx, start:end] = 0
        T13_isfree[nx - mn_d:nx + 1, start:end - 1] = 0

    return T13_isfree, T5_isfree


def around_free(T13_isfree, T5_isfree, nx, nz):
    """
    各ノードが接している自由境界の数を数える。
    粒子速度の更新式で 4/(4 - count) の係数に使う。

    元の二重ループ実装と同じ値を返す（ベクトル化のみ）。
    nx=2000, nz=4000 では 800万回のループが消えるので大幅に速い。

    Returns
    -------
    Ux_free_count : ndarray (nx, nz)
    Uz_free_count : ndarray (nx+1, nz+1)
    """
    is13 = (T13_isfree == 0)
    is5 = (T5_isfree == 0)

    # --- Ux: 上下の T13 と左右の T5 を見る ---
    Ux_free_count = (
        is13[0:nx, :].astype(float)
        + is13[1:nx + 1, :].astype(float)
        + is5[0:nx, 0:nz].astype(float)
        + is5[0:nx, 1:nz + 1].astype(float)
    )

    # --- Uz ---
    Uz_free_count = np.zeros((nx + 1, nz + 1), dtype=float)

    # 外周ぶんの加算（元実装の 1つ目・2つ目の if）
    Uz_free_count[0, :] += 1        # i == 0
    Uz_free_count[nx, 0] += 1       # 角 (nx, 0)
    Uz_free_count[nx, nz] += 1      # 角 (nx, nz)
    Uz_free_count[:, 0] += 1        # j == 0
    Uz_free_count[:, nz] += 1       # j == nz

    # 内部ノード (0 < i <= nx, 0 < j < nz) だけマスクを数える。
    # 元実装では j が端のとき elif で分岐して数えないので、ここでも数えない。
    Uz_free_count[1:, 1:nz] += (
        is13[1:, 0:nz - 1].astype(float)
        + is13[1:, 1:nz].astype(float)
        + is5[0:nx, 1:nz].astype(float)
        + is5[1:, 1:nz].astype(float)
    )

    return Ux_free_count, Uz_free_count
