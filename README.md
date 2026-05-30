# EduVault AI – Intelligent Student Portfolio & Placement Readiness Platform

## Overview

EduVault AI is an AI-powered student portfolio management and placement readiness platform designed to help educational institutions digitally manage student academic records, certifications, resumes, achievements, and placement preparation activities.

The platform serves as a centralized repository where students can securely upload and maintain their educational information while administrators can easily access, filter, and analyze student profiles.

By integrating Large Language Models (LLMs), EduVault AI goes beyond traditional student databases and provides intelligent career guidance, resume analysis, ATS scoring, placement readiness evaluation, skill-gap analysis, personalized learning roadmaps, and job recommendations.

---

## Problem Statement

Most colleges maintain student information across multiple spreadsheets, documents, and departmental databases, making it difficult to:

- Track student achievements
- Access academic records quickly
- Monitor placement readiness
- Identify skill gaps
- Recommend career paths
- Provide personalized placement guidance

Students also lack a centralized platform to maintain their complete academic and professional profile.

EduVault AI addresses these challenges by combining student portfolio management with AI-driven placement assistance.

---

## Objectives

### Primary Objectives

- Digitally store student academic records
- Maintain resumes and educational documents
- Track certifications and achievements
- Simplify profile access for administrators
- Improve placement preparation

### AI Objectives

- Resume Analysis
- ATS Score Generation
- Placement Readiness Evaluation
- Skill Gap Analysis
- Career Path Recommendations
- Personalized Learning Roadmaps
- Course Recommendations
- Interview Preparation Guidance

---

# Key Features

## Student Module

Students can:

- Register and Login
- Upload Academic Records
- Upload Resume
- Upload Marks Memos
- Add Certifications
- Add Skills
- Add Achievements
- Update Personal Information

---

## Admin Module

Administrators can:

- View All Student Records
- Search Students by Roll Number
- Filter Students by Skills
- Access Uploaded Resumes
- Access Academic Documents
- Analyze Placement Readiness
- Generate AI Career Reports

---

## AI Placement Readiness Module

Using Local LLM Integration (Ollama + TinyLlama/Mistral/Llama 3.1), the system can:

### Resume Analysis

- Analyze Resume Content
- Identify Strengths
- Identify Weaknesses
- Detect Missing Keywords

### ATS Score Evaluation

Provides:

- ATS Score (/100)
- Resume Improvement Suggestions
- Keyword Optimization Recommendations

### Career Guidance

Generates:

- Suitable Job Roles
- Skill Recommendations
- Learning Roadmaps
- Placement Preparation Plans

### Learning Resources

Recommends:

- Free Courses
- Certifications
- Practice Platforms
- Interview Resources

---

# AI Technologies Used

## Large Language Models (LLMs)

Integrated through Ollama:

- TinyLlama
- Mistral
- Llama 3.1

The AI system processes student profiles and generates placement readiness insights.

---

## Placement Analysis Components

### ATS Analysis

Evaluates:

- Resume Structure
- Keyword Density
- Technical Skills
- Certifications
- Projects
- Job Readiness

### Skill Gap Analysis

Identifies:

- Missing Technical Skills
- Missing Soft Skills
- Industry Requirements

### Personalized Roadmap Generation

Creates:

- Learning Path
- Project Suggestions
- Certification Recommendations
- Placement Preparation Plan

---

# System Architecture

```text
Student
   |
   v
Student Dashboard
   |
   v
Flask Backend
   |
   +-------------------+
   |                   |
   v                   v
MySQL Database     Uploaded Files
   |                   |
   +--------+----------+
            |
            v
        LLM Engine
        (Ollama)
            |
            v
 AI Placement Report
```

---

# Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## Database

- MySQL

## AI Layer

- Ollama
- TinyLlama
- Mistral
- Llama 3.1

## Security

- Bcrypt Password Hashing
- Session Management

## File Management

- Resume Upload
- Memo Upload
- Secure Storage

---

# Database Design

## Users Table

Stores:

- User ID
- Name
- Roll Number
- Email
- Password
- Role

### Roles

- Student
- Admin

---

## Student Records Table

Stores:

- Roll Number
- 10th Marks
- Intermediate Marks
- BTech CGPA
- Skills
- Certifications
- Achievements
- Resume File
- Memo File

---

# Folder Structure

```text
edulocker/
│
├── app.py
├── database.sql
├── requirements.txt
├── README.md
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   └── ai_roadmap.html
│
├── uploads/
│   ├── resumes
│   └── memos
│
└── __pycache__/
```

---

# Installation Guide

## Clone Repository

```bash
git clone <repository-url>
cd edulocker
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Database

Open MySQL Workbench:

```sql
CREATE DATABASE eduvault_ai;
```

Run:

```sql
database.sql
```

---

## Configure MySQL

Inside app.py:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'eduvault_ai'
```

---

## Install Ollama

Download:

https://ollama.com

---

## Pull TinyLlama

```bash
ollama pull tinyllama
```

---

## Start Flask

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Future Enhancements

- PDF Resume Parsing
- Automatic Resume Builder
- Real-Time Job Recommendations
- LinkedIn Integration
- Student Ranking Dashboard
- Placement Analytics
- Recruiter Portal
- AI Interview Simulator
- Voice-Based Career Assistant
- Cloud Deployment
- Multi-College Support
- Mobile Application

---

# Research Contribution

EduVault AI demonstrates how Large Language Models can be integrated into educational management systems to provide intelligent placement support, resume evaluation, and personalized career guidance.

The project combines:

- Student Information Management
- Artificial Intelligence
- Resume Analytics
- Placement Readiness Assessment
- Career Recommendation Systems

into a single platform.

---

# Author

**Pavan Reddy**

BBA – Digital Technology  
Mahindra University

### Interests

- Artificial Intelligence
- Generative AI
- Large Language Models
- Product Development
- Entrepreneurship
- Placement Technology Solutions

---

# License

This project is developed for educational and academic purposes.

© 2026 EduVault AI
