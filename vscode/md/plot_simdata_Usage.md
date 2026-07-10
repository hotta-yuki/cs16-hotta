# plot_simdata.py 使い方説明書 (Usage)

## 1. 概要
`plot_simdata.py` は、シミュレーション結果（複数ファイル）を読み込み、それぞれの時間領域の波形（インデックス対振幅）および周波数領域の FFT スペクトル（周波数対振幅）のプロット画像を、各ファイルごとに個別出力するためのスクリプトです。

---

## 2. 処理内容
1.  **入力ファイルの読み込み**:
    *   `vscode/simulation/tmp/sim_*.csv` にマッチするシミュレーション波形CSV群を自動ロードします。
2.  **波形カット (切り出し) とバイアス補正**:
    *   初期パルス等の不要な受信成分を避けるため、一定のオフセットインデックス（`search_offset = 8000`）から切り出しを行います。
    *   `sourse_new_2.py` に定義された共通カット（`left`, `right`）を適用した波形を抽出します。
3.  **波形のプロットと保存**:
    *   横軸をインデックス、縦軸を電圧振幅（範囲：$-1.5$ 〜 $1.5$ V）として、グラフをプロットし保存します。
4.  **FFT の計算とプロット・保存**:
    *   `sourse_new_2.py` の `make_fftdata` を用いて振幅スペクトルを求め、横軸を周波数 [Hz]（範囲：$2.0$ 〜 $10.0$ MHz）、縦軸を大きさ（範囲：$0$ 〜 $0.04$）としてプロットし保存します。

---

## 3. 動作要件・依存ライブラリ
*   **環境**: Python 3.x
*   **ライブラリ**: `numpy`, `pandas`, `matplotlib`
*   **依存関係**: 共通処理ライブラリ `vscode/simulation/sourse_new_2.py` が必要です。

---

## 4. 使用方法
以下のコマンドを実行します。
```powershell
python vscode/simulation/plot_simdata.py
```

---

## 5. 入出力フォルダ
*   **入力**: `vscode/simulation/tmp/sim_*.csv`
*   **出力**:
    *   波形プロット保存先: `tmp_output/plots_simulation_waveform/sim_*_waveform.png`
    *   FFTプロット保存先: `tmp_output/plots_simulation_fft/sim_*_fft.png`
