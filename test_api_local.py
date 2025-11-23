from fastapi.testclient import TestClient
from api import app


def run_test():
    client = TestClient(app)
    jd = (
        "We are seeking a Senior Python Developer with experience in Django, AWS, Docker, "
        "REST APIs, and SQL. Experience with CI/CD and unit testing is a plus."
    )
    resume = (
        "Senior Software Engineer with 6 years experience. Skilled in Python, Django, Flask, "
        "AWS (EC2, S3), Docker, PostgreSQL, REST APIs, and CI/CD pipelines. Worked on unit testing."
    )

    resp = client.post("/score", data={"job_description": jd, "resume_text": resume})
    print("Status:", resp.status_code)
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


if __name__ == '__main__':
    run_test()
