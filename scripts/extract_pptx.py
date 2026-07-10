import zipfile
import re
import sys

def extract_text_from_pptx(pptx_path):
    with zipfile.ZipFile(pptx_path, 'r') as z:
        slide_xmls = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
        # Sort slides numerically
        slide_xmls.sort(key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))
        
        for slide_xml in slide_xmls:
            xml_content = z.read(slide_xml).decode('utf-8')
            # Extract text from a:t tags
            texts = re.findall(r'<a:t>(.*?)</a:t>', xml_content)
            print(f"--- {slide_xml} ---")
            for t in texts:
                if t.strip():
                    print(t)
            print()

if __name__ == '__main__':
    extract_text_from_pptx(sys.argv[1])