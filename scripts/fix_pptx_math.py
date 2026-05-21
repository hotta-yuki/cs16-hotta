from pptx import Presentation
import os

pptx_path = r'資料\GMM_Presentation_fixed.pptx'
output_path = r'資料\GMM_Presentation_fixed_v2.pptx'

if not os.path.exists(pptx_path):
    print(f"File not found: {pptx_path}")
    exit(1)

prs = Presentation(pptx_path)

# Mapping of mojibake to correct characters
# These are based on UTF-8 bytes being interpreted as Shift-JIS or similar
replacements = {
    "ﾎｼ": "μ",
    "ﾎ｣": "Σ",
    "ﾏ": "π",
    "ﾎｸ": "θ",
    "ﾎ": "Π",
    "ﾎｾ": "φ", # likely
    "ﾎ": "Φ", # likely
    "ﾎｻ": "λ", # likely
    "ﾎｴ": "δ", # likely
    "ﾎｵ": "ε", # likely
    "ﾎｱ": "α", # likely
    "ﾎｲ": "β", # likely
    "ﾎｳ": "γ", # likely
}

def beautify_math(text):
    # Fix mojibake
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Simple LaTeX-like to Unicode math improvements
    # This is speculative but helpful
    text = text.replace("\\text new", " (new)")
    text = text.replace("\\boldsymbol", "")
    text = text.replace("\\mathcal{N}", "N")
    text = text.replace("\\ldots", "...")
    text = text.replace("\\sum", "Σ")
    text = text.replace("\\pi", "π")
    text = text.replace("\\mu", "μ")
    text = text.replace("\\Sigma", "Σ")
    text = text.replace("\\theta", "θ")
    
    # Try to fix some common patterns seen in the inspection
    # e.g. "rn k" -> "r_nk"
    if "rn k" in text:
        text = text.replace("rn k", "r_nk")
    if "Nk" in text:
        text = text.replace("Nk", "N_k")
    
    return text

for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    original = run.text
                    new_text = beautify_math(original)
                    if original != new_text:
                        run.text = new_text

prs.save(output_path)
print(f"Saved to {output_path}")
