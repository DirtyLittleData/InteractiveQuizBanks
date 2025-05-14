import streamlit as st
import csv
import random
import string
import os

def load_questions(filename="quiz_questions.csv"):
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
            letter_to_choice = {letter: choice for letter, choice in zip(string.ascii_uppercase, choices)}

            row["Choices"] = letter_to_choice
            row["Correct"] = correct_letters
            questions.append(row)
    return questions

if "questions" not in st.session_state:
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "correct" not in st.session_state:
    st.session_state.correct = False
if "score" not in st.session_state:
    st.session_state.score = 0

question = st.session_state.questions[st.session_state.current_question]
choices = question["Choices"]
correct_answers = question["Correct"]

st.title("Interactive Quiz")
st.sidebar.write(f"Score: {st.session_state.score}")
st.markdown(f"**{question['Question']}**")

if not st.session_state.answered:
    st.markdown("**Choose your answer:**")

    choice_keys = list(choices.keys())
    radio_options = [f"{k}) {choices[k]}" for k in choice_keys]
    default_index = choice_keys.index(st.session_state.selected_answer) if st.session_state.selected_answer else 0

    selected_display = st.radio(
        label="",
        options=radio_options,
        index=default_index if default_index is not None else 0,
        key=f"radio_{st.session_state.current_question}"
    )

    st.session_state.selected_answer = selected_display[0]

    if st.button("✅ Submit Answer"):
        if st.session_state.selected_answer:
            if st.session_state.selected_answer in correct_answers:
                st.session_state.correct = True
                st.session_state.score += 1
            else:
                st.session_state.correct = False
            st.session_state.answered = True
            st.rerun()

else:
    for letter, text in choices.items():
        label = f"{letter}) {text}"
        if letter in correct_answers:
            st.success(label)
        elif letter == st.session_state.selected_answer:
            st.error(label)
        else:
            st.write(label)

    st.markdown(
    "<div style='margin-top: 1.5em; font-weight: 700; letter-spacing: 1px; font-size: 1.1em;'>EXPLANATION:</div>",
    unsafe_allow_html=True
)
    st.markdown(f"""
    <div style="
        background-color: #fff3cd;
        color: #000;
        padding: 1.25em;
        margin: 1em 0 1.5em 0;
        border: 1px solid #ffeeba;
    ">
        {question.get("Explanation", "No explanation provided.")}
    </div>
    """, unsafe_allow_html=True)

    if st.button("➡ Next Question"):
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(st.session_state.questions):
            st.session_state.current_question = 0
            st.session_state.score = 0
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.session_state.correct = False
        st.rerun()
