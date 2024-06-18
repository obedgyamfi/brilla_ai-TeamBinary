import json

quiz_state_path = 'quiz_state.json'

def initialize_quiz_state():
    quiz_state = {
        "answer_states": [],
        "levenshtein_distances": [],
        "cosine_similarities": [],
        "response_times": []
    }
    
    with open(quiz_state_path, 'w') as json_file:
        json.dump(quiz_state, json_file, indent=4)



def update_quiz_state(answer_state, levenshtein_distance, cosine_similarity, response_time):
    with open(quiz_state_path, 'r') as json_file:
        quiz_state = json.load(json_file)
        
    # Update arrays
    quiz_state["answer_states"].append(answer_state)
    quiz_state["levenshtein_distances"].append(levenshtein_distance)
    quiz_state["cosine_similarities"].append(cosine_similarity)
    quiz_state["response_times"].append(response_time)
    
    with open(quiz_state_path, 'w') as json_file:
        json.dump(quiz_state, json_file, indent=4)


def is_round_complete():
    quiz_state = get_quiz_state()
    
    # Check if all questions have been answered
    return len(quiz_state["answer_states"]) >= quiz_state["total_questions"]

def get_quiz_state():
    with open(quiz_state_path, 'r') as json_file:
        quiz_state = json.load(json_file)
    
    return quiz_state

def get_correct_answer(answer_index_name):
    with open('database/nsmq_questions/2021/json_data_map/2021_contest_1_audio_metadata.json', 'r') as json_file:
        metadata = json.load(json_file)
        
        correct_answer = metadata[answer_index_name]["answer_text"]
        
        return correct_answer


# print(get_correct_answer("Round 1_question_0"))