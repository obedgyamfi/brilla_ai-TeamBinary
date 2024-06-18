import openpyxl
import json
import re

# Load the Excel file
workbook = openpyxl.load_workbook('./updated_excel_file.xlsx')

# Load the expression locations from the JSON file
with open('./new_expression_location4.json', 'r') as json_file:
    expression_locations = json.load(json_file)

# Define a function to remove word groups from all worksheets
def remove_word_groups_in_worksheets(workbook, expression_locations, word_group):
    word_group_pattern = re.compile(r'\b' + word_group.replace(' ', r'\ ') + r'\b', re.IGNORECASE)

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        for item in expression_locations:
            if item["worksheet"] == sheet_name:
                cell_location = item["cell"]
                cell = sheet[cell_location]
                current_sentence = item["value"]
                current_sentence = word_group_pattern.sub('', current_sentence)
                cell.value = current_sentence

# Prompt the user for the word group to remove
word_group = input("Enter the word group to remove (e.g., 'open parenthesis'): ")

# Call the function to remove word groups in all worksheets
remove_word_groups_in_worksheets(workbook, expression_locations, word_group)

# Save the updated Excel file
workbook.save('updated_excel_file.xlsx')

print("Word groups removed. Excel file updated.")