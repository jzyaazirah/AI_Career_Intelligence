
import streamlit as st
import subprocess
import sys
subprocess.check_call([sys.executable,"-m","pip","install","pdfminer.six"])

from pdfminer.six import extract_text
import pandas as pd
import json

# App Title
st.title("AI Career Intelligence Platform")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# Load roles and jobs
with open("roles.json") as f:
    roles = json.load(f)

jobs_df = pd.read_csv("jobs.csv")

if uploaded_file:
    # Extract text from PDF
    text = extract_text(uploaded_file)
    st.subheader("Resume Text (Preview)")
    st.write(text[:500], "...")  # show first 500 characters

    # Simple skill extraction
    resume_skills = []
    for role, skills in roles.items():
        for skill in skills:
            if skill.lower() in text.lower() and skill not in resume_skills:
                resume_skills.append(skill)

    st.subheader("Skills Found")
    st.write(resume_skills)

    # ATS Keyword Suggestions
    st.subheader("ATS Keyword Suggestions (Missing Skills)")
    required_skills = [skill for sublist in roles.values() for skill in sublist]
    missing_skills = list(set(required_skills) - set(resume_skills))
    st.write(missing_skills)

    # Show jobs table
    st.subheader("Job Opportunities")
    st.table(jobs_df)


