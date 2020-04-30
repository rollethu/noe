import re


def is_healthcare_number_valid(value):
    pattern = re.compile("[0-9]{9}")
    print(pattern, value, pattern.match(value))
    return pattern.fullmatch(value) is not None
