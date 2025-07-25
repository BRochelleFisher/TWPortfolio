import requests
import json
import time
import os

def get_definition_from_free_dictionary_api(word):
    """
    Fetches the definition of a word from the Free Dictionary API.
    Returns a cleaned, single-line definition or an error/not-found message.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404 for not found)

        data = response.json()

        if isinstance(data, list) and data:
            # Prioritize a concise definition
            definitions_list = []
            if 'meanings' in data[0]:
                for meaning in data[0]['meanings']:
                    if 'definitions' in meaning:
                        for definition_obj in meaning['definitions']:
                            definition_text = definition_obj.get('definition')
                            if definition_text:
                                definitions_list.append(definition_text.replace('\n', ' ').strip()) # Remove newlines within definition

                if definitions_list:
                    # Join the first few distinct definitions if available
                    # Take unique definitions to avoid repetition
                    unique_defs = []
                    for d in definitions_list:
                        if d not in unique_defs:
                            unique_defs.append(d)
                        if len(unique_defs) >= 2: # Get up to 2 concise definitions
                            break
                    return "; ".join(unique_defs)
            return "No concise definition found."

        elif isinstance(data, dict) and data.get('title') == 'No Definitions Found':
            return "No definition found for this word."
        else:
            return f"API returned unexpected data for '{word}'."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except json.JSONDecodeError:
        return f"Error: Invalid JSON response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_word_list_file(filepath):
    """
    Reads words from the file, fetches definitions, and writes them back
    to the same file with a comma delimiter.
    """
    temp_lines = []
    processed_count = 0

    try:
        # Read the existing content first
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                original_line = line.strip()
                word = original_line.split(',')[0].strip() # Get the word before the first comma

                if not word: # Skip empty lines
                    temp_lines.append(original_line) # Keep empty lines as they are
                    continue

                # Check if the line already contains a definition (e.g., has a comma)
                if ',' in original_line:
                    # Assuming if a comma exists, it's already processed, or we want to re-process it
                    # If you want to skip already defined words, add a check here.
                    pass

                print(f"Processing '{word}'...")
                definition = get_definition_from_free_dictionary_api(word)

                # Combine word and definition with a comma
                new_line = f"{word},{definition}"
                temp_lines.append(new_line)
                processed_count += 1
                time.sleep(0.5) # Be polite to the API

        # Write all processed lines back to the same file
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in temp_lines:
                f.write(line + '\n') # Add newline back for each line

        print(f"\nSuccessfully processed {processed_count} words and updated '{filepath}'.")

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred during file processing: {e}")

if __name__ == "__main__":
    # Define the name of your word list file
    word_list_filename = "UWords.txt"

    # Construct the full path to the words file
    script_dir = os.path.dirname(__file__)
    word_file_path = os.path.join(script_dir, word_list_filename)

    # Ensure the file exists, if not, create it with some example words
    if not os.path.exists(word_file_path):
        print(f"'{word_list_filename}' not found. Creating it with example words.")
        with open(word_file_path, 'w', encoding='utf-8') as f:
            f.write("apple\n")
            f.write("run\n")
            f.write("beautiful\n")
            f.write("galaxy\n")
            f.write("nonexistentword123\n")
            f.write("serendipity\n")
            f.write("ubiquitous\n")
        print("Example words added. Run the script again to fetch definitions.")
    else:
        # If the file exists, process it
        process_word_list_file(word_file_path)