import streamlit as st
import csv
import random
import string
import os

# Load questions from CSV
def load_questions(filename="quiz_questions.csv"):
    # Ensure it works no matter where it's run from
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)

    questions = []
    with open(full_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "Question" not in row or "Choices" not in row or "Correct" not in row:
                continue

            choices = row["Choices"].split("|")
            correct_letters = set(row["Correct"].split("|"))

            # Map choices to letters (A, B, C...)
            letter_to_choice = {letter: choice for letter, choice in zip(string.ascii_uppercase, choices)}

            # Store question data
            row["Choices"] = letter_to_choice
            row["Correct"] = correct_letters
            questions.append(row)

    return questions

# Load questions globally
QUESTIONS = load_questions()
random.shuffle(QUESTIONS)

# Track session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_answers' not in st.session_state:
    st.session_state.selected_answers = []

def get_current_question():
    return QUESTIONS[st.session_state.current_question]

def submit_answer():
    question = get_current_question()
    correct_answers = question["Correct"]
    selected_answers = set(st.session_state.selected_answers)
    
    if selected_answers == correct_answers:
        st.session_state.score += 1
        st.session_state.correct = True
    else:
        st.session_state.correct = False
    
    st.session_state.answered = True

def next_question():
    if st.session_state.current_question < len(QUESTIONS) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.current_question = 0  # Reset to first question
        st.session_state.score = 0  # Reset score
    
    st.session_state.answered = False
    st.session_state.selected_answers = []

# UI
st.title("Interactive Quiz")
st.sidebar.write(f"Score: {st.session_state.score}")

question = get_current_question()
st.markdown(f"**{question['Question']}**")

# Display answer choices with letter labels
choices_display = {letter: choice for letter, choice in question["Choices"].items()}
selected_answers = st.multiselect(
    "Select your answer(s):",
    choices_display.keys(),
    format_func=lambda x: f"{x}) {choices_display[x]}",
    default=st.session_state.selected_answers
)
st.session_state.selected_answers = selected_answers

if not st.session_state.answered:
    if st.button("✅ Submit Answer"):
        submit_answer()
else:
    if st.session_state.correct:
        st.success("Correct! ✅")
    else:
        st.error("Incorrect ❌")
    st.info(question.get("Explanation", "No explanation provided."))  # Fallback if Explanation is missing


if st.session_state.answered:
    if st.session_state.correct:
        st.success("Correct! ✅")
    else:
        st.error("Incorrect ❌")
    st.info(question.get("Explanation", "No explanation provided."))  # Fallback if Explanation is missing

# Navigation buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 Home"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected_answers = []
with col2:
    if st.session_state.answered:
        if st.button("➡ Next Question"):
            next_question()
    else:
        st.write("Submit an answer to continue ⬆️")

disabled_state = st.session_state.answered

selected_answers = st.multiselect(
    "Select your answer(s):",
    choices_display.keys(),
    format_func=lambda x: f"{x}) {choices_display[x]}",
    default=st.session_state.selected_answers,
    disabled=disabled_state
)
