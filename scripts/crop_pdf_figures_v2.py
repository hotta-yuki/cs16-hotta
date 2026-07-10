import fitz  # PyMuPDF
import os

"""
PDF の各ページから「図や表のキャプション」を特定し、
その図本体を含めた領域を正確に切り出して JPG 保存するスクリプト (改良版)。
"""

pdf_path = r"text/0522/2025_藤井滉太郎.pdf"
output_dir = r"text/0522/extracted_jpgs_v2"
os.makedirs(output_dir, exist_ok=True)

def crop_figures_refined():
    doc = fitz.open(pdf_path)
    count = 0
    
    print(f"Refining figure/table extraction: {pdf_path}")
    
    for page_index in range(len(doc)):
        page = doc[page_index]
        zoom = 300 / 72  # 300 DPI
        mat = fitz.Matrix(zoom, zoom)
        
        # ページ内のテキストブロックを取得
        blocks = page.get_text("blocks")
        
        # 「Fig.」または「Table」で始まるブロック（キャプション）を特定
        for block in blocks:
            text = block[4].strip()
            # 「Fig. x.x」または「Table x.x」で始まるものをキャプションとみなす
            # 文中の引用（(Fig. x.x) など）を避けるため、ブロックの先頭を厳密にチェック
            if text.startswith("Fig.") or text.startswith("Table"):
                rect = fitz.Rect(block[:4])
                
                # キャプションの直上にある図を切り出す
                # ※ 論文のレイアウトに合わせて高さを調整 (350pt 程度)
                crop_rect = fitz.Rect(0, max(0, rect.y0 - 350), page.rect.width, rect.y1 + 10)
                
                # ファイル名のクリーンアップ
                safe_name = text.split("\n")[0][:30].replace(".", "_").replace(" ", "_").replace(":", "").replace("/", "_")
                
                # クロップして保存
                pix = page.get_pixmap(matrix=mat, clip=crop_rect)
                img_filename = f"page{page_index+1:02d}_{safe_name}.jpg"
                img_path = os.path.join(output_dir, img_filename)
                
                pix.save(img_path)
                count += 1
                # print(f"    Extracted: {safe_name}")

    doc.close()
    print(f"\nDone. Extracted {count} figures/tables to {output_dir}")

if __name__ == "__main__":
    crop_figures_refined()
