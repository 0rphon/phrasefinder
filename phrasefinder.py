import pandas as pd
from sys import argv
from os import listdir, path as pathlib

def get_args():
    if "--help" in argv:
        print("Usage: python phrasefinder.py [name of text folder] [name of xlsx file]")
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
        return ["/".join((path,f)) for f in listdir(path) if f.endswith(".txt")]
    else:
        print("Error: cannot find text file directory")
        exit(3)


def get_phrases(doc):
    if pathlib.exists(doc):
        return [line[0] for line in pd.read_excel(doc).iloc()]
    else:
        print("Error: cannot find excel file")
        exit(4)


def main():
    (txt_dir, xlsx_path) =  get_args()
    phrases = get_phrases(xlsx_path)
    files = get_files(txt_dir)
    output = open("output.txt","w")

    for name in files:
        text = open(name, "r").read()
        for phrase in phrases:
            split = text.partition(phrase)
            while len(split[1]) == len(phrase):
                context = (
                            (" ".join(split[0].split(" ")[-10:])).replace("\n","    ") + 
                            split[1] + 
                            (" ".join(split[2].split(" ")[:10])).replace("\n","    ")
                )
                result = name+"      "+context
                print(result)
                output.write(result+"\n")
                split = split[2].partition(phrase)

    print("results saved to output.txt")
    output.close()
    exit(0)


if __name__ == "__main__":
    main()