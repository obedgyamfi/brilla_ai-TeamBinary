from database import quiz_state
from answer_evaluation.answer_evaluator import AnswerComparator
import json


comparator = AnswerComparator()
answer_index_name = "Round 1_question_0"
correct_answer_text = [quiz_state.get_correct_answer(answer_index_name)]

preprocessed_correct_answers = [comparator.preprocess(answer) for answer in correct_answer_text]
print(preprocessed_correct_answers)

if not preprocessed_correct_answers or not preprocessed_correct_answers[0]:
    print(jsonify({'error': 'Correct answer text is empty or invalid'}))

comparator.get_tfidf_vectorizer(preprocessed_correct_answers)

is_correct, levenshtein_distance, cosine_sm = comparator.compare_answer(quiz_state.get_correct_answer(answer_index_name), correct_answer_text[0])

print("is_correct:", is_correct)
print("levenshtein_distance:", levenshtein_distance)
print("cosine similarity:", cosine_sm)

