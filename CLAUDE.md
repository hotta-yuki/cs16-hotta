# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

**Read `AGENTS.md` first (imported above).** This project is worked on by two agents: Antigravity
(Gemini) owns *prose* — the weekly LaTeX reports, manuscripts, slide text — and Claude Code owns
*code and reasoning*. `AGENTS.md` holds the shared contract (role split, directory ownership, the
`HANDOFF.md` protocol, environment, commands) and is authoritative on those points; this file adds
the Claude-side depth. Do not write report prose yourself — put the material (figures with real
paths, numbers with units, bullet facts) into `HANDOFF.md` for Antigravity instead. Check the end of
`HANDOFF.md` before starting work, and append an entry when handing something back.

> 📝 補足: このリポジトリは Antigravity(文章担当)と Claude Code(コード・推論担当)の2つで作業します。
> 共通ルールは `AGENTS.md`、相手への引き継ぎは `HANDOFF.md` です。

> **日本語での補足について**: このファイルは Claude Code が参照する技術文書のため英語で記述していますが、
> ユーザー(第一言語が日本語)向けに、各セクションの末尾に日本語の要約(`📝 補足:`)を添えています。
> `Gemini.md` と、既存のシミュレーション/レポート運用フロー(Windows + Anaconda + PowerShell + ptex2pdf)は
> このドキュメントによって変更されません。あくまで既存の運用を Claude Code に説明するための追記です。

## Project overview

This is a research lab repository for ultrasonic testing (UT) FDTD (finite-difference time-domain)
simulation research: simulating elastic wave propagation in steel plates with saw-tooth/rectangular
flaws, comparing simulated waveforms against experimental scope data, and producing weekly LaTeX
progress reports. See `Gemini.md` for the authoritative directory map, the AI-usage audit log
requirements, and the report build procedure — read it before making structural changes.

**Research goals:** the near-term goal is understanding *double mode conversion* (P-wave↔S-wave
conversion occurring twice at a flaw during scattering/reflection) — this is what the
`vscode/project1/`/`vscode/project2/` mode-conversion visualization forks are for. The longer-term
goal is to enable *inverse estimation* (recovering flaw parameters from observed waveforms) using a
PINN (Physics-Informed Neural Network). Keep this direction in mind when scoping analysis or
feature-extraction work (e.g. `extract_features.py`, `simulation_features.csv`) — it may end up
feeding a future PINN training/constraint pipeline.

**Verified environment (2026-09-17, lab Windows PC):** this machine *is* the Windows/Anaconda setup
the scripts assume, and the toolchain was checked end to end — Anaconda env `venv` (Python 3.12.13)
with every required package, TeX Live 2026 `ptex2pdf` (Japanese jarticle build confirmed),
`update_history.ps1` (runs against `C:\Users\cs16\anaconda3\python.exe`, Python 3.13, stdlib only),
and the CuPy FDTD solver on an RTX 3060. The working copy is still synced via Google Drive, so it
may also be opened on macOS, where the hardcoded `C:\...` paths in `update_history.ps1`,
`build_report.ps1` and `sourse_new_2.py` will not resolve.

**CuPy / CUDA setup on this machine — do not remove:** `CUDA_PATH` points at CUDA Toolkit v13.2,
which ships only `nvrtc64_130_0.dll`, while `cupy-cuda12x` requires `nvrtc64_120_0.dll`. The correct
DLLs live in the pip `nvidia-*-cu12` wheels under `site-packages/nvidia/*/bin`, but CuPy only adds
`%CUDA_PATH%\bin` and `cupy/.data/lib` to its DLL search path, so it cannot find them. Two files in
the env fix this by registering those wheel dirs through both `os.add_dll_directory()` and `PATH`
(both are needed — nvrtc itself loads `nvrtc-builtins64_129.dll` via `PATH`):

- `<venv>/Lib/site-packages/_cupy_cuda_path_fix.py`
- `<venv>/Lib/site-packages/zzz_cupy_cuda_path_fix.pth`

This is scoped to `venv` only (the base env and the system `CUDA_PATH` are untouched) and applies to
every interpreter launch, including VS Code's, without needing `conda activate`. Deleting the two
files reverts it. `cp.fft` / `cp.linalg` additionally need the `nvidia-cufft-cu12`,
`nvidia-cublas-cu12`, `nvidia-cusolver-cu12`, `nvidia-cusparse-cu12` and `nvidia-curand-cu12` wheels,
which are installed; the hook picks up any `nvidia/*/bin` dir automatically.

