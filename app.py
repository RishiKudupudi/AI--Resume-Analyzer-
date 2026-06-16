from flask import Flask, render_template, request,send_file
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import pdfplumber

app = Flask(__name__)
report_data = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "No file chosen upload a resume file."
    file = request.files["resume"]
    if file.filename == "":
        return "No file chosen upload a resume file."

    file = request.files["resume"]

    import os
    os.makedirs("resumes",exist_ok=True)
    file_path=os.path.join("resumes",file.filename)
    file.save(file_path)
    pdf_path = "resumes/" + file.filename

    with pdfplumber.open(pdf_path) as pdf:
        resume_text = ""

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text

    skills_db = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "aws",
        "docker",
        "machine learning",
        "react",
        "mongodb",
    ]

    domains = {
        "CSE": [
            "python",
            "java",
            "sql",
            "html",
            "css",
            "javascript",
            "react",
            "flask",
            "mongodb",
            "machine learning"
        ],

        "ECE": [
            "vlsi",
            "verilog",
            "embedded systems",
            "iot",
            "arduino",
            "microcontroller"
        ],

        "EEE": [
            "power systems",
            "electrical machines",
            "transformers",
            "power electronics"
        ],

        "MECHANICAL": [
            "autocad",
            "solidworks",
            "catia",
            "manufacturing"
        ],

        "CIVIL": [
            "staad pro",
            "surveying",
            "construction",
            "autocad civil"
        ]
    }

    resume_lower = resume_text.lower()

    has_projects = "project" in resume_lower

    has_certifications = (
        "certification" in resume_lower
        or "certificate" in resume_lower
        or "certifications" in resume_lower
        or "certificates" in resume_lower
        or "CERTIFICATION" in resume_lower
        or "CERTIFICATIONS" in resume_lower
    )

    has_education = (
        "b.tech" in resume_lower
        or "btech" in resume_lower
        or "education" in resume_lower
        or "degree" in resume_lower
        or "B.Tech" in resume_lower
        or "BTech" in resume_lower
        or "Education" in resume_lower
        or "Degree" in resume_lower
    )

    has_internships=(
        "internship" in resume_lower
        or "intern" in resume_lower
        or "internships" in resume_lower
        or "interns" in resume_lower
        or "INTERNSHIP" in resume_lower
        or "INTERNSHIPS" in resume_lower
        or "Internship" in resume_lower
    )

    has_achievements=(
        "achievement" in resume_lower
        or "achievements" in resume_lower
        or "award" in resume_lower
        or "awards" in resume_lower
        or "ACHIEVEMENT" in resume_lower
        or "ACHIEVEMENTS" in resume_lower
        or "Achievement" in resume_lower
        or "Achievements" in resume_lower
    )

     
    domain_scores = {}

    for domain, domain_skills in domains.items():

        score = 0

        for skill in domain_skills:

            if skill in resume_lower:
                score += 1

        domain_scores[domain] = score

    predicted_domain = max(domain_scores, key=domain_scores.get)

    found_skills = []

    for skill in domains[predicted_domain]:

     if skill in resume_lower:
         found_skills.append(skill)

    domain_match_count = domain_scores[predicted_domain]

    total_domain_skills = len(domains[predicted_domain])

    domain_confidence = round(
        (domain_match_count / total_domain_skills) * 100,
        2
    )

    skill_score = (len(found_skills) / len(skills_db)) * 70

    project_score = 10 if has_projects else 0

    certification_score = 10 if has_certifications else 0

    education_score = 10 if has_education else 0

    ats_score = round(
      skill_score +
      project_score +
     certification_score +
     education_score,
     2
  )

    if ats_score >= 80:
        verdict = "Excellent"
    elif ats_score >= 60:
        verdict = "Good"
    else:
        verdict = "Needs Improvement"

    missing_skills = []

    for skill in domains[predicted_domain]:
        if skill not in found_skills:
            missing_skills.append(skill)


    strengths=[]
    weaknesses=[]
    if ats_score >= 80:
        strengths.append("Good ATS Score")
    if has_projects:
        strengths.append("Has Projects")
    if has_certifications:
        strengths.append("Has Certifications")
    if has_achievements:
        strengths.append("Has Achievements")
    if has_internships:
        strengths.append("Has Internships")
    if not has_projects:
        weaknesses.append("No Projects")
    if not has_certifications:
        weaknesses.append("No Certifications")
    if not has_achievements:
        weaknesses.append("No Achievements")
    if not has_internships:
        weaknesses.append("No Internships")

    suggestions = []
    if not has_internships:
        suggestions.append("Add Internship  Experience.")
    if not has_certifications:
        suggestions.append("Add More certifications.")
    if not has_achievements:
        suggestions.append("Add Achievements.")
    if not has_projects:
        suggestions.append("Add Projects.")
    for skill in missing_skills:
        suggestions.append(f"Learn {skill}")
    
    domain = predicted_domain


    #CSE JOB RECOMMENDATIONS
    recommended_jobs=[]

    
    if "python"  in found_skills:
        recommended_jobs.append("Python Developer")
    if "java" in found_skills:
        recommended_jobs.append("Java Developer")
    if "sql" in found_skills:
        recommended_jobs.append("SQL Developer")
    if "html" in found_skills:
        recommended_jobs.append("Frontend Developer")
    if "css" in found_skills:
        recommended_jobs.append("Frontend Developer")
    if "javascript" in found_skills:
        recommended_jobs.append("Frontend Developer")
    if "react" in found_skills:
        recommended_jobs.append("Frontend Developer")
    if "flask" in found_skills:
        recommended_jobs.append("Backend Developer")
    if "mongodb" in found_skills:
        recommended_jobs.append("Database Administrator")
    if "machine learning" in found_skills:
        recommended_jobs.append("Machine Learning Engineer")

    #ece job recommendations
    if "vlsi" in found_skills:
        recommended_jobs.append("VLSI Engineer")
    if "verilog" in found_skills:
        recommended_jobs.append("VLSI Engineer")
    if "embedded systems" in found_skills:
        recommended_jobs.append("Embedded Systems Engineer")
    if "iot" in found_skills:
        recommended_jobs.append("IoT Developer")
    if "arduino" in found_skills:
        recommended_jobs.append("Embedded Systems Engineer")
    if "microcontroller" in found_skills:
        recommended_jobs.append("Embedded Systems Engineer")

    #eee job recommendations

    if "power systems" in found_skills:
        recommended_jobs.append("Power Systems Engineer")
    if "electrical machines" in found_skills:
        recommended_jobs.append("Electrical Engineer")
    if "transformers" in found_skills:
        recommended_jobs.append("Electrical Engineer")
    if "power electronics" in found_skills:
        recommended_jobs.append("Power Electronics Engineer")

    #mechanical job recommendations

    if "autocad" in found_skills:
        recommended_jobs.append("Design Engineer")
    if "solidworks" in found_skills:
        recommended_jobs.append("Design Engineer")
    if "catia" in found_skills:
        recommended_jobs.append("Design Engineer")
    if "manufacturing" in found_skills:
        recommended_jobs.append("Manufacturing Engineer")
    #civil job recommendations

    if "staad pro" in found_skills:
        recommended_jobs.append("Structural Engineer")
    if "surveying" in found_skills:
        recommended_jobs.append("Surveyor")
    if "construction" in found_skills:
        recommended_jobs.append("Construction Engineer")
    if "autocad civil" in found_skills:
        recommended_jobs.append("Civil Engineer")

    global report_data
    report_data = {
        "filename": file.filename,
        "resume_text": resume_text,
        "found_skills": found_skills,
        "ats_score": ats_score,
        "missing_skills": missing_skills,
        "verdict": verdict,
        "domain": domain,
        "domain_confidence": domain_confidence,
        "has_projects": has_projects,
        "has_certifications": has_certifications,
        "has_education": has_education,
        "recommended_jobs": list(set(recommended_jobs)),
        "skill_score": round(skill_score, 2),
        "project_score": project_score,
        "certification_score": certification_score,
        "education_score": education_score,
        "has_internships": has_internships,
        "has_achievements": has_achievements,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }

    #rendering the result template with all the calculated values and recommendations
    return render_template(
        "result.html",
        filename=file.filename,
        resume_text=resume_text,
        found_skills=found_skills,
        ats_score=ats_score,
        missing_skills=missing_skills,
        verdict=verdict,
        domain=domain,
        domain_confidence=domain_confidence,
        has_projects=has_projects,
        has_certifications=has_certifications,
        has_education=has_education,
        recommended_jobs=list(set(recommended_jobs)),
        skill_score=round(skill_score, 2),
        project_score=project_score,
        certification_score=certification_score,
        education_score=education_score,
        has_internships=has_internships,
        has_achievements=has_achievements,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions
    )

