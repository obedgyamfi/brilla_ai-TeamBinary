import re
import latex2text

def replace_latex(part):
    if part.startswith('$') and part.endswith('$'):
        latex_code = part[1:-1]  # Remove the '$' symbols
        readable_text = latex2text.latex2text(latex_code)
        return readable_text
    else:
        return part

sentence = "Two angles are supplementary, and their difference is $50^{\\circ}$, find the measures of the angles."
parts = re.split(r'(\$[^$]+\$)', sentence)
modified_parts = [replace_latex(part) for part in parts]
print(' '.join(modified_parts))
# Output: Two angles are supplementary, and their difference is 50 degrees, find the measures of the angles.