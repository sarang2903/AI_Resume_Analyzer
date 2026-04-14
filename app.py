import streamlit as st
import pdfplumber
import re
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer Pro+", layout="wide")

# ---------------- THEME TOGGLE ----------------
theme = st.sidebar.toggle("🌙 Dark Mode")

if theme:
    st.markdown("<style>body{background-color:#0E1117;color:white;}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🚀 AI Resume Analyzer Pro+")

# ---------------- SKILLS ----------------
skills_list = [
    "python","java","c++","machine learning","data science","sql",
    "html","css","javascript","react","node","deep learning",
    "nlp","power bi","excel","communication","teamwork"
]

# ---------------- FUNCTIONS ----------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text.lower()

def extract_email(text):
    match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match[0] if match else "Not Found"

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if len(line.split()) <= 4:
            return line
    return "Not Found"

def extract_skills(text):
    return list(set([s for s in skills_list if s in text]))

# 🤖 Smart Score
def smart_score(skills, match):
    return min(int(len(skills)*4 + match*0.6), 100)

# 🎯 Match + keywords
def match_analysis(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]

    words = cv.get_feature_names_out()
    jd_words = set(jd.split())
    matched = [w for w in words if w in jd_words]

    return round(similarity*100,2), matched

# 📄 PDF Report
def generate_pdf(name, email, score):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"Name: {name}", styles["Normal"]))
    content.append(Paragraph(f"Email: {email}", styles["Normal"]))
    content.append(Paragraph(f"Score: {score}", styles["Normal"]))

    doc.build(content)

# ---------------- INPUT ----------------
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
    skills = extract_skills(text)

    match, keywords = match_analysis(text, jd if jd else "")
    score = smart_score(skills, match)

    # ---------------- METRICS ----------------
    c1, c2, c3 = st.columns(3)
    c1.metric("🤖 AI Score", f"{score}/100")
    c2.metric("🎯 JD Match", f"{match}%")
    c3.metric("💡 Skills", len(skills))

    # ---------------- INFO ----------------
    st.subheader("👤 Candidate Info")
    st.write("Name:", name)
    st.write("Email:", email)

    # ---------------- SKILLS ----------------
    st.subheader("🛠 Skills Found")
    st.write(skills)

    # ---------------- CHART ----------------
    st.subheader("📊 Skill Distribution")
    df = pd.DataFrame({"Skill": skills, "Value":[1]*len(skills)})
    fig = px.bar(df, x="Skill", y="Value")
    st.plotly_chart(fig)

    # ---------------- MATCH ANALYSIS ----------------
    st.subheader("🎯 Matching Keywords")
    st.write(keywords[:20])

    # ---------------- SUGGESTIONS ----------------
    st.subheader("📌 Smart Suggestions")

    if score < 50:
        st.warning("Improve resume with more skills and projects")
    if match < 50:
        st.warning("Customize resume based on job description")
    if "machine learning" not in skills:
        st.info("Add Machine Learning skills")

    # ---------------- PDF DOWNLOAD ----------------
    generate_pdf(name, email, score)

    with open("report.pdf", "rb") as f:
        st.download_button("📄 Download PDF Report", f, "report.pdf")
