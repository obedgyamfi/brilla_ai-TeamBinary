import re
from collections import defaultdict

# Function to extract LaTeX tags
def extract_latex_tags(expressions):
    tags = defaultdict(int)
    for expr in expressions:
        found_tags = re.findall(r"\\[a-zA-Z]+", expr)
        for tag in found_tags:
            tags[tag] += 1
    return tags

# Function to read LaTeX expressions from a file
def read_latex_expressions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Extract LaTeX expressions from each line
    latex_expressions = [line.strip() for line in lines if line.strip()]
    return latex_expressions

# File path to the text file containing LaTeX expressions
file_path = 'latex_expressions.txt'  # Replace with your file path

# Read LaTeX expressions from the file
latex_expressions = read_latex_expressions(file_path)

# Extract and count LaTeX tags
latex_tags = extract_latex_tags(latex_expressions)

# Print the grouped and counted LaTeX tags
for tag, count in latex_tags.items():
    print(f"{tag}")

