import requests
import json
import os

def fetch_sort_and_save_words_by_length(url: str, sorted_file_name:str=None) -> dict: 
    """
    Fetches a list of words from a specified URL, sorts them by their first letter and length,
    and then saves the sorted list to a JSON file.

    Args:
        url (str): The URL from which to fetch the words.
        sorted_file_name (Optional[str]): The name of the file to save the sorted words. Defaults to "words_sorted.json".

    Returns:
        Optional[Dict[str, Dict[int, list]]]: A dictionary containing sorted words if successful, None otherwise.

    Raises:
        RequestException: If an error occurs during the network request.
        IOError: If an error occurs while writing to the file.
        json.JSONDecodeError: If an existing JSON file is not in a valid JSON format.
    """

    # 1st check if file exists and is json readable
    if sorted_file_name and os.path.isfile(sorted_file_name):
        try:
            with open(sorted_file_name, 'r') as f:
                sorted_words = json.load(f)
            return sorted_words
        except json.JSONDecodeError:
            print("The file is not in a valid JSON format, and will be re-created.")
        except FileNotFoundError:
            print("The file was not found and will be created.")

    words_url = url
    
    try:
        response = requests.get(words_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        words = response.text.replace('\r\n', '\n').split('\n') # Fix for both windows and linux
    except requests.exceptions.RequestException as e:
        print(f"Error fetching words from URL: {e}")
        raise e

    sorted_words = {}
    for word in words:
        if not word:
            continue
        word_length = len(word)
        first_letter = word[0]

        if first_letter in sorted_words:
            if word_length in sorted_words[first_letter]:
                sorted_words[first_letter][word_length].append(word)
            else:
                sorted_words[first_letter][word_length] = [word]
        else:
            sorted_words[first_letter] = {
                word_length: [word]
            }


    try:
        with open("words_sorted.json", "w") as f:
            json.dump(sorted_words, f, indent=4)
        return sorted_words
    except IOError as e:
        print(f"Error writing to file: {e}")
        raise e
