# 周期的粗面・超音波探傷 FDTD シミュレーション プログラム構成と用途説明

本ディレクトリ (`vscode/project3_2026_09_17`) には、周期的粗面/欠陥（きず）における超音波探傷試験 (UT) の 2次元/3次元 弾性波動 FDTD シミュレーション、自動ループ処理、信号解析、および可視化のための主要プログラムが格納されています。

---

## 🧱 モジュールの階層

定数と形状の定義は**必ず 1 か所**に置く。下の層は上の層を知らない。

```
config.py      物理定数・メッシュ・データ一覧・パス   ← 値を変えるのはここだけ
naming.py      ファイル名の命名規則
   ↓
geometry.py    きずの形状マスク・自由境界カウント（2D）
signal_utils.py 波形の切り出し・FFT・補間・帯域抽出
   ↓
dataio.py      実験 CSV / シミュレーション CSV の読み込み
metrics.py     RMSE など誤差評価
plotting.py    正規化 FFT スペクトルの作図
   ↓
UT_FlawVariation_Sim.py / kukei_ani.py / loop_UT_sim.py /
extract_features.py / plot_simdata_compare.py        ← 実行するもの
```

`sourse_new_2.py` は**旧名の互換中継**。`import sourse_new_2 as sn2` と書いてある
古いスクリプトが動くように、分割後の名前を再公開しているだけ。
**新しいコードは `signal_utils` / `dataio` / `plotting` を直接 import する。**

---

## 📄 各ファイルの用途一覧

### 共通モジュール（直接は実行しない）

| ファイル名 | 用途区分 | 概要・詳細な機能 |
| :--- | :--- | :--- |
| **`config.py`** | 設定 | 材料定数・メッシュ・時間刻み・探触子・FFT 設定・pitch/depth 一覧・入出力パス。**物理定数をここ以外に書かない。** データの置き場所は環境変数 `LAB_DOC_ROOT` で差し替えられる。 |
| **`naming.py`** | 命名規則 | 出力ファイル名の組み立て（AGENTS.md 7章）。解析対象の形状 `SIM_SHAPE` もここ。 |
| **`geometry.py`** | 形状定義 | 矩形きずの自由境界マスク `isfree` と自由境界カウント `around_free`。**FDTD 本体とアニメーションが同じ関数を使う**ことで、描いた形状と計算した形状のズレを防ぐ。 |
| **`signal_utils.py`** | 信号処理 | ピーク切り出し `kiritori2`、ゼロパディング FFT、実験⇔シミュレーションの時間軸補間、周波数帯域抽出、正規化スペクトル。ファイルは読まないし図も描かない。 |
| **`dataio.py`** | データ読み込み | 実験 CSV（SHIFT-JIS・バイアス除去）とシミュレーション CSV の読み込み、データセット作成。 |
| **`metrics.py`** | 誤差評価 | 指定周波数帯での行ごと RMSE、列ごとの誤差統計。 |
| **`plotting.py`** | 作図 | 正規化 FFT スペクトルの重ね書きと EPS 保存（周波数軸・波数軸）。 |
| **`sourse_new_2.py`** | 互換用 | 上記モジュールの再公開のみ。新規のコードは書かない。 |

### 実行するスクリプト

