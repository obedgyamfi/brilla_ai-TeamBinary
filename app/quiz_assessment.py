import os
import json
import pandas as pd

# Function to get the file path from the JSON data
def get_file_path(year, contest, json_data):
    try:
        file_path = json_data[str(year)][str(contest)]
        return file_path
    except KeyError:
        return None

# Function to load the worksheet and process the data
def extract_questions(file_path, round_number):
    round_name = f"Round {round_number}"
    data_array = []

    # Load the Excel file
    try:
        xls = pd.ExcelFile(file_path)
        
        # Check if the worksheet exists
        if round_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=round_name)
            
            
            # Ensure the columns "preamble text" and "question" exist
            if 'Preamble Text' in df.columns and 'Question' in df.columns:
                # Iterate through the rows and concatenate the text
                for index, row in df.iterrows():
                    preamble_text = row['Preamble Text']
                    question = row['Question']
                    concatenated_text = f"{preamble_text} {question}"
                    data_array.append(concatenated_text)
            else:
                print(f"Columns 'Preamble Text' and/or 'Question' not found in {round_name}")
        else:
            print(f"Worksheet {round_name} not found in the Excel file.")
    
    except Exception as e:
        print(f"Error processing file: {e}")

    return data_array

# Function to load application settings froma app_settings.json
def get_app_settings():
    try:
        with open('database/app_settings.json') as json_file:
            settings = json.load(json_file)
        return settings
    except FileNotFoundError:
        raise FileExistsError("Settings file not found")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON")
    except Exception as e:
        raise Exception(f"An error occured: {e}")

# # Define the base directory and load the JSON data
# base_directory = './nsmq_questions/2021'  # Change this to your base directory path if different
# json_file_path = './audio_database/2021_contest_1_map.json'  # JSON file containing the paths

# # Load the JSON data
# with open(json_file_path, 'r') as json_file:
#     contest_data = json.load(json_file)

# # Specify the year, contest, and round
# year = 2021
# contest = 1
# round_number = 1

# # Get the file path from the JSON data
# file_path = get_file_path(year, contest, contest_data)
# if file_path:
#     # Adjust the file path to be absolute
#     absolute_file_path = os.path.join(base_directory, os.path.basename(file_path))
    
#     # Process the contest file and get the concatenated data array
#     result_array = extract_questions(absolute_file_path, round_number)
    
#     # Print the result
#     print(result_array[0])
# else:
#     print(f"No file path found for year {year}, contest {contest}")

# settings = get_app_settings()
# print(settings)