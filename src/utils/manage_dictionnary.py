#!/usr/bin/env python3

import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICTIONARY_PATH = os.path.join(BASE_DIR, 'dictionnary.txt')
NEW_WORDS_PATH = os.path.join(BASE_DIR, 'new_words.txt')
TEMP_GAME_DICT_PATH = os.path.join(BASE_DIR, 'temp_game_dictionnary.txt')


def extract_words_from_file(path_to_file):
    """ Extracts words from a file separated by spaces """
    with open(path_to_file, 'r', encoding='utf-8') as file:
        return file.read().split()


def create_list_for_game(params, source=DICTIONARY_PATH, dest=TEMP_GAME_DICT_PATH):
    """ Creates a list of words for the game from the source file and writes it to dest, using params."""
    words = extract_words_from_file(source)

    if not params['capital_letters']:
        words = [word.lower() for word in words]

    if not params['accents']:
        words = [word for word in words if not any(
            char in word for char in 'éèêëàâäùûüîïôöç')]

    if not params['punctuation']:
        words = [word for word in words if not any(
            char in word for char in ',.;:?!')]

    if not params['numbers']:
        words = [word for word in words if not any(
            char in word for char in '0123456789')]

    random.shuffle(words)

    # Write the organized words to dest
    # Organize words into lines <= 40 characters
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) <= 40:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())

    with open(dest, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

    return lines


def add_new_word_list_to_dest(source=NEW_WORDS_PATH, dest=DICTIONARY_PATH):
    """Adds words from source file to the dest file, filter duplicates"""
    new_words = extract_words_from_file(source)
    already_used_words = extract_words_from_file(dest)

    # Combine and de-duplicate words
    combined_words = list(set(new_words + already_used_words))

    # Write the organized words back to dest
    with open(dest, 'w', encoding='utf-8') as file:
        file.write('\n'.join(combined_words))

    with open(source, 'w', encoding='utf-8') as file:
        file.write('')

    return combined_words


if __name__ == "__main__":
    add_new_word_list_to_dest()