#route to download the report as a PDF file
@app.route("/download_report")
def download_report():

    from datetime import datetime
    pdf_file=f"Resume_Report_{report_data['domain']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(pdf_file)
    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, "AI Resume Analyzer Report")
    c.setFillColor(colors.black)
    c.line(100, 790, 500, 790)
    c.setFont("Helvetica", 12)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,770, "ATS INFORMATION")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 12)

    c.drawString(100,745, f"ATS Score: {report_data['ats_score']}")
    c.drawString(100,725, f"Verdict: {report_data['verdict']}")
    c.drawString(100,705, f"Domain: {report_data['domain']}")
    c.drawString(100,685, f"Domain Confidence: {report_data['domain_confidence']}")

    y=640
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,y,"Skills Found:")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 12)
    y-=30
    for skill in report_data['found_skills']:
        c.drawString(120, y, f"- {skill}")
        y -= 20

    y-=30
    if y<100:
        c.showPage()
        y=750
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,y,"Missing Skills:")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 12)
    y-=20
    if len(report_data['missing_skills'])==0:
        c.drawString(120, y, "None")
        y-=20
    else:
        for skill in report_data['missing_skills']:
            c.drawString(120, y, f"- {skill}")
            y -= 20  
    
    y-=30

    if y<100:
        c.showPage()
        y=750
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,y,"Recommended Jobs:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    y-=20

    for job in report_data['recommended_jobs']:
        c.drawString(120, y, f"- {job}")
        y -= 20

    y-=30
    if y<100:
        c.showPage()
        y=750
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,y,"Strengths:")
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 12)
    y-=20
    if report_data['has_projects']:
        c.drawString(120, y, "- Projects included")
        y-=20
    if report_data['has_certifications']:
        c.drawString(120, y, "- Certifications included")
        y-=20
    if report_data['has_education']:
        c.drawString(120, y, "- Education included")
        y-=20
    if report_data['has_internships']:
        c.drawString(120, y, "- Internships included")
        y-=20
    if report_data['has_achievements']:
        c.drawString(120, y, "- Achievements included")
        y-=20

    y-=30

    if y <100:
        c.showPage()
        y=750
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkred)
    c.drawString(100,y,"Weaknesses:")
    

    c.setFont("Helvetica", 12)
    y-=20
    if not report_data['has_internships']:
        c.drawString(120, y, "- No Internships")
        y-=20
    if not report_data['has_achievements']:
        c.drawString(120, y, "- No Achievements")
        y-=20
    if not report_data['has_certifications']:
        c.drawString(120, y, "- No Certifications")
        y-=20
    if not report_data['has_projects']:
        c.drawString(120, y, "- No Projects")
        y-=20
    
    y-=30

    if y<100:
        c.showPage()
        y=750
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.darkgreen)
    c.drawString(100,y," Resume Suggestions:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    y-=20

    for suggestion in report_data['suggestions']:
        c.drawString(120, y, f"- {suggestion}")
        y -= 20

    y-=20

    c.line(100,25,500,25)
    c.drawString(100,30,"Generated by AI Resume Analyzer")
    c.save()

    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)