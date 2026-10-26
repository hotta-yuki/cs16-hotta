"""
test_geometry.py — geometry.py が元実装と同じ値を返すことの検証
=============================================================
geometry.isfree / around_free は、共通化する前に
UT_FlawVariation_Sim.py に直接書かれていた実装をベクトル化したもの。
「速くしただけで結果は 1 ビットも変えていない」ことをここで確かめる。

元実装は参照用にこのファイルへ丸ごと写してある（_ref_ 接頭辞）。
UT_FlawVariation_Sim.py 側を変更したら、ここも見直すこと。

実行:
    python test_geometry.py
"""

import numpy as np

import geometry


# =============================================================================
# 元実装（UT_FlawVariation_Sim.py 2026-09-17 時点のコピー。変更しないこと）
# =============================================================================

def _ref_isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length):
    T13_isfree = np.ones((nx + 1, nz))
    T5_isfree = np.ones((nx + 1, nz + 1))
    mn_w = int(f_width / mesh_length)
    mn_p = int(f_pitch / mesh_length)
    mn_nf = int((f_pitch - f_width) / mesh_length)
    mn_d = int(f_depth / mesh_length)
    num_f = int(nz * mesh_length / f_pitch)
    T13_isfree[0, 0:nz] = 0
    T13_isfree[nx, 0:nz] = 0
    T5_isfree[0:nx, 0] = 0
    T5_isfree[0:nx, nz] = 0
    T5_isfree[nx, 0:nz + 1] = 0

    for i in range(num_f):
        if (i + 1) * mn_p >= nz:
            break
        T5_isfree[nx - mn_d:nx, mn_nf + i * mn_p:(i + 1) * mn_p] = 0
        T13_isfree[nx - mn_d:nx + 1, mn_nf + i * mn_p:(i + 1) * mn_p - 1] = 0
    return T13_isfree, T5_isfree


def _ref_around_free(T13_isfree, T5_isfree, nx, nz):
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


# =============================================================================
# 検証
# =============================================================================

# (nx, nz, f_width, f_pitch, f_depth, mesh_length)
# 二重ループの参照実装が重いので格子は小さめ。きずの配置パターンは
# simdata.csv の実パラメータ（width 1.05〜2.00mm / pitch 2.0mm / depth 0.2mm）を
# メッシュを粗くして再現している。
CASES = [
    (40, 80, 1.05e-3, 2.00e-3, 0.20e-3, 1.0e-4),   # 幅がピッチより十分狭い
    (40, 80, 1.50e-3, 2.00e-3, 0.20e-3, 1.0e-4),
    (40, 80, 2.00e-3, 2.00e-3, 0.20e-3, 1.0e-4),   # 幅 = ピッチ（平坦部なし）
    (40, 80, 1.25e-3, 2.00e-3, 0.50e-3, 1.0e-4),   # 深いきず
    (30, 60, 0.15e-3, 2.00e-3, 0.20e-3, 1.0e-4),   # きずが 1 メッシュ以下に潰れる
    (25, 50, 1.25e-3, 1.25e-3, 0.10e-3, 1.0e-4),   # ピッチが領域と割り切れない
]


def check_groove_count_quirk():
    """
    元コードでは isfree とループ内の応力ゼロ化で、きずの本数の数え方が違った。
        isfree               : nz * mesh_length で数える
        run_simulation のループ: z_length        で数える
    nz=3999（4000 ではない）のせいで pitch 1.25mm では 31 本と 32 本に割れる。
    既存の出力 CSV を再現するため、この食い違いは意図的に残してある。
    直すときは config.py の nx/nz を int(round(...)) にする。
    """
    import config

    print("--- きず本数の数え方（既知の食い違い） ---")
    ok = True
    for pitch in (2.00e-3, 1.75e-3, 1.50e-3, 1.25e-3):
        by_mask = geometry.groove_ranges(config.nz, 1.05e-3, pitch, config.mesh_length)
        by_loop = geometry.groove_ranges(config.nz, 1.05e-3, pitch, config.mesh_length,
                                         domain_length=config.z_length)
        # 元実装のループをそのまま再現したもの
        mn_p = int(pitch / config.mesh_length)
        mn_nf = int((pitch - 1.05e-3) / config.mesh_length)
        ref_loop = []
        for i in range(int(config.z_length / pitch)):
            if (i + 1) * mn_p >= config.nz:
                break
            ref_loop.append((mn_nf + i * mn_p, (i + 1) * mn_p))

        same_as_ref = (by_loop == ref_loop)
        ok &= same_as_ref
        note = "" if len(by_mask) == len(by_loop) else "  ← マスクとループで本数が違う"
        print(f"[{'OK' if same_as_ref else 'NG'}] pitch={pitch*1e3:.2f}mm  "
              f"マスク {len(by_mask)} 本 / ループ {len(by_loop)} 本{note}")
    return ok


def main():
    all_ok = True
    for nx, nz, f_width, f_pitch, f_depth, mesh_length in CASES:
        label = (f"nx={nx} nz={nz} w={f_width*1e3:.2f}mm "
                 f"p={f_pitch*1e3:.2f}mm d={f_depth*1e3:.2f}mm")

        ref_t13, ref_t5 = _ref_isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length)
        new_t13, new_t5 = geometry.isfree(nx, nz, f_width, f_pitch, f_depth, mesh_length)

        ref_ux, ref_uz = _ref_around_free(ref_t13, ref_t5, nx, nz)
        new_ux, new_uz = geometry.around_free(new_t13, new_t5, nx, nz)

        checks = {
            "T13_isfree": np.array_equal(ref_t13, new_t13),
            "T5_isfree": np.array_equal(ref_t5, new_t5),
            "Ux_free_count": np.array_equal(ref_ux, new_ux),
            "Uz_free_count": np.array_equal(ref_uz, new_uz),
        }
        ok = all(checks.values())
        all_ok &= ok
        print(f"[{'OK' if ok else 'NG'}] {label}")
        for name, passed in checks.items():
            if not passed:
                print(f"       {name} が不一致: 差分 {int(np.sum(ref_ux != new_ux))} 要素")

    print()
    all_ok &= check_groove_count_quirk()

    print()
    if all_ok:
        print("すべて一致。geometry.py は元実装と同じ結果を返す。")
        return 0
    print("不一致あり。geometry.py を使うと計算結果が変わる。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
