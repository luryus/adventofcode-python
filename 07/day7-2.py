#!/usr/bin/env python3

import sys, re


ABA_REGEX = re.compile(r"(?!(?:\w*\]))(?=(\w)(?!\1)(\w)\1)")


def matching_bab(line: str, m) -> bool:
    pattern = r"\[\w*?" + "{1}{0}{1}".format(m[0], m[1]) + r"\w*?\]"
    rex = re.compile(pattern)
    return rex.search(line) is not None


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        aba_line_matches = ((line, ABA_REGEX.findall(line)) for line in f)
        bab_found = (line for (line, matches) in aba_line_matches
                     if any((True for m in matches if matching_bab(line, m))))
        print("Count", sum(1 for b in bab_found))



main()
