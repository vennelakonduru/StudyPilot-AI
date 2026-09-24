import json
import re
import time

import streamlit as st
from google import genai
from google.genai.errors import APIError

st.set_page_config(
    page_title="StudyPilot AI",
    page_icon="🎓",
    layout="centered"
)

if "operation" not in st.session_state:
    st.session_state.operation = "Summarize"

if "result" not in st.session_state:
    st.session_state.result = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

try:

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:

    client = None

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite"
]

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f8fafc;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 45px;
        padding-bottom: 60px;
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #d9e1ea !important;
        background-color: #ffffff !important;
        color: #111827 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    textarea:hover {
        border-color: #94a3b8 !important;
    }

    textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 1px #2563eb !important;
    }

    div.stButton > button {
        border-radius: 13px !important;
        min-height: 68px !important;
        border: 1px solid #d9e1ea !important;
        background-color: #ffffff !important;
        color: #111827 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #f8fbff !important;
        transform: translateY(-2px);
    }

    div.stButton > button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        min-height: 52px !important;
        font-weight: 700 !important;
        box-shadow:
            0 6px 18px rgba(37, 99, 235, 0.18);
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    hr {
        border-color: #e5e7eb !important;
    }

    .quiz-header {
        background-color: #111827;
        color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .result-card {
        background-color: #ffffff;
        border: 1px solid #e1e7ef;
        border-radius: 15px;
        padding: 22px;
        box-shadow:
            0 5px 20px rgba(15, 23, 42, 0.04);
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 StudyPilot AI")

st.subheader(
    "Your Smart Learning Companion"
)

st.write(
    "Turn your study material into clear summaries, "
    "organized notes, simple explanations, and "
    "interactive quizzes."
)

st.divider()

st.subheader("📚 Study Material")

st.caption(
    "Paste your topic, paragraph, notes, or study material below."
)

study_text = st.text_area(
    "Study material",
    height=220,
    placeholder=(
        "Example:\n\n"
        "Paste your Operating Systems notes here..."
    ),
    label_visibility="collapsed"
)

st.subheader("⚙️ Choose an Operation")

st.caption(
    "Select one operation and then click Run Operation."
)

col1, col2 = st.columns(2)

with col1:

    if st.session_state.operation == "Summarize":

        clicked = st.button(
            "📝 Summarize\nMake the material concise",
            type="primary",
            use_container_width=True
        )

    else:

        clicked = st.button(
            "📝 Summarize\nMake the material concise",
            use_container_width=True
        )

    if clicked:

        st.session_state.operation = "Summarize"

        st.rerun()

with col2:

    if st.session_state.operation == "Organize Notes":

        clicked = st.button(
            "📌 Organize Notes\nConvert into key points",
            type="primary",
            use_container_width=True
        )

    else:

        clicked = st.button(
            "📌 Organize Notes\nConvert into key points",
            use_container_width=True
        )

    if clicked:

        st.session_state.operation = "Organize Notes"

        st.rerun()

col3, col4 = st.columns(2)

with col3:

    if st.session_state.operation == "Explain Topic":

        clicked = st.button(
            "💡 Explain Topic\nUnderstand it simply",
            type="primary",
            use_container_width=True
        )

    else:

        clicked = st.button(
            "💡 Explain Topic\nUnderstand it simply",
            use_container_width=True
        )

    if clicked:

        st.session_state.operation = "Explain Topic"

        st.rerun()

with col4:

    if st.session_state.operation == "Generate Quiz":

        clicked = st.button(
            "❓ Generate Quiz\nTest your understanding",
            type="primary",
            use_container_width=True
        )

    else:

        clicked = st.button(
            "❓ Generate Quiz\nTest your understanding",
            use_container_width=True
        )

    if clicked:

        st.session_state.operation = "Generate Quiz"

        st.rerun()

st.write("")

st.info(
    f"Selected operation: **{st.session_state.operation}**"
)

run_operation = st.button(
    "🚀 Run Operation",
    type="primary",
    use_container_width=True
)

if run_operation:

    if not study_text.strip():

        st.warning(
            "Please paste some study material first."
        )

        st.stop()

    selected = st.session_state.operation

    st.session_state.result = ""

    st.session_state.quiz = []

    st.session_state.quiz_submitted = False

    st.session_state.quiz_score = 0

    if selected == "Summarize":

        prompt = f"""
You are StudyPilot AI, an academic study assistant.

Summarize the following study material for a college student.

Requirements:

- Keep all important information.
- Remove unnecessary repetition.
- Use clear headings where useful.
- Use short paragraphs or bullet points.
- Preserve important definitions and technical terms.
- Make the result useful for examination revision.
- Do not add unrelated information.

Study material:

{study_text}
"""

    elif selected == "Organize Notes":

        prompt = f"""
You are StudyPilot AI, an academic note organizer.

Convert the following study material into exactly
6 or 7 meaningful bullet points.

Requirements:

- Cover the important ideas from the complete material.
- Each bullet should contain useful information.
- Use simple student-friendly language.
- Keep important technical terms.
- Avoid unnecessary repetition.
- Do not add information that is not present.

Material:

{study_text}
"""

    elif selected == "Explain Topic":

        prompt = f"""
You are StudyPilot AI, a college academic tutor.

Explain the following topic in simple,
student-friendly language.

Use this structure:

## Simple Definition

Give a short and clear definition.

## Explanation

Explain the concept clearly.

## Important Points

Give the important points.

## Example

Give one simple example.

## Quick Takeaway

Give a short final takeaway.

Do not make the explanation unnecessarily long.

Topic:

{study_text}
"""

    if selected != "Generate Quiz":

        try:

            if client is None:

                st.error(
                    "Gemini API key is missing. "
                    "Please check .streamlit/secrets.toml."
                )

                st.stop()

            response = None

            last_error = ""

            loading_messages = {

                "Summarize":
                    "StudyPilot AI is preparing your summary...",

                "Organize Notes":
                    "StudyPilot AI is organizing your notes...",

                "Explain Topic":
                    "StudyPilot AI is preparing your explanation..."

            }

            with st.spinner(
                loading_messages.get(
                    selected,
                    "StudyPilot AI is working..."
                )
            ):

                for model_name in MODELS:

                    for attempt in range(3):

                        try:

                            response = (
                                client.models.generate_content(
                                    model=model_name,
                                    contents=prompt
                                )
                            )

                            if (
                                response
                                and response.text
                            ):

                                break

                        except APIError as error:

                            last_error = str(error)

                            if error.code in [429, 503]:

                                if attempt < 2:

                                    time.sleep(
                                        2 * (attempt + 1)
                                    )

                                    continue

                                break

                            if error.code in [400, 404]:

                                break

                            raise

                        except Exception as error:

                            last_error = str(error)

                            error_text = (
                                str(error).lower()
                            )

                            if (
                                "404" in error_text
                                or "429" in error_text
                                or "503" in error_text
                                or "unavailable"
                                in error_text
                                or "not found"
                                in error_text
                            ):

                                if attempt < 2:

                                    time.sleep(
                                        2 * (attempt + 1)
                                    )

                                    continue

                                break

                            raise

                    if (
                        response
                        and response.text
                    ):

                        break

            if not response or not response.text:

                raise Exception(
                    "Gemini AI is temporarily unavailable. "
                    "Please try again."
                )

            st.session_state.result = (
                response.text.strip()
            )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )

    else:

        quiz_prompt = f"""
You are StudyPilot AI, an expert college quiz creator.

Create EXACTLY 10 multiple-choice questions
based ONLY on the study material below.

Rules:

- Exactly 10 questions.
- Each question must have exactly 4 options.
- Options must be A, B, C and D.
- Questions should test understanding.
- Each question must have one correct answer.
- Give a short explanation for each correct answer.
- Do not reveal the answers in the question section.

Return ONLY valid JSON.

Use exactly this structure:

[
  {{
    "number": 1,
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct": "A",
    "explanation": "Short explanation"
  }}
]

Study material:

{study_text}
"""

        try:

            if client is None:

                st.error(
                    "Gemini API key is missing."
                )

                st.stop()

            response = None

            with st.spinner(
                "StudyPilot AI is creating your quiz..."
            ):

                for model_name in MODELS:

                    for attempt in range(3):

                        try:

                            response = (
                                client.models.generate_content(
                                    model=model_name,
                                    contents=quiz_prompt
                                )
                            )

                            if (
                                response
                                and response.text
                            ):

                                break

                        except APIError as error:

                            if error.code in [429, 503]:

                                if attempt < 2:

                                    time.sleep(
                                        2 * (attempt + 1)
                                    )

                                    continue

                                break

                            if error.code in [400, 404]:

                                break

                            raise

                    if (
                        response
                        and response.text
                    ):

                        break

            if not response or not response.text:

                raise Exception(
                    "Unable to generate the quiz."
                )

            raw_quiz = response.text.strip()

            raw_quiz = re.sub(
                r"^```json\s*",
                "",
                raw_quiz,
                flags=re.IGNORECASE
            )

            raw_quiz = re.sub(
                r"^```\s*",
                "",
                raw_quiz
            )

            raw_quiz = re.sub(
                r"\s*```$",
                "",
                raw_quiz
            )

            quiz = json.loads(
                raw_quiz
            )

            if (
                not isinstance(quiz, list)
                or len(quiz) != 10
            ):

                raise Exception(
                    "The AI did not generate exactly 10 questions."
                )

            st.session_state.quiz = quiz

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = 0

        except Exception as error:

            st.error(
                f"Unable to generate quiz: {error}"
            )

if (
    st.session_state.operation != "Generate Quiz"
    and st.session_state.result
):

    st.divider()

    st.subheader(
        f"✨ {st.session_state.operation} Result"
    )

    result = st.session_state.result

    result = re.sub(
        r"<[^>]+>",
        "",
        result
    )

    st.markdown(
        result
    )

    st.caption(
        "Copy the complete result using the copy button "
        "in the box below."
    )

    st.code(
        result,
        language="text"
    )

if (
    st.session_state.operation == "Generate Quiz"
    and st.session_state.quiz
):

    quiz = st.session_state.quiz

    if not st.session_state.quiz_submitted:

        st.divider()

        st.subheader(
            "🧠 Knowledge Check"
        )

        st.caption(
            "Answer all 10 questions and submit your quiz."
        )

        st.progress(
            0,
            text="10 questions"
        )

        with st.form(
            "quiz_form"
        ):

            for index, question in enumerate(quiz):

                st.markdown(
                    f"### Question {question['number']}"
                )

                st.write(
                    question["question"]
                )

                options = [

                    f"A) {question['options']['A']}",

                    f"B) {question['options']['B']}",

                    f"C) {question['options']['C']}",

                    f"D) {question['options']['D']}"

                ]

                st.radio(
                    "Select your answer",
                    options,
                    index=None,
                    key=f"answer_{index}"
                )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz",
                use_container_width=True
            )

        if submitted:

            score = 0

            unanswered = 0

            for index, question in enumerate(quiz):

                selected_answer = st.session_state.get(
                    f"answer_{index}"
                )

                if selected_answer is None:

                    unanswered += 1

                    continue

                selected_letter = (
                    selected_answer[0]
                )

                if (
                    selected_letter
                    == question["correct"]
                ):

                    score += 1

            if unanswered > 0:

                st.warning(
                    f"Please answer all questions. "
                    f"{unanswered} question(s) are unanswered."
                )

            else:

                st.session_state.quiz_score = score

                st.session_state.quiz_submitted = True

                st.rerun()

    else:

        score = st.session_state.quiz_score

        percentage = score * 10

        st.divider()

        st.subheader(
            "🎉 Quiz Completed"
        )

        score_col1, score_col2 = st.columns(2)

        with score_col1:

            st.metric(
                "Your Score",
                f"{score} / 10"
            )

        with score_col2:

            st.metric(
                "Percentage",
                f"{percentage}%"
            )

        st.progress(
            percentage / 100
        )

        st.subheader(
            "📋 Answer Review"
        )

        for index, question in enumerate(quiz):

            selected_answer = st.session_state.get(
                f"answer_{index}"
            )

            user_letter = (

                selected_answer[0]

                if selected_answer

                else "-"
            )

            correct_letter = (
                question["correct"]
            )

            st.markdown(
                f"### Question {question['number']}"
            )

            st.write(
                question["question"]
            )

            if user_letter == correct_letter:

                st.success(
                    f"Correct ✓\n\n"
                    f"Your answer: "
                    f"{user_letter}) "
                    f"{question['options'][user_letter]}"
                )

            else:

                user_text = (
                    question["options"].get(
                        user_letter,
                        "Not answered"
                    )
                )

                correct_text = (
                    question["options"][
                        correct_letter
                    ]
                )

                st.error(
                    f"Incorrect ✗\n\n"
                    f"Your answer: "
                    f"{user_letter}) {user_text}\n\n"
                    f"Correct answer: "
                    f"{correct_letter}) "
                    f"{correct_text}"
                )

            st.info(
                "Explanation: "
                + question["explanation"]
            )

            st.divider()

        if st.button(
            "🔄 Create New Quiz",
            use_container_width=True
        ):

            st.session_state.quiz = []

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = 0

            st.rerun()

st.divider()

st.caption(
    "🎓 StudyPilot AI · Smart Learning Companion"
)
