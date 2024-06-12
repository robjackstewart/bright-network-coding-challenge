import re


def strip_non_alphanumeric_chars(subject: str):
    return re.sub(r"[^a-zA-Z0-9 ]", "", subject)
