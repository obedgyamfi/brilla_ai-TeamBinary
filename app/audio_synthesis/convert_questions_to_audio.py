import pandas as pd
import os
import json
from tts_custom_client import TextToSpeechSynthesizer  # Replace with actual module path

filepath = './updated_excel_file.xlsx'
questions_output_folder = './audio_database/questions_audio'  # Folder to store synthesized question audio files
answers_output_folder = './audio_database/answers_audio'
model_name = 'quizmistress'
year = 2021 # enter the year you're converting here
contest = 1 # enter the contest number of

def read_data_from_excel(filepath):
    xl = pd.ExcelFile(filepath)
    data = {}
    
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        has_preamble = df["Has Preamble"].tolist()
        preamble_text = df["Preamble Text"].tolist()
        questions = df["Question"].tolist()
        answers = df["Answers"].tolist()
        
        data[sheet_name] = {
            "has_preamble": has_preamble,
            "preamble_text": preamble_text,
            "questions": questions,
            "answers": answers
        }
        
    
    return data

def main():
    # Initialize your custom TTS synthesizer
    tts = TextToSpeechSynthesizer(model_type=model_name)
    
    # Synthesize questions and answers
    
    data = read_data_from_excel(filepath)
    audio_metadata = {}
    
    for sheet_name, sheet_data in data.items():
        has_preamble = sheet_data["has_preamble"]
        preamble_text = sheet_data["preamble_text"]
        questions = sheet_data["questions"]
        answers = sheet_data["answers"]
        
        for i in range(len(questions)):
            if has_preamble[i] == "Yes":
                question_text = f"{preamble_text[i]} {questions[i]}"
            else:
                question_text = questions[i]
                
            answer_text = answers[i]
            
            # Generate filename based on your conventions
            cell_value = questions[i].replace(" ", "_").lower()[:20]  # Adjust as needed
            question_filename = f"{cell_value}_{year}_contest_{contest}_{sheet_name}_question_{i}"
            answer_filename = f"{cell_value}_{year}_contest_{contest}_{sheet_name}_answer_{i}"
            
            # Synthesize text to audio using your custom TTS synthesizer
            question_audio_file = tts.synthesize_text(question_text, output_file=os.path.join(questions_output_folder, f"{question_filename}.wav"))
            answer_audio_file = tts.synthesize_text(answer_text, output_file=os.path.join(answers_output_folder, f"{answer_filename}.wav"))
            
            print(f"Question Audio file '{question_filename}.wav' saved at '{question_audio_file}'.")
            print(f"Answer Audio file '{answer_filename}.wav' saved at '{answer_audio_file}'.")
            
            # Store metadata
            audio_metadata[f"{sheet_name}_question_{i}"] = {
                "preamble_text": preamble_text[i] if has_preamble[i] == "Yes" else None,
                "question_text": question_text,
                "answer_text": answer_text,
                "question_audio_file": question_audio_file,
                "answer_audio_file": answer_audio_file
            }

    # Save metadata to a JSON file
    metadata_filename = f"{year}_contest_{contest}_audio_metadata.json"
    with open(metadata_filename, 'w') as json_file:
        json.dump(audio_metadata, json_file, indent=4)
        
    print(f"Audio metadata saved to '{metadata_filename}'.")
            
    
    
    # Clean up resources
    tts.close()

if __name__ == '__main__':
    if not os.path.exists(questions_output_folder):
        os.makedirs(questions_output_folder)
        
    if not os.path.exists(answers_output_folder):
        os.makedirs(answers_output_folder)
    main()
