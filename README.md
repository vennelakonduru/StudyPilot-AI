````markdown
# 🎓 StudyPilot AI

> An AI-powered smart learning companion built with Python, Streamlit, and Google Gemini.

## 🌐 Live Demo

Try the deployed application:

**https://studypilot-ai-vennelakonduru.streamlit.app/**

## 📌 What is StudyPilot AI?

StudyPilot AI is a simple AI-powered learning assistant that helps students transform their study material into useful learning resources.

Users can paste their study material into the application and select one of four available operations. The selected operation is processed using the Google Gemini API, and the generated result is displayed directly in the application.

## ✨ Features

### 📝 Summarize

The Summarize operation converts lengthy study material into a concise and easy-to-revise summary. It keeps important information, definitions, and technical terms while removing unnecessary repetition.

### 📌 Organize Notes

The Organize Notes operation converts the provided study material into exactly 6–7 meaningful key points. This makes the content easier to review and revise.

### 💡 Explain Topic

The Explain Topic operation explains the provided topic in simple, student-friendly language. The response includes a simple definition, explanation, important points, an example, and a quick takeaway.

### 🧠 Generate Quiz

The Generate Quiz operation creates an interactive quiz from the provided study material. It generates exactly 10 multiple-choice questions, with four options for each question. After the student submits the quiz, the application calculates the score and percentage and provides an answer review with correct answers and explanations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Google Gemini API | AI-powered content generation |
| Google Gen AI SDK | Gemini API integration |
| JSON | Quiz data handling |
| Regular Expressions (`re`) | Response processing |

## 📂 File Structure

After downloading or cloning the project, the required structure is:

```text
StudyPilot-AI/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
````

The `.streamlit/secrets.toml` file is used to store the Gemini API key when running the application locally.

## 🔑 Gemini API Setup

A Gemini API key is required for StudyPilot AI to generate AI responses.

### Step 1: Get a Gemini API Key

Go to Google AI Studio:

**[https://aistudio.google.com/](https://aistudio.google.com/)**

Sign in with your Google account and create a new Gemini API key.

Copy the generated API key.

### Step 2: Create the `.streamlit` Folder

Inside the `StudyPilot-AI` project folder, create a folder named:

```text
.streamlit
```

Inside this folder, create:

```text
secrets.toml
```

The structure should now be:

```text
StudyPilot-AI/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Step 3: Add the API Key

Open:

```text
.streamlit/secrets.toml
```

and add:

```toml
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"
```

Replace `YOUR_ACTUAL_GEMINI_API_KEY` with the API key you created in Google AI Studio.

After adding the API key, the required project structure is complete.

## ⚠️ Important

Do not upload your actual `secrets.toml` file to GitHub because it contains your private Gemini API key.

Your `.gitignore` should contain:

```text
.streamlit/secrets.toml
__pycache__/
*.pyc
.venv/
```

## 🚀 Run the Project

After completing the file structure and adding your Gemini API key, open a terminal inside the `StudyPilot-AI` project folder.

### Step 1: Install the Required Packages

Run:

```bash
python -m pip install -r requirements.txt
```

This installs the required dependencies for the project.

### Step 2: Start the Streamlit Application

Run:

```bash
streamlit run app.py
```

Streamlit will start the application locally.

The application will normally be available at:

```text
http://localhost:8501
```

Open the localhost address in your browser to view and use StudyPilot AI.

## 📦 Requirements

The `requirements.txt` file contains:

```text
streamlit
google-genai
```

````
**Author:** Vennela Raghava Konduru
