# 超音波探傷(UT)の FDTD シミュレーション研究

鋼板中の弾性波伝搬を 2D/3D の FDTD（時間領域差分法）で計算し、鋸歯状・矩形の欠陥で
散乱した波形を、実験のスコープ波形と突き合わせて調べるためのリポジトリです。
週次の進捗報告（LaTeX）もここで作っています。

- **当面の目標**: 二重モード変換（欠陥での散乱・反射時に P波↔S波 変換が2回起こる現象）の理解
- **最終目標**: PINN（物理情報ニューラルネットワーク）で、観測波形から欠陥パラメータを逆推定する

---

## 最初に読むもの

| 知りたいこと | 見るファイル |
|---|---|
| 環境の作り方（Python・CuPy・TeX） | [`SETUP.md`](SETUP.md) |
| 作業のルール全般（役割分担・命名規則・git・データ） | [`AGENTS.md`](AGENTS.md) |
| 前回までの経緯、次にやること | [`HANDOFF.md`](HANDOFF.md) の末尾 |
| ディレクトリ構成と AI 利用ログの詳細 | [`Gemini.md`](Gemini.md) |
| データの中身 | `lab-data/README.md`（別リポジトリ） |

`CLAUDE.md` と `Gemini.md` は AI エージェント向けの指示書です。人が読む必要はありませんが、
中身は上の各ファイルと矛盾しないようにしてあります。

---

## リポジトリは2つある

```
<任意のディレクトリ>/
├── lab/        ← このリポジトリ。コード・レポート・ルール（Google Drive 同期）
└── lab-data/   ← データ（実験波形・シミュレーション結果・図）★Drive の外に置く
```

分けている理由は、データが**再現できるけれど再現に時間がかかる**ためです。
シミュレーションは1条件あたり約2.5分の GPU 計算で、全条件を回し直すと数時間かかります。
共同研究者が再実行するのも大変なので、計算結果そのものを git の履歴に残します。
ただしデータはコードより桁違いに大きいので、本体リポジトリには混ぜません。

**`lab-data` を Google Drive のフォルダの中に置かないでください。** 同期のタイミングで
`.git` への書き込みが失敗し、リポジトリが壊れます。

2つのリポジトリは**並べて clone** するだけで、submodule にはしていません。
スクリプトは [`vscode/simulation/data_paths.py`](vscode/simulation/data_paths.py) が場所を
自動で解決します（別の場所に置く場合は環境変数 `LAB_DATA_DIR` を設定）。

```bash
git clone https://github.com/hotta-yuki/-laboratory-cs16.git lab
git clone <lab-data の URL> lab-data
```

---

## セットアップ（要点）

詳しい手順は [`SETUP.md`](SETUP.md)。

- **Windows 11 + Anaconda**。Python は必ず `venv` 環境（base ではない）
- GPU は NVIDIA RTX 3060。FDTD ソルバーは **CuPy** なので CUDA が要る
- LaTeX は TeX Live 2026 の **pTeX/upTeX（`ptex2pdf`）**。pdflatex や xelatex ではない
- 依存は `environment.yml`（conda・こちらが正）と `requirements.txt`（pip）に固定済み

```powershell
& "C:\Users\cs16\anaconda3\shell\condabin\conda-hook.ps1"
conda activate venv
```

**Mac では シミュレーションは動きません**（CUDA が無いため）。解析・作図・レポート執筆用です。

---

## よく使うコマンド

VS Code / Antigravity のタスク（`Ctrl+Shift+P` → Run Task）からも実行できます。

```powershell
# シミュレーションの一括実行（リポジトリルートから。simdata.csv を相対パスで読むため）
python vscode/simulation/loop_UT_sim.py

# 週次レポートのビルド（拡張子なし。省略すると tex/ の最新ファイル）
.\build_report.ps1 20260716_report

# AI 利用の監査ログを更新
.\update_history.ps1

# データリポジトリとの同期
python scripts/sync_data_repo.py --to repo --commit "feat: ..."   # 計算した後
python scripts/sync_data_repo.py --to work                        # 相手の機械の結果を取り込む
```

**実行時間の目安**: `run_simulation()` 1条件あたり約2.5分、`simdata.csv` の19条件で約50分。
レポート締め切りの直前に回し始めないこと。

---

## ディレクトリ構成

