from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

from matcher import calculate_similarity, find_skills


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


@app.get("/")
def home():
    return {
        "message": "BERT Resume Matcher API is running"
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    resume_text = extract_text_from_pdf(resume.file)

    score = calculate_similarity(
        resume_text,
        job_description
    )

    matching_skills, missing_skills = find_skills(
        resume_text,
        job_description
    )

    return {
        "match_score": score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }