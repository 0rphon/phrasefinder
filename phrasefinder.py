import pandas as pd
from sys import argv
from os import listdir, path as pathlib


def get_args():
    if "--help" in argv:
        print("Usage: python phrasefinder.py [name of text folder] [name of excel file]")
        exit(0)
    elif len(argv) < 3:
        print("Error: not enough specified arguments! try --help")
        exit(1)
    elif len(argv) > 3:
        print("Error: too many specified arguments! try --help")
        exit(2)
    else:
        return (argv[1],argv[2])


def get_files(path):
    if pathlib.exists(path):
        files = ["/".join((path,f)) for f in listdir(path) if f.endswith(".txt")]
        file_data = []
        for name in files:
            file_data.append((name,open(name, "r", encoding="utf-8").read().lower()))
        return file_data
    else:
        print("Error: cannot find text file directory")
        exit(3)


def get_phrases(doc):
    if pathlib.exists(doc):
        return [line[0].lower() for line in pd.read_excel(doc).iloc()]
    else:
        print("Error: cannot find excel file")
        exit(4)


def find_phrases(phrases, files):
    html_tags = ["<div>", "</div>", "<br>", "<b>", "</b>", "<u>", "</u>", "<li>", "</li>", "<i>", "</i>", "<ol>", "</ol>"]
    found = {}
    for phrase in phrases:
        found[phrase] = []
        for (name,text) in files:
            parted = text.partition(phrase)
            while len(parted[1]) == len(phrase):
                context = "{}{}{}".format(
                        (" ".join(parted[0].split(" ")[-10:])), 
                        parted[1], 
                        (" ".join(parted[2].split(" ")[:10]))
                    ).replace("\n", " ")
                for x in html_tags: context = context.replace(x, "")
                found[phrase].append((name.split("/")[-1], context))
                parted = parted[2].partition(phrase)
    return found


def display_and_save(found, longest_filename):
    output = open("output.txt","w", encoding="utf-8")
    for (phrase, instance) in found.items(): 
        if len(instance) != 0:
            out = '\n"{}"'.format(phrase)
            print(out)
            output.write(out+"\n")
            for (filename, context) in instance:
                out = "    {n:{l}}    {c}".format(n=filename, l=longest_filename, c=context)
                print(out)
                output.write(out+"\n")
            print("\n")
            output.write("\n")
        else:
            out = '"{}" not found'.format(phrase)
            print(out)
            output.write(out+"\n")
    output.close()


def main():
    print("Starting...")

    (txt_dir, xlsx_path) =  get_args()

    phrases = get_phrases(xlsx_path)
    files = get_files(txt_dir)
    longest_filename = 0
    for (name,_) in files: 
        legnth = len(name.split("/")[-1])
        if legnth > longest_filename: longest_filename = legnth

    found = find_phrases(phrases, files)
    display_and_save(found, longest_filename)

    total = 0
    for (_,data) in found.items():
        total+=len(data)
    print("\n%d results saved to output.txt"%total)
    exit(0)


if __name__ == "__main__":
    main()
