# AI Resume Screening System (Enhanced Version)

This repository contains an AI-powered Resume Screening application built using **Streamlit**.  
It allows users to upload a **PDF resume** or paste resume text directly, and the system evaluates overall resume strength.

---

## 🚀 Features

### ✅ PDF Resume Upload
Upload a PDF file — the app extracts all text using `pdfminer.six`.

### ✅ Manual Resume Text Input
Users can paste their resume text directly if they don’t want to upload a file.

### ✅ Skills Extraction
Automatically detects predefined technical skills such as:
- Python, Java, SQL, C++
- Machine Learning, Deep Learning
- AWS, Docker, Kubernetes  
(and more)

### ✅ Experience Scoring
Counts strong action verbs like:
- managed, led, developed, created, designed, built, implemented

### ✅ Keyword Score
Counts total words to estimate resume richness.

### ✅ Weak Points Detection
The system identifies common resume weaknesses:
- Resume too short  
- No action verbs (weak experience section)  
- Very few technical skills  
- No measurable achievements (missing numbers)  

### 🧹 Cleaned Resume View
Shows processed/cleaned text used for analysis.

---

## 📂 Project Structure

