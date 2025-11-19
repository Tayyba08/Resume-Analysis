
import streamlit as st
import re
import pickle
import os

# Basic text cleaning
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Extract skills
skills_dict = [
    'python','java','sql','machine learning','deep learning','excel','communication',
    'leadership','tensorflow','pytorch','html','css','javascript','data analysis',
    'project management','tableau','power bi','problem solving'
]

def extract_skills(text):
    return [skill for skill in skills_dict if skill in text]

# Experience score
action_verbs = ['managed','led','developed','created','designed','organized']
def experience_score(text):
    return sum(text.count(v) for v in action_verbs)

# Grammar score (simple fallback)
def grammar_score(text):
    return 7

# TF-IDF score (fallback if model not uploaded)
def keyword_score(text):
    return len(set(text.split())) / 10

# Final score
def final_score(skills, key, exp, grammar):
    return skills*2 + key*3 + exp*2 + grammar

st.title("AI Resume Screening System")

resume = st.text_area("Paste your resume text here...", height=300)

if st.button("Analyze"):
    clean = clean_text(resume)
    skills = extract_skills(clean)
    exp = experience_score(clean)
    key = keyword_score(clean)
    gram = grammar_score(clean)
    score = final_score(len(skills), key, exp, gram)

    st.subheader("Results")
    st.write("Matched Skills:", skills)
    st.write("Skills Score:", len(skills))
    st.write("Keyword Score:", key)
    st.write("Experience Score:", exp)
    st.write("Grammar Score:", gram)
    st.success(f"Final Score: {score}")