| ファイル名 | 用途区分 | 概要・詳細な機能 |
| :--- | :--- | :--- |
| **`UT_FlawVariation_Sim.py`** | 2D FDTD シミュレーション | CuPy (GPU) を使用した 2次元弾性波動 FDTD 計算エンジン。欠陥のパラメータ（幅 $w$, 深さ $d$, ピッチ $p$）を入力として音場・応力場を計算し、探触子位置での時間領域反射波形データを `lab/tmp_output/sim/` に保存します。 |
| **`loop_UT_sim.py`** | 自動ループ実行 | `simdata.csv` から欠陥パラメータ一覧を読み込み、`UT_FlawVariation_Sim.run_simulation` を自動でバッチ実行します。計算ずみの条件は飛ばすので、途中で止めても続きから再開できます。 |
| **`simdata.csv`** | 設定ファイル | `loop_UT_sim.py` でバッチ処理を行うための欠陥形状パラメータリスト（`f_width`, `f_pitch`, `f_depth`）です。 |
| **`kukei_ani.py`** | 波動場可視化 | FDTD シミュレーション実行中の音場・応力場 ($T_1, T_3, T_5$) の二次元分布の波動伝搬アニメーション (GIF/MP4/NPZ) を生成・表示します。形状マスクは `geometry.py` 経由で FDTD 本体と共通。 |
| **`extract_features.py`** | 特徴量自動抽出 | 反射波形から振幅・エネルギー・ピーク周波数・重心周波数・−6dB 帯域幅などを抽出して CSV にまとめます。`--input-dir` で入力フォルダを変更可。 |
| **`plot_simdata_compare.py`** | データ比較描画 | 異なる欠陥形状条件の波形と FFT スペクトルを重ね書きして比較します。`--input-dir` / `--output-dir` で入出力を変更可。 |
| **`test_geometry.py`** | 検証 | `geometry.py` が共通化前の実装と同じ値を返すことを確認します。`geometry.py` を触ったら実行すること。 |
| **`UT_FlawVariation_Sim_3d.py`** | 3D FDTD シミュレーション | 3次元弾性波動 FDTD モデルへの拡張用スクリプト。メッシュ間隔が 2D と異なるため、`config.py` は参照せず独自に定数を持っています。 |

---

## 🚀 実行・利用の流れの例

### 1. 単体パラメータでの 2D シミュレーション実行
```bash
python UT_FlawVariation_Sim.py
```
* **入力**: `config.py` のメッシュ・材料定数と、`run_simulation()` に渡す欠陥寸法
* **出力**: `lab/tmp_output/sim/` に時間領域反射波形 CSV（実行したディレクトリに依存しない）

### 2. 条件を変えた自動バッチシミュレーション
```bash
python loop_UT_sim.py
```
* `simdata.csv` 内のリストに従って複数の欠陥形状について連続計算します。

### 3. 波形の比較と特徴量抽出
```bash
python plot_simdata_compare.py            # 既定で lab/tmp_output/sim を読む
python extract_features.py --input-dir ../simulation/tmp
```

### 4. 解析ライブラリとして使う
```python
from signal_utils import kiritori2, make_fftdata
from plotting import select_pitch_and_image_exp

select_pitch_and_image_exp(200, [10, 15, 20])
```

---

## ⚠️ 既知の問題（数値に影響するので触る前に読むこと）

1. **`nx = 1999`, `nz = 3999` になっている**
   `int(0.02 / 1.0e-5)` は浮動小数点の都合で 1999 になる（2000 ではない）。
   そのため `dx = 1.0005e-5` で `mesh_length` と 0.05% ズレ、`dt` も同じだけズレる。
   既存の出力 CSV はすべてこの条件で計算済み。直すなら `config.py` の 2 行を
   `int(round(...))` にするだけだが、**過去のデータと比較できなくなる**。

2. **きずの本数の数え方が 2 通りある**
   マスク (`isfree`) は `nz * mesh_length = 0.03999 m`、FDTD ループ内の応力ゼロ化は
   `z_length = 0.04 m` で本数を数えている。pitch 1.25mm では 31 本と 32 本に割れ、
   **マスクが知らない 32 本目のきずで応力だけがゼロにされる**。
   pitch 1.5 / 1.75 / 2.0mm では結果に差は出ない。上の 1 を直せばこれも消える。
   現状は既存データを保つためそのまま再現している（`geometry.groove_ranges` の
   `domain_length` 引数）。

3. **`interpolate_sim` が波形長によっては落ちる**
   `np.arange(0, len*dt, dt)` の点数が丸め次第で 1 点ずれ、`interp1d` が
   長さ不一致で `ValueError` を投げることがある。分割前から同じ挙動。

---

## 💡 物理的・力学的背景メモ
* **$T_1$ ($\sigma_{xx}$)**: $x$ 方向垂直応力（主に縦波バルク波に対応）
* **$T_3$ ($\sigma_{zz}$)**: $z$ 方向垂直応力（粗面境界に沿う表面波/レイリー波に対応）
* **$T_5$ ($\sigma_{xz}$)**: せん断応力（欠陥角部での L波 $\rightleftharpoons$ SV波・レイリー波のモード変換を媒介）
