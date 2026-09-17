# AGENTS.md — Antigravity / Claude Code 共通ルール

このファイルは **Antigravity と Claude Code の両方が読む共通の作業ルール**です。
片方にしか当てはまらない詳細は `Gemini.md`(Antigravity 用) と `CLAUDE.md`(Claude Code 用) に置きます。
個別ファイルとこのファイルが矛盾した場合、**役割分担(2章)・引き継ぎ手順(4章)・git の運用(10章)はこのファイルが優先**します。

---

## 1. プロジェクト概要

超音波探傷(UT)の FDTD シミュレーション研究。鋼板中の鋸歯状・矩形欠陥での弾性波伝搬を
シミュレートし、実験のスコープ波形と比較して、週次の LaTeX 進捗報告にまとめる。

- **当面の目標**: 「二重モード変換」(欠陥での散乱・反射時に P波↔S波 変換が2回起こる現象)の理解
- **最終目標**: PINN(物理情報ニューラルネットワーク)で観測波形から欠陥パラメータを逆推定する

---

## 2. 役割分担

|  | **Antigravity (Gemini)** | **Claude Code** |
|---|---|---|
| 担当 | **文章** | **コードと推論** |
| 具体例 | 進捗報告の本文、スライド・原稿の執筆、論文の要約、日本語の推敲・構成 | シミュレーション/解析コードの実装・修正、デバッグ、数式と物理の検証、実行環境の管理 |

守ってほしいのは次の2点だけです。

- **Antigravity はコードを編集しない。** コード側の修正が必要になったら、自分で直さずに
  `HANDOFF.md` へ依頼として書く。
- **Claude Code は報告書の本文を書かない。** 文章が必要になったら、材料(数値・図のパス・
  事実の箇条書き)を `HANDOFF.md` に置いて Antigravity に渡す。

読むのは互いに自由です。制限がかかるのは**書き込むとき**だけです。

---

## 3. 担当ディレクトリ

| パス | 書き込む側 | 内容 |
|---|---|---|
| `進捗報告/tex/` | Antigravity | 週次レポートの LaTeX ソース |
| `text/`, `資料/` | Antigravity | 原稿、プレゼン構成案、輪読資料 |
| `vscode/`, `scripts/` | Claude Code | シミュレーション・解析コード、ツール類 |
| `*.ps1` | Claude Code | ビルド/ログ更新スクリプト |
| `tmp_output/`, `data/`, `pic/` | Claude Code が生成 | 図とシミュレーション出力。Antigravity は参照のみ(図のパスをレポートに書くため)。git 管理は別リポジトリ `lab-data`(11章) |
| `HANDOFF.md` | 両方(末尾に追記) | 引き継ぎメモ |
| `AGENTS.md` | 両方(要相談) | このファイル |

**`進捗報告/gemini_log/` と `scripts/history.db` は AI 利用監査ログ**(学術的誠実性のための記録)です。
`update_history.ps1` が自動生成するので手で編集しない。削除も禁止。詳細は `Gemini.md` の2章。

Gemini CLI と Claude Code のログは自動で取り込まれますが、**Antigravity だけは会話がローカルに
残らないため手動記録が必要**です。作業の区切りごとに `進捗報告/antigravity_log/YYYYMMDD.md` へ
追記してください(書式は同ディレクトリの `README.md`)。

---

## 4. 引き継ぎ手順 (HANDOFF.md)

作業が相手の担当領域に及ぶとき、および相手に続きを頼むときは、`HANDOFF.md` の**末尾に追記**します。
過去のエントリは消さない(消すと経緯が追えなくなる)。書式:

```markdown
## YYYY-MM-DD — <Antigravity|Claude Code>

### やったこと
- 事実だけ。変更したファイルは相対パスで書く

### 相手への依頼
- 具体的に。「文章を書いて」ではなく「この数値とこの図でこの節を書いて」

### 未解決・注意
- 引っかかっている点、確認が必要な前提
```

**Claude → Antigravity に渡すときのコツ**: 図は `tmp_output/...` の**実在するパス**で、数値は**単位つき**で
書く。`\includegraphics` は `進捗報告/tex/` からの相対パス(例 `../../tmp_output/xxx.png`)になる点に注意。

**Antigravity → Claude に渡すときのコツ**: 「グラフがおかしい」ではなく、どのスクリプトの
どの出力が期待とどう違うかを書く。

---

## 5. 実行環境 (2026-09-17 検証済み)

Windows 11 + Anaconda。**Python は必ず Anaconda の `venv` 環境**を使う(base 環境ではない)。

```powershell
& "C:\Users\cs16\anaconda3\shell\condabin\conda-hook.ps1"
conda activate venv
```

