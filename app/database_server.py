from flask import Flask,request, jsonify, send_from_directory, url_for
from flask_cors import CORS, cross_origin
import os 
import json
import quiz_assessment
# from audio_synthesis.stt_custom_client import SpeechToTextSynthesizer
import audio_synthesis.stt_client as stt_client
from answer_evaluation.answer_evaluator import AnswerComparator
from database import quiz_state

# Set the directory for the static files
STATIC_DIR = os.path.join(os.getcwd(), 'database')

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)   # Enable CORS for all routes

# Speech To Text model setup
# model_path = 'database/ai_voice_models/stt_voice_model/vosk-model-en-us-0.22'
# stt = SpeechToTextSynthesizer(model_path)

# Answer evaluation and comparator setup
comparator = AnswerComparator()

# initiliaze quiz state
quiz_state.initialize_quiz_state()
answer_index_name = ''


@app.route('/static/<path:filename>')
def static_files(filename):
    # Log the requested file path for debugging
    print(f"Serving static file: {os.path.join(STATIC_DIR, filename)}")
    return send_from_directory(STATIC_DIR, filename)

# Databse Routes
@app.route('/', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provieded"}), 400
    
    # Perform action here with the recieved data
    # example
    print("Recieved data:", data)
    
    # Respond back with a success message
    return jsonify({"message": "Data was recieved successfully"}), 200 

@app.route('/api/process_user_answer', methods=['POST'])
@cross_origin()
def process_user_answer():
    # Get the uploaded file from the request
    audio_file = request.files['audioFile']
    
    # # Save the file to disk or process it in memory
    filename = 'user_answer.wav'
    audio_file.save(os.path.join('database/audio_data/user_answers_audio', filename))
    
    audio_file_path = 'database/audio_data/user_answers_audio/user_answer.wav'
    # user_answer_text = stt.transcribe(audio_file_path)
    stt_result = stt_client.pipe(audio_file_path)
    user_answer_text = stt_result["text"]
  
    
    # Evaluate answers
    
      # Get correct answer from excel sheet
    correct_answer_text = [quiz_state.get_correct_answer(answer_index_name)]
   
    preprocessed_correct_answers = [comparator.preprocess(answer) for answer in correct_answer_text]
    
    if not preprocessed_correct_answers or not preprocessed_correct_answers[0]:
        return jsonify({'error': 'Correct answer text is empty or invalid'}), 400
    
    comparator.get_tfidf_vectorizer(preprocessed_correct_answers)
    
    is_correct, levenshtein_distance, cosine_sim = comparator.compare_answer(user_answer_text, correct_answer_text[0])
    
    print("User Answer:", user_answer_text)
    print("Correct Answer:", correct_answer_text[0])
    print("Levenshtein:", levenshtein_distance)
    print("Cosine similarity:", cosine_sim)
    
    response_data = {}
    if is_correct:
        is_correct_audio_path = 'database/audio_data/is_correct.wav'
        filename = os.path.relpath(is_correct_audio_path, STATIC_DIR)
        response_data["audio_url"] = url_for('static_files', filename=filename, _external=True)
        return jsonify(response_data)
    else:
        is_incorrect_audio_path = 'database/audio_data/that_is_incorrect.wav'
        filename = os.path.relpath(is_incorrect_audio_path, STATIC_DIR)
        response_data["audio_url"] = url_for('static_files', filename=filename, _external=True)
        return jsonify(response_data)
    
    # response_time = request.files['response_time']
    response_time = 15
    quiz_state.update_quiz_state(is_correct, levenshtein_distance, cosine_sim, response_time)
    round_state = quiz_state.is_round_complete()
    
    # Return a success message
    response = {
        'message': 'Audio file uploaded successfully', 
        'is_round_complete': round_state, 
        'answer_state': is_correct
        }
    
    return jsonify(response)
    
@app.route('/api/save_app_settings', methods=['POST'])
def save_app_settings():
   try:
    
        # Extract parentMenu and selectedValue from the request body
        parentMenu = next(iter(request.form))
        selectedValue = request.form[parentMenu]

        # Load existing settings from app_settings.json
        with open('database/app_settings.json', 'r') as json_file:
            settings = json.load(json_file)

        # Update the corresponding setting based on parentMenu
        if parentMenu == 'selectedYear':
            settings['selectedYear'] = selectedValue
        elif parentMenu == 'selectedContest':
            settings['selectedContest'] = selectedValue
        elif parentMenu == 'selectedRound':
            settings['selectedRound'] = selectedValue
        else:
            return jsonify({"error": "Invalid parentMenu specified"}), 400

        # write updated setting back to app_settings.json file
        with open('database/app_settings.json', 'w') as json_file:
            json.dump(settings, json_file, indent=4)

        # Respond with a success message
        return jsonify({"message": f"Setting '{parentMenu}'  updated to '{selectedValue}'"}), 201
    
   except Exception as e:
       # Handle errors
       return jsonify({"error": str(e)}), 400


@app.route('/api/play_questions', methods=['POST'])
@cross_origin()
def play_questions():
    
    
    # app_settings = db.get_app_setting()
    app_settings = quiz_assessment.get_app_settings()
    request_data = request.get_json() # parse the incoming JSON data
    question_index = request_data.get('index')
    
    
    print('Recieved data:', request_data)
    print('Question index:', question_index)
    
    #params
    selected_year = app_settings['selectedYear']
    selected_contest = app_settings['selectedContest']
    selected_rounds = app_settings['selectedRound']
    print(selected_year, selected_contest, selected_rounds)
    
    global answer_index_name
    answer_index_name = f"Round {selected_rounds}_question_{question_index}"
    print("Answer Index Name:", answer_index_name)
    
    
    json_file_path = 'database/nsmq_questions/2021/json_data_map/2021_contest_1_map.json' # this is where we'll find the excel sheet
    base_directory = os.path.join(STATIC_DIR, 'nsmq_questions', '2021')
    
   
   # Begin quiz program
   # base on settings get the location of the audio to play
   
   # Load the JSON data
    with open(json_file_path, 'r') as json_file:
        question_json_data = json.load(json_file)
        
    try:
        # Initialize response data
        response_data = {}

        # Get question file path and parse it
        question_file_path = quiz_assessment.get_file_path(selected_year, selected_contest, question_json_data)
        question_audio_path = os.path.join(STATIC_DIR, 'audio_data', 'questions_audio', f"{selected_year}_contest_{selected_contest}_Round {selected_rounds}_question_{question_index}.wav")

        if question_file_path:
            # Adjust the file path to be absolute
            absolute_file_path = os.path.join(base_directory, os.path.basename(question_file_path))

            # Process the contest file and get the concatenated data array
            if selected_rounds == "None":
                selected_rounds = 1
            result_array = quiz_assessment.extract_questions(absolute_file_path, selected_rounds)

            if isinstance(result_array, dict) and "error" in result_array:
                response_data["questions_error"] = result_array["error"]
            else:
                # Add the questions to the response data
                response_data["questions"] = result_array[question_index]
        else:
            response_data["questions_error"] = f"No file path found for year {selected_year}, contest {selected_contest}"

        if question_audio_path and os.path.isfile(question_audio_path):
            # response_data["audio_url"] = url_for('static_files', filename=os.path.relpath(question_audio_path, STATIC_DIR))
            filename = os.path.relpath(question_audio_path, STATIC_DIR)
            response_data["audio_url"] = url_for('static_files', filename=filename, _external=True)
            
        else:
            response_data["audio_error"] = "Audio file not found"

        # Check if there were any errors and set the appropriate status code
        if "questions_error" in response_data or "audio_error" in response_data:
            return jsonify(response_data), 400

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=3001)

    
    
    
