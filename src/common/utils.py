import re
from typing import Tuple


def strip_non_alphanumeric_chars(subject: str):
    return re.sub(r"[^a-zA-Z0-9 ]", "", subject)


def replace_whitespace_with(subject: str, replacement: str):
    return re.sub(r"\s+", replacement, subject).strip()


def chunk(text: str, split_words: set[str]) -> Tuple[str, list[int]]:
    # Sort the split words by length in descending order to handle overlapping cases
    # split_words = sorted(split_on, key=len, reverse=True)

    # Escape special characters in split words
    split_words = [re.escape(word) for word in split_words]

    # Create a regex pattern to match any of the split words
    pattern = "|".join(split_words)

    # Initialize the result list and indices list
    result = []
    indices = []

    # Keep track of the current position in the text
    last_pos = 0

    # Find all matches and their positions
    for match in re.finditer(pattern, text):
        start, end = match.span()
        if last_pos < start:
            result.append(text[last_pos:start])
        result.append(text[start:end])
        indices.append(len(result) - 1)  # Index where the split word is added
        last_pos = end

    # Append any remaining part of the text
    if last_pos < len(text):
        result.append(text[last_pos:])

    return result, indices
