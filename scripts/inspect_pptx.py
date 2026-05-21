from pptx import Presentation
import os

pptx_path = r'資料\GMM_Presentation_fixed.pptx'

if not os.path.exists(pptx_path):
    print(f"File not found: {pptx_path}")
    exit(1)

prs = Presentation(pptx_path)

for i, slide in enumerate(prs.slides):
    print(f"--- Slide {i+1} ---")
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            # Only print shapes that have text and look like they might contain math (e.g. backslashes, underscores, carets)
            text = shape.text.strip()
            if text:
                print(f"  [Shape] {text}")
