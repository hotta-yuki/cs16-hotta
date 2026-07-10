# extract_features.py 使い方説明書 (Usage)

## 1. 概要
`extract_features.py` は、シミュレーションで得られた時間領域の超音波波形データから、機械学習や統計的解析に用いるための特徴量（時間・周波数領域の特徴）を自動抽出し、単一の CSV ファイルにまとめるためのスクリプトです。

---

## 2. 抽出される特徴量
各シミュレーション波形から以下の **7 つの特徴量** が計算されます。

### 時間領域特徴 (Time Domain)
*   `max_amplitude`: 波形の絶対最大値（最大振幅）。
*   `peak_to_peak`: 波形の最大値と最小値の差。
*   `energy`: 波形データの二乗和（エネルギー）。
*   `rms`: 波形の二乗平均平方根（Root Mean Square）。

### 周波数領域特徴 (Frequency Domain / FFT)
※ `sourse_new_2.py` に準拠し、信号の S/N 比が高い **$2.0$ 〜 $10.0$ MHz** の帯域に絞って抽出を行います。
*   `peak_frequency`: 最大振幅を示す周波数（ピーク周波数）。
*   `centroid_frequency`: パワースペクトルの重心にあたる周波数（重心周波数）。
*   `bandwidth_6dB`: ピークから $-6$ dB（振幅が半分）以上の強さを持つ周波数範囲の広さ（$-6$dB 帯域幅）。

---

## 3. 動作要件・依存ライブラリ
*   **環境**: Python 3.x
*   **ライブラリ**: `numpy`, `pandas`
*   **依存関係**: 共通処理ライブラリ `vscode/simulation/sourse_new_2.py` のインポートが必要です。同一ディレクトリに配置されていることを確認してください。

---

## 4. 使用方法

### 事前準備
入力データとなるシミュレーション結果（`sim_*.csv`）を、以下の入力フォルダに配置します。
*   **入力フォルダ**: `vscode/simulation/tmp/`
    *   ファイル名形式：`sim_pitch[pitch_um]_depth[depth_um]_width[width_um].csv`

### 実行
以下のコマンドでスクリプトを実行します。
```powershell
python vscode/simulation/extract_features.py
```

---

## 5. 入出力ファイル
*   **入力**: `vscode/simulation/tmp/sim_*.csv`（一連のパラメータ別シミュレーション波形、1列データ）
*   **出力**: `simulation_features.csv`（ルートディレクトリ、または指定先に生成されるメタデータ付き特徴量一覧）

### 出力 CSV のヘッダー構成
```text
filename, pitch, depth, width, max_amplitude, peak_to_peak, energy, rms, peak_frequency, centroid_frequency, bandwidth_6dB
```
各行に各試験体パラメータのシミュレーション波形から抽出された特徴量が保存されます。
