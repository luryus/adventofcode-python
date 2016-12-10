#!/usr/bin/env python3

import sys, re
from collections import deque

HILO_REGEX = re.compile(r"bot (\d+) gives low to " +
                        r"((?:bot|output) \d+) and high to " +
                        r"((?:bot|output) \d+)")
VAL_REGEX = re.compile(r"value (\d+) goes to bot (\d+)")


def add_bot(graph: dict, bot_id: int, low_id: str, hi_id: str):
    graph[bot_id] = ([], low_id, hi_id)


def main():
    bot_graph = {}
    outputs = {}
    initial_values = []

    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            m = HILO_REGEX.match(line)
            if m:
                add_bot(bot_graph, int(m.group(1)),
                        m.group(2), m.group(3))
            m = VAL_REGEX.match(line)
            if m:
                initial_values.append((int(m.group(2)), int(m.group(1))))

    for val in initial_values:
        bot_graph[val[0]][0].append(val[1])

    while True:
        two_val_bots = [(bot_id, bot) for bot_id, bot in bot_graph.items()
                                      if len(bot[0]) == 2]

        if not two_val_bots:
            break;

        for bot_id, bot in two_val_bots:
            lo_val, hi_val = min(bot[0]), max(bot[0])
            if lo_val == 17 and hi_val == 61:
                print("Bot comparing 17 and 61:", bot_id)
            bot[0].clear()
            if bot[1].startswith("bot"):
                bot_graph[int(bot[1][4:])][0].append(lo_val)
            else:
                outputs[int(bot[1][7:])] = lo_val

            if bot[2].startswith("bot"):
                bot_graph[int(bot[2][4:])][0].append(hi_val)
            else:
                outputs[int(bot[2][7:])] = hi_val

    print("Outputs 0*1*2:", outputs[0] * outputs[1] * outputs[2])


main()
