import fitz  # PyMuPDF
import os

"""
PDF の各ページを画像化し、「Fig.」や「Table」というキーワードの周辺を
自動で切り出して JPG として保存するスクリプト。
"""

pdf_path = r"text/0522/2025_藤井滉太郎.pdf"
output_dir = r"text/0522/extracted_jpgs"
os.makedirs(output_dir, exist_ok=True)

def crop_figures():
    doc = fitz.open(pdf_path)
    count = 0
    
    print(f"Analyzing PDF for figures and tables: {pdf_path}")
    
    for page_index in range(len(doc)):
        page = doc[page_index]
        
        # ページを画像化 (DPI=300)
        zoom = 300 / 72  # 300 DPI
        mat = fitz.Matrix(zoom, zoom)
        
        # 「Fig.」や「Table」を検索
        # ※ 論文のスタイルに合わせて調整
        targets = page.search_for("Fig.") + page.search_for("Table")
        
        if not targets:
            continue
            
        print(f"  Page {page_index + 1}: Found {len(targets)} potential figures/tables")
        
        # 各ターゲット（キャプション位置）の「上」にある図を推定して切り出す
        # 簡易的なロジック：キャプションの上方一定範囲を切り出し
        for i, rect in enumerate(targets):
            # 切り出し範囲の決定 (キャプションの少し下から、ページ上部に向かって)
            # キャプション文字列そのものも含める
            
            # キャプション周辺のテキストを取得して識別名にする
            text_around = page.get_text("text", clip=rect).strip()
            # 無効な文字を置換
            safe_name = text_around.replace(".", "_").replace(" ", "_").replace(":", "")
            
            # 図の領域を推定 (キャプションの上 400pt 分 + キャプション 50pt 分)
            # PDFの座標系は上が0
            crop_rect = fitz.Rect(0, max(0, rect.y0 - 300), page.rect.width, rect.y1 + 20)
            
            # クロップして保存
            pix = page.get_pixmap(matrix=mat, clip=crop_rect)
            img_filename = f"page{page_index+1:02d}_{safe_name}.jpg"
            img_path = os.path.join(output_dir, img_filename)
            
            pix.save(img_path)
            count += 1
            # print(f"    Saved: {img_filename}")

    doc.close()
    print(f"\nDone. Saved {count} JPG files to {output_dir}")

if __name__ == "__main__":
    crop_figures()
