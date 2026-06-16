import pandas as pd
import numpy as np
import pdfplumber

# Libraries used for text processing and similarity calculation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# Load Resume and Job datasets
# -------------------------------

resume_df = pd.read_csv("data/Resume.csv")
job_df = pd.read_csv("data/job_descriptions.csv")


# -------------------------------
# Select one resume from dataset
# -------------------------------

# Taking the first resume for testing
with pdfplumber.open("sample_resume.pdf") as pdf:
    resume_text = ""

    for page in pdf.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"


# -------------------------------
# Get job descriptions
# -------------------------------

# Using first 100 jobs to make processing faster
job_texts = job_df["Job Description"].fillna("").head(100)


# -------------------------------
# Combine resume and jobs
# -------------------------------

# Resume is placed first and job descriptions are added after it
documents = [resume_text] + list(job_texts)


# -------------------------------
# Convert text into numerical form
# -------------------------------

# TF-IDF gives importance to meaningful words
vectorizer = TfidfVectorizer(stop_words="english")

# Create TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(documents)


# -------------------------------
# Calculate similarity
# -------------------------------

# Compare resume with all job descriptions
similarity_scores = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:]
)

# Convert result into 1-D array
similarity_scores = similarity_scores.flatten()
best_match=similarity_scores.argmax()


# -------------------------------
# Find Top 5 matching jobs
# -------------------------------

top_5_matches = np.argsort(similarity_scores)[-5:][::-1]


# -------------------------------
# Display recommendations
# -------------------------------


print("=" * 50)
print("        AI RESUME ANALYZER")
print("=" * 50)

print("\nTOP 5 RECOMMENDED JOBS\n")

rank = 1

for index in top_5_matches:

    job_title = job_df.iloc[index]["Job Title"]

    score = round(similarity_scores[index] * 100, 2)

    print(f"{rank}. {job_title}")
    print(f"   Match Score: {score}%")
    print("-" * 50)

    rank += 1
# -------------------------------
# Skill Extraction
# -------------------------------

skills_db = [
    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "machine learning",
    "deep learning",
    "data science",
    "pandas",
    "numpy",
    "aws",
    "docker",
    "git"
]

resume_lower = resume_text.lower()

found_skills = []

for skill in skills_db:
    if skill in resume_lower:
        found_skills.append(skill)

print("\n" + "=" * 50)
print("SKILLS FOUND IN RESUME")
print("=" * 50)

for skill in found_skills:
    print(skill)


# -------------------------------
# Missing Skills Analysis
# -------------------------------
# Get skills required by best matching job

job_skills_text = str(job_df.iloc[best_match]["skills"]).lower()

print("\nSkills Required By Job:\n")
print(job_skills_text)

required_skills = []

for skill in skills_db:
    if skill in job_skills_text:
        required_skills.append(skill)

print("\nRequired Skills Found In Job:\n")

for skill in required_skills:
    print(skill)

missing_skills = []

for skill in required_skills:
    if skill not in found_skills:
        missing_skills.append(skill)

print("\n" + "=" * 50)
print("MISSING SKILLS")
print("=" * 50)

for skill in missing_skills:
    print(skill)

print("\nRECOMMENDED LEARNING\n")

for skill in missing_skills:
    print(f"Learn {skill}")

#for ats score calculation
total_required = len(required_skills)

matched_skills = len(required_skills) - len(missing_skills)

ats_score = round(
    (matched_skills / total_required) * 100, 2
) if total_required > 0 else 0

print("\n" + "=" * 50)
print("ATS SCORE REPORT")
print("=" * 50)

print(f"Resume Skills Found : {len(found_skills)}")
print(f"Required Skills : {total_required}")
print(f"Matched Skills : {matched_skills}")
print(f"ATS Score : {ats_score}%")

if ats_score >= 80:
    print("Verdict : Excellent")
elif ats_score >= 60:
    print("Verdict : Good")
else:
    print("Verdict : Needs Improvement")