**Runtime cost:** one `run_simulation()` call is 19,586 time steps at roughly 7 ms/step plus ~9 s of
`isfree()`/`around_free()` Python-loop setup — **about 2.5 minutes per parameter combination**. The
19 combinations currently in `simdata.csv` take **roughly 50 minutes** in total.

**Data locations that are not self-evident:** `sourse_new_2.py`'s `doc_path`
(`C:/Users/cs16/Roughness/project4`) exists on this machine but currently holds only
`animation_files` — the `Simulation_Data/` and `Experiment_Data/` trees it expects are absent, so
the plotting scripts that import it need their paths pointed somewhere real first.
`calculate_avg_waveforms.py` is fine: its `vscode/simulation/data/` (`ex_index.csv`, `ex_data/`) and
`tmp_output/sim_csv/` are both populated. `loop_UT_sim.py` reads `simdata.csv` via a relative path,
so it must be run from the repo root.

> 📝 補足: 本リポジトリは超音波探傷(UT)のFDTDシミュレーション研究用です。詳細な構成やAI利用監査ログの
> ルールは `Gemini.md` を参照してください(このCLAUDE.mdは`Gemini.md`の内容を置き換えるものではありません)。
> **環境について(2026-09-17 研究室Windows機で検証済み)**: この機体はスクリプトが想定するWindows/Anaconda
> 環境そのもので、Anaconda環境`venv`(Python 3.12.13)の全依存パッケージ、TeX Live 2026の`ptex2pdf`
> (日本語jarticleのPDF生成)、`update_history.ps1`、RTX 3060上でのCuPy版FDTDソルバーまで一通り動作を
> 確認しました。ただしGoogle Drive同期のためmacOS上から開かれる可能性は残っており、その場合は
> `update_history.ps1`・`build_report.ps1`・`sourse_new_2.py`内の`C:\...`ハードコードパスは解決できません。
>
> **CuPy/CUDAの設定(削除しないこと)**: このPCの`CUDA_PATH`はCUDA Toolkit v13.2を指しており
> `nvrtc64_130_0.dll`しかありませんが、`cupy-cuda12x`は`nvrtc64_120_0.dll`を要求します。正しいDLLは
> pipの`nvidia-*-cu12` wheel(`site-packages/nvidia/*/bin`)にありますが、CuPyは`%CUDA_PATH%\bin`と
> `cupy/.data/lib`しかDLL検索パスに追加しないため見つけられません。これを解決するため、venv内に
> `_cupy_cuda_path_fix.py`と`zzz_cupy_cuda_path_fix.pth`の2ファイルを置き、wheelのbinディレクトリを
> `os.add_dll_directory()`と`PATH`の両方に登録しています(nvrtc自身が`nvrtc-builtins64_129.dll`を
> `PATH`経由で読むため両方必要)。影響範囲は`venv`内だけで(base環境とシステムの`CUDA_PATH`は無変更)、
> `conda activate`の有無に関係なくVS Codeからの起動でも効きます。2ファイルを削除すれば元に戻ります。
> `cp.fft`/`cp.linalg`には`nvidia-cufft-cu12`等のwheelが追加で必要で、これらも導入済みです。
>
> **実行時間の目安**: `run_simulation()`1回は19,586ステップ(約7ms/step)＋初期化約9秒で
> **1条件あたり約2.5分**。現在の`simdata.csv`の19条件をすべて回すと**約50分**です。
>
> **データ配置の注意**: `sourse_new_2.py`の`doc_path`(`C:/Users/cs16/Roughness/project4`)は存在しますが
> 中身は`animation_files`だけで、期待される`Simulation_Data/`・`Experiment_Data/`がありません。これを
> importするプロット系スクリプトは、先にパスを実在する場所へ向ける必要があります。
> `calculate_avg_waveforms.py`が使う`vscode/simulation/data/`(`ex_index.csv`・`ex_data/`)と
> `tmp_output/sim_csv/`は揃っています。`loop_UT_sim.py`は`simdata.csv`を相対パスで読むため、
> リポジトリルートから実行してください。
>
> **研究目標**: 当面の目標は「二重モード変換」(欠陥での散乱・反射時にP波↔S波変換が2回起こる現象)を
> 理解すること(`vscode/project1/`・`vscode/project2/`のモード変換可視化はこのための取り組み)。
> 最終的な目標はPINN(物理情報ニューラルネットワーク)を用いて、観測波形から欠陥パラメータを逆推定
> できるようにすること。特徴量抽出(`extract_features.py`等)やデータ整理は、将来のPINN学習用データ
> 作成につながる可能性があることを意識する。

