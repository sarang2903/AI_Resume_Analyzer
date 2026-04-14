import streamlit as st
import pdfplumber
import re
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer Ultimate", layout="wide")

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.login = True
        else:
            st.error("Wrong credentials")
    st.stop()

# ---------------- API KEY ----------------
api_key = st.sidebar.text_input("🔑 Enter OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

# ---------------- THEME ----------------
dark = st.sidebar.toggle("🌙 Dark Mode")

if dark:
    st.markdown("<style>body{background-color:#0E1117;color:white;}</style>", unsafe_allow_html=True)

st.title("🚀 AI Resume Analyzer Ultimate")

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

def match_score(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    return round(cosine_similarity(matrix)[0][1]*100,2)

def smart_score(skills, match):
    return min(int(len(skills)*4 + match*0.6),100)

# 🤖 AI Feedback
def ai_feedback(text, jd):
    if not client:
        return "⚠️ Enter API key to get AI feedback"
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a resume expert."},
                {"role": "user", "content": f"Analyze this resume:\n{text}\n\nJob Description:\n{jd}\nGive improvements."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "API Error"

# 📄 PDF
def generate_pdf(name, email, score, feedback):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"Name: {name}", styles["Normal"]),
        Paragraph(f"Email: {email}", styles["Normal"]),
        Paragraph(f"Score: {score}", styles["Normal"]),
        Paragraph(f"Feedback: {feedback}", styles["Normal"])
    ]

    doc.build(content)

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    jd = st.text_area("📝 Job Description")

# ---------------- PROCESS ----------------
if file:
    text = extract_text(file)

    name = extract_name(text)
    email = extract_email(text)
    skills = extract_skills(text)

    match = match_score(text, jd if jd else "")
    score = smart_score(skills, match)

    # ---------------- METRICS ----------------
    c1, c2, c3 = st.columns(3)
    c1.metric("🤖 AI Score", f"{score}/100")
    c2.metric("🎯 JD Match", f"{match}%")
    c3.metric("💡 Skills", len(skills))

    # ---------------- INFO ----------------
    st.subheader("👤 Info")
    st.write(name, "|", email)

    # ---------------- CHART ----------------
    df = pd.DataFrame({"Skill": skills, "Value":[1]*len(skills)})
    fig = px.bar(df, x="Skill", y="Value")
    st.plotly_chart(fig)

    # ---------------- AI FEEDBACK ----------------
    st.subheader("🤖 AI Suggestions")
    feedback = ai_feedback(text, jd if jd else "")
    st.write(feedback)

    # ---------------- PDF ----------------
    generate_pdf(name, email, score, feedback)

    with open("report.pdf","rb") as f:
        st.download_button("📄 Download Full Report", f, "report.pdf")
