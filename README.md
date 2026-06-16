# AI Resume Analyzer & Job Predictor

An AI-powered Resume Analyzer that evaluates resumes, calculates ATS scores, detects domains, identifies skills, predicts suitable job roles, and generates a professional PDF report.

---

## Features

- ATS Score Calculation
- Resume Domain Detection
- Skill Extraction
- Missing Skills Identification
- Job Role Prediction
- Resume Strength Analysis
- Resume Weakness Analysis
- Resume Improvement Suggestions
- Professional PDF Report Generation
- Color-Coded PDF Sections

---

## Technologies Used

- Python
- Flask
- HTML
- CSS
- ReportLab
- Regular Expressions (Regex)

---

## Project Structure

```
AI-Resume-analyzer/
│
├── app.py
├── README.md
├── requirements.txt
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   └── style.css
│
└── reports/
    └── Generated PDF Reports
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd AI-Resume-analyzer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

in your browser.

---

## How It Works

1. Upload Resume (PDF/TXT)
2. Resume content is extracted
3. ATS Score is calculated
4. Domain is identified
5. Skills are detected
6. Recommended jobs are generated
7. Strengths and weaknesses are analyzed
8. Improvement suggestions are generated
9. PDF report is created

---

## Sample Report Contents

- ATS Score
- Verdict
- Domain
- Domain Confidence
- Skills Found
- Missing Skills
- Recommended Jobs
- Strengths
- Weaknesses
- Resume Suggestions

---

## Supported Domains

- Computer Science Engineering (CSE)
- Electronics and Communication Engineering (ECE)
- Electrical and Electronics Engineering (EEE)
- Mechanical Engineering
- Civil Engineering

---

## Future Improvements

- Advanced ATS Scoring
- AI-based Resume Recommendations
- Resume Ranking System
- Multiple Resume Comparison
- Resume Template Suggestions

---

## Author

Developed as a Resume Analysis and Job Prediction Project using Flask and Python.