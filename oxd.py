#!/usr/bin/env python

import argparse
import subprocess
import urllib.error
import urllib.request


def definition(word):
    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    if term_width > 80:
        term_width = 80

    if term_width < 28:
        print("Terminal width less than 28 is not supported")
        quit()

    if len(word) > 1:
        word = "_".join(word)
    else:
        word = word[0]
        if "-" in word:
            word = word.replace("-", "_")

    link = "https://en.oxforddictionaries.com/definition/us/{}".format(word)

    try:
        site = urllib.request.urlopen(link).read().decode("utf-8")
    except urllib.error.URLError:
        print("\n  Check your internet connection!\n")
        quit()

    results = []
    pronunciations = []
    origin = ""

    if "No exact matches found" in site:
        try:
            word = word[len(word) - word[::-1].index("_"):] + ",_" + \
                word[:len(word) - word[::-1].index("_") - 1]
        except ValueError:
            print("\n  No matches found.\n")
            quit()

        link = \
            "https://en.oxforddictionaries.com/definition/us/{}".format(word)
        site = urllib.request.urlopen(link).read().decode("utf-8")

        if "No exact matches found" in site:
            print("\n  No matches found.\n")
            quit()

    if link not in site:
        start = site.index("definition of ") + 14
        end = start + site[start:].index(" in")
        word = site[start:end]

    if "_" in word:
        word = word.replace("_", " ")

    if "&#39;" in word:
        word = word.replace("&#39;", "'")

    print("\n  DEFINITION OF {}:\n".format(word.upper()))

    for i in range(len(site)):
        if site[i:i + 16] == "class=\"ex\"> <em>":
            results.append("-EX-{}".format(
                site[i + 16:i + 16 + site[i + 16:].index("<")]))

        if site[i:i + 12] == "class=\"pos\">":
            results.append("-P-{}".format(
                site[i + 12:i + 12 + site[i + 12:].index("<")]))

        if site[i:i + 18] == "class=\"iteration\">":
            results.append("-I-{}".format(
                site[i + 18:i + 18 + site[i + 18:].index("<")]))

        if site[i:i + 26] == "class=\"subsenseIteration\">":
            results.append("-SI-{}".format(
                site[i + 26:i + 26 + site[i + 26:].index("<")]))

        if site[i:i + 12] == "class=\"ind\">":
            results.append(
                "-D-" + site[i + 12:i + 12 + site[i + 12:].index("<")])

        if site[i:i + 22] == "class=\"derivative_of\">" \
           and site[i + 22] != "<":
            results.append(
                "-DO-" + site[i + 22:i + 22 + site[i + 22:].index("<")] +
                site[i + 22 + site[i + 22:].index(">") + 1:i + 22 +
                     site[i + 22:].index(">") + 1 + site[i
                     + 22 + site[i + 22:].index(">") + 1:].index("<")])

        if site[i:i + 23] == "class=\"crossReference\">" \
           and site[i + 23] != "<":
            results.append(
                "-CR-" + site[i + 23:i + 23 + site[i + 23:].index("<")] +
                site[i + 23 + site[i + 23:].index(">") + 1:i + 23 +
                     site[i + 23:].index(">") + 1 + site[i
                     + 23 + site[i + 23:].index(">") + 1:].index("<")])

        if site[i:i + 15] == "class=\"phrase\">":
            break

    for j in range(len(site), 0, -1):
        if site[j:j + 25] == "class=\"phoneticspelling\">":
            pronunciations.append(site[j + 25:j + 25
                                  + site[j + 25:].index("<")])

        if site[j:j + 8] == ">Origin<":
            origin = site[j + site[j:].index("<p>") + 3:
                          j + site[j:].index("</p>")]
            break

    if len(results) > 1:
        results = [
            results[i] for i in range(len(results))
            if results[i] not in "-EX-P-I-SI-D-DO-"
            and not (results[i][:4] == "-EX-"
                     and results[i - 1][:4] == "-EX-")]

    last_spaces = 0
    position = 0

    for item in results:
        prepend_symbol = "|"
        spaces = 1

        if position > 0:
            last = results[position - 1]

            if "&lsquo;" in item and "&lsquo;" in last:
                position += 1
                continue
        else:
            last = ""

        if position > 1:
            second_last = results[position - 2]
        else:
            second_last = ""

        if position > 2:
            third_last = results[position - 3]
        else:
            third_last = ""

        if position < len(results) - 1:
            first_next = results[position + 1]
        else:
            first_next = ""

        if position < len(results) - 2:
            second_next = results[position + 2]
        else:
            second_next = ""

        if item[:4] == "-EX-":
            if position + 1 < len(results) - 1:
                if last[:4] == "-CR-" \
                        and first_next[:4] == "-SI-":
                    position += 1
                    continue

            item = item.replace("&lsquo;", "'")
            item = item.replace("&rsquo;", "'")

            if second_last[:3] != "-I-" and second_last[:4] != "-SI-":
                item = " " + item[4:]
            else:
                item = "  " + item[4:]

        if item[:3] == "-P-":
            print("  {}\n".format(item[3:].upper()))
            position += 1
            continue

        if item[:3] == "-I-":
            position += 1
            continue

        if item[:4] == "-SI-":
            position += 1
            continue

        if last[:3] == "-I-":
            if item[:4] == "-CR-":
                item = item[4:]

            item = last[3:] + "  " + item

        if last[:4] == "-SI-":
            if item[:4] == "-CR-":
                item = item[4:]

            prepend_symbol = "+"
            item = last[4:] + "  " + item
            spaces += len(last[4:])

        if second_last[:3] == "-I-":
            if last[:4] == "-CR-":
                item = "   " + item
            else:
                spaces += len(second_last[3:]) + 1

        if second_last[:4] == "-SI-":
            if last[:4] == "-CR-":
                item = " " * (len(second_last[4:]) + 4) + item

            spaces += len(second_last[4:]) + 4

        if third_last[:4] == "-SI-" and last[:4] == "-SI-" \
           and first_next[:4] != "-SI-" and first_next[:3] != "-I-" \
           and second_next[:3] != "-P-" and second_next[:3] != "-I-" \
           and position < len(results) - 2:
            spaces -= 5

        if last[:4] == "-SI-":
            if third_last[:3] == "-I-" or len(last[4:]) > 3:
                spaces -= 1

        if position + 1 <= len(results) - 2 \
           and third_last[:4] == "-SI-" \
           and second_next[:4] == "-SI-" \
           and last[:3] != "-I-":
            spaces += len(third_last[:4]) + 1

        if item[:4] == "-CR-":
            if len(results) > 1 and item != results[-2]:
                if last[:3] == "-D-":
                    if second_last[:3] == "-I-":
                        spaces += len(second_last[3:]) + 1
                    elif second_last[:4] == "-SI-":
                        spaces += len(second_last[4:]) - 1
                    else:
                        spaces += 1
                elif position < len(results) - 2 \
                        and (first_next[:4] == "-SI-"
                             or second_next[:4] == "-SI-"):
                    spaces += 4
                elif position != 0 and last[:3] != "-P-":
                    spaces += 2
            elif len(results) > 1 and position == len(results) - 2:
                if last[:4] == "-EX-" and second_last[:3] == "-D-":
                    if third_last[:3] == "-I-":
                        spaces += len(third_last[3:]) + 3
                    if third_last[:3] == "-P-":
                        spaces += 1
                elif last[:3] == "-D-" and second_last[:3] == "-P-":
                    spaces += 1
            else:
                spaces += 1

            item = item[4:]

        if (item[spaces] == "'" or item.count("'") >= 2) and item[-1] == "'":
            if last[:4] == "-CR-":
                if second_last[:4] == "-EX-":
                    if second_last[:3] == "-P-" and second_last == results[-3]:
                        spaces = last_spaces - 1
                    else:
                        spaces = last_spaces - 2
                elif second_last[:4] == "-SI-":
                    if results[position] == results[-1]:
                        spaces = len(second_last[4:]) - last_spaces + 1
                    else:
                        spaces = len(second_last[4:]) - last_spaces + 2
                elif first_next[:3] == "-P-":
                    spaces = last_spaces - 1
                elif second_last[:3] == "-D-" and third_last[:3] == "-P-":
                    spaces -= 1
                elif position != len(results) - 1:
                    spaces = last_spaces - 3

            if second_last[:3] == "-D-" and third_last[:3] != "-I-":
                spaces = last_spaces - 1

            if last[:3] == "-I-" or last[:4] == "-SI-":
                item = item[:item.index("'") - 1] + item[item.index("'"):]

        if last[:4] == "-CR-" and last == results[-2]:
            if third_last[:4] == "-SI-":
                if item.count("'") < 2 and second_last[:3] != "-D-":
                    spaces += 2
            elif second_last[:3] != "-P-" and third_last[:3] != "-P-":
                spaces += 1

        if last[:4] == "-EX-" and second_last[:3] == "-P-":
            spaces -= 1

        item = " " * spaces + item
        last_spaces = spaces

        if last[:3] == "-P-":
            if item.count("'") >= 2 and item[-1] == "'":
                item = prepend_symbol + item[1:]
            elif results[position][:4] == "-CR-" \
                    and position != len(results) - 1:
                item = prepend_symbol + item

        if position == 0 and results[position][:4] == "-CR-":
            item = prepend_symbol + item

        if item[spaces:spaces + 4] == "-CR-":
            if second_last[:4] == "-SI-":
                item = "  " + item[:spaces] + item[spaces + 4:]
            elif "|" not in item:
                item = prepend_symbol + item[:spaces] + item[spaces + 4:]

        if item[spaces:spaces + 4] == "-DO-":
            item = prepend_symbol + " " + item[1:].replace("-DO-", "")

        if last[:3] == "-I-" or last[:4] == "-SI-":
            item = prepend_symbol + item

        if last[:3] == "-P-":
            if item[spaces:] in results[-1]:
                if item[spaces:spaces + 3] == "-D-":
                    item = prepend_symbol + "  " + item[spaces + 3:]
                elif "|" not in item:
                    item = prepend_symbol + item[2:]

            if position + 1 < len(results) \
               and results[position + 1][:3] == "-P-":
                if item[spaces:spaces + 3] == "-D-":
                    item = prepend_symbol + "   " + item[spaces + 3:]

            if position + 1 <= len(results) - 1 \
               and first_next[:3] == "-P-":
                item = prepend_symbol + item[3:]

        if (last[:4] == "-EX-" and second_last[:3] == "-D-"
                and results.index(last) < len(results) - 3
                and results[results.index(last) + 3][:4] != "-SI-"
                or len(results) == 1) and "-D-" not in item:
            item = prepend_symbol + item[2:]

        if item[3:] in results[-1] and "See" not in item and last[:3] == "-P-":
            if results[position][:3] == "-D-" and position != 1:
                item = item[:1] + " " + item[2:]

            if position == 1:
                if len(results) == 2:
                    item = prepend_symbol + item[2:]
                else:
                    item = prepend_symbol + item[4:]
            else:
                item = prepend_symbol + item[2:]

        if "-D-" in item:
            if last[:3] != "-I-" and last[:4] != "-SI-":
                item = prepend_symbol + " " + item[spaces + 3:]
            else:
                if third_last[:3] == "-I-" and last[:4] == "-SI-":
                    item = item[0] + " " + item[1:item.index("-D-")] \
                        + item[item.index("-D-") + 3:]
                else:
                    item = item[:item.index("-D-")] \
                        + item[item.index("-D-") + 3:]

        if "&#39;" in item:
            item = item.replace("&#39;", "'")

        if len(item) + 4 > term_width:
            if second_last[:3] == "-I-":
                if last[:4] == "-CR-":
                    if first_next[:3] == "-I-":
                        spaces += len(second_last[3:]) + 5
                    if first_next[:3] == "-P-":
                        spaces += len(second_last[3:]) + 3
                else:
                    spaces += 1

            if second_last[:4] == "-SI-":
                if last[:4] == "-CR-":
                    spaces += len(second_last[4:]) + 5
                else:
                    spaces += 1

            if third_last[:3] == "-I-" and last[:4] == "-SI-":
                spaces += 1

            if last[:3] == "-I-":
                spaces += len(last[3:]) + 3

            if last[:4] == "-SI-":
                spaces += len(last[4:]) + 3

            if item[spaces + 1] != "'" and item[-1] != "'":
                if last[:3] != "-I-" and last[:4] != "-SI-":
                    spaces += 1
            else:
                spaces += 2

            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print(item[:term_width - (4 + space)])
                item = " " * spaces + item[term_width - (4 + space):]

        print(item + "\n")
        position += 1

    if len(origin) > 0:
        origin = "  " + origin
        print("  ORIGIN\n")

        if len(origin) + 4 > term_width:
            while len(origin) + 4 >= term_width:
                space = origin[:term_width - 4][::-1].index(" ")
                print(origin[:term_width - (4 + space)])
                origin = "  " + origin[term_width - (4 + space):]

        print(origin + "\n")

    if len(pronunciations) > 0:
        if len(pronunciations) > 1:
            pronunciations = ", ".join(set(pronunciations))
        else:
            pronunciations = pronunciations[0]

        print("  PRONUNCIATION\n")
        print("  " + pronunciations + "\n")


