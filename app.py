import streamlit as st
from resume_parser import extract_text, extract_skills
from job_recommender import get_job_links

st.title("AI Resume Job Recommender ")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)
    skills = extract_skills(text)
    
    st.subheader(" Detected Skills")
    st.write(skills)
    
    job_links = get_job_links(skills)
    
    st.subheader(" Recommended Jobs")
    
    for role, link in job_links:
        st.markdown(f"👉 [{role}]({link})")