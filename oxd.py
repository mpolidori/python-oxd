import argparse
import os
import requests
import subprocess
import urllib


def lookup(selection, word, identifier):

    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    link = "https://en.oxforddictionaries.com/{}/{}".format(selection, word)
    site = str(urllib.request.urlopen(link).read())
    synonyms = []
    definitions = []

    if "No exact matches found" in site:
        print("No matches found.")
    else:
        print("\n " + word.upper() + "\n" + "-" * (len(word) + 2) + "\n")

        for i in range(len(site)):
            if site[i:i + 12] == "class=\"{}\">".format(identifier):
                if identifier == "syn":
                    synonyms += \
                        site[i + 12:i + 12 + site[i + 12:].index(
                            "</")].split(", ")

                if identifier == "ind":
                    definitions.append(
                        site[i + 12:i + 12 + site[i + 12:].index("</")])

    synonyms = [_ for _ in synonyms if len(_) > 0]

    if len(synonyms) > 20:
        synonyms = synonyms[:20]

    for item in synonyms:
        if "&#39;" in item:
            item = item.replace("&#39;", "\'")
        print("| " + item + "\n")

    for item in definitions:
        if "&#39;" in item:
            item = item.replace("&#39;", "\'")

        if "<strong class=\"phrase\">" in item:
            continue
            # Uncomment to enable phrases
            # item = item.replace("<strong class=\"phrase\">", "")

        if len(item) + 4 > term_width:
            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print("| " + item[:term_width - (4 + space)])
                item = item[term_width - (4 + space):]

            print("| " + item + "\n")

        else:
            print("| " + item + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--definition",
        help="show definition",
        metavar=""
    )
    parser.add_argument(
        "-s",
        "--synonyms",
        help="show synonyms",
        metavar=""
    )
    args = parser.parse_args()

    if args.synonyms and len(args.synonyms) > 1:
        lookup("thesaurus", args.synonyms, "syn")

    if args.definition and len(args.definition) > 1:
        lookup("definition", args.definition, "ind")


if __name__ == "__main__":
    main()
