from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity


# Load BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")


# Convert text into BERT embedding
def get_embedding(text):

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        output = model(**encoded)

    # Take [CLS] vector
    cls_vector = output.last_hidden_state[:, 0, :]

    return cls_vector


# Calculate semantic similarity
def calculate_similarity(resume_text, job_text):

    resume_embedding = get_embedding(resume_text)
    job_embedding = get_embedding(job_text)

    similarity = cosine_similarity(
        resume_embedding.numpy(),
        job_embedding.numpy()
    )[0][0]

    return round(float(similarity * 100), 2)


# Skills we want to detect
SKILLS = [
    "java",
    "python",
    "javascript",
    "react",
    "node.js",
    "sql",
    "mysql",
    "postgresql",
    "html",
    "css",
    "git",
    "github",
    "spring boot",
    "rest api",
    "machine learning",
    "tensorflow",
    "pytorch",
    "fastapi",
    "docker"
]


# Find matching and missing skills
def find_skills(resume_text, job_text):

    resume_lower = resume_text.lower()
    job_lower = job_text.lower()

    # Skills required by the job
    job_skills = [
        skill for skill in SKILLS
        if skill in job_lower
    ]

    # Skills present in both resume and job
    matching_skills = [
        skill for skill in job_skills
        if skill in resume_lower
    ]

    # Skills required by job but missing from resume
    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_lower
    ]

    return matching_skills, missing_skills