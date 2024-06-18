import os
import json

def generate_contest_urls(base_directory):
    contest_data = {}

    # Scan the base directory for year subdirectories
    for year_dir in os.listdir(base_directory):
        year_path = os.path.join(base_directory, year_dir)
        if os.path.isdir(year_path) and year_dir.isdigit():  # Check if it is a directory and is a year
            contest_data[year_dir] = {}
            
            # Scan the year's directory for contest files
            for file_name in os.listdir(year_path):
                if file_name.startswith("2021 NSMQ contest") and file_name.endswith(".xlsx"):
                    contest_number = file_name.split("contest ")[1].split(".xlsx")[0]
                    relative_path = os.path.join(base_directory, year_dir, file_name)
                    contest_data[year_dir][contest_number] = relative_path

    return contest_data

def save_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Define the base directory
base_directory = '../nsmq_questions'  # Change this to your base directory path

# Generate the contest URLs
contest_data = generate_contest_urls(base_directory)

# Save the JSON structure to a file
output_file = 'contests.json'
save_json(contest_data, output_file)

print(f"JSON file '{output_file}' has been created.")
