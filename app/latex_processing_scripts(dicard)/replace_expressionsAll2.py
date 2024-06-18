import openpyxl
import json
import re

# Load the Excel file
workbook = openpyxl.load_workbook('./nsmq_questions/2021/2021 NSMQ contest 1.xlsx')

# Load the expression locations from the JSON file
with open('./new_expression_location4.json', 'r') as json_file:
    expression_locations = json.load(json_file)

# Define a function to replace expressions in all worksheets
def replace_expressions_in_worksheets(workbook, expression_locations):
    single_dollar_pattern = r"\$([^\$]+?)\$"
    double_dollar_pattern = r"\$\$([^\$]+?)\$\$"

    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        for item in expression_locations:
            if item["worksheet"] == sheet_name:
                cell_location = item["cell"]
                cell = sheet[cell_location]
                current_sentence = item["value"]
                expressions = item["expressions"]
                replacements = item["replacements"]
                for expression, replacement in zip(expressions, replacements):
                    # Replace expressions surrounded by single $
                    current_sentence = re.sub(single_dollar_pattern, lambda match: match.group(0).replace(match.group(1), replacement), current_sentence)
                    # Replace expressions surrounded by double $$
                    current_sentence = re.sub(double_dollar_pattern, lambda match: match.group(0).replace(match.group(1), replacement), current_sentence)
                # Remove all $ symbols
                current_sentence = current_sentence.replace("$", "")
                cell.value = current_sentence

# Call the function to replace expressions in all worksheets
replace_expressions_in_worksheets(workbook, expression_locations)

# Save the updated Excel file
workbook.save('updated_excel_file.xlsx')

print("Replacements done. Excel file updated.")