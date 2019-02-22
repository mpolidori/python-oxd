#!/usr/bin/env python

import argparse
# import os
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
        if link not in site:
            start = site.index(" of ") + 4
            end = start + site[start:].index(" ")
            word = site[start:end]

        for i in range(len(site)):
            if site[i:i + 12] == "class=\"pos\">".format(identifier):
                parts_of_speech.append(
                    site[i + 12:i + 12 + site[i + 12:].index("<")])

            if site[i:i + 12] == "class=\"{}\">".format(identifier):
                if identifier == "syn":
                    results += \
                        site[i + 12:i + 12 + site[i + 12:].index(
                            "<")].split(", ")

                if identifier == "ind":
                    results.append(
                        site[i + 12:i + 12 + site[i + 12:].index("<")])

    results = [_ for _ in results if len(_) > 0]

    # Uncomment to shorten results output
    """
    if len(results) > 10:
        results = results[:10]
    """

    if len(results) > 0:
        if identifier == "ind":
            print("\n {} - {}\n".format(
                word.upper(), ", ".join(
                    set([i for i in parts_of_speech if len(i) > 0]))))
        else:
            print("\n {}\n".format(word.upper()))

    if identifier == "syn":
        results = [", ".join(results)]

    for item in results:
        if item == "":
            break
        if "&#39;" in item:
            item = item.replace("&#39;", "\'")

        if len(item) + 4 > term_width:
            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print("| " + item[:term_width - (4 + space)])
                item = item[term_width - (4 + space):]

        print("| " + item + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--definition",
        help="show definition(s)",
        metavar=""
    )
    parser.add_argument(
        "-s",
        "--synonyms",
        help="show synonyms",
        metavar=""
    )
    args = parser.parse_args()

    if args.synonyms:
        lookup("thesaurus", args.synonyms, "syn")

    elif args.definition:
        lookup("definition", args.definition, "ind")

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError:
        print("Check your internet connection!")
