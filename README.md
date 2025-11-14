<div align="center">

<h1>🧠 Resume Assessment & Objective MCQ Generator</h1>
<p>
<strong>An AI-powered agent that ingests a resume (PDF / Image / Text) and a Job Description, then produces an objective assessment and interactive multiple-choice questions with instant feedback.</strong>
</p>
<img width="1600" height="4767" alt="1" src="https://github.com/user-attachments/assets/daeebe4c-b0a0-4bcd-a3e9-db290460a248"   width="650"/>

<br/>
<a href="#features"><img src="https://img.shields.io/badge/status-active-brightgreen" /></a>
<a href="#tech-stack"><img src="https://img.shields.io/badge/python-3.10+-blue" /></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey" /></a>
<a href="https://openai.com"><img src="https://img.shields.io/badge/LLM-OpenAIChat-purple" /></a>

</div>

---

## 📌 Overview
This project helps candidates and recruiters quickly evaluate how well a resume aligns with a job description. It returns:

- Objective match score (0–100) with rationale
- Strengths mapped to JD requirements
- Gaps / missing skills / risks
- Actionable recommendations to tailor the resume
- A set of auto-generated MCQs (4 options each) based on resume-JD alignment
- Interactive answer submission with correctness + explanations

The UI is built in Streamlit; the assessment/MCQ generation uses the `agno` agent framework with an OpenAI chat model.

---

## ✨ Features
- Upload resume: PDF, image (OCR via Tesseract), or raw text
- Paste Job Description directly
- JSON-based agent output (strict schema) for reliability
- Interactive MCQs with scoring & downloadable results
- Session persistence via SQLite (`user_memories/data.db`)
- Resilient PDF extraction (pdfminer + PyPDF2 fallback)
- Easy extensibility for more question types (true/false, scenario-based, etc.)

---

## 🗂️ Project Structure
```
llm_agent.py                  # Agent orchestration & LLM prompt schema
streamlit_interface.py        # Streamlit UI for input, MCQs & feedback
resume_handling/              # Resume ingestion utilities
  pdf_user_resume.py          # PDF parsing (pdfminer + PyPDF2 fallback)
  image_user_resume.py        # OCR via pytesseract
  text_user_resume.py         # Plain text passthrough
user_memories/                # SQLite DB file (auto-created)
README.md                     # Project documentation
requirements.txt              # Python dependencies
```

---

## 🧪 Output JSON Schema
```json
{
  "assessment_markdown": "# Score...",
  "mcqs": [
    {
      "question": "Which skill is missing?",
      "options": ["Docker", "Kubernetes", "Git", "Linux"],
      "answer_index": 1,
      "explanation": "JD emphasizes container orchestration absent in resume."
    }
  ]
}
```

---

## 🏗️ Tech Stack
| Layer | Tools |
|-------|-------|
| UI | Streamlit |
| LLM Agent | agno Agent + OpenAIChat (gpt-4o or compatible) |
| Persistence | SQLite (via agno) |
| PDF Parsing | pdfminer.six, PyPDF2 |
| OCR | pytesseract + Tesseract binary |
| Imaging | Pillow |

---

## 🔧 Prerequisites
1. Python 3.10+ recommended
2. OpenAI API key
3. Tesseract OCR (for image resumes)
   - Windows installer: https://github.com/UB-Mannheim/tesseract/wiki
   - Default path assumed: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`
4. (Optional) Virtual environment

---

## 🚀 Installation & Setup
```powershell
git clone https://github.com/pawan941394/evaluate-resume-with-job-description-and-make-assessment.git
cd "evaluate-resume-with-job-description-and-make-assessment"

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

For image resumes, ensure Tesseract is installed. Adjust path in `resume_handling/image_user_resume.py` if needed.

---

## 🔑 Environment
Set the OpenAI API key in PowerShell or through the Streamlit sidebar:
```powershell
$Env:OPENAI_API_KEY = "sk-yourkey"
```

---

## ▶️ Run the App
```powershell
streamlit run streamlit_interface.py
```
Workflow:
1. Enter API key
2. Select resume source type
3. Upload/paste resume
4. Paste Job Description
5. Generate & interact with MCQs

---

## 📤 Downloadable Results
After submission you can download a Markdown summary including assessment, MCQs and score.

---

## 🧩 Extensibility Ideas
- Adjustable MCQ count
- Difficulty levels
- Embedding-based skill gap analysis
- Export as PDF/JSON API
- Additional question formats

---

## 🛠️ Troubleshooting
| Issue | Resolution |
|-------|------------|
| Empty OCR | Check Tesseract path & image clarity |
| PDF empty | Try alternate PDF (security restrictions) |
| Non-JSON output | Regenerate; strict schema prompt included |
| Radio render error | Ensure 4 options per MCQ |

---

## 🤝 Contributing
Fork → Branch → Commit → Push → PR.

---

## 📄 License
MIT License (see `LICENSE`).

---

## 📽️ Demo / Animation
Place a GIF at `assets/demo.gif` (record with ScreenToGif or OBS). Update link above.

---

## ✅ Publish Checklist
- [ ] Add demo GIF
- [ ] Verify dependency versions
- [ ] Add any missing badges
- [ ] Confirm LICENSE exists

---

## 💬 Acknowledgements
- Tesseract OCR (UB Mannheim build)
- OpenAI API
- agno agent framework

Enjoy building smarter resume assessments! 🎯
