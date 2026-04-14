import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🧠 AI Resume Analyzer")

# Load skills
def load_skills():
    with open("skills.txt", "r") as f:
        skills = f.read().splitlines()
    return skills

skills_list = load_skills()

# Extract text from PDF
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + " "
    return text.lower()

# Skill extraction
def extract_skills(text):
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

# ATS Score
def ats_score(text, skills):
    score = 0
    
    # Skill score
    score += len(skills) * 5
    
    # Keyword score
    keywords = ["project", "experience", "education", "skills"]
    for word in keywords:
        if word in text:
            score += 5
    
    return min(score, 100)

# Suggestions
def give_suggestions(score, skills):
    suggestions = []
    
    if score < 50:
        suggestions.append("Add more relevant skills.")
        suggestions.append("Include projects and experience.")
    
    if "machine learning" not in skills:
        suggestions.append("Consider adding Machine Learning skills.")
    
    if "communication" not in skills:
        suggestions.append("Add soft skills like communication.")
    
    return suggestions

# Upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)
    
    st.subheader("📄 Extracted Resume Text")
    st.write(text[:1000])
    
    skills = extract_skills(text)
    
    st.subheader("💡 Skills Found")
    st.write(skills)
    
    score = ats_score(text, skills)
    
    st.subheader("📊 ATS Score")
    st.progress(score)
    st.write(f"{score}/100")
    
    suggestions = give_suggestions(score, skills)
    
    st.subheader("📌 Suggestions")
    for s in suggestions:
        st.write("✔️", s)
