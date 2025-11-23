import urllib.request
import urllib.parse

def run_sample():
    url = "http://127.0.0.1:8000/score"
    data = {
        'job_description': (
            "We are seeking a Senior Python Developer with experience in Django, AWS, Docker, "
            "REST APIs, and SQL. Experience with CI/CD and unit testing is a plus."
        ),
        'resume_text': (
            "Senior Software Engineer with 6 years experience. Skilled in Python, Django, Flask, "
            "AWS (EC2, S3), Docker, PostgreSQL, REST APIs, and CI/CD pipelines. Worked on unit testing."
        )
    }

    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(resp.read().decode())
    except Exception as e:
        print("Request failed:", e)

if __name__ == '__main__':
    run_sample()
