#!/usr/bin/env python

import argparse
import os
import requests
import subprocess
import urllib


def lookup(selection, word, identifier):

    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    link = "https://en.oxforddictionaries.com/{}/{}".format(selection, word)
    site = urllib.request.urlopen(link).read().decode("utf-8")
    results = []
    parts_of_speech = []

    if "No exact matches found" in site:
        print("No matches found.")
    else:
        for i in range(len(site)):
            if site[i:i + 12] == "class=\"pos\">".format(identifier):
                parts_of_speech.append(
                    site[i + 12:i + 12 + site[i + 12:].index("</")])

            if site[i:i + 12] == "class=\"{}\">".format(identifier):
                if identifier == "syn":
                    results += \
                        site[i + 12:i + 12 + site[i + 12:].index(
                            "</")].split(", ")

                if identifier == "ind":
                    results.append(
                        site[i + 12:i + 12 + site[i + 12:].index("</")])

    results = [_ for _ in results if len(_) > 0]

    if len(results) > 20:
        results = results[:20]

    if len(results) > 0:
        if identifier == "ind":
            print("\n {} - {}\n".format(
                word.upper(), ", ".join(parts_of_speech)))
        else:
            print("\n {}\n".format(word.upper()))

    for item in results:
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
