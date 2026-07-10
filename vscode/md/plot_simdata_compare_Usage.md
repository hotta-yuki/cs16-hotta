# plot_simdata_compare.py 使い方説明書 (Usage)

## 1. 概要
`plot_simdata_compare.py` は、`vscode/simulation/tmp/` 内にある複数のシミュレーション波形データを一斉に読み込み、それらの「時間領域波形」および「FFT スペクトル」をそれぞれ**1枚のグラフに重ね書き（比較）プロット**して保存するためのスクリプトです。
複数のパラメータ間の信号挙動やスペクトルの差異を視覚的に比較するために非常に有効です。

---

## 2. 処理プロセス
1.  **データのソートロード**:
    *   `vscode/simulation/tmp/sim_*.csv` に合致するCSVファイルを昇順で並び替え、各データを一列ずつ取り込みます。
2.  **ノイズカット・オフセット調整**:
    *   初期送信パルスや多重反射などを除外するため、インデックス $8000$ 以降（`search_offset = 8000`）から波形を切り出します。
    *   共通ライブラリ `sourse_new_2.py` の `kiritori2` 関数（および定数 `left`, `right`）を使用して、有効なエコー領域を抽出します。
3.  **重ね書きプロットの生成**:
    *   **時間領域**: 横軸：インデックス、縦軸：振幅。各パラメータが異なる凡例ラベル（例: `pitch1250_depth100` など）で色分けされ重ねて描画されます。
    *   **周波数領域 (FFT)**: 横軸：周波数 [Hz]（$2.0$ 〜 $10.0$ MHz 範囲に拡大）、縦軸：振幅スペクトルの強度。各信号のピークや周波数シフトの差異を重ねて表示します。

---

## 3. 動作要件・依存ライブラリ
*   **環境**: Python 3.x
*   **ライブラリ**: `numpy`, `pandas`, `matplotlib`
*   **依存関係**: 共通処理ライブラリ `vscode/simulation/sourse_new_2.py`

---

## 4. 使用方法
以下のコマンドを実行します。
```powershell
python vscode/simulation/plot_simdata_compare.py
```

---

## 5. 出力ファイル
*   **波形一括比較プロット (PNG)**:
    `tmp_output/comparison_plots/comparison_waveform.png`
*   **FFT一括比較プロット (PNG)**:
    `tmp_output/comparison_plots/comparison_fft.png`

*(※凡例の数が極めて多くなる場合を考慮し、凡例はグラフ外側の右スペースに綺麗にレイアウトされるように自動配置されます。)*
