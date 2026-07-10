# sourse_0211.py 使い方説明書 (Usage)

## 1. 概要
`sourse_0211.py` は、複数の超音波時間領域波形データを効率的に管理、比較、および解析するための各種補助関数を提供するユーティリティライブラリです。
特に、波形のピーク強度の平均値や絶対平均値を計算する機能のほか、時間経過に伴う波形の変化をインタラクティブなアニメーション動画として可視化するための機能を提供します。

---

## 2. 主要関数 (APIs)

### `create_wave_matrix(wave_list)`
*   **説明**: 長さが異なる可能性のある複数の 1次元波形データのリストを受け取り、最も短い波形の長さに揃えて切り詰め、2次元配列（`shape = (パラメータ数, 時間点数)`）に変換して返します。

### `calculate_peak_means(wave_matrix)`
*   **説明**: `scipy.signal.find_peaks` を用いて、波形マトリックスの各パラメータについて正および負の両方のピーク（極大点・極小点）を検出し、その絶対値の平均を算出します。

### `calculate_absolute_means(wave_matrix)`
*   **説明**: 各パラメータ波形の全時間軸にわたる「絶対値の平均」を計算します。全体の減衰特性や波形全体の強度の定量評価に使用されます。

### `adjust_data_length(*wave_data_list)`
*   **説明**: 引数として与えられた複数の波形行列データの時間軸の長さを、最も短いものの長さに統一して一括切り詰めを行います。

### `create_wave_animation(*wave_data_list, param_values, dt, ...)`
*   **説明**: 
    *   Matplotlib の `FuncAnimation` を用いて、パラメータ（例：傷の寸法やピッチなど）の推移に伴って時間領域波形がどのように変化（波形シフト、振幅減衰、多重散乱の発生など）するかを、動的なアニメーションとして生成します。
    *   検出されたピークの位置を波形上にプロットし、視覚的にピークの移動を追跡することができます。

---

## 3. 動作要件・依存ライブラリ
*   **環境**: Python 3.x
*   **ライブラリ**: `numpy`, `matplotlib`, `scipy`

---

## 4. ライブラリとしての利用方法
他のスクリプト（データ比較や解析、可視化用プログラム）から以下のようにインポートして使用します。

```python
import sourse_0211 as s0211
import numpy as np

# ダミー波形データの作成 (3つのパラメータ別データ)
wave_p1 = np.sin(np.linspace(0, 10, 100))
wave_p2 = np.sin(np.linspace(0, 10, 100)) * 0.8
wave_p3 = np.sin(np.linspace(0, 10, 100)) * 0.5

# 2次元波形行列の生成
wave_matrix = s0211.create_wave_matrix([wave_p1, wave_p2, wave_p3])

# ピーク平均の計算
peak_means, peak_indices = s0211.calculate_peak_means(wave_matrix)
print("Peak absolute means:", peak_means)
```
*(※アニメーション機能 `create_wave_animation` を利用すれば、パラメータ別の時間発展の重ね書き比較アニメーションもその場で描画・MP4保存可能です。)*