def synonyms(word):
    term_width = int(
        subprocess.check_output(['stty', 'size']).decode().split()[1])

    if term_width > 80:
        term_width = 80

    if term_width < 28:
        print("Terminal width less than 28 is not supported")
        quit()

    if len(word) > 1:
        word = "_".join(word)
    else:
        word = word[0]
        if "-" in word:
            word = word.replace("-", "_")

    link = "https://en.oxforddictionaries.com/thesaurus/{}".format(word)

    try:
        site = urllib.request.urlopen(link).read().decode("utf-8")
    except urllib.error.URLError:
        print("\n  Check your internet connection!\n")
        quit()

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

        if "&#39;" in word:
            word = word.replace("&#39;", "'")

        print("\n  SYNONYMS OF {}:\n".format(word.upper()))

        for i in range(len(site)):
            if site[i:i + 12] == "class=\"syn\">":
                results += \
                    site[i + 12:i + 12 + site[i + 12:].index("<")].split(", ")

    results = [item for item in results if len(item) > 0]
    results = [", ".join(results)]

    for item in results:
        if "&#39;" in item:
            item = item.replace("&#39;", "'")

        if len(item) + 4 > term_width:
            while len(item) + 4 >= term_width:
                space = item[:term_width - 4][::-1].index(" ")
                print("  " + item[:term_width - (4 + space)])
                item = item[term_width - (4 + space):]

        print("  " + item + "\n")


def main():
    parser = argparse.ArgumentParser(
        prog="oxd",
        description="oxd is a CLI for the Oxford Dictionaries website.",
        usage="%(prog)s [option] WORD(S)"
    )
    parser.add_argument(
        "-d",
        "--definition",
        nargs="+",
        help="show definition(s)",
        metavar="WORD(S)"
    )
    parser.add_argument(
        "-s",
        "--synonyms",
        nargs="+",
        help="show synonyms",
        metavar="WORD(S)"
    )
    args = parser.parse_args()

    if args.synonyms:
        synonyms(args.synonyms)
    elif args.definition:
        definition(args.definition)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
