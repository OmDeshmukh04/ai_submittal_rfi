# backend/app/services/ocr.py
import fitz  # PyMuPDF
import io
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract selectable text with PyMuPDF; if a page has no text, fall back to OCR.
    Returns concatenated text for all pages.
    """
    text_pages = []
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception:
        return ""

    for page in doc:
        page_text = page.get_text("text").strip()
        if page_text:
            text_pages.append(page_text)
        else:
            try:
                pix = page.get_pixmap(dpi=200)
                img = Image.open(io.BytesIO(pix.tobytes()))
                ocr_text = pytesseract.image_to_string(img)
                text_pages.append(ocr_text)
            except Exception:
                text_pages.append("")
    return "\n\n".join(text_pages)

def ocr_from_saved_pdf(path: str) -> str:
    """Read a saved PDF file and run the same extraction (useful for deferred OCR)."""
    with open(path, "rb") as f:
        data = f.read()
    return extract_text_from_pdf(data)