## Commands

There is no package manifest (no `requirements.txt`/`environment.yml`/`pyproject.toml`) and no test
suite. Dependencies are inferred from imports and installed into an Anaconda env named `venv`:
`numpy`, `cupy` (GPU FDTD — requires CUDA), `pandas`, `scipy`, `matplotlib`, `japanize_matplotlib`,
Pillow, `python-pptx`, `PyMuPDF` (`fitz`), `tkinter`.

Activate the environment (PowerShell, Windows):
```powershell
& "C:\Users\cs16\anaconda3\shell\condabin\conda-hook.ps1"
conda activate venv
```

Run a parameter sweep of the FDTD simulation (reads `vscode/simulation/simdata.csv`, skips
combinations already present in `tmp_output\sim` / `data_im\simdata_out`):
```
python vscode/simulation/loop_UT_sim.py
```

Run a single simulation programmatically by importing the solver:
```python
import UT_FlawVariation_Sim as sim
sim.run_simulation(f_width, f_pitch, f_depth)  # writes tmp_output/sim/sim_pitch{..}_depth{..}_width{..}.csv
```

Build a weekly LaTeX progress report (auto-discovers the `tex` dir, runs `ptex2pdf` — pTeX/upTeX,
not pdflatex/xelatex — twice, then cleans `.aux`/`.log`):
```powershell
.\build_report.ps1 [report_filename_without_extension]
```

Regenerate the LLM-usage audit log into `進捗報告/gemini_log/YYYYMMDD.md`:
```powershell
.\update_history.ps1
# or directly:
python scripts/render_llm_history.py
```
`render_llm_history.py` ingests three sources: Gemini CLI JSONL and Claude Code JSONL
(`~/.claude/projects/c--Users-cs16-lab/*.jsonl`) automatically, plus **Antigravity's manually written
notes** in `進捗報告/antigravity_log/YYYYMMDD.md`. Antigravity is manual because it keeps no local
transcript — its `state.vscdb` holds only base64 protobuf title summaries alongside an OAuth token,
so it is not parsed. The rendered log groups sessions under a `# <tool>` heading per source.

`.vscode/tasks.json` now exists and exposes **Update LLM History**, **Build Report**, **Run
Simulation Sweep** and **Check GPU (CuPy)** — usable from both VS Code and Antigravity.
Dependencies are pinned in `environment.yml` (conda, authoritative) and `requirements.txt` (pip);
rebuild instructions, including the CuPy DLL hook, are in `SETUP.md`.

> 📝 補足: 監査ログは Gemini CLI・Claude Code・Antigravity の3ソースに対応しました。Antigravity だけは
> 会話がローカルに残らないため、`進捗報告/antigravity_log/YYYYMMDD.md` への手動記録が必要です
> (書式は同ディレクトリの README.md)。VS Code タスク(`tasks.json`)も作成済みで、Antigravity からも
> 同じタスクが使えます。依存パッケージは `environment.yml` と `requirements.txt` に固定し、
> 再構築手順は `SETUP.md` にまとめました。

## Architecture

### `vscode/simulation/` — canonical simulation + plotting pipeline
- `UT_FlawVariation_Sim.py` — 2D staggered-grid elastic FDTD solver (CuPy). `run_simulation(f_width,
  f_pitch, f_depth)` is the function other scripts import and call; `isfree()`/`around_free()` build
  the free-boundary masks for periodic saw-tooth flaws.
- `UT_FlawVariation_Sim_3d.py` — 3D extension of the same scheme (full stress tensor,
  `run_simulation_3d`), standalone, not imported elsewhere.
- `loop_UT_sim.py` — batch driver: parses `simdata.csv` (custom key/value text format, not CSV
  columns) into `f_width`/`f_pitch`/`f_depth` lists, runs `itertools.product` over them, calling
  `UT_FlawVariation_Sim.run_simulation()` for each combination.
- `sourse_new_2.py` — the shared library ("超音波実験・シミュレーション共通ライブラリ"): physical
  constants (rho, E, G, cl, ct, stiffness tensor components), mesh/time step parameters, and helpers
  (`kiritori2` for waveform windowing, `make_fftdata` for FFT) imported by `plot.py`,
  `plot_simdata.py`, `plot_simdata_compare.py`, `plot_rough_waveform.py`, `plot_smooth_waveform.py`,
  and `extract_features.py`. Its experiment/simulation data paths are hardcoded and meant to be
  edited per-use (see its docstring) — check them before running any script that imports it.
