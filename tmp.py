import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# ==========================================
# 1. パラメータの定義
# ==========================================
# 条件 T1 > T2 を満たす正の定数を設定
T1 = 10.0
T2 = 1.0
m = 1.0

# 折れ点周波数の算出
omega_T1 = 1.0 / T1
omega_T2 = 1.0 / T2

# ==========================================
# 2. 伝達関数の構築
# ==========================================
s = ctrl.TransferFunction.s

# 制御器 C(s)
C = (T1 * s + 1) / (T2 * s + 1)

# 制御対象 P(s)
P = 1 / (m * s**2)

# 開ループ伝達関数 C(s)P(s)
CP = C * P

# 解析する角周波数の範囲を設定（10^-2 から 10^2 rad/s）
omega = np.logspace(-2, 2, 1000)

# ==========================================
# 3. 周波数応答の算出
# ==========================================
# C(s) のボード線図データ
mag_C, phase_C, omega_C = ctrl.bode(C, omega, plot=False)
mag_C_dB = 20 * np.log10(mag_C)
phase_C_deg = np.degrees(phase_C)

# C(s)P(s) のボード線図データ
mag_CP, phase_CP, omega_CP = ctrl.bode(CP, omega, plot=False)
mag_CP_dB = 20 * np.log10(mag_CP)
phase_CP_deg = np.degrees(phase_CP)

# ==========================================
# 4. グラフの描画
# ==========================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Bode Plots of C(s) and C(s)P(s)', fontsize=16)

# 共通設定関数
def add_break_frequencies(ax):
    ax.axvline(omega_T1, color='red', linestyle='--', alpha=0.7, label='$\omega = 1/T_1$')
    ax.axvline(omega_T2, color='green', linestyle='--', alpha=0.7, label='$\omega = 1/T_2$')
    ax.grid(True, which="both", ls="-", alpha=0.5)

# --- [左列] 制御器 C(s) の描画 ---
# ゲイン線図
axs[0, 0].semilogx(omega_C, mag_C_dB, color='blue')
axs[0, 0].set_title('Controller $C(s)$')
axs[0, 0].set_ylabel('Gain [dB]')
add_break_frequencies(axs[0, 0])
axs[0, 0].legend()

# 位相線図
axs[1, 0].semilogx(omega_C, phase_C_deg, color='orange')
axs[1, 0].set_ylabel('Phase [deg]')
axs[1, 0].set_xlabel('Frequency $\omega$ [rad/s]')
add_break_frequencies(axs[1, 0])

# --- [右列] 開ループ伝達関数 C(s)P(s) の描画 ---
# ゲイン線図
axs[0, 1].semilogx(omega_CP, mag_CP_dB, color='blue')
axs[0, 1].set_title('Open-Loop Transfer Function $C(s)P(s)$')
axs[0, 1].set_ylabel('Gain [dB]')
add_break_frequencies(axs[0, 1])
axs[0, 1].legend()

# 位相線図
# 位相が-180度基準であることを明瞭にするための調整
axs[1, 1].semilogx(omega_CP, phase_CP_deg, color='orange')
axs[1, 1].axhline(-180, color='black', linestyle=':', label='-180 deg line')
axs[1, 1].set_ylabel('Phase [deg]')
axs[1, 1].set_xlabel('Frequency $\omega$ [rad/s]')
add_break_frequencies(axs[1, 1])
axs[1, 1].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()