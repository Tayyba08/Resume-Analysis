import streamlit as st
import re
from pdfminer.high_level import extract_text

# -------------------------
# TEXT CLEANING FUNCTION
# -------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------
# SKILLS DICTIONARY
# -------------------------
skills_dict = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "excel", "power bi", "tableau", "django", "flask", "html", "css",
    "javascript", "react", "node", "aws", "docker", "kubernetes"
]

# -------------------------
# ACTION VERBS FOR EXPERIENCE
# -------------------------
action_verbs = [
    "managed", "led", "developed", "created", "designed",
    "organized", "implemented", "built", "optimized"
]

# -------------------------
# WEAK POINTS FINDER
# -------------------------
def find_weak_points(text):
    weak_points = []

    # 1. Too short resume
    if len(text.split()) < 100:
        weak_points.append("Resume seems too short.")

    # 2. No action verbs (weak experience section)
    if not any(verb in text for verb in action_verbs):
        weak_points.append("Weak experience section (no action verbs found).")

    # 3. Few or no skills
    matched = [skill for skill in skills_dict if skill in text]
    if len(matched) < 3:
        weak_points.append("Very few technical skills detected.")

    # 4. No numbers (metrics missing)
    if not re.search(r"\d", text):
        weak_points.append("No measurable achievements (no numbers found).")

    return weak_points

# -------------------------
# STREAMLIT APP UI
# -------------------------
st.set_page_config(page_title="AI Resume Screening App", layout="wide")
st.title("AI Resume Screening System")

st.write("Upload your resume as PDF or paste the text below:")

resume_text = ""

# PDF upload
uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_pdf is not None:
    try:
        resume_text = extract_text(uploaded_pdf)
        st.success("PDF text extracted successfully!")
    except:
        st.error("Error reading PDF file.")

# Manual text input
manual_text = st.text_area("Or paste your resume text here:", height=250)

if manual_text.strip():
    resume_text = manual_text

# -------------------------
# RUN ANALYSIS
# -------------------------
if st.button("Analyze Resume"):

    if not resume_text.strip():
        st.warning("Please upload a PDF or paste resume text.")
        st.stop()

    cleaned = clean_text(resume_text)

    # Skills score
    matched_skills = [skill for skill in skills_dict if skill in cleaned]
    skills_score = len(matched_skills)

    # Keyword score
    keyword_score = len(cleaned.split())

    # Experience score
    experience_score = sum(cleaned.count(verb) for verb in action_verbs)

    # Weak points
    weak_points = find_weak_points(cleaned)

    # -------------------------
    # SHOW RESULTS
    # -------------------------
    st.subheader("Resume Analysis Results")

    st.write("### Matched Skills:")
    st.write(matched_skills if matched_skills else "No major skills detected.")

    st.write("### Score Summary:")
    st.write(f"**Skills Score:** {skills_score}")
    st.write(f"**Keyword Score:** {keyword_score}")
    st.write(f"**Experience Score:** {experience_score}")

    st.write("### Weak Points:")
    if weak_points:
        for wp in weak_points:
            st.error(f"- {wp}")
    else:
        st.success("No major weak points found! Your resume looks strong.")

    st.write("### Cleaned Resume Text (for reference):")
    st.text(cleaned)

