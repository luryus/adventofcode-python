#!/usr/bin/env python3


def main(part2: bool):
    discs = [
        (13, 10),
        (17, 15),
        (19, 17),
        (7, 1),
        (5, 0),
        (3, 1)
    ]

    if part2:
        discs.append((11, 0))

    t = 0
    while True:
        all_valid = True
        for i in range(len(discs)):
            if (discs[i][1] + t + i + 1) % discs[i][0] != 0:
                all_valid = False
                break

        if all_valid:
            break
        t += 1

    print("Discs aligned first at t =", t)


main(False)
main(True)
