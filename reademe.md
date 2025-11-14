<div align="center">

<h1>🧠 Resume Assessment & Objective MCQ Generator</h1>
<p>
<strong>An AI-powered agent that ingests a resume (PDF / Image / Text) and a Job Description, then produces an objective assessment and interactive multiple-choice questions with instant feedback.</strong>
</p>

<img src="https://raw.githubusercontent.com/USER/REPO/main/assets/demo.gif" alt="Demo" width="650" />
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
reademe.md                    # This README (rename to README.md if desired)
requirements.txt              # Python dependencies
```

---

## 🧪 Output JSON Schema
The agent always attempts to return strict JSON:
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
	 - Default path assumed: `C:\Program Files\Tesseract-OCR\tesseract.exe`
4. (Optional) Virtual environment

---

## 🚀 Installation & Setup
```powershell
# Clone the repository
git clone https://github.com/your-user/your-repo.git
cd "resume analzyer with questions"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Upgrade pip & install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure Tesseract is installed (image support). If installed in a custom path, update `image_user_resume.py`.

---

## 🔑 Environment
You can either set the key before launching or enter it in the sidebar:
```powershell
$Env:OPENAI_API_KEY = "sk-XXXX"  # PowerShell temporary env var
```

---

## ▶️ Run the App
```powershell
streamlit run streamlit_interface.py
```
Then:
1. Enter API key in sidebar
2. Select resume source type
3. Upload / paste resume
4. Paste Job Description
5. Click "Generate Assessment + Questions"
6. Answer MCQs → Submit → View score & explanations

---

## 📤 Downloadable Results
After submission you can download a Markdown summary including:
- Assessment block
- MCQs with correct answer marked
- Your score (%)

---

## 🧩 Extensibility Ideas
- Variable number of MCQs (UI slider)
- Difficulty levels (easy / medium / hard)
- Skill gap remediation suggestions with links
- Export to PDF or JSON via an API endpoint
- Add semantic skill extraction using embeddings

---

## 🛠️ Troubleshooting
| Issue | Resolution |
|-------|------------|
| OCR returns empty text | Confirm Tesseract path & image clarity |
| PDF text empty | Fallback PyPDF2 path triggers; try a different PDF or remove restrictions |
| Model returns non-JSON | Regenerate; prompt enforces schema, but LLM may drift |
| Streamlit radio errors | Ensure each MCQ has exactly 4 options |

---

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/xyz`
3. Commit changes: `git commit -m "Add xyz"`
4. Push: `git push origin feature/xyz`
5. Open a Pull Request

---

## 📄 License
MIT – See `LICENSE` (add one if not present).

---

## 📽️ Demo / Animation
Add a GIF or Lottie animation under `assets/demo.gif`. You can record using:
- ScreenToGif (Windows)
- OBS Studio
Then optimize via https://ezgif.com.

---

## ✅ Checklist Before Publishing
- [ ] Replace `USER/REPO` placeholder in badge & image links
- [ ] Add real demo GIF in `assets/`
- [ ] Confirm requirements are correct
- [ ] Add LICENSE file
- [ ] Rename `reademe.md` → `README.md` if desired

---

## 💬 Acknowledgements
- Tesseract OCR (UB Mannheim build for Windows)
- OpenAI API
- agno agent framework

Enjoy building smarter resume assessments! 🎯