| パス | 中身 |
|---|---|
| `vscode/simulation/` | **FDTD 物理の正**。ソルバー・一括実行・プロット・共通ライブラリ |
| `vscode/project1/`, `project2/`, `project3_*/` | モード変換可視化の実験用フォーク。本体をコピーして派生させたもの |
| `vscode/md/` | スクリプトの解説メモ（FDTD の手法、各スクリプトの使い方） |
| `vscode/project_ex/` | **研究とは無関係**の 3D 散歩ゲームの試作（Three.js）。混同しないこと |
| `scripts/` | AI 利用ログの生成、図・アニメーションの作成、pptx 修復（目的の異なる3系統） |
| `進捗報告/` | 週次レポート（`tex/` が原稿、ルートに PDF）と AI 利用ログ |
| `text/`, `資料/` | 原稿・プレゼン構成案・輪読資料 |
| `tmp_output/`, `pic/`, `output/`, `data/` | 生成物。git 管理外（再生成できるため） |

**`vscode/simulation/` を直しても、フォーク（`project1` 等）には自動で反映されません。**
どちらを触っているか意識してください。

---

## データの置き場所

| | 場所 | 役割 |
|---|---|---|
| 作業コピー | `lab/vscode/simulation/data/`, `lab/tmp_output/` | スクリプトが読み書きする。Drive 同期＝バックアップも兼ねる |
| 履歴 | `lab-data/` | git で版を残す。GitHub 経由で Mac・共同研究者と共有 |

**どちらも消さないでください。** 両者の同期は `scripts/sync_data_repo.py` で行います。

動画（`*.mp4`・`*.gif`）とアニメーションの NPZ は、どちらの git にも入れていません
（GitHub の1ファイル100MB制限を超えるものがあり、再生成もできるため）。必要なものだけ
Google Drive か GitHub Releases で個別に渡します。

---

## ファイル名の規則

共同研究者（ichikawa san）のリポジトリ
[erin621-arch/Roughness](https://github.com/erin621-arch/Roughness) と揃えています。
**規則の正は [`AGENTS.md`](AGENTS.md) 7章**、実装は `vscode/simulation/naming.py` です。
自分で文字列を組み立てず、この関数を使ってください。

- パラメータコードは **値[mm] × 100**。整数にならない値は小数のまま（0.125 mm → `12.5`）
- `int(round(value * 100))` は使わない（`round(12.5)` が 12 になり depth 0.12 と衝突する）
- シミュレーション CSV: `kukei_cupy_pitch125_width15_depth20.csv`
- 軸は **x = 縦方向**（探触子が x=0、溝が x=nx 側）、**z = 横方向**。`y` は使わない

---

## AI（Antigravity / Claude Code）の使い方

このリポジトリは2つの AI エージェントと一緒に作業しています。

- **Antigravity (Gemini)** … 文章担当。進捗報告の本文、原稿、日本語の推敲。コードは編集しない
- **Claude Code** … コードと推論担当。シミュレーション/解析の実装、デバッグ、環境管理。
  報告書の本文は書かない

両者の引き継ぎは [`HANDOFF.md`](HANDOFF.md) に追記する形で行います（過去のエントリは消さない）。

**`進捗報告/gemini_log/` と `scripts/history.db` は AI 利用の監査ログ**です。学術的誠実性の
ための記録なので、手で編集したり削除したりしないでください。`update_history.ps1` が
自動生成します。Antigravity だけは会話がローカルに残らないため、
`進捗報告/antigravity_log/YYYYMMDD.md` への手動記録が必要です。

---

## 落とし穴（先に知っておくと困らないこと）

- **作業は必ず git にコミットする。** Google Drive 同期は最新状態しか持たないバックアップで、
  履歴ではありません。壊したものを戻せるのは git だけです（ルールは `AGENTS.md` 10章）
- **`lab-data` を Drive の中に置かない。** `.git` が壊れます
- **実験のスコープ CSV は SHIFT-JIS**、LaTeX ソースは UTF-8（BOM なし）
- **CuPy の DLL 設定を消さない。** `venv` 内の `_cupy_cuda_path_fix.py` と
  `zzz_cupy_cuda_path_fix.pth` が CUDA の DLL 検索パスを通しています（理由は `CLAUDE.md`）
- **`sourse_new_2.py` の `doc_path`** は中身が揃っていません。これを import するプロット系
  スクリプトは、使う前にパスの確認が必要です
- スクリプトのパスは Windows 前提でハードコードされている箇所があります（`*.ps1` と
  `C:\...`）。Mac では解決できません
- **ichikawa san のリポジトリには commit・push しない。** 参照は読み取り目的に限り、
  clone 先はこのリポジトリの外に置きます（`AGENTS.md` 8章）
