import re

class CleanCellOfParenthesis:

    # Removes all parenthetical statements from a given string.
    def clean(self,input):
        input_str = str(input)
        pattern = r'\([^)]*\)'
        matches = re.findall(pattern, input_str)
        for match in matches:
            input_str = input_str.replace(match, '')
        return input_str