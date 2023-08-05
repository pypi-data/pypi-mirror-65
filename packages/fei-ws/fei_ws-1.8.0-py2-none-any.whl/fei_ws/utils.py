import fei_ws.config as config
import re

NAME_REGEX = re.compile(r"([A-Za-z']\.|\b[A-Za-z']{1,3}\b|'[tT])", re.UNICODE)
ROMAN_REGEX = re.compile(r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', re.IGNORECASE)


def normalize_name(value, roman_numerals=False):
    def _transform(match):
        word = match.group()
        if len(word) == 2 and word[1] == '.':  # If word is a letter followed by a .(dot) Then use capitals
            return word.upper()
        if word.lower() in config.FEI_WS_LOWER_CASE_WORDS:
            return word.lower()
        if word.upper() in config.FEI_WS_UPPER_CASE_ACRONYMS:
            return word.upper()
        return word

    if not value:
        return value
    value = value.title()
    value = NAME_REGEX.sub(_transform, value)
    if roman_numerals:
        value = ROMAN_REGEX.sub(
            lambda match: match.group().upper() if match.group() else match.group(), value)
    return value[0].upper() + value[1:]