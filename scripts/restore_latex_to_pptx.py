import re
from pptx import Presentation
import os

md_path = r'text\mml\GMM_Presentation_Detailed_30.md'
pptx_path = r'資料\GMM_Presentation_fixed.pptx'
output_path = r'資料\GMM_Presentation_fixed_v3.pptx'

# 1. Extract formulas from Markdown
# We'll map them by slide number
formulas_by_slide = {}
current_slide = 0

with open(md_path, 'r', encoding='utf-8') as f:
    for line in f:
        slide_match = re.search(r'## スライド(\d+)', line)
        if slide_match:
            current_slide = int(slide_match.group(1))
            formulas_by_slide[current_slide] = []
        
        # Find all formulas in the slide
        # Inline $...$
        inline = re.findall(r'\$([^$]+)\$', line)
        if inline:
            formulas_by_slide[current_slide].extend(inline)
        
        # Block $$...$$
        block = re.findall(r'\$\$\s*(.+?)\s*\$\$', line)
        if block:
            formulas_by_slide[current_slide].extend(block)

# 2. Open PPTX
if not os.path.exists(pptx_path):
    print(f"File not found: {pptx_path}")
    exit(1)

prs = Presentation(pptx_path)

# 3. Try to match and replace
# This is tricky because the PPTX text is already corrupted.
# We'll look for shapes that contain typical math keywords in the slide.
for i, slide in enumerate(prs.slides):
    slide_num = i + 1
    if slide_num not in formulas_by_slide:
        continue
    
    target_formulas = formulas_by_slide[slide_num]
    if not target_formulas:
        continue
    
    # Simple strategy: If a shape has a backslash or a Greek-like character (mojibake)
    # and we have a formula for this slide, let's try to replace it.
    # This is a bit aggressive, but given the state of the file, it's probably what's needed.
    
    formula_idx = 0
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            text = shape.text
            # Look for math-like indicators
            if any(k in text for k in ["ﾎ", "ﾏ", "\\", "=", "p(", "rn", "Nk", "L ="]):
                if formula_idx < len(target_formulas):
                    # Replace the entire text of the shape with the clean LaTeX
                    # We'll wrap it in spaces to make it distinct
                    new_formula = target_formulas[formula_idx]
                    print(f"Slide {slide_num}: Replacing '{text[:30]}...' with '{new_formula[:30]}...'")
                    
                    # Clear paragraphs and add a new one with the formula
                    shape.text_frame.clear()
                    p = shape.text_frame.paragraphs[0]
                    run = p.add_run()
                    run.text = new_formula
                    
                    formula_idx += 1

prs.save(output_path)
print(f"Saved to {output_path}")
