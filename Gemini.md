# プロジェクト構成と AI 利用監査ログ (GEMINI.md)

このファイルは、プロジェクトの構成管理および学術的誠実性（Academic Integrity）を担保するための AI 利用履歴（監査ログ）を記録するものです。

---

## 1. プロジェクト構成 (Directory Structure)

```text
C:\Users\cs16\lab\
├── build_report.ps1           # LaTeX レポート作成用自動化スクリプト
├── update_history.ps1         # LLM 会話ログ更新用スクリプト
├── pic/                       # 解析結果や実験のスクリーンショット
├── scripts/                   # 汎用スクリプト（ログ解析など）
│   ├── render_llm_history.py  # ログ変換プロセッサ
│   └── history.db             # ログ管理用 SQLite DB
├── text/                      # プレゼン構成案などのテキスト原稿 (Markdown)
│   └── mml/                   # 数理統計・機械学習関連の構成案と画像
├── vscode/
│   ├── md/                    # シミュレーションや解析手法の解説資料
│   └── simulation/            # メインの解析・シミュレーション環境
│       ├── sourse_new_2.py    # 信号処理共通ライブラリ (FFT, 正規化, プロット等)
│       ├── sourse_new_2_Usage.md # ライブラリの使用説明書
│       ├── plot_experimental_only.py # 実験データ (patA) のプロット用スクリプト
│       ├── UT_FlawVariation_Sim.py   # シミュレーション実行コード（関数化済み）
│       ├── loop_UT_sim.py            # パラメータを変えてシミュレーションをループ実行するスクリプト
│       ├── simdata.csv               # ループ実行用パラメータ設定ファイル
│       ├── data/              # 解析用データ (CSV等)
│       └── tmp_output/        # 生成された図の出力先
├── 試験問題/                  # 過去の試験問題・回答資料 (PDF, Zip)
├── 資料/                      # 超音波関連の論文、スライド資料 (PPTX, PDF)
│   └── 済/                    # 過去の輪読資料（参考用）
└── 進捗報告/                  # 週次進捗報告
    ├── gemini_log/            # AI 利用監査ログ (YYYYMMDD.md)
    ├── tex/                   # レポートの LaTeX ソース
    └── template/              # レポート作成用テンプレート
```

---

## 2. AI 利用監査ログ (AI Utilization Audit Log)

研究の透明性、客観性、および再現性を担保するため、AI の利用履歴を正確に記録します。
詳細な監査ログ（プロンプト、出力、検証プロセス）は、以下のディレクトリに日付別のファイルとして保存されます。

**保存先**: `進捗報告/gemini_log/YYYYMMDD.md`

### ログ生成システム
Gemini CLI の会話ログを自動的に集計し、人間が読みやすい Markdown 形式に変換するシステムを導入しています。

- **`scripts/render_llm_history.py`**: 会話ログ (JSONL) を解析し、SQLite データベースで管理・レンダリングする本体スクリプト。
- **`update_history.ps1`**: ログ更新用 PowerShell スクリプト。
- **VS Code Task**: `Update LLM History` を実行することで、いつでも最新のログを生成できます。

### 記録項目
1. **利用環境**: 利用日、モデル名・バージョン。
2. **利用目的と適用範囲**: 実験のどのプロセスで利用したか。
3. **入力プロンプトと生成結果**: 具体的な指示と出力の要約。
4. **事実確認（ファクトチェック）**: 一次情報源やコード検証による妥当性の確認。
5. **最終成果物への反映方法**: 引用か再構築かの区別。

---

## 3. 進捗報告（LaTeX）の作成手順

週次の進捗報告書 (PDF) を作成するための標準的な手順です。

### 作成フロー
1.  **画像の準備**: シミュレーションや実験で生成された画像が `tmp_output/` または `vscode/simulation/tmp_output/` に配置されていることを確認する。
2.  **LaTeX ソースの作成**: `進捗報告/tex/YYYYMMDD_report.tex` を作成または更新する。
    -   **画像の参照**: `\includegraphics` では、`tex` ディレクトリからの相対パス（例: `../../tmp_output/image.png`）を正確に指定する。
    -   **特殊文字の注意**: URL などにアンダースコア (`_`) が含まれる場合は、`\url{...}` でラップしてコンパイルエラーを防ぐ。
3.  **ビルドの実行**: ルートディレクトリで以下のコマンドを実行する。
    ```powershell
    .\build_report.ps1 [ファイル名]
    ```
    例: `.\build_report.ps1 20260528_report_v2`
4.  **成果物のリネーム**: 生成された PDF を提出形式（`YYYYMMDD.pdf`）にリネームして保存する。

### 注意事項
-   **文字コード**: LaTeX ソースは UTF-8 (BOMなし) で保存すること。
-   **中間ファイル**: `build_report.ps1` は正常終了時に `.aux`, `.log` 等の中間ファイルを自動的にクリーンアップする。

