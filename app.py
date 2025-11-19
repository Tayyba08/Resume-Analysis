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
# FULL SKILLS DICTIONARY (UPDATED)
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
    'social media', 'digital marketing', 'seo', 'content writing', 'analytics',
    'team leadership', 'coaching', 'mentoring', 'training', 'networking',
    'customer relations', 'event planning', 'salesforce', 'crm', 'excel pivot',
    'power bi', 'tableau', 'cloud computing', 'aws', 'azure', 'gcp',
    'linux', 'windows', 'network security', 'cybersecurity', 'risk management',
    'budgeting', 'strategic planning', 'negotiation', 'procurement', 'logistics',
    'supply chain', 'operations', 'classroom management',
    'lesson planning', 'curriculum design', 'fitness training',
    'agriculture', 'farm management', 'bpo', 'customer support', 'engineering',
    'mechanical', 'electrical', 'civil', 'aviation', 'chef', 'hospitality',
    'apparel', 'fashion', 'public relations', 'banking', 'arts', 'digital media'
]

# Remove duplicates
skills_dict = list(set(skills_dict))

# -------------------------
# ACTION VERBS FOR EXPERIENCE
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
# WEAK POINTS FINDER
# -------------------------
def find_weak_points(text):
    weak_points = []

    # 1. Too short
    if len(text.split()) < 100:
        weak_points.append("Resume seems too short.")

    # 2. No action verbs
    if not any(verb in text for verb in action_verbs):
        weak_points.append("Weak experience section (no action verbs found).")

    # 3. Low skills count
    matched = [skill for skill in skills_dict if skill in text]
    if len(matched) < 5:
        weak_points.append("Very few skills detected.")

    # 4. No numbers
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
        st.success("PDF extracted successfully!")
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

    # Keyword score (total words)
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
        st.success("No major weak points found!")

    st.write("### Cleaned Resume Text:")
    st.text(cleaned)


