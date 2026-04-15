import streamlit as st
import pdfplumber
import re
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Career Assistant", layout="wide")

st.title("🚀 AI Career Assistant Platform")

# ---------------- SKILLS DATABASE ----------------
skills_db = [
    "python","java","c++","machine learning","data science","sql",
    "html","css","javascript","react","node","deep learning",
    "nlp","power bi","excel","communication","teamwork"
]

# ---------------- FUNCTIONS ----------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def extract_email(text):
    match = re.findall(r"\S+@\S+", text)
    return match[0] if match else "Not Found"

def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s\-]{8,15}\d", text)
    return match[0] if match else "Not Found"

def extract_name(text):
    for line in text.split("\n"):
        if 2 <= len(line.split()) <= 4:
            return line
    return "Not Found"

def extract_skills(text):
    return list(set([s for s in skills_db if s in text]))

# -------- MATCH --------
def match_score(resume, jd):
    if not jd.strip():
        return 0, [], []

    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]

    words = cv.get_feature_names_out()
    jd_words = set(jd.split())

    matched = [w for w in words if w in jd_words]
    missing = [w for w in jd_words if w not in words]

    return round(similarity*100,2), matched, missing

# -------- SCORE --------
def final_score(skills, match):
    return min(int(len(skills)*4 + match*0.6), 100)

# -------- CAREER SUGGESTION --------
def suggest_career(skills):
    if "machine learning" in skills:
        return "Data Scientist / ML Engineer"
    elif "react" in skills:
        return "Frontend Developer"
    elif "node" in skills:
        return "Backend Developer"
    elif "sql" in skills:
        return "Data Analyst"
    else:
        return "Software Developer"

# -------- PDF --------
def generate_pdf(name, email, phone, score, career):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("<b>AI Career Report</b>", styles["Title"]))
    content.append(Spacer(1,10))

    content.append(Paragraph(f"Name: {name}", styles["Normal"]))
    content.append(Paragraph(f"Email: {email}", styles["Normal"]))
    content.append(Paragraph(f"Phone: {phone}", styles["Normal"]))
    content.append(Paragraph(f"Score: {score}", styles["Normal"]))
    content.append(Paragraph(f"Suggested Career: {career}", styles["Normal"]))

    doc.build(content)

# ---------------- UI ----------------
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    jd = st.text_area("📝 Paste Job Description")

# ---------------- PROCESS ----------------
if file:
    text = extract_text(file)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    skills = extract_skills(text)
    match, matched, missing = match_score(text, jd)
    score = final_score(skills, match)
    career = suggest_career(skills)

    # -------- METRICS --------
    c1, c2, c3 = st.columns(3)
    c1.metric("🤖 AI Score", score)
    c2.metric("🎯 Match %", match)
    c3.metric("💡 Skills", len(skills))

    st.progress(score/100)

    # -------- INFO --------
    st.subheader("👤 Candidate Info")
    st.write(name, email, phone)

    # -------- SKILLS --------
    st.subheader("🛠 Skills")
    st.success(skills)

    # -------- CHART --------
    df = pd.DataFrame({"Skill": skills, "Value":[1]*len(skills)})
    fig = px.bar(df, x="Skill", y="Value", title="Skill Chart")
    st.plotly_chart(fig)

    # -------- MATCH --------
    st.subheader("🎯 Matched Keywords")
    st.write(matched[:15])

    st.subheader("⚠️ Missing Skills")
    st.error(missing[:15])

    # -------- CAREER --------
    st.subheader("🎓 Suggested Career")
    st.success(career)

    # -------- SUGGESTIONS --------
    st.subheader("📌 Suggestions")
    if score < 50:
        st.warning("Improve skills & projects")
    elif score < 75:
        st.info("Good resume, optimize keywords")
    else:
        st.success("Excellent resume")

    # -------- PDF --------
    generate_pdf(name, email, phone, score, career)

    with open("report.pdf", "rb") as f:
        st.download_button("📄 Download Report", f, "report.pdf")
