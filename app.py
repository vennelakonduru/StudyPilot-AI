import streamlit as st
import PyPDF2
import docx
from google import genai

st.set_page_config(
    page_title="StudyPilot AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

if "study_history" not in st.session_state:
    st.session_state.study_history = [
        {"title": "Photosynthesis - Quiz", "time": "2 mins ago"},
        {"title": "Machine Learning - Summary", "time": "15 mins ago"},
        {"title": "Python Basics - Explanation", "time": "32 mins ago"}
    ]

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Summarize Notes"

if "generated_output" not in st.session_state:
    st.session_state.generated_output = ""

def extract_file_content(file):
    if file is None:
        return ""
    text = ""
    try:
        if file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            for p in doc.paragraphs:
                text += p.text + "\n"
        elif file.name.endswith(".txt") or file.name.endswith(".md"):
            text = file.read().decode("utf-8")
    except Exception:
        st.error("Failed to read file.")
    return text

with st.sidebar:
    st.title("🎓 StudyPilot AI")
    st.caption("Learn Smarter • Understand Better • Achieve More")
    st.write("")
    nav = st.radio("Navigation", ["Home", "Summarize Notes", "Explain Concept", "Generate Quiz", "Improve Answer"], label_visibility="collapsed")
    if nav != "Home":
        st.session_state.selected_mode = nav
    st.write("---")
    st.subheader("🕒 Study History")
    for item in st.session_state.study_history:
        st.markdown(f"**{item['title']}**\n*{item['time']}*")
    st.write("---")
    difficulty = st.selectbox("📊 Difficulty Level", ["Beginner", "Intermediate", "Advanced"], index=1)
    st.write("")
    st.caption("✨ Powered by Gemini")

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.title("Hello, Student! 👋")
    st.write("Upload your study material or paste your notes, and I'll help you learn, understand and grow.")

with top_col2:
    st.caption("✨ Powered by Gemini")

st.subheader("Upload Your Study Material")
up_col1, up_col2 = st.columns(2)

with up_col1:
    uploaded_file = st.file_uploader("Drag & drop your file here", type=["pdf", "docx", "txt", "md"])
    if uploaded_file:
        parsed_text = extract_file_content(uploaded_file)
        if parsed_text:
            st.session_state.extracted_text = parsed_text
            st.success(f"File '{uploaded_file.name}' processed successfully!")

with up_col2:
    pasted_text = st.text_area("Paste your text here", value=st.session_state.extracted_text, height=180, max_chars=10000, placeholder="Paste your notes, topic or question...")
    if pasted_text:
        st.session_state.extracted_text = pasted_text

st.subheader("Choose a Study Mode")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    if st.button("📝 Summarize Notes\nGet concise bullet points", use_container_width=True):
        st.session_state.selected_mode = "Summarize Notes"

with m_col2:
    if st.button("💡 Explain Concept\nUnderstand complex topics", use_container_width=True):
        st.session_state.selected_mode = "Explain Concept"

with m_col3:
    if st.button("🧠 Generate Quiz\nCreate 5-question test", use_container_width=True):
        st.session_state.selected_mode = "Generate Quiz"

with m_col4:
    if st.button("✍️ Improve Answer\nRefine grammar and structure", use_container_width=True):
        st.session_state.selected_mode = "Improve Answer"

st.write("")
if st.button(f"🚀 Run {st.session_state.selected_mode}", use_container_width=True):
    if not st.session_state.extracted_text.strip():
        st.warning("Please upload a file or paste some text first.")
    else:
        current_text = st.session_state.extracted_text.strip()
        mode = st.session_state.selected_mode
        if mode == "Summarize Notes":
            prompt = f"You are StudyPilot AI. Summarize the following study material at a {difficulty} level. Use concise bullet points:\n\n{current_text}"
        elif mode == "Explain Concept":
            prompt = f"You are StudyPilot AI. Explain the core concept in the following text for a {difficulty} level student. Include simple definitions and practical examples:\n\n{current_text}"
        elif mode == "Generate Quiz":
            prompt = f"You are StudyPilot AI. Generate a 5-question multiple choice quiz with choices (A-D) and an answer key based on this text at a {difficulty} level:\n\n{current_text}"
        else:
            prompt = f"You are StudyPilot AI. Improve this draft answer for clarity, structure, and academic precision at a {difficulty} level:\n\n{current_text}"
        try:
            with st.spinner("Processing with Gemini..."):
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.session_state.generated_output = res.text
                st.session_state.study_history.insert(0, {"title": f"Custom - {mode}", "time": "Just now"})
        except Exception as err:
            st.error(f"API Error: {str(err)}")

if st.session_state.generated_output:
    st.subheader(f"Output ({st.session_state.selected_mode})")
    st.markdown(st.session_state.generated_output)
    st.caption("📋 Copy your output below:")
    st.code(st.session_state.generated_output, language=None)

st.write("---")
st.subheader("💡 Quick Tips & Info")
info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    * Use clear and specific questions or notes.
    * Choose the right difficulty level on the left sidebar.
    * You can upload PDF, DOCX, TXT, or MD files.
    * Click the code block copy icon to save your output instantly.
    """)

with info_col2:
    st.success("Small Steps, Big Progress! Keep learning and growing with StudyPilot AI.")

st.write("---")
st.caption("StudyPilot AI • Built with Python, Streamlit & Gemini")
