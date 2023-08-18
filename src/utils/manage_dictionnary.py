import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICTIONARY_PATH = os.path.join(BASE_DIR, 'dictionnary.txt')
NEW_WORDS_PATH = os.path.join(BASE_DIR, 'new_words.txt')
TEMP_GAME_DICT_PATH = os.path.join(BASE_DIR, 'temp_game_dictionnary.txt')

def extract_words_from_file(path_to_file):
    """ Extracts words from a file separated by spaces """
    with open(path_to_file, 'r') as file:
        return file.read().split()


def add_words_to_file(filename, words):
    """ Adds words to a file separated by spaces """
    with open(filename, 'a') as file:
        file.write(" ".join(words))


def create_list_for_game(params, source=DICTIONARY_PATH, dest=TEMP_GAME_DICT_PATH):
    """ Creates a list of words for the game from the source file and writes it to dest, using params."""
    # Extract words from source
    words = extract_words_from_file(source)
    print("we are creating")
    print("params", params)
    print("Initial words:", len(words))

    # Check if we use capital letters
    if not params['capital_letters']:
        # put all words in lowercase
        words = [word.lower() for word in words]

    # Check if we use accents
    if not params['accents']:
        words = [word for word in words if not any(
            char in word for char in 'éèêëàâäùûüîïôöç')]

    # Check if we use punctuation
    if not params['punctuation']:
        words = [word for word in words if not any(
            char in word for char in ',.;:?!')]

    # Check if we use numbers
    if not params['numbers']:
        words = [word for word in words if not any(
            char in word for char in '0123456789')]

    # Shuffle the words
    random.shuffle(words)

    # Write the organized words to dest
    # Organize words into lines <= 40 characters
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) <= 40:
            line += word + " "
        else:
            # Strip is used to remove trailing space
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())

    # Write the organized words to dest
    with open(dest, 'w') as file:
        file.write('\n'.join(lines))

    return lines


def add_new_word_list_to_dest(source=NEW_WORDS_PATH, dest=DICTIONARY_PATH):
    """Adds words from source file to the dest file, filter duplicates"""
    # Extract words from source and dest
    new_words = extract_words_from_file(source)
    already_used_words = extract_words_from_file(dest)

    # Combine and de-duplicate words
    combined_words = list(set(new_words + already_used_words))

    # Write the organized words back to dest
    with open(dest, 'w') as file:
        file.write('\n'.join(combined_words))

    return combined_words


def add_word_to_dest(word, dest=DICTIONARY_PATH):
    """Adds a word to the dest file, filter duplicates"""
    # Extract words from dest
    already_used_words = extract_words_from_file(dest)

    # Combine and de-duplicate words
    combined_words = list(set([word] + already_used_words))

    # Write the organized words back to dest
    with open(dest, 'w') as file:
        file.write('\n'.join(combined_words))

    return combined_words


if __name__ == "__main__":
    params = {
        'capital_letters': True,
        'accents': True,
        'punctuation': True,
        'numbers': True
    }
    add_new_word_list_to_dest()
