import fitz  # PyMuPDF
import os

"""
PDF から埋め込み画像を抽出し、JPG として保存するスクリプト。
"""

pdf_path = r"text/0522/2025_藤井滉太郎.pdf"
output_dir = r"text/0522/extracted_images"
os.makedirs(output_dir, exist_ok=True)

def extract_images():
    doc = fitz.open(pdf_path)
    img_count = 0
    
    print(f"Opening PDF: {pdf_path}")
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        
        if image_list:
            print(f"  Page {page_index + 1}: Found {len(image_list)} images")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            # 出力ファイル名 (ページ番号_画像番号)
            img_filename = f"page{page_index+1:02d}_img{img_index+1:02d}.{ext}"
            img_path = os.path.join(output_dir, img_filename)
            
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            img_count += 1
            # print(f"    Saved: {img_filename}")

    doc.close()
    print(f"\nDone. Extracted {img_count} images to {output_dir}")

if __name__ == "__main__":
    extract_images()
