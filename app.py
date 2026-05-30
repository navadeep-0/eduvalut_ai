from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
import requests
from docx import Document
import PyPDF2



app = Flask(__name__)
app.secret_key = "eduvault_secret_key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "navadeep"
app.config["MYSQL_PASSWORD"] = "Root@143"
app.config["MYSQL_DB"] = "eduvault_ai"

app.config["UPLOAD_FOLDER"] = "uploads"

mysql = MySQL(app)
bcrypt = Bcrypt(app)

if not os.path.exists("uploads"):
    os.makedirs("uploads")


def ask_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        if response.status_code != 200:
            return "LLM Error: Ollama server returned an error."

        data = response.json()
        return data.get("response", "No response received from Llama.")

    except requests.exceptions.ConnectionError:
        return "LLM Error: Ollama is not running. Open Command Prompt and run: ollama serve"

    except requests.exceptions.Timeout:
        return "LLM Error: Llama took too long to respond. Try again."

    except Exception as e:
        return f"LLM Error: {str(e)}"
def read_docx(path):
    doc = Document(path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_pdf(path):
    text = ""

    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return text


def read_resume_file(path):
    if path.endswith(".docx"):
        return read_docx(path)

    elif path.endswith(".pdf"):
        return read_pdf(path)

    else:
        return "Resume format not supported. Please upload PDF or DOCX."
    


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        role = request.form["role"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, roll_no, email, password, role) VALUES(%s,%s,%s,%s,%s)",
            (name, roll_no, email, password, role)
        )
        mysql.connection.commit()
        cur.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        roll_no = request.form["roll_no"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE roll_no=%s", (roll_no,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[4], password):
            session["roll_no"] = user[2]
            session["role"] = user[5]

            if user[5] == "admin":
                return redirect("/admin")
            else:
                return redirect("/student")

    return render_template("login.html")


@app.route("/student", methods=["GET", "POST"])
def student_dashboard():

    if "roll_no" not in session:
        return redirect("/login")

    if request.method == "POST":

        roll_no = session["roll_no"]

        tenth_marks = request.form["tenth_marks"]
        inter_marks = request.form["inter_marks"]
        btech_cgpa = request.form["btech_cgpa"]
        skills = request.form["skills"]
        certifications = request.form["certifications"]
        achievements = request.form["achievements"]

        resume = request.files["resume"]
        memo = request.files["memo"]

        resume_filename = roll_no + "_resume_" + resume.filename
        memo_filename = roll_no + "_memo_" + memo.filename

        resume_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume_filename
        )

        memo_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            memo_filename
        )

        resume.save(resume_path)
        memo.save(memo_path)

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO student_records
            (
                roll_no,
                tenth_marks,
                inter_marks,
                btech_cgpa,
                skills,
                certifications,
                achievements,
                resume_file,
                memo_file
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                roll_no,
                tenth_marks,
                inter_marks,
                btech_cgpa,
                skills,
                certifications,
                achievements,
                resume_filename,
                memo_filename
            )
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/student")

    return render_template("student_dashboard.html")


@app.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    search = request.args.get("search", "")

    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            "SELECT * FROM student_records WHERE roll_no LIKE %s OR skills LIKE %s",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cur.execute("SELECT * FROM student_records")

    records = cur.fetchall()
    cur.close()

    return render_template("admin_dashboard.html", records=records)


@app.route("/ai-roadmap/<roll_no>")
def ai_roadmap(roll_no):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_records WHERE roll_no=%s", (roll_no,))
    student = cur.fetchone()
    cur.close()

    if not student:
        return "Student record not found"

    resume_filename = os.path.basename(student[8])
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_filename)

    resume_text = read_resume_file(resume_path)

    if len(resume_text) > 1000:
        resume_text = resume_text[:1000]

    prompt = f"""
Analyze this student briefly.

Student:
CGPA: {student[4]}
Skills: {student[5]}
Certifications: {student[6]}
Achievements: {student[7]}

Resume:
{resume_text}

Give only:
1. ATS score out of 100
2. 3 strengths
3. 3 weaknesses
4. 3 missing keywords
5. 3 suitable job roles
6. final placement score out of 100
"""

    ai_text = ask_llm(prompt)

    result = f"""
<div class="score-box">
    <h2>1. AI Resume & ATS Analysis</h2>
    <pre>{ai_text}</pre>
</div>

<div class="report-card">
    <h2>2. Placement Roadmap Tree</h2>
    <div class="tree-box">
Student Placement Goal
├── Resume Improvement
│   ├── Add measurable achievements
│   ├── Add strong project descriptions
│   ├── Add role-based keywords
│   └── Add GitHub and LinkedIn links
├── Core Technical Skills
│   ├── Python
│   ├── SQL
│   ├── Data Structures
│   ├── HTML, CSS, JavaScript
│   └── Git & GitHub
├── AI / GenAI Skills
│   ├── NLP Basics
│   ├── LLM Concepts
│   ├── Prompt Engineering
│   ├── RAG Basics
│   └── Hugging Face
├── Projects To Build
│   ├── AI Resume Analyzer
│   ├── Student Placement Portal
│   ├── PDF Chatbot using LLM
│   └── AI Interview Preparation Bot
├── Certifications
│   ├── Kaggle Python
│   ├── Google ML Crash Course
│   ├── Hugging Face NLP Course
│   └── Salesforce Trailhead
└── Interview Preparation
    ├── Aptitude
    ├── Coding Practice
    ├── Technical Interview
    ├── HR Interview
    └── Mock Interviews
    </div>
</div>

<div class="report-card">
    <h2>3. 30-Day Placement Plan</h2>
    <ul>
        <li><b>Week 1:</b> Fix resume, add GitHub/LinkedIn, revise Python and SQL.</li>
        <li><b>Week 2:</b> Practice DSA basics, aptitude, and build one mini project.</li>
        <li><b>Week 3:</b> Build one strong AI/LLM project and upload it to GitHub.</li>
        <li><b>Week 4:</b> Apply to jobs, attend mock interviews, and prepare HR answers.</li>
    </ul>
</div>

<div class="report-card">
    <h2>4. Recommended Free Courses</h2>
    <ul>
        <li><a href="https://www.kaggle.com/learn/python" target="_blank">Kaggle Python</a></li>
        <li><a href="https://developers.google.com/machine-learning/crash-course" target="_blank">Google Machine Learning Crash Course</a></li>
        <li><a href="https://huggingface.co/learn/nlp-course" target="_blank">Hugging Face NLP Course</a></li>
        <li><a href="https://www.freecodecamp.org/learn/" target="_blank">freeCodeCamp</a></li>
        <li><a href="https://trailhead.salesforce.com/" target="_blank">Salesforce Trailhead</a></li>
    </ul>
</div>

<div class="report-card">
    <h2>5. Job Application Links</h2>
    <ul>
        <li><a href="https://www.linkedin.com/jobs/search/?keywords=python%20developer" target="_blank">LinkedIn - Python Developer Jobs</a></li>
        <li><a href="https://www.naukri.com/python-developer-jobs" target="_blank">Naukri - Python Developer Jobs</a></li>
        <li><a href="https://internshala.com/internships/python-internship" target="_blank">Internshala - Python Internships</a></li>
        <li><a href="https://www.linkedin.com/jobs/search/?keywords=data%20analyst" target="_blank">LinkedIn - Data Analyst Jobs</a></li>
        <li><a href="https://www.naukri.com/data-analyst-jobs" target="_blank">Naukri - Data Analyst Jobs</a></li>
    </ul>
</div>
"""

    return render_template("ai_roadmap.html", result=result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)