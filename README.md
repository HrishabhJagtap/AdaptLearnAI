# 🎓 AdaptLearn AI
### AI-Based Personalized Learning Content Generator

**Problem Statement:** PS-1 | Generative AI & Creative Intelligence

AdaptLearn AI is an AI-powered personalized learning application that generates educational content according to a student's knowledge level and learning preferences.

Built using **Python, Streamlit, and Google's Gemini API**, the application combines generative AI, knowledge assessments, and adaptive difficulty adjustment to create a more personalized learning experience.

---

## 📌 Project Overview

Traditional learning platforms often provide the same educational material to every student, regardless of their individual knowledge, understanding, or learning speed.

**AdaptLearn AI addresses this problem** by generating personalized explanations, examples, and quizzes based on each student's selected proficiency level.

After every assessment, the application evaluates the student's performance and recommends an appropriate difficulty level for the next lesson.

The project demonstrates how existing Large Language Models (LLMs) can be integrated into educational applications without training a custom AI model.

## ✨ Key Features

**1. AI-Powered Content Generation**
- Generates educational explanations for user-selected topics.
- Provides important concepts and worked examples.
- Uses Google's Gemini API for dynamic lesson generation.

**2. Personalized Learning**
- Supports three proficiency levels: Beginner, Intermediate, and Advanced.
- Allows students to select their preferred explanation format and language.
- Adjusts generated content according to selected learning preferences.

**3. Interactive Knowledge Assessment**
- Generates five multiple-choice questions per lesson.
- Automatically evaluates submitted answers.
- Displays scores, correct answers, and explanations.

**4. Adaptive Difficulty Adjustment**
- Evaluates student performance after each quiz.
- Recommends an easier, equivalent, or more challenging learning level.
- Supports follow-up lessons based on previous assessment results.

**5. Learning Progress Tracking**
- Displays attempted topics and quiz scores.
- Records the current and recommended proficiency levels.
- Maintains progress during the active application session.

**6. Offline Demonstration Mode**
- Includes predefined Linked Lists lessons.
- Supports all three proficiency levels.
- Demonstrates quizzes and difficulty adjustment without an API key or internet connection.

*Note: Offline lessons are predefined. Live AI generation requires the Gemini API.*

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and quiz evaluation |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-generated educational content |
| Prompt Engineering | Difficulty-specific content generation |
| Pydantic | Structured AI response validation |
| Streamlit Session State | Temporary learning progress tracking |
| python-dotenv | Environment and API key configuration |

## ⚙️ Installation and Setup

### Prerequisites

Before running the application, ensure that you have:

- Python 3.10 or newer
- pip (Python package manager)
- An internet connection for live AI features
- A Gemini API key for AI-powered generation

### Step 1: Download the project

Clone the repository using Git:

`git clone https://github.com/YOUR_USERNAME/AdaptLearn-AI.git`

Then navigate into the project directory:

`cd AdaptLearn-AI`

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### Step 2: Install the dependencies

Open a terminal inside the project folder and run:

`python -m pip install -r requirements.txt`

### Step 3: Launch the application

Run the following command:

`python -m streamlit run app.py`

The application should open automatically in your browser.

**Local URL:** http://localhost:8501

## 🚀 How to Use AdaptLearn AI

**Step 1 — Select a Learning Topic**

Enter the subject or topic you want to learn, such as Linked Lists, Binary Trees, or Operating Systems.

**Step 2 — Customize Your Learning Experience**

Choose your knowledge level, preferred explanation format, and language.

**Step 3 — Generate Personalized Content**

Select a content source and click **Generate Personalized Lesson**.

The application displays an explanation, key concepts, and a worked example.

**Step 4 — Attempt the Quiz**

Open the Quiz tab, answer the five multiple-choice questions, and submit your answers.

**Step 5 — Receive Personalized Feedback**

The system evaluates the answers, displays the score, and recommends the next proficiency level.

**Step 6 — Continue Learning**

Generate the next adaptive lesson or open the Progress tab to review performance.

---

## 🧠 Adaptive Learning Mechanism

AdaptLearn AI implements a rule-based adaptive difficulty algorithm.

The system calculates the student's quiz score using:

**Score (%) = (Correct Answers / Total Questions) × 100**

The difficulty adjustment follows these rules:

| Quiz Performance | System Response |
|---|---|
| 0–2 correct (0–40%) | Move one level easier, if possible |
| 3–4 correct (60–80%) | Continue at the same level |
| 5 correct (100%) | Move one level harder, if possible |

The system supports three levels: **Beginner → Intermediate → Advanced**.

Difficulty is automatically recommended after assessment, and the student can generate the next lesson using the updated level.

## 🤖 Gemini AI Integration

AdaptLearn AI uses Google's Gemini API to generate personalized learning content.

To enable live AI functionality:

1. Visit [Google AI Studio](https://aistudio.google.com/apikey).
2. Generate your Gemini API key.
3. Launch the AdaptLearn AI application.
4. Select **Gemini AI (live)** in the sidebar.
5. Enter your API key securely.
6. Select an available Gemini model and generate a lesson.

API access is subject to model availability, quotas, and applicable pricing.

**Security:** Never commit API keys or your actual `.env` file to a public repository. The included `.env.example` is a configuration template only.

## 📂 Project Structure

The repository contains:

| File | Description |
|---|---|
| `app.py` | Main Streamlit application and Gemini integration |
| `engine.py` | Adaptive difficulty logic and predefined lessons |
| `requirements.txt` | Required Python dependencies |
| `smoke_test.py` | Basic application consistency tests |
| `PROMPT_AND_REPORT.md` | Prompt design documentation and project report notes |
| `.env.example` | Example environment configuration |
| `.gitignore` | Git exclusion rules |
| `README.md` | Project documentation |

### Running Tests

To run the included consistency tests:

`python smoke_test.py`

---

## 🎥 Project Demonstration

A video walkthrough demonstrates the application's major features, including:

- Learning preferences and topic selection
- Personalized lesson generation
- Interactive quizzes and scoring
- Adaptive difficulty recommendations
- Learning progress tracking

**[▶ Watch AdaptLearn AI Demo Video](https://youtu.be/7rC_v1rntbA)**

## 📊 Project Presentation

The presentation covers the problem statement, objectives, technologies, system architecture, prompt engineering, adaptive learning mechanism, and project results.

**[📄 View Project Presentation](AdaptLearn_AI_Project_Presentation.pptx)**

---

## ⚠️ Current Limitations

AdaptLearn AI is an academic proof-of-concept rather than a complete Learning Management System.

Current limitations include:

- Live AI generation requires internet connectivity and API availability.
- Generated educational content may occasionally contain inaccuracies.
- Progress is temporarily stored using Streamlit Session State.
- Student authentication and permanent database storage are not implemented.
- Offline demonstration content is predefined.
- Adaptive recommendations use fixed quiz-score thresholds.

## 🔮 Future Enhancements

Potential future improvements include:

- Student login and personalized user profiles
- Permanent database-based learning history
- PDF and syllabus upload support
- AI-powered doubt-solving assistant
- Advanced weakness detection and learner analytics
- Personalized study plans and learning roadmaps
- Teacher dashboard and performance monitoring

## 🎯 Conclusion

AdaptLearn AI demonstrates how generative AI can be combined with automated knowledge assessment and adaptive difficulty adjustment to support personalized education.

By providing content suited to different proficiency levels and recommending the next learning stage based on performance, the project offers a foundation for future AI-powered educational applications.

---

**Developed as a B.Tech Artificial Intelligence & Machine Learning academic project — 2026.**
