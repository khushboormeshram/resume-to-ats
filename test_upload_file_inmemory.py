from fastapi.testclient import TestClient
from api import app
from reportlab.pdfgen import canvas
import io


def make_sample_pdf_bytes(text: str) -> bytes:
    """Create a simple one-page PDF in-memory containing `text`."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    # write lines, wrap roughly
    y = 800
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 14
        if y < 50:
            break
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


def run_test_upload():
    client = TestClient(app)

    jd = (
        "We are seeking a Senior Python Developer with experience in Django, AWS, Docker, "
        "REST APIs, and SQL. Experience with CI/CD and unit testing is a plus."
    )

    resume_text = (
        "Senior Software Engineer with 6 years experience. Skilled in Python, Django, Flask, "
        "AWS (EC2, S3), Docker, PostgreSQL, REST APIs, and CI/CD pipelines. Worked on unit testing."
    )

    pdf_bytes = make_sample_pdf_bytes(resume_text)

    files = {
        "resume_file": ("resume.pdf", pdf_bytes, "application/pdf")
    }

    resp = client.post("/score", data={"job_description": jd}, files=files)
    print("Status:", resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


if __name__ == '__main__':
    run_test_upload()
