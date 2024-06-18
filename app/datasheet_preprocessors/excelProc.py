import openpyxl
import json
import shutil

def copy_and_edit_excel(file_path, expressions_with_sentences):
    # Create a copy of the Excel file
    edited_file_path = file_path.replace('.xlsx', '_edited.xlsx')
    shutil.copyfile(file_path, edited_file_path)

    # Edit the copied Excel file
    edit_excel(edited_file_path, expressions_with_sentences)

    return edited_file_path

def edit_excel(file_path, expressions_with_sentences):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(file_path)

    # Iterate through each sheet in the workbook
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        if sheet_name.startswith('Round'):
            # Iterate through expressions with sentences
            for expression_with_sentence in expressions_with_sentences:
                row = expression_with_sentence['row']
                col = expression_with_sentence['column']
                sentence = expression_with_sentence['sentence']

                # Locate the cell in the sheet
                cell = sheet[col + str(row)]
                content = cell.value

                # Replace LaTeX expressions with sentences
                if content:
                    content = content.replace('$$', sentence)

                    # Update the content of the cell
                    cell.value = content

    # Save the edited Excel workbook
    workbook.save(file_path)

def read_expressions_with_sentences(json_file_path):
    with open(json_file_path, 'r') as json_file:
        expressions_with_sentences = json.load(json_file)
    return expressions_with_sentences

# Example usage
file_path = '../ai_models_and_data/models_and_data/nsmq_past_questions/NSMQ QUESTIONS SPREADSHEETS/2020/2020 NSMQ contest 1.xlsx'  # Replace with the actual file path
json_file_path = './converted_expressions.json'  # Replace with the actual JSON file path

# Read expressions with sentences from the JSON file
expressions_with_sentences = read_expressions_with_sentences(json_file_path)

# Copy the Excel file, edit the copy, and replace LaTeX expressions with sentences
edited_file_path = copy_and_edit_excel(file_path, expressions_with_sentences)

