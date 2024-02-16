import re

class CleanCellOfParenthesis:

    def clean(self,input):
        input_str = str(input)
        pattern = r'\([^)]*\)'
        matches = re.findall(pattern, input_str)
        for match in matches:
            input_str = input_str.replace(match, '')
        return input_str