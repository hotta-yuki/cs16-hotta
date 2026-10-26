"""サロゲートモデルの設計空間（pitch / width / depth）の定義と、メッシュ量子化。

範囲の根拠は `README.md` の 1.。試験体 48 件（`specimens.csv`）の範囲を各軸で
15〜25% 外側に広げた箱にしてある。試験体を箱の**内側**に置くのは、GPR の精度が
学習領域の端で落ちるため。

量子化（README の 2.）でいちばん注意が要るのは、FDTD 側が

    mn_p = int(f_pitch / mesh_length)

と**切り捨て**で離散化していること（`UT_FlawVariation_Sim.isfree()`）。[m] 単位の
浮動小数には誤差があるので、1.25e-3 / 1.0e-5 は 124.99999999999999 になり 124 セル
＝ 1.24 mm の溝が彫られる。公称値と実形状が最大 1 セルずれ、しかもずれ方が値ごとに
違う（0.20 や 0.40 はぴったり、0.15 や 0.60 や 1.25 はずれる）。

ここではソルバー側を書き換えず、**ソルバーが実際に作る形状のほうを正とする**。
`cells_to_m()` が「切り捨てても狙ったセル数になる [m] 値」を返し、教師ラベルには
セル数 × mesh_length を使う。既存データもこの実現値で振り直せば再計算は要らない。
"""

import math

MESH_M = 1.0e-5          # UT_FlawVariation_Sim.mesh_length [m]
MESH_MM = MESH_M * 1e3   # 0.01 mm

# 設計空間の箱 [mm]。(下限, 上限)
BOX_MM = {
    "pitch": (1.10, 2.20),   # 試験体 1.25 - 2.00
    "width": (0.10, 0.50),   # 試験体 0.15 - 0.40
    "depth": (0.02, 0.32),   # 試験体 0.02 - 0.28
}

# セル数に直した箱。LHS はこの整数格子の上で振る
BOX_CELLS = {k: (round(lo / MESH_MM), round(hi / MESH_MM)) for k, (lo, hi) in BOX_MM.items()}


def cells_to_m(cells):
    """切り捨て離散化を通しても `cells` になる [m] 値を返す。"""
    v = cells * MESH_M
    while int(v / MESH_M) < cells:
        v = math.nextafter(v, math.inf)
    return v


def realized_mm(cells):
    """FDTD が実際に作る寸法 [mm]。教師ラベルはこちらを使う。"""
    return round(cells * MESH_MM, 6)


def make_condition(c_pitch, c_width, c_depth):
    """セル数の組から、ソルバーに渡す [m] 値を作る。

    `isfree()` は pitch / width / depth のほかに
    ``mn_nf = int((f_pitch - f_width) / mesh_length)`` も計算する。差を取ってから
    切り捨てるので、pitch と width を個別に合わせただけでは mn_nf が 1 ずれることが
    ある。ここで実際に検算し、合うまで pitch を 1 ulp ずつ持ち上げる。
    """
    p = cells_to_m(c_pitch)
    w = cells_to_m(c_width)
    d = cells_to_m(c_depth)
    for _ in range(64):
        if int((p - w) / MESH_M) == c_pitch - c_width:
            break
        p = math.nextafter(p, math.inf)
    else:
        raise ValueError(f"mn_nf を合わせられない: {c_pitch=} {c_width=}")
    verify_condition(p, w, d, c_pitch, c_width, c_depth)
    return p, w, d


def verify_condition(p, w, d, c_pitch, c_width, c_depth):
    """`isfree()` と同じ式で離散化し、狙ったセル数になっているか確かめる。"""
    got = (
        int(p / MESH_M),
        int(w / MESH_M),
        int((p - w) / MESH_M),
        int(d / MESH_M),
    )
    want = (c_pitch, c_width, c_pitch - c_width, c_depth)
    if got != want:
        raise ValueError(f"離散化が一致しない: got={got} want={want}")


def rms_um(c_pitch, c_width, c_depth):
    """二値表面の RMS 粗さ [um]。

    σ = h * sqrt(r(1-r)), r = w/p。`specimens.csv` の RMS 列 48 件すべてが
    この式に厳密に一致する（試験体はこの軸の上で設計されている）。
    """
    r = c_width / c_pitch
    return realized_mm(c_depth) * 1e3 * math.sqrt(r * (1.0 - r))
