# SETUP.md — 環境構築手順

このリポジトリを別の Windows マシンで動かす、または現在の環境を作り直すための手順です。
役割分担や日々の運用ルールは `AGENTS.md` を参照してください。

検証日: 2026-09-17 / 検証機: Windows 11 + Anaconda + NVIDIA GeForce RTX 3060 (12GB)

---

## 1. 必要なもの

| | バージョン | 備考 |
|---|---|---|
| Anaconda | Python 3.12 系の env を作れるもの | base は 3.13 でも可 |
| NVIDIA ドライバ | CUDA 12.x 以降に対応するもの | 検証機は 591.86 (CUDA 13.1) |
| TeX Live | 2026 | **pTeX/upTeX (`ptex2pdf`)** を使う。pdflatex/xelatex ではない |

CUDA Toolkit のインストールは**必須ではありません**。CUDA のライブラリは pip の
`nvidia-*-cu12` wheel から供給します（3章参照）。

---

## 2. Python 環境

```powershell
& "C:\Users\cs16\anaconda3\shell\condabin\conda-hook.ps1"

# 完全再現する場合
conda env create -n venv -f environment.yml

# pip だけで最小構成を組む場合
conda create -n venv python=3.12
conda activate venv
pip install -r requirements.txt
```

このプロジェクトの Python は**必ず `venv` 環境**を使います。base 環境では CuPy が入っていません。
`.vscode/settings.json` で VS Code / Antigravity の既定インタープリタも `venv` に設定済みです。

---

## 3. CuPy の CUDA DLL 設定（重要）

**症状**: 何もしないと CuPy は次のエラーで落ちます。

```
RuntimeError: CuPy failed to load nvrtc64_120_0.dll
```

**原因**: 検証機の `CUDA_PATH` は CUDA Toolkit v13.2 を指していて `nvrtc64_130_0.dll` しか
持っていませんが、`cupy-cuda12x` は `nvrtc64_120_0.dll`（CUDA 12 系）を要求します。
正しい DLL は pip の `nvidia-cuda-nvrtc-cu12` wheel（`site-packages/nvidia/cuda_nvrtc/bin`）に
ありますが、CuPy は `%CUDA_PATH%\bin` と `cupy/.data/lib` しか DLL 検索パスに追加しないため
見つけられません。

**対処**: `venv` の `site-packages` に次の2ファイルを置きます。これで `conda activate` の
有無に関係なく、VS Code や Antigravity からの起動でも自動的に効きます。

`<venv>/Lib/site-packages/_cupy_cuda_path_fix.py`:

```python
import os
import sys
import glob

_added = []

if sys.platform == "win32":
    _pattern = os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "*", "bin")
    for _d in sorted(glob.glob(_pattern)):
        if not os.path.isdir(_d):
            continue
        try:
            os.add_dll_directory(_d)
        except OSError:
            continue
        _added.append(_d)

    if _added:
        os.environ["PATH"] = os.pathsep.join(_added) + os.pathsep + os.environ.get("PATH", "")
```

`<venv>/Lib/site-packages/zzz_cupy_cuda_path_fix.pth`（1行だけ）:

```
import _cupy_cuda_path_fix
```

**なぜ2通りの登録が必要か**: `os.add_dll_directory()` は Python (ctypes) が
`nvrtc64_120_0.dll` を開くために必要で、`PATH` は nvrtc 自身が内部で
`nvrtc-builtins64_129.dll` を読むために必要です。片方だけでは別のエラーになります。

**なぜ `CUDA_PATH` を書き換えないか**: システムの `CUDA_PATH` を変えると、この PC の
他の CUDA 13.2 利用に影響するためです。上の方法なら影響は `venv` の中だけに閉じます。

### 動作確認

```powershell
python -c "import cupy as cp; print((cp.arange(10)*2).sum()); print(abs(cp.fft.fft(cp.arange(8, dtype=cp.float64)))[0])"
```

VS Code / Antigravity からは タスク **「Check GPU (CuPy)」** でも確認できます。

---

## 4. LaTeX

TeX Live 2026 をインストールし、`ptex2pdf` に PATH を通します
（既定: `C:\texlive\2026\bin\windows`）。`build_report.ps1` は PATH に無い場合、
このパスにフォールバックします。

レポートは `jarticle` + `\usepackage[dvipdfmx]{graphicx}` で、UTF-8 (BOM なし) で保存します。

---

## 5. 動作確認チェックリスト

```powershell
# Python とパッケージ
python -c "import numpy, scipy, pandas, matplotlib, japanize_matplotlib, PIL, pptx, fitz, tkinter; print('OK')"

# GPU
python -c "import cupy as cp; print(cp.cuda.Device(0).compute_capability)"

# LaTeX
ptex2pdf -v

# レポートのビルド
.\build_report.ps1

# 監査ログの更新
.\update_history.ps1
```

---

## 6. 既知の制約

- `sourse_new_2.py` の `doc_path`（`C:/Users/cs16/Roughness/project4`）に
  `Simulation_Data/`・`Experiment_Data/` が無く、これを import するプロット系スクリプトは
  そのままでは動きません。使う前にパスを実在する場所へ向けてください。
- スクリプト内のパスは Windows 前提でハードコードされています。リポジトリは Google Drive で
  同期されているため macOS から開くこともできますが、その場合これらは解決できません。
- 依存パッケージに `requirements.txt` の pin がありますが、`environment.yml` のほうが
  conda 由来のパッケージを含むぶん再現性が高いです。
