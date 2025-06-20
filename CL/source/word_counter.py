import re
import string
import sys
from collections import Counter

def analyze_document_frequency(filepath="sampleAgg.txt"):
    
    try:
        with open(filepath, 'r', encoding='utf-8') as document_file:
            text_string = document_file.read().lower()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.", file=sys.stderr)
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}", file=sys.stderr)
        return

    match_pattern = re.findall(r'\b[a-z]{4,15}\b', text_string)

    word_counts = Counter(match_pattern)

    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

    print("Word Frequencies:")
    print("-----------------")
    for word, count in sorted_words:
        print(f"{word} | {count}")

if __name__ == "__main__":
    analyze_document_frequency()