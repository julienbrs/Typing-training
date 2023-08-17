import random


def extract_words_from_file(filename):
    """Extracts words from a file separated by spaces."""
    with open(filename, 'r') as file:
        return file.read().split()


def main(source, dest):
    """Extracts, combines, shuffles words from source and dest. Then writes them back to dest."""
    # Extract words from source and dest
    new_words = extract_words_from_file(source)
    already_used_words = extract_words_from_file(dest)

    # Combine and de-duplicate words
    combined_words = list(set(new_words + already_used_words))

    # Shuffle the words
    random.shuffle(combined_words)

    # Organize words into lines <= 40 characters
    lines = []
    line = ""
    for word in combined_words:
        if len(line) + len(word) <= 40:
            line += word + " "
        else:
            # Strip is used to remove trailing space
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())

    # Write the organized words back to dest
    with open(dest, 'w') as file:
        file.write('\n'.join(lines))

    return lines


if __name__ == "__main__":
    main("temp.txt", "dictionary.txt")
