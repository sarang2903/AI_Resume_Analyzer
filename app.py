import streamlit as st
import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
if "login" not in st.session_state:
    st.session_state.login = False

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.login = True
        else:
            st.error("Invalid credentials")

if not st.session_state.login:
    login()
    st.stop()

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.main {background-color: #f0f2f6;}
.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Resume Analyzer Pro")

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
    return lines[0] if lines else "Not Found"

def extract_skills(text):
    return list(set([s for s in skills_list if s in text]))

def ats_score(text, skills):
    score = len(skills) * 5
    keywords = ["project","experience","education","skills"]
    for k in keywords:
        if k in text:
            score += 5
    return min(score,100)

def match_score(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    return round(cosine_similarity(matrix)[0][1]*100,2)

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    jd = st.text_area("📝 Job Description")

# ---------------- PROCESS ----------------
if uploaded_file:
    text = extract_text(uploaded_file)

    # Extract info
    email = extract_email(text)
    name = extract_name(text)
    skills = extract_skills(text)
    score = ats_score(text, skills)
    match = match_score(text, jd) if jd else 0

    # ---------------- METRICS ----------------
    c1, c2, c3 = st.columns(3)

    c1.metric("📊 ATS Score", f"{score}/100")
    c2.metric("🎯 JD Match", f"{match}%")
    c3.metric("💡 Skills", len(skills))

    # ---------------- BASIC INFO ----------------
    st.subheader("👤 Candidate Info")
    st.write("**Name:**", name)
    st.write("**Email:**", email)

    # ---------------- SKILLS ----------------
    st.subheader("🛠 Skills")
    st.write(skills)

    # ---------------- CHART ----------------
    st.subheader("📊 Skills Visualization")

    skill_counts = [1]*len(skills)
    plt.figure()
    plt.bar(skills, skill_counts)
    plt.xticks(rotation=45)

    st.pyplot(plt)

    # ---------------- SUGGESTIONS ----------------
    st.subheader("📌 Suggestions")

    if score < 50:
        st.warning("Add more skills and projects.")
    if "machine learning" not in skills:
        st.info("Add Machine Learning skills.")
    if "communication" not in skills:
        st.info("Add communication skills.")

    # ---------------- DOWNLOAD ----------------
    report = pd.DataFrame({
        "Name":[name],
        "Email":[email],
        "ATS Score":[score],
        "JD Match":[match],
        "Skills":[", ".join(skills)]
    })

    csv = report.to_csv(index=False).encode()
    st.download_button("⬇️ Download Report", csv, "resume_report.csv")
