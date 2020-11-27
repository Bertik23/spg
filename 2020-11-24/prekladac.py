with open("2020-11-24\encs.txt", encoding="utf-8") as f:
    slovnik = list((i.split("|") for i in f.read().split("\n")[:-1]))


while True:
    text = input("K překladu: ")
    for znak in ".,?!":
            text = text.replace(znak,"")

    out = ""
    for slovo in text.split():
        translated = False
        for s in slovnik:
            if s[0] == slovo:
                out += f"{s[1]} "
                translated = True
                break
        if not translated:
            out += f"{slovo} "

    print(out)