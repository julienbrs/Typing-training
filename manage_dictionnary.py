from collections import OrderedDict

def extract(source):
    list_words = []
    with open(source) as f:
        lines = f.readlines()
        for line in lines:
            word = ""
            for char in line:
                if char != " ":
                    word += char
                else:
                    list_words.append(word)
                    word = ""
    return list_words



def affiche(dico):
    print("on print le dico ")
    for word in dico:
        print(word, len(word))
    print("")

def main(source, dest):
    already_used = extract(dest)
    new_words = []
    with open(source) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            word = ""
            for char in line:
                if char in ("|", " ") and word != "":
                    new_words.append(word)
                    word = ""
                elif char not in ("|", " ", "-"):
                    word += str(char)
            new_words.append(word)

    affiche(already_used)
    affiche(new_words)
    temp_dico = new_words + already_used
    affiche(temp_dico)

    #final_words = [i for n, i in enumerate(temp_dico) if i not in temp_dico[:n]]
    final_words = list(OrderedDict.fromkeys(temp_dico))     #utiliser methode compréhension liste ? 

    affiche(final_words)
    final_dico = []
    line = ""
    for word in final_words:
        if len(line) + len(word) <= 40:
            line += word + " "
        else:
            final_dico.append(line)
            line = word + " "
    final_dico.append(line)

    with open(dest, 'w') as f:
        f.writelines('\n'.join(final_dico))

    return final_dico

if __name__ == "__main__":
    main("temp.txt", "dictionnary.txt")