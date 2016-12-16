#!/usr/bin/env python3

from tkinter import *

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3


def is_intersection(a, a_min, a_max, b, b_start, b_end) -> bool:
    a_valid = a_min <= a <= a_max
    if b_start < b_end:
        b_valid = b_start < b <= b_end
    else:
        b_valid = b_end <= b < b_start
    return a_valid and b_valid


def first_intersection(inters: list, start_b: int, end_b: int):
    if start_b < end_b:
        return min(inters, key=lambda i: i[0])
    else:
        return max(inters, key=lambda i: i[0])


def find_intersection(a_moves: list, a_pos, start_b: int, end_b: int):
    intersections = list(filter(lambda move: is_intersection(a_pos, move[1],
                                                             move[2], move[0],
                                                             start_b, end_b),
                                a_moves))

    if len(intersections) == 0:
        return None
    elif len(intersections) == 1:
        return a_pos, intersections[0][0]
    else:
        return a_pos, first_intersection(intersections, start_b, end_b)[0]


def draw_line(w, x1, y1, x2, y2):
    w.create_line(2 * x1, 2 * y1, 2 * x2, 2 * y2)


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile, 'r') as f:
        inputtext = f.read()

    if not inputtext:
        print("Invalid input file")
        return

    commands = inputtext.strip().split(', ')

    x = 0
    y = 0
    direction = DIR_NORTH
    xmoves = []
    ymoves = []

    master = Tk()
    w = Canvas(master, width=600, height=600)
    w.pack()
    w.configure(scrollregion=(-300, -300, 300, 300))

    for c in commands:
        if c[0] == 'L':
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4

        distance = int(c[1:])
        intersection = None

        if direction == DIR_NORTH:
            ymoves.append((x, y - distance, y))
            draw_line(w, x, y, x, y - distance)
            intersection = find_intersection(xmoves, x, y, y - distance)
            y -= distance
        elif direction == DIR_WEST:
            xmoves.append((y, x - distance, x))
            draw_line(w, x, y, x - distance, y)
            intersection = find_intersection(ymoves, y, x, x - distance)
            x -= distance
        elif direction == DIR_SOUTH:
            ymoves.append((x, y, y + distance))
            draw_line(w, x, y, x, y + distance)
            intersection = find_intersection(xmoves, x, y, y + distance)
            y += distance
        elif direction == DIR_EAST:
            xmoves.append((y, x, x + distance))
            draw_line(w, x, y, x + distance, y)
            intersection = find_intersection(ymoves, y, x, x + distance)
            x += distance

        if intersection:
            if direction in (DIR_WEST, DIR_EAST):
                intersection = intersection[::-1]
            print("Found intersection at x:{}, y:{}".format(intersection[0],
                                                            intersection[1]))
            print("Distance:", sum(map(abs, intersection)))
            master.mainloop()
            return


main()
