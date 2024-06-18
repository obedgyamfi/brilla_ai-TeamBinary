import os
import json
import pandas as pd
from tts_custom_client import TextToSpeechSynthesizer  # Replace 'YourTTSModule' with the actual module name

# Initialize the TextToSpeechSynthesizer
tts_synth = TextToSpeechSynthesizer(db_path='./nsmq_db', output_dir='./output', model_type='quizmistress')

# Load the Excel file
excel_file = "updated_excel_file.xlsx"
excel_data = pd.read_excel(excel_file, sheet_name=None)

# Function to create directories and subdirectories
def create_directories(worksheet_name):
    # Create directory for the worksheet
    os.makedirs(worksheet_name, exist_ok=True)
    
    # Create subdirectories for Preamble Text, Question, and Answer
    for subdir in ["Preamble Text", "Question", "Answer"]:
        os.makedirs(os.path.join(worksheet_name, subdir), exist_ok=True)

# Iterate over each worksheet
for worksheet_name, data in excel_data.items():
    # Create directories for the current worksheet
    create_directories(worksheet_name)
    
    # Iterate over rows and process data
    for index, row in data.iterrows():
        # Extract data from columns
        preamble_text = row["Preamble Text"]
        question = row["Question"]
        answer = row["Answer"]
        
        # Save data to respective files
        with open(os.path.join(worksheet_name, "Preamble Text", f"{index + 1}.txt"), "w") as file:
            file.write(preamble_text)
        
        with open(os.path.join(worksheet_name, "Question", f"{index + 1}.txt"), "w") as file:
            file.write(question)
        
        with open(os.path.join(worksheet_name, "Answer", f"{index + 1}.txt"), "w") as file:
            file.write(answer)
        
        # Text-to-speech synthesis
        preamble_audio_path = tts_synth.synthesize_text(preamble_text)
        question_audio_path = tts_synth.synthesize_text(question)
        answer_audio_path = tts_synth.synthesize_text(answer)
        
        # Update paths in JSON data
        audio_data = {
            "Preamble Text": {"path": preamble_audio_path, "cell_value": preamble_text},
            "Question": {"path": question_audio_path, "cell_value": question},
            "Answer": {"path": answer_audio_path, "cell_value": answer}
        }
        
        # Save JSON data
        json_file_path = os.path.join(worksheet_name, f"{index + 1}_audio_data.json")
        with open(json_file_path, "w") as json_file:
            json.dump(audio_data, json_file, indent=4)

# Close the TextToSpeechSynthesizer
tts_synth.close()

print("Directories created and JSON files with audio paths generated successfully.")
