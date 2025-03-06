import csv
import random
import string

def load_questions(filename="quiz_questions.csv"):
    """Load quiz questions from a CSV file"""
    questions = []
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "Question" not in row or "Choices" not in row or "Correct" not in row:
                print("❌ ERROR: Missing key in row:", row)
                continue

            choices = row["Choices"].split("|")
            correct_letters = set(row["Correct"].split("|"))  # Store correct answers as letters

            # Create a letter-to-choice mapping
            letter_to_choice = {letter: choice for letter, choice in zip(string.ascii_uppercase, choices)}

            # Store question data
            row["Choices"] = letter_to_choice  # Store choices as a letter-based dictionary
            row["Correct"] = correct_letters  # Store correct answer letters
            questions.append(row)

    return questions

def ask_question(question_data):
    """Display a question and get user input"""
    print("\n" + question_data["Question"])

    # Display choices
    for letter, choice in question_data["Choices"].items():
        print(f"{letter}) {choice}")

    correct_answers = question_data["Correct"]

    # Debugging output to verify correct answers
    print(f"DEBUG - Expected correct answer(s): {correct_answers}")

    # Get and normalize user input
    user_input = input("Your answer (comma-separated, multiple allowed): ").strip().upper()
    user_answers = {ans.strip() for ans in user_input.split(",") if ans.strip() in question_data["Choices"]}

    # Check correctness
    if not user_answers:
        print("❌ Incorrect! (No answer given)")
    elif user_answers == correct_answers:
        print("✅ Correct!")
    else:
        print("❌ Incorrect!")

    print(f"Explanation: {question_data['Explanation']}\n")

def run_quiz():
    """Main quiz loop"""
    questions = load_questions()
    random.shuffle(questions)

    for question in questions:
        ask_question(question)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    run_quiz()