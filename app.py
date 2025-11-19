import streamlit as st
import re
from pdfminer.high_level import extract_text
import matplotlib.pyplot as plt

# -------------------------
# TEXT CLEANING FUNCTION
# -------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------
# FULL SKILLS DICTIONARY
# -------------------------
skills_dict = [
    'python', 'sql', 'excel', 'machine learning', 'data analysis',
    'communication', 'teamwork', 'project management', 'design', 'photoshop',
    'teaching', 'leadership', 'marketing', 'sales', 'accounting', 'finance',
    'healthcare', 'customer service', 'research', 'public speaking', 'writing',
    'problem solving', 'data entry', 'presentation', 'project planning',
    'creative thinking', 'time management', 'html', 'css', 'javascript',
    'java', 'c++', 'react', 'angular', 'node.js', 'database', 'sql server',
    'oracle', 'illustrator', 'autocad', 'solidworks', 'adobe xd',
    'social media', 'digital marketing', 'seo', 'content writing', 'analytics'
]
skills_dict = list(set(skills_dict))

# -------------------------
# ACTION VERBS
# -------------------------
action_verbs = [
    "managed", "led", "developed", "created", "designed", "organized",
    "implemented", "built", "optimized", "executed", "achieved", "supervised",
    "coordinated", "improved", "increased", "decreased", "delivered",
    "launched", "enhanced", "maintained", "streamlined", "analyzed",
    "evaluated", "planned", "trained", "mentored", "supported", "resolved",
    "researched", "produced", "initiated", "facilitated", "collaborated",
    "negotiated", "documented", "upgraded", "tested", "monitored",
    "configured", "engineered", "programmed", "assisted", "advised",
    "recommended", "presented", "oversaw"
]

# -------------------------
# WEAK POINTS FUNCTION
# -------------------------
def find_weak_points(text, matched_skills, experience_score):
    weak_points = []
    if len(text.split()) < 100:
        weak_points.append("Resume seems too short.")
    if experience_score == 0:
        weak_points.append("Weak experience section (no action verbs found).")
    if len(matched_skills) < 5:
        weak_points.append("Very few skills detected.")
    if not re.search(r"\d", text):
        weak_points.append("No measurable achievements (no numbers found).")
    return weak_points

# -------------------------
# STREAMLIT UI SETUP
# -------------------------
st.set_page_config(page_title="AI Resume Screening", layout="wide")
st.markdown("<h1 style='text-align:center; color:#1F77B4;'>📄 AI Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#555;'>Upload PDF or paste your resume text below</h4>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# SIDEBAR UPLOAD
# -------------------------
st.sidebar.title("Resume Analyzer")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
manual_text = st.sidebar.text_area("Or paste resume text here:", height=200)

resume_text = ""
if uploaded_pdf is not None:
    try:
        resume_text = extract_text(uploaded_pdf)
        st.sidebar.success("PDF extracted successfully!")
    except:
        st.sidebar.error("Error reading PDF file.")

if manual_text.strip():
    resume_text = manual_text

# -------------------------
# ANALYSIS
# -------------------------
if st.button("Analyze Resume"):

    if not resume_text.strip():
        st.warning("Please upload PDF or paste resume text.")
        st.stop()

    cleaned = clean_text(resume_text)
    matched_skills = [skill for skill in skills_dict if skill in cleaned]
    skills_score = len(matched_skills)
    skills_coverage = round((skills_score / len(skills_dict)) * 100, 2)
    keyword_score = len(cleaned.split())
    experience_score = sum(cleaned.count(verb) for verb in action_verbs)
    weak_points = find_weak_points(cleaned, matched_skills, experience_score)

    resume_score = round(
        0.4 * skills_coverage + 
        0.3 * min(experience_score, 50) * 2 + 
        0.2 * min(keyword_score, 100), 2
    )

    # -------------------------
    # TWO COLUMN LAYOUT
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("📑 Resume Preview")
        st.write(" ".join(cleaned.split()))

    with col2:
        st.subheader("💼 Detected Skills")
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"<span style='background-color:#FFDD57; padding:5px 12px; border-radius:12px; margin:2px; display:inline-block;'>{skill.capitalize()}</span>", unsafe_allow_html=True)
        else:
            st.info("No major skills detected.")

    # -------------------------
    # SCORE INDICATOR
    st.subheader("🏆 Overall Resume Score")
    if resume_score >= 80:
        color = "#4CAF50"
        status = "Strong Resume"
    elif resume_score >= 50:
        color = "#FFC107"
        status = "Average Resume"
    else:
        color = "#F44336"
        status = "Weak Resume"

    st.markdown(f"<h3 style='color:{color};'>{resume_score}/100 — {status}</h3>", unsafe_allow_html=True)
    st.progress(int(resume_score))

    # -------------------------
    # PIE CHART
    st.subheader("📊 Score Breakdown")
    labels = ['Skills Score','Experience Score','Keyword Score']
    sizes = [min(skills_score,len(skills_dict)), min(experience_score,50), min(keyword_score,100)]
    colors = ['#4CAF50','#2196F3','#FFC107']
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

    # -------------------------
    # ACTION VERB HIGHLIGHTS
    st.subheader("📌 Experience Highlights")
    verb_counts = {verb: cleaned.count(verb) for verb in action_verbs if cleaned.count(verb) > 0}
    if verb_counts:
        fig2, ax2 = plt.subplots(figsize=(8,3))
        ax2.barh(list(verb_counts.keys()), list(verb_counts.values()), color='#2196F3')
        ax2.set_xlabel("Count")
        ax2.set_ylabel("Action Verbs")
        st.pyplot(fig2)
    else:
        st.info("No action verbs detected.")

    # -------------------------
    # WEAK POINTS
    st.subheader("⚠ Suggested Improvements")
    if weak_points:
        for wp in weak_points:
            st.error(f"- {wp}")
    else:
        st.success("No major weak points found! Resume looks good.")