- `sourse_0211.py` — a separate, older helper module (wave-matrix construction, peak detection);
  not the shared library and not imported by the plotting scripts above.
- `calculate_avg_waveforms.py` — independent of `sourse_new_2.py`: averages experimental scope CSVs
  (indexed by `data/ex_index.csv`) per pitch/depth/width group, aligns peaks against the matching
  simulation output in `tmp_output/sim_csv/`, and writes comparison plots to `data/comparison_plots/`.
- `kukei_ani.py` — Tkinter/matplotlib GUI that runs the FDTD scheme and animates a rectangular-groove
  flaw; the one script with a real `argparse` CLI (`--pitch-mm`, `--depth-mm`, `--width-mm`,
  `--probe-width-mm`, `--output-dir`, `--save-interval`, `--global-downsample`,
  `--zoom-width-mm/height-mm`). Writes NPZ frame data meant to be played back by
  `animation_player_for_npz.py` (lives under `vscode/project1/`, not here).

> 📝 補足: `vscode/simulation/`が本体のシミュレーション＋プロット処理系です。`UT_FlawVariation_Sim.py`の
> `run_simulation()`が中核関数で、`loop_UT_sim.py`から呼ばれます。共通ライブラリ`sourse_new_2.py`は
> パスがハードコードされているため、使う前に中身を確認・編集する必要がある点に注意してください
> (`sourse_0211.py`は別物の古いヘルパーで、共通ライブラリではありません)。

### `vscode/project1/`, `vscode/project2/` — exploratory forks
Both are downstream experiments on mode-conversion visualization (P-wave↔S-wave scattering at flaw
corners), each copying/extending `UT_FlawVariation_Sim.py`, `sourse_new_2.py`/`sourse_0211.py`, and
several `kukei_ani*.py` variants from `vscode/simulation/` rather than importing them. Read each
project's `plan.md` before editing — they diverge from the canonical pipeline on purpose. Treat
`vscode/simulation/` as the source of truth for the core FDTD physics; changes there do not
propagate automatically to the project1/project2 copies.

> 📝 補足: `project1`と`project2`は`vscode/simulation/`をコピー・拡張したモード変換可視化の実験用フォークです。
> `vscode/simulation/`側を修正しても自動的には反映されないので、本体を直すか各プロジェクトの`plan.md`に
> 従って個別に手を入れるか、意識して使い分けてください。

### `scripts/` — cross-cutting tooling, three unrelated groups
- **LLM audit log**: `render_llm_history.py` parses Gemini CLI session JSONL logs into
  `scripts/history.db` (SQLite, tracked in git) and renders `進捗報告/gemini_log/YYYYMMDD.md`;
  invoked by `update_history.ps1`. This log is a required academic-integrity artifact per
  `Gemini.md` — don't delete or bypass it when scripting LLM-assisted work in this repo.
- **Report figure/animation pipeline**: `create_animation.py` / `create_gif.py` build
  animations/GIFs from PNG sequences already produced under `tmp_output/plots_simulation_*` (no CLI
  args — edit the hardcoded `input_dir`/`output_file` in their `__main__` blocks before running);
  `crop_pdf_figures.py`, `crop_pdf_figures_v2.py`, `extract_pdf_figures.py` extract/crop figures out
  of source PDFs (PyMuPDF) for reuse in slides/reports.
- **pptx pipeline**: `fix_pptx_math.py`, `inspect_pptx.py`, `restore_latex_to_pptx.py` operate on a
  specific presentation (`資料\GMM_Presentation_fixed.pptx`), restoring LaTeX-derived formulas from
  a markdown source back into the pptx — separate from the LaTeX→PDF report flow.
- `verify_matplotlib.py` — plain environment sanity check.

> 📝 補足: `scripts/`配下は目的の異なる3系統が混在しています。①`render_llm_history.py`
> (AI利用監査ログの生成、`Gemini.md`が要求する成果物なので削除・迂回しないこと)、②アニメーション/PDF図表
> 抽出系(`create_animation.py`等)、③pptx修復系(`fix_pptx_math.py`等、特定のプレゼンファイル専用)です。

### Generated/data directories are gitignored
`tmp/`, `tmp_output/`, `pic/`, `output/`, `data_im/` and similar are excluded via `.gitignore` (see
that file for the full list) — they hold regenerable simulation outputs and plots, not source of
truth. `scripts/history.db` is intentionally tracked despite being a generated SQLite file, since it
backs the audit log.

