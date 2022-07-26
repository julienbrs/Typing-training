
def main(source, dest):
    new_words = []
    with open(source) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            word = ""
            for char in line:
                if char == "|" and word != "":
                    new_words.append(word)
                    word = ""
                elif char not in ("|", " "):
                    word += str(char)

    new_dico = []
    line = ""
    for word in new_words:
        if len(line) + len(word) <= 40:
            line += word + " "
        else:
            new_dico.append(line)
            line = word + " "
    


    with open(dest, 'a') as f:
        f.writelines('\n'.join(new_dico))
    return new_dico     

if __name__ == "__main__":
    main("temp.txt", "dictionnary.txt")