# AGENTS.md — Antigravity / Claude Code 共通ルール

このファイルは **Antigravity と Claude Code の両方が読む共通の作業ルール**です。
片方にしか当てはまらない詳細は `Gemini.md`(Antigravity 用) と `CLAUDE.md`(Claude Code 用) に置きます。
個別ファイルとこのファイルが矛盾した場合、**役割分担(2章)と引き継ぎ手順(4章)はこのファイルが優先**します。

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
| `tmp_output/`, `data_im/`, `pic/` | Claude Code が生成 | 図とシミュレーション出力。Antigravity は参照のみ(図のパスをレポートに書くため) |
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

## 7. 共通の注意点

- **文字コード**: LaTeX ソースは UTF-8 (BOM なし)。実験のスコープ CSV は SHIFT-JIS。
- **`vscode/simulation/` が FDTD 物理の正**。`vscode/project1/`・`project2/`・`project3_*/` は
  コピーして派生させた実験用フォークで、本体を直しても自動では反映されない。
- **`sourse_new_2.py` の `doc_path`** (`C:/Users/cs16/Roughness/project4`) は中身が揃っていない。
  これを import するプロット系スクリプトは、使う前にパスの確認が必要。
- **git**: `tmp_output/`・`pic/`・`output/`・`data_im/` は gitignore 済み(再生成できるため)。
  `scripts/history.db` は生成物だが監査ログの土台なので意図的に追跡している。
- 迷ったとき、相手の担当領域に手を出すより `HANDOFF.md` に書いて渡すほうが安全です。
