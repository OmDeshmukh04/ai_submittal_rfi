from fastapi import APIRouter, File, UploadFile, HTTPException
from services.ocr import extract_text_from_pdf, ocr_from_saved_pdf
from services.db import save_submittal, update_submittal_text, get_submittal
from services.quick_extract import quick_extract
import os, uuid

router = APIRouter()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "submittals")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_submittal(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    uid = str(uuid.uuid4())
    saved_name = f"{uid}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    contents = await file.read()
    with open(saved_path, "wb") as f:
        f.write(contents)

    # extract text (selectable text first)
    text = extract_text_from_pdf(contents)
    text_len = len(text)
    preview = text[:1000].replace("\n", " ")
    needs_ocr = text_len < 200

    # quick extraction for demo flags
    quick_flags = quick_extract(text)

    # save record
    sub_id = save_submittal(saved_name, text, status="uploaded", quick_flags=quick_flags)

    return {
        "submittal_id": sub_id,
        "filename": file.filename,
        "saved_path": saved_path,
        "text_len": text_len,
        "preview": preview,
        "needs_ocr": needs_ocr,
        "quick_flags": quick_flags
    }

@router.post("/ocr/{sub_id}")
def run_ocr_on_saved(sub_id: int):
    rec = get_submittal(sub_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Submittal not found")
    saved_name = rec[1]  # filename column
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    # run OCR on saved PDF and update DB
    ocr_text = ocr_from_saved_pdf(saved_path)
    update_submittal_text(sub_id, ocr_text)
    quick_flags = quick_extract(ocr_text)
    return {"submittal_id": sub_id, "text_len": len(ocr_text), "quick_flags": quick_flags}