- Python 3.12.13 / numpy 1.26.4 / cupy-cuda12x 13.3.0 / pandas 3.0.3 / scipy / matplotlib /
  japanize_matplotlib / Pillow / python-pptx / PyMuPDF(fitz) / tkinter
- GPU: NVIDIA RTX 3060 (12GB)。CuPy はフル動作(elementwise / FFT / 線形代数すべて確認済み)
- TeX: TeX Live 2026。**pTeX/upTeX (`ptex2pdf`)** を使う。pdflatex や xelatex ではない
- 依存は `environment.yml`(conda、こちらが正) と `requirements.txt`(pip) に固定済み。
  環境を作り直す手順と CuPy の DLL 設定は **`SETUP.md`** にまとめてある

**CuPy の DLL 設定は消さないこと**: `venv` 内の `_cupy_cuda_path_fix.py` と
`zzz_cupy_cuda_path_fix.pth` が CUDA の DLL 検索パスを通しています。消すと CuPy が起動しません。
理由は `CLAUDE.md` に記載。

**このリポジトリは Google Drive 同期**です。macOS から開くと `C:\...` のハードコードパスは解決できません。

---

## 6. 主要コマンド

VS Code / Antigravity のタスク(`Ctrl+Shift+P` → Run Task)からも実行できます:
**Update LLM History** / **Build Report** / **Run Simulation Sweep** / **Check GPU (CuPy)**。

```powershell
# シミュレーションの一括実行(リポジトリルートから。simdata.csv を相対パスで読むため)
python vscode/simulation/loop_UT_sim.py

# 週次レポートのビルド(ファイル名は拡張子なし。省略すると tex/ の最新ファイル)
.\build_report.ps1 20260716_report

# AI 利用監査ログの更新
.\update_history.ps1
```

実行時間の目安: `run_simulation()` 1条件あたり**約2.5分**、`simdata.csv` の19条件で**約50分**。
長時間かかるので、レポート締め切り直前に回し始めない。

---

## 7. 命名規則（ichikawa sanリポジトリと共通）

