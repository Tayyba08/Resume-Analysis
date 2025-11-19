import streamlit as st
import re
import pickle
import language_tool_python
from PyPDF2 import PdfReader

# ============================================
# Load ML Model and TF-IDF Vectorizer
# ============================================
model = pickle.load(open("resume_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf.pkl", "rb"))

# Grammar Checking Tool
tool = language_tool_python.LanguageTool('en-US')

# ============================================
# Skills Dictionary
# ============================================
skills_dict = [
    'python','java','sql','machine learning','deep learning','excel',
    'communication','leadership','html','css','javascript','data analysis',
    'project management','tableau','power bi','problem solving','react',
    'cloud','aws','api','django','flask'
]

# Important Skills (Weak Points check)
important_skills = ['python','sql','communication','project management','machine learning']

# Action Verbs for Experience Score
action_verbs = [
    'managed','led','developed','created','designed','organized',
    'implemented','supervised','analyzed','optimized'
]

# ============================================
# Clean Text Function
# ============================================
def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ============================================
# Extract Text from PDF
# ============================================
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# ============================================
# Streamlit UI
# ============================================
st.title("📄 AI Resume Screening System (PDF + Weak Points Analysis)")

uploaded_pdf = st.file_uploader("Upload Your Resume (PDF Only)", type=['pdf'])

if uploaded_pdf is not None:
    st.success("PDF Uploaded Successfully!")

    if st.button("Analyze Resume"):

        # Extract PDF Text
        raw_text = extract_pdf_text(uploaded_pdf)
        st.subheader("📌 Extracted Text (Preview)")
        st.write(raw_text[:1000] + " ...")

        clean_r = clean(raw_text)

        # ============================================
        # Skills Score
        # ============================================
        matched_skills = [s for s in skills_dict if s in clean_r]
        skills_score = len(matched_skills)

        # ============================================
        # Keyword Score (TF-IDF)
        # ============================================
        tfidf_score = vectorizer.transform([clean_r]).sum()

        # ============================================
        # Experience Score
        # ============================================
        exp_score = sum(clean_r.count(v) for v in action_verbs)

        # ============================================
        # Grammar Score
        # ============================================
        matches = tool.check(clean_r)
        grammar_score = max(10 - len(matches), 0)

        # ============================================
        # Final Score Calculation
        # ============================================
        final_score = (
            (skills_score * 25) +
            (tfidf_score * 30) +
            (exp_score * 25) +
            (grammar_score * 10)
        )

        # ============================================
        # WEAK POINTS DETECTION
        # ============================================
        weak_points = []

        if skills_score < 3:
            weak_points.append("Very few technical skills found.")

        if tfidf_score < 1:
            weak_points.append("Resume lacks important job-related keywords.")

        if exp_score == 0:
            weak_points.append("No strong action verbs (developed, managed, created, etc.) found.")

        if grammar_score < 7:
            weak_points.append("Too many grammar mistakes detected.")

        if len(raw_text) < 300:
            weak_points.append("Resume is too short. Add more work experience details.")

        missing = [skill for skill in important_skills if skill not in clean_r]
        if len(missing) > 0:
            weak_points.append("Missing important skills: " + ", ".join(missing))

        # ============================================
        # Display Results
        # ============================================
        st.subheader("📊 Resume Scores")
        st.write("Matched Skills:", matched_skills)
        st.write("Skills Score:", skills_score)
        st.write("Keyword Score:", float(tfidf_score))
        st.write("Experience Score:", exp_score)
        st.write("Grammar Score:", grammar_score)

        st.success(f"🎯 Final Resume Score: **{final_score:.2f} / 100**")

        # ============================================
        # WEAK POINTS SECTION
        # ============================================
        st.subheader("⚠️ Weak Points")
        if len(weak_points) == 0:
            st.success("No major weak points! Your resume is strong.")
        else:
            for w in weak_points:
                st.warning(f"- {w}")

        # ============================================
        # Job Category Prediction
        # ============================================
        st.subheader("📌 Predicted Job Category")
        features = [[skills_score, float(tfidf_score), exp_score, grammar_score]]
        pred = model.predict(features)
        st.info(f"Predicted Job Category: **{pred[0]}**")
