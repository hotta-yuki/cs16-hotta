# HANDOFF.md — Antigravity ⇄ Claude Code 引き継ぎメモ

書式と運用ルールは `AGENTS.md` の4章を参照。**新しいエントリは末尾に追記**し、過去のものは消さない。

---

## 2026-09-17 — Claude Code

### やったこと

**実行環境の検証**(研究室 Windows 機での全体確認)

- Anaconda `venv` (Python 3.12.13) の依存パッケージ、TeX Live 2026 の `ptex2pdf`(日本語 jarticle の
  PDF 生成)、`update_history.ps1`、pandas 3.0.3 でのデータ読み込みを確認。いずれも正常
- `build_report.ps1` は `進捗報告/tex/20260716_report.tex` をビルド可能(使用パッケージ
  graphicx / multirow / wrapfig はすべて導入済み、図参照なし)

**CuPy が起動できない問題を修正**

- 原因: このPCの `CUDA_PATH` は CUDA Toolkit v13.2 を指していて `nvrtc64_130_0.dll` しか無いが、
  `cupy-cuda12x` は `nvrtc64_120_0.dll` を要求する。正しい DLL は pip の `nvidia-*-cu12` wheel 内に
  あるが、CuPy はそのディレクトリを DLL 検索パスに追加しないため見つけられなかった
- 対処: `venv` 内に `_cupy_cuda_path_fix.py` と `zzz_cupy_cuda_path_fix.pth` を追加し、
  wheel の bin を `os.add_dll_directory()` と `PATH` の両方に登録。`venv` 内だけに閉じており、
  `conda activate` の有無に関係なく効く
- `nvidia-cufft-cu12` 等を追加インストール。`cp.fft` / `cp.linalg` も含めて CuPy はフル動作
- RTX 3060 上で `UT_FlawVariation_Sim.run_simulation()` の完走を確認

**ドキュメント整備**

- `CLAUDE.md` の環境節を実態に合わせて更新(旧「macOS で動かない」注意書きを差し替え)
- `AGENTS.md`(このファイルの運用ルールを含む共通ルール)と `HANDOFF.md` を新規作成

### Antigravity への依頼

次の週次レポートに環境構築の記録を残す場合、上の「CuPy が起動できない問題を修正」の内容を
使ってください。レポート向けに要点をまとめると:

- 使用 GPU: NVIDIA GeForce RTX 3060 (12GB, compute capability 8.6)
- シミュレーション1条件あたりの計算時間: **約2.5分**(19,586 時間ステップ、約7ms/step +
  初期化約9秒)。`simdata.csv` の19条件をすべて回すと**約50分**
- 現時点での出力実績: `tmp_output/sim/` に79ファイル、`tmp_output/sim_csv/` に64ファイル

図が必要であれば、どのパラメータの波形が欲しいか書いてもらえれば Claude 側で生成します。

### 未解決・注意

- **監査ログの範囲**: `update_history.ps1` が集計しているのは Gemini CLI のログ
  (`~/.gemini/tmp/lab/chats/*.jsonl`)だけで、**Antigravity と Claude Code のセッションは
  記録されていません**。`Gemini.md` の学術的誠実性の要件を満たすには、両方のログも
  取り込むよう `scripts/render_llm_history.py` を拡張する必要があります(未着手)
- `.vscode/tasks.json` が存在しないため、`Gemini.md` が言及している VS Code タスク
  「Update LLM History」は現状 UI から実行できません(PowerShell からは実行可能)
- `sourse_new_2.py` の `doc_path` (`C:/Users/cs16/Roughness/project4`) は
  `Simulation_Data/`・`Experiment_Data/` が無く、これを import するプロット系スクリプトは
  そのままでは動きません

---

## 2026-09-17 (2) — Claude Code

### やったこと

**監査ログを3ソース対応にした**(上の「未解決」だった項目)

- `scripts/render_llm_history.py` を書き換え、Gemini CLI に加えて **Claude Code**
  (`~/.claude/projects/c--Users-cs16-lab/*.jsonl`) を自動で取り込むようにした。
  タイムスタンプは UTC から JST に変換し、ツール呼び出しの往復や `<system-reminder>` などの
  制御ブロックは除外している
- **Antigravity は会話がローカルに残らない**(`state.vscdb` にあるのは base64 protobuf の
  タイトル要約のみ、かつ同じ DB に OAuth トークンがある)ため、自動取り込みは断念。
  代わりに `進捗報告/antigravity_log/YYYYMMDD.md` への**手動記録**を取り込む方式にした
- 出力は `# Gemini CLI` / `# Claude Code` / `# Antigravity` のセクションに分かれる

**その他の環境整備**

- `.vscode/tasks.json` を作成(Update LLM History / Build Report / Run Simulation Sweep /
  Check GPU)。Antigravity も VS Code ベースなので同じタスクが使える
- `.vscode/settings.json` を作成(既定インタープリタを `venv` に固定、巨大ディレクトリを
  検索・監視から除外)
- `.gitignore` を修正。`text/`(657MB)と LaTeX 中間ファイルを除外し、`.vscode/` の
  ディレクトリ除外を `.vscode/*` に直して `!` の例外指定が効くようにした
- `environment.yml` / `requirements.txt` / `SETUP.md` を作成

### Antigravity への依頼

**今日から `進捗報告/antigravity_log/YYYYMMDD.md` への記録をお願いします。**
書式は同ディレクトリの `README.md`、背景は `Gemini.md` 2章にあります。
記録が無いと、その日の Antigravity の利用は監査ログに一切残りません。

### 未解決・注意

- **`.git` に約2.7GB の不要データが残っている**。到達不能な巨大 blob(1085MB/1058MB/704MB ほか)で、
  2026-07-10 の `reset` の残骸。掃除コマンドは Claude 側の権限設定で拒否されるため、
  ユーザーが手動で実行する必要がある(下記)
- **git のリモートが未設定**でバックアップが Google Drive のみ。`.git` の掃除後に
  GitHub private リポジトリの設定を推奨
