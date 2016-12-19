#!/usr/bin/env python3

INPUT = 3014603


def main():
    elves = [n + 1 for n in range(INPUT)]
    while len(elves) > 1:
        odd_elves = len(elves) % 2 != 0
        elves = [elves[i] for i in range(len(elves)) if (i + 1) % 2 != 0]
        if odd_elves:
            elves = elves[1:]

    print(elves[0])


main()
