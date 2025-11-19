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
# STREAMLIT APP UI
# -------------------------
st.set_page_config(page_title="AI Resume Screening App", layout="wide")
st.title("AI Resume Screening System")
st.write("Upload your resume as PDF or paste the text below:")

resume_text = ""

uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])
if uploaded_pdf is not None:
    try:
        resume_text = extract_text(uploaded_pdf)
        st.success("PDF extracted successfully!")
    except:
        st.error("Error reading PDF file.")

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

    # Skills detection
    matched_skills = [skill for skill in skills_dict if skill in cleaned]
    skills_score = len(matched_skills)
    skills_coverage = round((skills_score / len(skills_dict)) * 100, 2)

    # Keyword score
    keyword_score = len(cleaned.split())

    # Experience score
    experience_score = sum(cleaned.count(verb) for verb in action_verbs)

    # Weak points
    weak_points = find_weak_points(cleaned, matched_skills, experience_score)

    # Overall Resume Score (weighted)
    resume_score = round(
        0.4 * skills_coverage + 
        0.3 * min(experience_score, 50) * 2 + 
        0.2 * min(keyword_score, 100), 2
    )

    # -------------------------
    # SHOW RESULTS
    st.subheader("Resume Analysis Results")
    st.write("### Matched Skills:")
    st.write(matched_skills if matched_skills else "No major skills detected.")

    st.write("### Score Summary:")
    st.write(f"**Skills Score:** {skills_score} / {len(skills_dict)} ({skills_coverage}%)")
    st.write(f"**Keyword Score (Total Words):** {keyword_score}")
    st.write(f"**Experience Score (Action Verbs Count):** {experience_score}")
    st.write(f"**Overall Resume Score:** {resume_score}/100")

    # Overall Resume Score Indicator
    st.write("### Overall Resume Score Indicator")
    if resume_score >= 80:
        color = "#4CAF50"
        status = "Strong Resume"
    elif resume_score >= 50:
        color = "#FFC107"
        status = "Average Resume"
    else:
        color = "#F44336"
        status = "Weak Resume"

    st.markdown(f"<h3 style='color:{color};'>Score: {resume_score}/100 — {status}</h3>", unsafe_allow_html=True)
    st.progress(int(resume_score))

    # -------------------------
    # Score Summary Pie Chart (Smaller)
    st.write("### Score Summary Visualization")
    labels = ['Skills Score', 'Experience Score', 'Keyword Score']
    sizes = [
        min(skills_score, len(skills_dict)),
        min(experience_score, 50),
        min(keyword_score, 100)
    ]
    colors = ['#4CAF50', '#2196F3', '#FFC107']
    fig, ax = plt.subplots(figsize=(4,4))  # smaller pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

    # -------------------------
    # Experience Highlights (Smaller Bar Chart)
    st.write("### Experience Highlights")
    verb_counts = {verb: cleaned.count(verb) for verb in action_verbs if cleaned.count(verb) > 0}
    if verb_counts:
        fig2, ax2 = plt.subplots(figsize=(8,3))  # smaller figure
        ax2.barh(list(verb_counts.keys()), list(verb_counts.values()), color='#2196F3')
        ax2.set_xlabel("Count in Resume")
        ax2.set_ylabel("Action Verbs")
        st.pyplot(fig2)
    else:
        st.info("No action verbs detected for experience highlights.")

    # -------------------------
    # Weak points / suggestions
    st.write("### Suggested Improvements")
    if weak_points:
        for wp in weak_points:
            st.error(f"- {wp}")
    else:
        st.success("No major weak points found! Resume looks good.")

    # Cleaned Resume Text (Paragraph Form)
    st.write("### Cleaned Resume Text:")
    st.write(" ".join(cleaned.split()))  # shows as readable paragraph
