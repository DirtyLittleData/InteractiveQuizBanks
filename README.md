# 📚 Streamlit Quiz App

This is a simple, no-frills quiz app we threw together using Python and Streamlit. It loads questions from a CSV file and gives users a clean little multiple-choice interface—complete with scoring, explanations, and the ability to retry questions. It’s got multi-answer support and doesn’t break if you shuffle around the directory structure, so it’s solid for demos or mini-training tools.

## ✨ Features

- Loads questions from a CSV (`quiz_questions.csv`)
- Supports multiple correct answers
- Randomized question order on each run
- Explanation shown after each submission (if included in the CSV)
- Tracks your score in the sidebar
- Simple state management with `st.session_state`

## 📁 CSV Format

Your `quiz_questions.csv` should look like this:

```csv
Question,Choices,Correct,Explanation
What are primary colors?,Red|Blue|Yellow|Green,A|B|C,"Red, Blue, and Yellow are the traditional primary colors."
Choices are separated by |

Correct answers use letter codes (A, B, C, etc.)
```

Explanation is optional but encouraged

## 🧠 How It Works
On load, it reads all the questions from the CSV and maps the choices to letter keys (A, B, C…).

The app tracks your progress and score using session state so it doesn’t reset every time you click a button.

You select one or more answers, hit submit, and get immediate feedback.

You can navigate forward or reset everything with the Home and Next buttons.

## 🚀 To Run
Make sure you’ve got Streamlit installed:

```bash
Copy
Edit
pip install streamlit
Then just run:

bash
Copy
Edit
streamlit run your_script_name.py
```

## 🤔 Why We Made This
Honestly? I just wanted a clean and easy way to test people on stuff without overcomplicating it. We're thinking about using it as a base model for AI training. This could be fun for onboarding, trivia, or just messing around. Plus it was a good excuse to practice more with session state and file handling in Streamlit.

