"""Markdown(数式・画像入り)を iPad などで読める PDF に変換する。

marked.js で Markdown を、KaTeX で $...$ / $$...$$ の数式を描画した HTML を作り、
ヘッドレス Chrome で PDF に印刷する。画像は Markdown からの相対パスで解決される。

    python scripts/md_to_pdf.py <input.md> [-o output.pdf] [--keep-html]

出力の既定は output/reading/<入力名>.pdf(output/ は gitignore 済みで Drive 同期される)。
"""
import argparse
import html
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

TEMPLATE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<base href="{base}">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
body {{ font-family: "Hiragino Mincho ProN", "Yu Mincho", serif; font-size: 11pt;
       line-height: 1.75; color: #111; }}
h1, h2, h3, h4 {{ font-family: "Hiragino Sans", "Yu Gothic", sans-serif; line-height: 1.4;
                 break-after: avoid; }}
h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4px; }}
h2 {{ font-size: 14pt; border-bottom: 1px solid #999; }}
h3 {{ font-size: 12pt; }}
img {{ max-width: 100%; display: block; margin: 8px auto; break-inside: avoid; }}
table {{ border-collapse: collapse; margin: 8px 0; font-size: 9.5pt; break-inside: avoid; }}
th, td {{ border: 1px solid #888; padding: 3px 6px; }}
th {{ background: #eee; }}
.katex-display {{ overflow-x: auto; overflow-y: hidden; }}
code {{ font-size: 9.5pt; }}
hr {{ border: none; border-top: 1px solid #ccc; }}
</style></head><body><div id="out"></div>
<script id="src" type="application/json">{src}</script>
<script>
const src = JSON.parse(document.getElementById('src').textContent);
// 数式を退避してから Markdown を処理する(_ や * が強調として解釈されるのを防ぐ)
const math = [];
const stash = (tex, display) => {{ math.push({{tex, display}}); return `@@MATH${{math.length - 1}}@@`; }};
let text = src
  .replace(/\\$\\$([\\s\\S]+?)\\$\\$/g, (_, t) => stash(t, true))
  .replace(/\\\\\\[([\\s\\S]+?)\\\\\\]/g, (_, t) => stash(t, true))
  .replace(/(^|[^\\\\$])\\$([^$\\n]+?)\\$/g, (_, pre, t) => pre + stash(t, false));
let out = marked.parse(text);
out = out.replace(/@@MATH(\\d+)@@/g, (_, i) => {{
  const m = math[+i];
  try {{ return katex.renderToString(m.tex, {{displayMode: m.display, throwOnError: false}}); }}
  catch (e) {{ return '<code>' + m.tex + '</code>'; }}
}});
document.getElementById('out').innerHTML = out;
</script></body></html>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    sys.exit("Chrome が見つかりません。CHROME_CANDIDATES にパスを追加してください。")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--keep-html", action="store_true", help="中間 HTML を PDF の隣に残す")
    args = ap.parse_args()

    md = args.input.resolve()
    pdf = (args.output or REPO / "output" / "reading" / (md.stem + ".pdf")).resolve()
    pdf.parent.mkdir(parents=True, exist_ok=True)

    page = TEMPLATE.format(
        base=md.parent.as_uri() + "/",
        title=html.escape(md.stem),
        # </script> で JSON が途切れないようにエスケープ
        src=json.dumps(md.read_text(encoding="utf-8")).replace("</", "<\\/"),
    )
    tmp_html = pdf.with_suffix(".html")
    tmp_html.write_text(page, encoding="utf-8")

    subprocess.run([
        find_chrome(), "--headless", "--disable-gpu", "--allow-file-access-from-files",
        "--no-pdf-header-footer", "--virtual-time-budget=30000",
        f"--print-to-pdf={pdf}", tmp_html.as_uri(),
    ], check=True, capture_output=True)

    if not args.keep_html:
        tmp_html.unlink()
    print(f"wrote {pdf} ({pdf.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
