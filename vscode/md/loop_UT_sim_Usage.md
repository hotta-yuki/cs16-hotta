# loop_UT_sim.py 使い方説明書 (Usage)

## 1. 概要
`loop_UT_sim.py` は、あらかじめ設定ファイル `simdata.csv` に定義されたきずパラメータ（ピッチ、深さ、幅）のすべての組み合わせについて、FDTD 超音波シミュレーション（`UT_FlawVariation_Sim.py`）をループ（一括バッチ）実行し、解析用の時間領域波形データを大量生成するための自動化スクリプトです。

---

## 2. 処理の流れ
1.  **パラメータのロード**:
    *   `vscode/simulation/simdata.csv` を解析し、幅（`f_width`）、ピッチ（`f_pitch`）、深さ（`f_depth`）の各パラメータ値のリストを取得します。
2.  **パラメータ組み合わせの生成**:
    *   Python の `itertools.product` を用いて、各パラメータのすべての組み合わせ（直積）を自動的に生成します。
3.  **重複実行の回避（スキップ機能）**:
    *   シミュレーションを開始する前に、該当するパラメータ名の出力ファイル（例: `sim_pitch1250000_depth100000_width250000.csv` など）がすでに `tmp_output/sim/` または `data/simdata_out/` フォルダに存在するかどうかを確認します。
    *   すでにファイルが存在する場合は、そのシミュレーションをスキップして次の組み合わせに進みます。
4.  **シミュレーションの実行**:
    *   出力が存在しない組み合わせについて、GPU を用いたシミュレーション本体（`UT_FlawVariation_Sim.run_simulation`）を呼び出し、計算を行います。

---

## 3. 動作要件・依存ライブラリ
*   **環境**: Python 3.x
*   **ライブラリ**: `numpy`, `cupy`（シミュレーション本体で GPU を使用するため）
*   **依存関係**: 
    *   シミュレーションモジュール `vscode/simulation/UT_FlawVariation_Sim.py`
    *   パラメータ定義ファイル `vscode/simulation/simdata.csv`

---

## 4. パラメータ定義ファイル (`simdata.csv`) の書式
`simdata.csv` は、以下のようにセクションヘッダー（`f_width`, `f_pitch`, `f_depth`）の下に、数値を1行ずつ記述する構造になっています。
```text
f_width
0.00015
0.0004
0.0006
0.0008
f_pitch
0.00125
0.002
f_depth
0.0001
0.00015
0.0002
```
*(※単位はメートル [m] です)*

---

## 5. 使用方法
以下のコマンドで、一括シミュレーションを開始します。
```powershell
python vscode/simulation/loop_UT_sim.py
```

---

## 6. 出力ファイル
シミュレーションが完了すると、指定の出力先に以下のCSVファイルが生成されます。
*   **保存先**: `tmp_output/sim/` または `data/simdata_out/`
*   **ファイル名命名ルール**:
    `sim_pitch[ピッチのnm表記]_depth[深さのnm表記]_width[幅のnm表記].csv`
    *   例：ピッチ $1.25$ mm ($1250000$ nm)、深さ $0.10$ mm ($100000$ nm)、幅 $0.15$ mm ($150000$ nm) の場合
        $\rightarrow$ `sim_pitch1250000_depth100000_width150000.csv`
*   **ファイル内容**: 垂直入射での探触子受信波形（時間領域電圧、1列の数値配列データ）
