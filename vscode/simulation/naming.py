"""ファイル名の命名規則（先輩リポジトリ erin621-arch/Roughness と共通）

規則の定義は リポジトリルートの `AGENTS.md` 7章。実装は先輩の
`project4/Sourse/ani_utils.py` の `mm_code()` に合わせてある。

このリポジトリのパラメータは **[m] 単位**（`f_pitch = 2.00e-3`）なので、
[m] のまま渡せる `m_code()` を用意している。
"""


# このリポジトリの FDTD が扱う傷形状。`UT_FlawVariation_Sim.isfree()` は
# 深さ mn_d・幅 mn_w の矩形溝をピッチ間隔で繰り返し彫るので Kukei（矩形）。
# 形状名の一覧は リポジトリルートの AGENTS.md 7章。
# ここに置いてあるのは、CuPy に依存しないスクリプト（プロット系）からも
# 参照できるようにするため。
SIM_SHAPE = "Kukei"


def mm_code(value_mm):
    """mm 値をファイル名用のコードに変換する（値[mm] × 100）。

    整数にならない値は小数のまま返す（0.125 → 12.5）。

    `int(round(value_mm * 100))` にしてはいけない。`round(12.5)` は
    バンカーズ・ラウンディングで 12 になり、depth 0.12 mm と区別できなくなる。
    このリポジトリにも depth 0.125 mm のデータが実在する。
    """
    code = round(value_mm * 100, 6)
    return int(code) if float(code).is_integer() else code


def m_code(value_m):
    """[m] 単位の値をファイル名用のコードに変換する（1.25e-3 → 125）。"""
    return mm_code(value_m * 1000)


def sim_csv_name(shape, pitch_m, width_m, depth_m):
    """シミュレーション出力 CSV のファイル名を作る。

        <shape>_cupy_pitch<p>_width<w>_depth<d>.csv

    例) sim_csv_name("Kukei", 2.00e-3, 1.25e-3, 0.125e-3)
        → 'kukei_cupy_pitch200_width125_depth12.5.csv'

    先輩側の同種ファイルは `<shape>_cupy_pitch<p>_depth<d>.csv` で width を持たない。
    こちらは width を掃引するため追加しており、位置は先輩の
    `make_ani_stem()`（psize → pitch → width → depth）の順に合わせている。
    """
    return (f"{shape.lower()}_cupy"
            f"_pitch{m_code(pitch_m)}"
            f"_width{m_code(width_m)}"
            f"_depth{m_code(depth_m)}.csv")


def sim3d_csv_name(shape, pitch_m, depth_m):
    """3D シミュレーション出力 CSV のファイル名を作る。

        <shape>_cupy3d_pitch<p>_depth<d>.csv

    例) sim3d_csv_name("Kukei", 2.00e-3, 0.20e-3)
        → 'kukei_cupy3d_pitch200_depth20.csv'

    2D と違い width を名前に入れない（ichikawa san 側の2D命名に合わせた形）。
    `run_simulation_3d()` は f_width を受け取るので、**width を変えて掃引すると
    同じ名前で上書きされる**。掃引を始めるときは width を足すか、ichikawa san と
    3D の命名を擦り合わせること。
    """
    return (f"{shape.lower()}_cupy3d"
            f"_pitch{m_code(pitch_m)}"
            f"_depth{m_code(depth_m)}.csv")


def ani_npz_name(prefix, probe_d_m, pitch_m, width_m, depth_m):
    """応力場アニメーション NPZ のファイル名を作る。

        <prefix>_psize<ps>_pitch<p>_width<w>_depth<d>_data.npz

    例) ani_npz_name("kukei_field", 0.007, 2.00e-3, 0.15e-3, 0.20e-3)
        → 'kukei_field_psize700_pitch200_width15_depth20_data.npz'

    順序は AGENTS.md 7章の表（psize → pitch → width → depth）に合わせてある。

    なお `kukei_ani.py` の `make_base_name()` は同じ順序だが
    `int(round(value_m * 1e5))` で組み立てているため、depth 0.125 mm が
    12.5 ではなく 12 になる（バンカーズ・ラウンディング）。こちらは m_code() を
    使うので 12.5 のまま残る。kukei_ani.py 側の移行は未着手（HANDOFF.md 参照）。
    """
    return (f"{prefix}"
            f"_psize{m_code(probe_d_m)}"
            f"_pitch{m_code(pitch_m)}"
            f"_width{m_code(width_m)}"
            f"_depth{m_code(depth_m)}_data.npz")
