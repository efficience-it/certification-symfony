import yaml
import sys
import os

def validate_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"YAML Error in {file_path}: {exc}")
            return False

    errors = []

    for i, question in enumerate(data.get('questions', [])):
        correct_answers = [answer for answer in question.get('answers', []) if answer.get('correct')]

        if not correct_answers:
            errors.append(f"Question {i + 1} ('{question.get('question', '')}') in {file_path} does not have any correct answers.")
        elif len(correct_answers) > 0 and not all(answer.get('correct') == True for answer in correct_answers):
            errors.append(f"Question {i + 1} ('{question.get('question', '')}') in {file_path} has some answers incorrectly marked as correct.")
        elif len(correct_answers) == 1 and any(answer.get('correct') == True for answer in correct_answers):
            # If there is only one correct answer, ensure there is no more than one correct answer
            if len(correct_answers) > 1:
                errors.append(f"Question {i + 1} ('{question.get('question', '')}') in {file_path} has multiple answers marked as correct, but should have only one.")
        elif len(correct_answers) > 1:
            # If there are multiple correct answers, no issue
            pass

    if errors:
        for error in errors:
            print(f"Error: {error}")
        return False

    return True

def validate_all_files(directory):
    all_valid = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                print(f"Validating {file_path}")
                if not validate_yaml(file_path):
                    all_valid = False
    return all_valid

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_quiz.py <path_to_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not validate_all_files(directory):
        sys.exit(1)
