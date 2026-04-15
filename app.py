import streamlit as st
import pdfplumber
import re
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer Pro+", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main { background: #f0f4ff; }
.hero {
    background: linear-gradient(135deg,#1e3a8a,#3b82f6);
    padding:30px;
    border-radius:15px;
    color:white;
}
.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 5px 20px rgba(0,0,0,0.1);
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🤖 Resume AI")
    page = st.radio("Navigation", [
        "📄 Resume Analyzer",
        "📊 Analytics Dashboard",
        "📌 Skill Insights",
        "ℹ️ About"
    ])

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

def extract_phone(text):
    match = re.findall(r"\+?\d[\d\s\-]{8,15}\d", text)
    return match[0] if match else "Not Found"

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if 2 <= len(line.split()) <= 4:
            return line.strip()
    return "Not Found"

def extract_skills(text):
    return list(set([s for s in skills_list if s in text]))

def match_analysis(resume, jd):
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

# ---------------- SESSION STORAGE ----------------
if "data" not in st.session_state:
    st.session_state.data = {}

# ---------------- PAGE 1 ----------------
if page == "📄 Resume Analyzer":

    st.markdown('<div class="hero"><h1>🚀 AI Resume Analyzer</h1><p>Analyze your resume with AI insights</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        file = st.file_uploader("Upload Resume (PDF)")

    with col2:
        jd = st.text_area("Paste Job Description")

    if file:
        text = extract_text(file)

        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)
        match, keywords, missing = match_analysis(text, jd)

        score = min(int(len(skills)*4 + match*0.6), 100)

        st.session_state.data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "match": match,
            "score": score,
            "keywords": keywords,
            "missing": missing
        }

        # METRICS
        c1, c2, c3 = st.columns(3)
        c1.metric("AI Score", f"{score}/100")
        c2.metric("JD Match", f"{match}%")
        c3.metric("Skills", len(skills))

        st.progress(score/100)

        # CONTACT
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Contact Info")
        st.write("Name:", name)
        st.write("Email:", email)
        st.write("Phone:", phone)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGE 2 ----------------
elif page == "📊 Analytics Dashboard":

    st.markdown('<div class="hero"><h1>📊 Resume Analytics</h1></div>', unsafe_allow_html=True)

    data = st.session_state.data

    if not data:
        st.warning("Upload resume first")
    else:
        skills = data["skills"]

        df = pd.DataFrame({"Skill": skills, "Value":[1]*len(skills)})

        fig = px.bar(df, x="Skill", y="Value", title="Skill Distribution")
        st.plotly_chart(fig, use_container_width=True)

        pie = px.pie(df, names="Skill", title="Skill Share")
        st.plotly_chart(pie)

# ---------------- PAGE 3 ----------------
elif page == "📌 Skill Insights":

    st.markdown('<div class="hero"><h1>📌 Skill Insights</h1></div>', unsafe_allow_html=True)

    data = st.session_state.data

    if not data:
        st.warning("Upload resume first")
    else:
        st.subheader("✅ Matching Skills")
        st.success(", ".join(data["keywords"][:15]))

        st.subheader("❌ Missing Skills")
        st.error(", ".join(data["missing"][:15]))

        if data["score"] < 50:
            st.warning("Improve resume with more skills")
        elif data["score"] < 75:
            st.info("Good resume, optimize keywords")
        else:
            st.success("Excellent Resume 🔥")

# ---------------- PAGE 4 ----------------
elif page == "ℹ️ About":

    st.markdown('<div class="hero"><h1>ℹ️ About</h1></div>', unsafe_allow_html=True)

    st.write("""
    This AI Resume Analyzer helps you:
    - Analyze resume
    - Match job description
    - Identify missing skills
    - Improve ATS score

    ### Tech Used:
    - Streamlit
    - NLP (Sklearn)
    - Plotly

    Built for Final Year Project 🚀
    """)
