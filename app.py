"""AdaptLearn AI: one-day personalized-learning MVP.

Run with: streamlit run app.py
Demo mode works without an API key (Linked Lists only).
"""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from engine import LEVELS, adapt_level, demo_lesson, validate_lesson

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
st.set_page_config(page_title="AdaptLearn AI", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1080px; padding-top: 2rem;}
h1 {font-weight: 780; letter-spacing: -.04em;}
div[data-testid="stMetric"] {border: 1px solid #dddddd44; border-radius: 12px; padding: 14px;}
</style>
""", unsafe_allow_html=True)


class Question(BaseModel):
    question: str
    options: list[str] = Field(description="Exactly four answer options")
    correct_index: int = Field(description="Zero-based index of correct answer (0-3)")
    explanation: str


class Lesson(BaseModel):
    title: str
    overview: str
    key_points: list[str]
    worked_example: str
    quiz: list[Question] = Field(description="Exactly five four-option questions")


def ai_lesson(topic: str, level: int, language: str, style: str, review_points: list[str], api_key: str, model: str) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    focus = "; ".join(review_points[:3]) if review_points else "None yet"
    difficulty_guide = {
        0: """BEGINNER: Assume no previous understanding. Start with a definition and
simple analogy. Explain new terms plainly. Use small, concrete, step-by-step
examples. Questions must test basic recognition and simple understanding.""",
        1: """INTERMEDIATE: Assume the learner already knows the basic definitions.
Do NOT spend the lesson defining elementary terms. Teach how the idea works
in practice, procedural steps, implementation or application, and typical
mistakes. Include a multi-step worked example; for computational topics,
include pseudocode, trace steps, or complexity analysis where relevant.
At least THREE quiz questions must require application, tracing, or analysis,
not just remembering definitions.""",
        2: """ADVANCED: Assume the learner already understands introductory and
intermediate material. Do NOT provide a beginner overview or basic-definition
quiz. Teach difficult variants, limitations, trade-offs, edge cases,
optimization, and deeper reasoning appropriate to this subject. Include
a nontrivial worked example with assumptions and step-by-step justification;
for algorithms, analyze time/space complexity and correctness when relevant.
At least THREE quiz questions must involve challenging scenarios, trade-offs,
edge cases, or multi-step analysis rather than basic recall.""",
    }[level]
    prompt = f"""You are an accurate university-level tutor creating a differentiated lesson.
Generate new personalized content matching the specified level STRICTLY.
TOPIC: {topic}
REQUIRED PROFICIENCY: {LEVELS[level].upper()}
LEVEL-SPECIFIC RULES: {difficulty_guide}
PREFERRED LANGUAGE: {language}
PREFERRED FORMAT: {style}
CONCEPTS THE STUDENT PREVIOUSLY MISSED: {focus}

NON-NEGOTIABLE RULES:
- The lesson title must include the required proficiency level.
- Make the overview, key points, worked example AND quiz match that level.
- Intermediate and Advanced MUST be noticeably harder than Beginner.
- When reviewing weak concepts, explain them at the requested level; do not
  silently reset the student to Beginner.
- Include 3–5 substantial key points plus ONE fully worked example.
- Exactly FIVE DISTINCT multiple-choice questions with FOUR plausible options.
- Every question must have exactly one unambiguously correct answer.
- correct_index is ZERO-BASED (0, 1, 2 or 3).
- Provide a useful explanation for each answer.
- Avoid invented citations and claims you cannot support.
- Return only a response matching the structured output schema.
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": Lesson},
    )
    if response.parsed is not None:
        parsed = response.parsed
        content = parsed.model_dump() if hasattr(parsed, "model_dump") else dict(parsed)
    else:
        import json
        content = json.loads(response.text)
    return validate_lesson(content)


