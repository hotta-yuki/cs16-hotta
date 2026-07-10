# calculate_avg_waveforms.py 使い方説明書 (Usage)

## 1. 概要
`calculate_avg_waveforms.py` は、実験データの測定値グループを平均化し、それと対応する FDTD シミュレーションデータとの重ね合わせ比較プロットを自動生成するためのスクリプトです。
実験波形とシミュレーション波形の位相ズレを補正するための「ピーク同期（Time-align）」機能、および FFT 解析機能を有しています。

---

## 2. 処理の流れ
1. **設定情報の読み込み**:
   * `data/ex_index.csv` から各試験体グループのインデックス範囲（開始・終了）、および傷パラメータ（ピッチ、深さ、幅）を取得します。
2. **シミュレーションデータの検索**:
   * 指定したパラメータに対応するシミュレーションCSV（`tmp_output/sim_csv/sim_pitch[pitch_um]_depth[depth_um]_width[width_um].csv`）を自動探索します。
3. **実験データの平均化**:
   * 対象グループの実験CSV（`data/ex_data/scope_*.csv`）を読み込み、指定範囲（5.5 〜 9.0 $\mu s$）で切り出した後、最頻値によるバイアス除去を施してグループ全体の平均波形および平均 FFT スペクトルを算出します。
4. **ピーク同期とスケーリング**:
   * シミュレーションデータを実験波形の時間軸に合わせて3次スプライン補間します。
   * 両波形の絶対最大値（ピーク）の位置を検出し、その差分だけシミュレーション時間軸をシフトして重ね合わせます（`align_peaks`）。
5. **成果物の保存**:
   * 平均化した実験時間領域波形およびFFTスペクトルを CSV 保存します。
   * シミュレーションと実験の重ね合わせ比較プロット（波形・FFT）を PNG 保存します。

---

## 3. 前提条件と依存ライブラリ
* **環境**: Python 3.x
* **ライブラリ**: `numpy`, `pandas`, `matplotlib`, `scipy`
* **入力データの配置**:
  * 実験データ: `vscode/simulation/data/ex_data/scope_*.csv`
  * インデックスファイル: `vscode/simulation/data/ex_index.csv`
  * シミュレーション結果: `tmp_output/sim_csv/sim_pitch[pitch]_depth[depth]_width[width].csv`

---

## 4. 設定項目 (スクリプト内パラメータ)
スクリプト冒頭部で以下の設定を変更できます。
* `T_START` / `T_END`: 波形のカット範囲（秒）。デフォルトは `5.5e-6` 〜 `9.0e-6` ($5.5$ 〜 $9.0\ \mu s$)。
* `fft_N`: FFT計算時のゼロパディング点数。デフォルトは `16384`（$2^{14}$ 点）。

---

## 5. 実行方法
以下のコマンドで実行します。
```powershell
python vscode/simulation/calculate_avg_waveforms.py
```

---

## 6. 出力ファイル
* **平均波形 CSV (実験)**: 
  `vscode/simulation/data/avg_waveforms/avg_wave_p[pitch]_d[depth]_w[width]_[start]_[end].csv`
* **平均 FFT CSV (実験)**: 
  `vscode/simulation/data/avg_waveforms/avg_fft_p[pitch]_d[depth]_w[width]_[start]_[end].csv`
* **重ね合わせ比較プロット (PNG)**:
  `vscode/simulation/data/comparison_plots/compare_wave_p[pitch]_d[depth]_w[width]_[start]_[end].png` (時間領域波形)
  `vscode/simulation/data/comparison_plots/compare_fft_p[pitch]_d[depth]_w[width]_[start]_[end].png` (周波数領域スペクトル)
