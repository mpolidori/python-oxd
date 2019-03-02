#!/usr/bin/env python

import argparse
import requests
import subprocess
import urllib


def definition(word):

    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    if term_width > 80:
        term_width = 80

    link = "https://en.oxforddictionaries.com/definition/{}".format(word)
    site = urllib.request.urlopen(link).read().decode("utf-8")
    results = []

    if "No exact matches found" in site:
        print("\n  No matches found.\n")

    else:
        if link not in site:
            start = site.index(" of ") + 4
            end = start + site[start:].index(" ")
            word = site[start:end]

        if "_" in word:
            word = word.replace("_", " ")

        print("\n  DEFINITION(S) OF {}:\n".format(word.upper()))

        for i in range(len(site)):
            if site[i:i + 16] == "class=\"ex\"> <em>":
                results.append("EX, {}".format(
                    site[i + 16:i + 16 + site[i + 16:].index("<")]))

            if site[i:i + 12] == "class=\"pos\">":
                results.append("P, {}".format(
                    site[i + 12:i + 12 + site[i + 12:].index("<")]))

            if site[i:i + 18] == "class=\"iteration\">":
                results.append("I, {}".format(
                    site[i + 18:i + 18 + site[i + 18:].index("<")]))

            if site[i:i + 26] == "class=\"subsenseIteration\">":
                results.append("SI, {}".format(
                    site[i + 26:i + 26 + site[i + 26:].index("<")]))

            if site[i:i + 12] == "class=\"ind\">":
                results.append(
                    "--D" + site[i + 12:i + 12 + site[i + 12:].index("<")])

            if site[i:i + 23] == "class=\"crossReference\">" \
               and site[i + 23] != "<":
                results.append(
                    "CR, " + site[i + 23:i + 23 + site[i + 23:].index("<")] +
                    site[i + 23 + site[i + 23:].index(">") + 1:i + 23 +
                         site[i + 23:].index(">") + 1 + site[i
                         + 23 + site[i + 23:].index(">") + 1:].index("<")])

            if site[i:i + 15] == "class=\"phrase\">":
                break

    results = [
        item for item in results if item not in ["EX,", "I, ", "SI, ", ""]]

    last_spaces = 0

    for item in results:
        prepend_symbol = "|"
        spaces = 1

        if results.index(item) > 1:
            last = results[results.index(item) - 1]

            if "&lsquo;" in item and "&lsquo;" in last:
                continue

        else:
            last = ""

        if results.index(item) > 2:
            second_last = results[results.index(item) - 2]

        else:
            second_last = ""

        if "EX, " in item:
            item = item.replace("&lsquo;", "'")
            item = item.replace("&rsquo;", "'")

            if second_last[:3] != "I, " and second_last[:4] != "SI, ":
                item = " " + item[4:]

            else:
                item = "  " + item[4:]

        if item[:3] == "P, ":
            print("  {}\n".format(item[3:].upper()))
            continue

        if item[:3] == "I, ":
            continue

        if item[:4] == "SI, ":
            continue

        if "&#39;" in item:
            item = item.replace("&#39;", "'")

        if last[:3] == "I, ":
            if item[:4] == "CR, ":
                item = item[4:]
            item = last[3:] + "  " + item

        if last[:4] == "SI, ":
            if item[:4] == "CR, ":
                item = item[4:]
            prepend_symbol = "+"
            item = last[4:] + "  " + item
            spaces += 3

        if second_last[:3] == "I, ":
            if last[:4] == "CR, ":
                item = "   " + item
            else:
                spaces += 2

        if second_last[:4] == "SI, ":
            if last[:4] == "CR, ":
                item = " " * 5 + item
            spaces += 7

        if item[:4] == "CR, ":
            if last[:3] == "--D":
                spaces += 1
            else:
                spaces += 2
            item = item[4:]

        if (item[spaces] == "'" or item.count("'") == 2) and item[-1] == "'":
            if last[:4] == "CR, ":
                spaces = last_spaces - 1
            if last[:3] == "I, " or last[:4] == "SI, ":
                item = item[:item.index("'") - 1] + item[item.index("'"):]

        item = " " * spaces + item
        last_spaces = spaces

        if last[:3] == "I, " or last[:4] == "SI, ":
            item = prepend_symbol + item

        if "--D" in item:
            if len(item) <= 4:
                continue
            elif last[:3] != "I, " and last[:4] != "SI, ":
                item = prepend_symbol + " " + item[spaces + 3:]
            else:
                item = item[:item.index("--D")] + item[item.index("--D") + 3:]

        if len(item) + 4 > term_width:
            if second_last[:3] == "I, " or second_last[:4] == "SI, ":
                if last[:4] == "CR, ":
                    spaces += 6
                else:
                    spaces += 1

            if last[:3] == "I, ":
                spaces += 4

            if last[:4] == "SI, ":
                spaces += 6

            if item[spaces + 1] != "'" and item[-1] != "'":
                if last[:3] != "I, " and last[:4] != "SI, ":
                    spaces += 1

            else:
                spaces += 2

            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print(item[:term_width - (4 + space)])
                item = " " * spaces + item[term_width - (4 + space):]

        print(item + "\n")


def synonyms(word):

    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    if term_width > 80:
        term_width = 80

    link = "https://en.oxforddictionaries.com/thesaurus/{}".format(word)
    site = urllib.request.urlopen(link).read().decode("utf-8")
    results = []

    if "No exact matches found" in site:
        print("\n  No matches found.\n")

    else:
        if link not in site:
            start = site.index(" of ") + 4
            end = start + site[start:].index(" ")
            word = site[start:end]

        print("\n  SYNONYMS OF {}:\n".format(word.upper()))

        for i in range(len(site)):

            if site[i:i + 12] == "class=\"syn\">":
                results += \
                    site[i + 12:i + 12 + site[i + 12:].index("<")].split(", ")

    results = [item for item in results if len(item) > 0]

    if len(results) > 50:
        results = results[:50]

    results = [", ".join(results)]

    for item in results:
        if item == "":
            break

        if "&#39;" in item:
            item = item.replace("&#39;", "\'")

        if len(item) + 4 > term_width:
            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print("  " + item[:term_width - (4 + space)])
                item = item[term_width - (4 + space):]

        print("  " + item + "\n")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--definition",
        nargs="*",
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
        synonyms(args.synonyms)

    elif args.definition:
        if len(args.definition) > 1:
            args.definition = "_".join(args.definition)
        else:
            args.definition = args.definition[0]
        definition(args.definition)

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()

    except urllib.error.URLError:
        print("Check your internet connection!")