共同研究者（ichikawa san）のリポジトリ **[erin621-arch/Roughness](https://github.com/erin621-arch/Roughness)**
と命名を揃える。**2026-09-17 に既存のコードと出力ファイル（143件）も移行済み**。
実装は `vscode/simulation/naming.py`（`mm_code()` / `sim_csv_name()` / `SIM_SHAPE`）。
自前で文字列を組み立てず、この関数を使う。

### パラメータコード

値[mm] × 100。整数にならない値は**小数のまま**にする（0.125 → `12.5`）。

| 実値 | コード |
|---|---|
| pitch 1.25 mm | `125` |
| depth 0.20 mm | `20` |
| width 1.25 mm | `125` |
| depth 0.125 mm (Ushape 最小) | `12.5` |

**`int(round(value * 100))` を使わない。** `round(12.5)` が 12 になり、depth 0.12 と区別できなくなる。
ichikawa san側の実装は `project4/Sourse/ani_utils.py` の `mm_code()`:

```python
def mm_code(value_mm):
    code = round(value_mm * 100, 6)
    return int(code) if float(code).is_integer() else code
```

このリポジトリのパラメータは **[m] 単位**（`f_pitch = 2.00e-3`）なので、mm に直してから渡す
（`mm_code(f_pitch * 1000)`）。

### 傷形状

**Kusabi**（楔型）/ **Ushape**（U字型）/ **Kukei**（矩形）/ **Sankaku**（三角形）/ **Smooth**（平滑面）

- ディレクトリは `Type_<Shape>`（先頭大文字）、ファイル名・スクリプト名の中は小文字
- Ushape は幅 w=0.25 mm 固定、最小 depth は R=w/2=0.125 mm

### ファイル名パターン

| 種類 | パターン | 例 |
|---|---|---|
| シミュレーション CSV（ichikawa san 側） | `<shape>_cupy_pitch<p>_depth<d>.csv` | `ushape_cupy_pitch100_depth12.5.csv` |
| シミュレーション CSV（こちら） | `<shape>_cupy_pitch<p>_width<w>_depth<d>.csv` | `kukei_cupy_pitch125_width15_depth12.5.csv` |
| 3D シミュレーション CSV | `<shape>_cupy3d_pitch<p>_depth<d>.csv` | `kukei_cupy3d_pitch200_depth20.csv` |
| 実験データのフォルダ | `<pitch>_<depth>` | `100_12.5` |
| アニメーション NPZ | `<prefix>_psize<ps>_pitch<p>_width<w>_depth<d>_data.npz` | 順序は psize→pitch→width→depth |
| 日付ログ | `YYYY_MM_DD.md` | `2026_09_17.md` |
| 過去版の保管 | `Type_<Shape>/<YYYYMM>_<shape>/` | `Type_Kukei/202605_kukei/` |

### 軸定義

**x軸 = 縦方向**（下方向が増加。音源・探触子が x=0、溝が x=nx 側）、**z軸 = 横方向**。
**z=0 は最初の溝の開始端**。`y` は使わない。

### 測定セットアップ

板厚方向のパルスエコー構成。探触子は**平滑な上面**に密着し、傷は**反対側の底面**にある。
溝を探触子側の面に描かない。Smooth ケースは傷があるはずの裏面が平ら。

---

## 8. ichikawa sanのリポジトリの扱い

対象: **[erin621-arch/Roughness](https://github.com/erin621-arch/Roughness)**（相互にコラボレーター登録済み）

- **ichikawa sanのファイルは直接変更しない。** 相手のリポジトリへ commit・push しない。
- 変更が必要なときは**ダウンロードして、自分の環境でのみ変更する**。
- 取得は読み取り目的に限る。clone 先は**このリポジトリの外**（作業用の一時フォルダ）に置き、
  `lab/` の中に持ち込まない。
- 相手側に反映してほしい変更は、自分で編集せず**ichikawa sanに伝える**。
- 逆に、こちらのリポジトリをichikawa sanが参照することもある。上の命名規則から外れると読み違いの原因に
  なるため、規則を変えたくなったら独断で変えずにと相談する。

---

## 9. 共通の注意点

- **文字コード**: LaTeX ソースは UTF-8 (BOM なし)。実験のスコープ CSV は SHIFT-JIS。
- **`vscode/simulation/` が FDTD 物理の正**。`vscode/project1/`・`project2/`・`project3_*/` は
  コピーして派生させた実験用フォークで、本体を直しても自動では反映されない。
- **`sourse_new_2.py` の `doc_path`** (`C:/Users/cs16/Roughness/project4`) は中身が揃っていない。
  これを import するプロット系スクリプトは、使う前にパスの確認が必要。
- **git**: 運用ルールは10章。`tmp_output/`・`pic/`・`output/`・`data/` は gitignore 済み
  (再生成できるため)。`scripts/history.db` は生成物だが監査ログの土台なので意図的に追跡している。
- 迷ったとき、相手の担当領域に手を出すより `HANDOFF.md` に書いて渡すほうが安全です。

---

## 10. Git の運用ルール（作業は必ず履歴に残す）

**このリポジトリの作業は必ず git に残す。** 壊しても戻せるようにするため、そして
「いつ・何を・なぜ変えたか」を後から追えるようにするため（AI 利用の記録と同じく、
研究の経緯を示す資料になる）。

Google Drive 同期は**バックアップであって履歴ではない**。同期は最新の状態しか持たないので、
壊れたファイルはそのまま上書きされて元に戻せない。戻せるのは git だけ。

### 誰がコミットするか

3章の担当ディレクトリと同じ。**自分が書き込んだものは、書いた側がコミットする。**

| 変更内容 | コミットする側 |
|---|---|
| `進捗報告/tex/`・`text/`・`資料/` の文章 | Antigravity |
| `vscode/`・`scripts/`・`*.ps1` のコード | Claude Code |
| `AGENTS.md`・`HANDOFF.md` | 変更した側 |

**相手の担当ディレクトリを巻き込んでコミットしない。** `git add -A` ではなく
`git add <自分が変えたパス>` を使う。相手の書きかけを巻き込むと、どちらの意図の変更なのか
後から分からなくなる。

### コミットするタイミング

- 作業の区切りがついたとき（最低でも、その日の作業の終わりに1回）
- **`HANDOFF.md` に追記して相手に渡す前**。渡した時点の状態が残っていないと、相手が
  「どのコードの話か」を特定できない
- レポートをビルドする前、長時間のシミュレーション（19条件で約50分）を回し始める前
- 動いている状態にたどり着いたとき。「後でまとめて」にすると、壊れた原因を切り分けられない

### コミットメッセージ

1行目は `<type>: <日本語の要約>`。本文には**なぜそうしたか**を書く。何をしたかは diff を
見れば分かるので、diff から読み取れないこと（理由・検証の結果・残っている懸念）を残す。

| type | 使いどころ |
|---|---|
| `feat` | 機能・スクリプトの追加 |
| `fix` | バグ修正 |
| `docs` | レポート本文、原稿、ルールファイル |
| `refactor` | 挙動を変えない整理 |
| `chore` | 設定、`.gitignore`、依存関係 |

Claude Code のコミットは末尾に `Co-Authored-By: Claude ...` を付ける（AI 利用の記録として）。

### 追跡するもの・しないもの

- **追跡する**: コード、`*.ps1`、`*.tex`、ルールファイル、`environment.yml` /
  `requirements.txt`、`進捗報告/gemini_log/`（監査ログ）、`scripts/history.db`
  （生成物だが監査ログの土台なので例外的に追跡）
- **追跡しない**: 再生成できる出力（`tmp_output/`・`pic/`・`output/`・`data/`）、
  実験データ `vscode/simulation/data/`（**別リポジトリ `lab-data` で管理する。11章**）、
  PDF・PPTX などの大きいバイナリ、`*.npz`・`*.mp4`・`*.gif`
- 除外を増やすときは `.gitignore` に**理由をコメントで添えて**書く（後から外してよいか判断できる）
- 50 MB を超えるファイルは入れない（GitHub が警告を出すライン）

### やってはいけないこと

- `git push --force` / `git reset --hard` / `git clean -fd` / `git checkout -- <path>`
  —— **コミットしていない作業が消える**。必要になったらユーザーに確認してから
- push 済みのコミットに対する `rebase`・`commit --amend`（履歴の書き換え）
- ichikawa san のリポジトリへの commit・push（8章）
- `進捗報告/gemini_log/`・`scripts/history.db` の削除（監査ログ。3章）

### push について

remote は `origin`（`https://github.com/hotta-yuki/-laboratory-cs16.git`）。
**push はユーザーが判断する。エージェントは自動で push しない**（Claude Code は
`.claude/settings.json` で `git push` を拒否設定にしてある）。コミットまでを済ませて、
「push できる状態です」と伝えるところまでが担当。

### 困ったとき

| やりたいこと | コマンド |
|---|---|
| 今の状態を見る | `git status` / `git diff` |
| 履歴を見る | `git log --oneline` / `git show <hash>` |
| 直前のコミットを取り消す（変更は残す） | `git reset --soft HEAD~1` |
| 変更を捨てずに一旦避ける | `git stash` → `git stash pop` |

**消えて困るものが消えそうな操作は、実行せずに聞く。**

---

## 11. データリポジトリ (lab-data)

**データはコードとは別のリポジトリで管理する。** 対象は実験のスコープ波形、シミュレーション
出力の CSV、そこから作った図。

分ける理由は、データが**再現可能だが再現に時間がかかる**こと（1条件あたり約2.5分の GPU 計算）。
ichikawa san が同じものを回し直すのも負担なので、計算結果そのものを履歴に残す。一方でデータは
コードより桁違いに大きく、本体リポジトリに混ぜると clone が重くなるため分離している。

### 置き場所

```
<任意のディレクトリ>/
├── lab/        ← 本体リポジトリ（コード。Google Drive 同期の対象）
└── lab-data/   ← データリポジトリ（Drive の外に置く）
```

**lab-data を Google Drive のフォルダの中に置かないこと。** 同期のタイミングで `.git` が壊れる
（実際、Drive 内では `git add` が `Permission denied` で失敗する事例が出ている）。

データの実体は2か所にある。役割が違うのでどちらも消さない。

| 場所 | 役割 |
|---|---|
| `lab/vscode/simulation/data/`・`lab/tmp_output/` | スクリプトが読み書きする作業コピー。Drive 同期の対象なのでバックアップも兼ねる |
| `lab-data/` | git で履歴を残す場所。GitHub 経由で Mac・ichikawa san と共有する |

| lab-data 側 | 作業コピー側 | 中身 |
|---|---|---|
| `experiment/` | `vscode/simulation/data/` | 実験のスコープ波形・索引・平均波形 |
| `simulation/sim/`・`simulation/sim_csv/` | `tmp_output/sim/`・`tmp_output/sim_csv/` | FDTD 出力の CSV |
| `plots/…` | `tmp_output/…` | CSV から作った図 |

### 同期

```bash
# 計算した後: 作業コピー -> lab-data（コミットまで。push はしない）
python scripts/sync_data_repo.py --to repo --commit "feat: pitch 2.0mm の掃引結果を追加"

# 相手の機械の結果を取り込む: lab-data -> 作業コピー
python scripts/sync_data_repo.py --to work

# 何が動くか先に見る
python scripts/sync_data_repo.py --to repo --dry-run
```

既定では**上書きと追加だけ**を行い、送り元に無いファイルは消さずに報告する（消すなら `--delete`）。

### スクリプトから参照するとき

パスを直接書かず **`vscode/simulation/data_paths.py`** を使う。`experiment_dir()` /
`sim_csv_dir()` / `sim_dir()` が、作業コピー → 隣の `lab-data` の順に実在する方を返す。
別の場所に置いた場合は環境変数 `LAB_DATA_DIR` で指定する。

### lab-data にも入れないもの

動画（`*.mp4`・`*.gif`）とアニメーションの NPZ。GitHub の上限（1ファイル100MB）を超えるものが
あり、再生成もできるため。必要なものだけ Google Drive か GitHub Releases で個別に渡す。