for key, default in {
    "lesson": None, "stage": "start", "level": 0, "answers": [], "history": [],
    "topic_active": "Linked Lists", "language_active": "English", "style_active": "Step by step",
    "source_active": "Demo mode (offline)", "weak_concepts": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


with st.sidebar:
    st.header("⚙️ Learning Settings")
    topic = st.text_input("Topic", value="Linked Lists", help="For offline demo, use Linked Lists")
    initial_level = st.select_slider("Starting knowledge level", options=LEVELS, value="Beginner")
    style = st.selectbox("Explanation format", ["Step by step", "Real-world analogies", "Quick exam revision"])
    language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
    source = st.radio("Content source", ["Demo mode (offline)", "Gemini AI (live)"], help="Offline is a curated demonstration; live mode generates new content for any topic.")
    api_key = ""
    model = "gemini-3.5-flash-lite"
    if source == "Gemini AI (live)":
        api_key = st.text_input("Gemini API key", type="password", help="Or set GEMINI_API_KEY in a local .env file.") or os.getenv("GEMINI_API_KEY", "")
        model = st.text_input("Gemini model", value="gemini-3.5-flash-lite")
        st.caption("Never commit your API key to GitHub or embed it into frontend source code.")
    st.divider()
    st.caption("Demo mode covers Linked Lists at 3 proficiency levels. Live mode requires internet and an API key.")
    st.caption("After changing a level, click 'Generate lesson with sidebar settings' to apply it to your current lesson.")


def produce(topic_value: str, level_value: int, weak: list[str]):
    if source == "Gemini AI (live)":
        if not api_key:
            raise ValueError("Enter a Gemini API key or put GEMINI_API_KEY in your .env file.")
        result = ai_lesson(topic_value, level_value, language, style, weak, api_key, model)
    else:
        result = validate_lesson(demo_lesson(topic_value, level_value))
    st.session_state.lesson = result
    st.session_state.level = level_value
    st.session_state.topic_active = topic_value
    st.session_state.language_active = language
    st.session_state.style_active = style
    st.session_state.source_active = source
    st.session_state.answers = []
    st.session_state.stage = "lesson"


st.title("🎓 AdaptLearn AI")
st.caption("Personalized learning content • Five-question assessments • Adaptive difficulty")

if st.session_state.stage == "start":
    st.info("Choose a topic and a difficulty level in the sidebar. Then generate a lesson to begin.")
    st.markdown("### What the prototype demonstrates")
    a, b, c = st.columns(3)
    a.metric("Difficulty levels", "3")
    b.metric("Questions per quiz", "5")
    c.metric("Adaptation", "Automatic")
    if st.button("✨ Generate Personalized Lesson", type="primary", use_container_width=True):
        try:
            with st.spinner("Preparing your lesson..."):
                produce(topic.strip(), LEVELS.index(initial_level), [])
            st.rerun()
        except Exception as exc:
            st.error(f"Could not generate lesson: {exc}")

else:
    st.markdown(f"**Topic:** {st.session_state.topic_active}  ·  **Current level:** {LEVELS[st.session_state.level]}  ·  **Source:** {st.session_state.source_active}")
    if (topic.strip() != st.session_state.topic_active
            or LEVELS.index(initial_level) != st.session_state.level
            or source != st.session_state.source_active):
        st.info("Your sidebar settings differ from this lesson. Click the button below to generate content using the new topic, level, or source.")
    if st.button("✨ Generate lesson with sidebar settings", use_container_width=True):
        try:
            with st.spinner(f"Generating {initial_level.lower()} lesson..."):
                produce(topic.strip(), LEVELS.index(initial_level), [])
            st.rerun()
        except Exception as exc:
            st.error(f"Could not generate lesson: {exc}")
    learn_tab, quiz_tab, progress_tab = st.tabs(["📘 Lesson", "📝 Quiz", "📈 Progress"])
    lesson = st.session_state.lesson
    with learn_tab:
        st.subheader(lesson["title"])
        st.write(lesson["overview"])
        st.markdown("#### Key concepts")
        for point in lesson["key_points"]:
            st.markdown(f"- {point}")
        st.markdown("#### Worked example")
        st.info(lesson["worked_example"])
        st.caption("AI-generated lessons may contain errors; verify important technical details.")

    with quiz_tab:
        st.subheader("Check your understanding")
        if st.session_state.stage == "lesson":
            with st.form("quiz_form"):
                answers = []
                for i, item in enumerate(lesson["quiz"]):
                    st.markdown(f"**Q{i + 1}. {item['question']}**")
                    answer = st.radio("Select one option", item["options"], index=None,
                                      key=f"q_{i}_{st.session_state.level}_{len(st.session_state.history)}", label_visibility="collapsed")
                    answers.append(answer)
                submitted = st.form_submit_button("Submit Quiz", type="primary", use_container_width=True)
            if submitted:
                if any(answer is None for answer in answers):
                    st.warning("Please answer all five questions before submitting.")
                else:
                    correctness = [item["options"].index(answer) == item["correct_index"] for answer, item in zip(answers, lesson["quiz"])]
                    correct = sum(correctness)
                    next_level, message = adapt_level(st.session_state.level, correct, len(lesson["quiz"]))
                    misses = [item["question"] for item, right in zip(lesson["quiz"], correctness) if not right]
                    st.session_state.answers = answers
                    st.session_state.weak_concepts = misses
                    st.session_state.history.append({
                        "topic": st.session_state.topic_active, "level": LEVELS[st.session_state.level],
                        "correct": correct, "total": len(lesson["quiz"]), "next_level": next_level,
                        "message": message,
                    })
                    st.session_state.stage = "results"
                    st.rerun()
        else:
            result = st.session_state.history[-1]
            st.metric("Your quiz score", f"{result['correct']}/{result['total']}")
            st.progress(result["correct"] / result["total"])
            st.success(result["message"])
            st.markdown(f"**Next recommended level:** {LEVELS[result['next_level']]}")
            for i, item in enumerate(lesson["quiz"]):
                is_correct = st.session_state.answers[i] == item["options"][item["correct_index"]]
                with st.expander(f"{'✅' if is_correct else '❌'} Q{i+1}: {item['question']}"):
                    st.write(f"**Your answer:** {st.session_state.answers[i]}")
                    st.write(f"**Correct answer:** {item['options'][item['correct_index']]}")
                    st.write(f"**Why:** {item['explanation']}")
            if st.button("➡️ Generate Next Adaptive Lesson", type="primary", use_container_width=True):
                try:
                    with st.spinner("Adjusting difficulty..."):
                        produce(st.session_state.topic_active, result["next_level"], st.session_state.weak_concepts)
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not generate next lesson: {exc}")

    with progress_tab:
        if st.session_state.history:
            st.subheader("Learning progress in this session")
            st.dataframe([{
                "Topic": row["topic"], "Level": row["level"],
                "Score": f"{row['correct']}/{row['total']}",
                "Next level": LEVELS[row["next_level"]],
            } for row in st.session_state.history], use_container_width=True, hide_index=True)
            st.caption("Progress is session-only in this MVP and may be lost after a refresh. A database is a future improvement.")
        else:
            st.info("Complete your first quiz to see performance tracking.")

    st.divider()
    if st.button("🔄 Start New Learning Session"):
        for key in ("lesson", "answers", "history", "weak_concepts"):
            st.session_state[key] = None if key == "lesson" else []
        st.session_state.stage = "start"
        st.rerun()
