# AI Resume Screening System

This is a **Streamlit-based AI Resume Screening App** that analyzes resumes to evaluate skills, experience, keyword usage, and provides an overall score along with visual insights.

---

## Features

- **Skills Detection**: Identifies key skills mentioned in the resume and calculates skills coverage.  
- **Experience Highlights**: Counts action verbs to evaluate experience sections.  
- **Keyword Score**: Total word count in the resume.  
- **Overall Resume Score**: Weighted score (0-100) combining skills, experience, and keywords.  
- **Weak Points / Suggested Improvements**: Highlights areas where the resume can be improved.  
- **Visualizations**:  
  - Skills coverage pie chart  
  - Action verbs (experience) bar chart  
  - Overall resume score progress bar with color-coded indicator (green=strong, yellow=average, red=weak)

---

## Installation

1. Clone the repository or download the code.
2. Install required Python packages:

```bash
pip install -r requirements.txt
