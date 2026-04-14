import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Custom CSS (UI improvement)
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AI Resume Analyzer Dashboard")

# Skills list
skills_list = [
    "python", "java", "c++", "machine learning", "data science",
    "sql", "html", "css", "javascript", "react", "node",
    "deep learning", "nlp", "power bi", "excel",
    "communication", "teamwork"
]

# Extract text
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text.lower()

# Extract skills
def extract_skills(text):
    return list(set([skill for skill in skills_list if skill in text]))

# ATS Score
def ats_score(text, skills):
    score = len(skills) * 5
    keywords = ["project", "experience", "education", "skills"]
    for word in keywords:
        if word in text:
            score += 5
    return min(score, 100)

# Resume vs JD Match
def match_score(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]
    return round(similarity * 100, 2)

# Suggestions
def suggestions(score, skills):
    tips = []
    if score < 50:
        tips.append("Add more relevant technical skills.")
        tips.append("Include projects and work experience.")
    if "machine learning" not in skills:
        tips.append("Add Machine Learning for better opportunities.")
    if "communication" not in skills:
        tips.append("Include soft skills like communication.")
    return tips

# Layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    jd_input = st.text_area("📝 Paste Job Description")

if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(text[:800])

    skills = extract_skills(text)

    # Dashboard layout
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("💡 Skills Found", len(skills))

    score = ats_score(text, skills)

    with c2:
        st.metric("📊 ATS Score", f"{score}/100")

    if jd_input:
        match = match_score(text, jd_input)
    else:
        match = 0

    with c3:
        st.metric("🎯 JD Match %", f"{match}%")

    # Skills Display
    st.subheader("🛠 Skills Detected")
    st.write(skills)

    # Suggestions
    st.subheader("📌 Suggestions")
    for tip in suggestions(score, skills):
        st.write("✔️", tip)

    # Report Data
    report = pd.DataFrame({
        "Metric": ["Skills Found", "ATS Score", "JD Match"],
        "Value": [len(skills), score, match]
    })

    # Download button
    st.subheader("⬇️ Download Report")
    csv = report.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV Report", csv, "report.csv", "text/csv")
