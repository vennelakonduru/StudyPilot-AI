# 🎓 StudyPilot AI

> An intelligent learning assistant built with Streamlit and Google Gemini.

## 📌 Overview
StudyPilot AI allows students to upload study documents or paste notes to summarize content, explain complex concepts, generate quizzes, and refine draft exam answers.

## ✨ Features
* **Document Parsing**: Supports PDF, DOCX, TXT, and MD files.
* **4 Study Modes**: Summarize Notes, Explain Concept, Generate Quiz, Improve Answer.
* **Difficulty Modes**: Beginner, Intermediate, and Advanced.
* **Easy Copying**: Instant output copying built into the workspace.

## 🛠️ Local Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/StudyPilot-AI.git](https://github.com/YOUR_USERNAME/StudyPilot-AI.git)
   cd StudyPilot-AI
2. Create and Activate a Virtual Environment
Bash
python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install Requirements
Bash
pip install -r requirements.txt
4. Add Your API Key in .streamlit/secrets.toml
Create a .streamlit directory in your project root and add a secrets.toml file inside it:

Ini, TOML
GEMINI_API_KEY = "your_actual_key_here"
5. Run the App
Bash
streamlit run app.py
📂 Project Structure
Plaintext
StudyPilot-AI/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
💻 Tech Stack
Frontend/Framework: Streamlit

AI Model & SDK: Google Gemini API (google-genai)

Document Processing: PyPDF2, python-docx

Language: Python 3.10
