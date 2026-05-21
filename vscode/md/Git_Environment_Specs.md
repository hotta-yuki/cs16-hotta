# Git環境仕様書 (Git Environment Specifications)

このプロジェクトでは、ソースコードのバージョン管理および開発履歴の保存のために Git を導入しています。

## 1. インストール情報
- **Git本体**: Git for Windows (C:\Program Files\Git\cmd\git.exe)
- **設定済ユーザー**:
  - Name: Yuki Hotta
  - Email: hotta@example.com

## 2. リポジトリ構成
- **初期化日**: 2026年5月21日
- **メインブランチ**: `main`

## 3. 除外設定 (.gitignore)
以下のファイルおよびディレクトリは、バイナリサイズや機密性、自動生成の観点から Git の管理対象外としています。

### 自動生成ファイル
- `__pycache__/`: Pythonコンパイル済みキャッシュ
- `tmp_output/`: シミュレーション結果や図の出力先
- `tmp/`: 一時作業ディレクトリ

### 大規模バイナリ・アーカイブ
- `install-tl-20260520/`, `install-tl.zip`: TeX Live インストーラー
- `試験問題/`: 過去問PDF等
- `資料/`: 参考文献PDF、PowerPoint等
- `pic/`: スクリーンショット画像

### その他
- `進捗報告/**/*.pdf`: 生成されたレポートPDF（ソースの .tex は管理対象）

## 4. 基本的な操作方法
現在の環境では `git` コマンドが標準の `PATH` に通っていない場合があるため、VS Code の統合ターミナル（PowerShell）では以下のエイリアス設定またはフルパスでの利用を推奨します。

```powershell
# エイリアス設定例
$git = "C:\Program Files\Git\cmd\git.exe"
& $git status
```

### 推奨ワークフロー
1. **変更の確認**: `git status`
2. **ステージング**: `git add <ファイル名>`
3. **コミット**: `git commit -m "変更内容の簡潔な説明"`
4. **履歴の確認**: `git log --oneline`

## 5. 参考資料
- [Gitのインストールから使い方まで (Qiita)](https://qiita.com/kouatht/items/7a8b935e6885d22ff62e)
- [Git チュートリアル (Qiita - 参照先)](https://qiita.com/takeru-hirai/items/4fbe6593d42f9a844b1c)
