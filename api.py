from fastapi import FastAPI, UploadFile, File, Form
import pdf2image
import base64
import io
import os
from dotenv import load_dotenv
import re
from typing import Optional
import PyPDF2

load_dotenv()

app = FastAPI()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyPDF2."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        texts = []
        for page in reader.pages:
            try:
                t = page.extract_text()
            except Exception:
                t = None
            if t:
                texts.append(t)
        return "\n".join(texts)
    except Exception:
        return ""


def tokenize(text: str):
    words = re.findall(r"\b[a-zA-Z0-9+#\-\.]+\b", text.lower())
    stopwords = {
        "the", "and", "to", "of", "a", "in", "for", "with", "on", "is", "are", "that",
        "as", "be", "this", "by", "or", "an", "it", "from", "at", "will", "we", "you"
    }
    return [w for w in words if w not in stopwords and len(w) > 1]


def compute_ats_score(job_description: str, resume_text: str) -> dict:
    """Compute a simple ATS-like score based on keyword overlap.

    Returns a dict with numeric `score` (0-100), `matched_keywords`, `missing_keywords`, and `total_keywords`.
    """
    jd_tokens = tokenize(job_description)
    resume_tokens = set(tokenize(resume_text or ""))

    # Take top unique keywords from JD (preserve order)
    seen = set()
    jd_keywords = []
    for w in jd_tokens:
        if w not in seen:
            jd_keywords.append(w)
            seen.add(w)
        if len(jd_keywords) >= 30:
            break

    if not jd_keywords:
        return {"score": 0, "matched_keywords": [], "missing_keywords": [], "total_keywords": 0}

    matched = [w for w in jd_keywords if w in resume_tokens]
    missing = [w for w in jd_keywords if w not in resume_tokens]

    score = int(len(matched) / len(jd_keywords) * 100)

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "total_keywords": len(jd_keywords),
    }


@app.post("/score")
async def score_resume(
    job_description: str = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
):
    """Endpoint to return a basic ATS score given a job description and a resume (text or PDF)."""
    try:
        if not resume_text and not resume_file:
            return {"error": "Provide `resume_text` or upload `resume_file` (PDF or text)."}

        if resume_file:
            content = await resume_file.read()
            filename = (resume_file.filename or "").lower()
            if resume_file.content_type == "application/pdf" or filename.endswith(".pdf"):
                resume_text = extract_text_from_pdf_bytes(content)
            else:
                try:
                    resume_text = content.decode(errors="ignore")
                except Exception:
                    resume_text = ""

        result = compute_ats_score(job_description, resume_text or "")
        return result
    except Exception as e:
        return {"error": str(e)}