> 📝 補足: `tmp/`, `tmp_output/`, `pic/`, `output/`, `data_im/`等は`.gitignore`で除外されている
> 「再生成可能な出力」であり、正のデータではありません。一方`scripts/history.db`は生成物ですが
> 監査ログの実体を保持するため意図的にgit管理下に置かれています。

## Git — save the work, every time

The shared rules live in **`AGENTS.md` §10** (both agents read them); this is the Claude-side
depth. The repo is synced through Google Drive, which keeps only the latest state — git is the only
thing that can put a broken file back, so work that is not committed is work that can vanish.

- **Commit after each meaningful unit of code work**, and always **before appending to
  `HANDOFF.md`** — Antigravity needs a committed state to point at when it writes the report.
  Also commit before starting a ~50 min sweep or a report build.
- **Stage paths, not everything.** `git add vscode/... scripts/...`, never `git add -A`: Antigravity
  may have uncommitted prose in `進捗報告/tex/`, `text/` or `資料/`, and those are its commits to make.
- **Message format**: `<type>: <日本語の要約>` (`feat`/`fix`/`docs`/`refactor`/`chore`), body explains
  *why* plus any verification result — the diff already shows *what*. End Claude Code's commits with
  the `Co-Authored-By: Claude ...` trailer; it is part of the AI-usage record this repo must keep.
- **Never** `push`, `reset --hard`, `clean -fd`, `checkout -- <path>` or history rewrites — these are
  in the `deny` list below precisely because they destroy uncommitted work. `push` is the user's call;
  commit, then tell them it is ready to push.
- `scripts/history.db` and `進捗報告/gemini_log/` stay tracked (audit log); regenerable output
  (`tmp_output/`, `pic/`, `output/`, `data_im/`) stays ignored. New ignore entries get a comment
  saying why.

> 📝 補足: **作業は必ず git にコミットする**(共通ルールは `AGENTS.md` 10章)。Google Drive 同期は
> 最新状態しか持たないバックアップで、履歴ではありません。壊したものを戻せるのは git だけです。
> コード作業の区切りごと、そして **`HANDOFF.md` に追記する前**に必ずコミットしてください
> (Antigravity がレポートを書くとき、参照できる確定状態が必要になるため)。
> `git add -A` は使わず、自分が変更したパスだけを stage します(Antigravity の書きかけの原稿を
> 巻き込まないため)。`push`・`reset --hard`・`clean -fd`・`checkout -- <path>` は禁止で、
> push を実行するかどうかはユーザーが判断します。

## Claude Code の権限設定 (`.claude/settings.json`)

This repo has a minimal `.claude/settings.json` permissions allowlist for this single-user academic
workflow. JSON does not support comments, so the rationale is documented here instead of inline.

- `allow`: read-only git inspection (`status`/`diff`/`log`/`show`/`branch`), running Python scripts
  (`python`/`python3`), read-only pip/conda inspection (`pip list`/`show`/`freeze`,
  `conda env list`/`list`), and basic filesystem listing (`ls`, `find`, `pwd`, `wc`).
- `deny`: anything that pushes to a remote, rewrites git history destructively (`push`, `reset --hard`,
  `clean`, `checkout --`/`checkout .`), deletes recursively (`rm -rf`), or mutates the Python
  environment (`pip install/uninstall`, `conda install/remove`) — these still require explicit manual
  confirmation outside of Claude Code's permission system.

> 📝 補足(日本語): `.claude/settings.json`はJSON形式のためファイル内にコメントを書けません。ここに代わりに
> 意図をまとめます。
> - **許可(allow)**: git の状態確認系(status/diff/log/show/branch)、Pythonスクリプトの実行、
>   pip/condaの一覧・情報確認(インストールはしない)、ls/find/pwd/wcなどの基本的なファイル一覧表示。
> - **拒否(deny)**: `git push`、`git reset --hard`、`git clean`、`git checkout --`(変更の破棄)、
>   `rm -rf`(再帰削除)、`pip install/uninstall`、`conda install/remove`など、取り消しづらい操作や
>   環境を書き換える操作。これらは意図的に許可リストから外してあり、実行時は毎回確認が必要になります。
> - 研究室の単独ユーザー用リポジトリという前提で、必要最小限かつ安全側に倒した設定にしています。
>   チーム利用やCI導入など状況が変わった場合は見直してください。
