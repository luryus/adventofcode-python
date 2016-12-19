#!/usr/bin/env python3

from collections import deque

INPUT = 3014603


def main():
    left_queue = deque(n + 1 for n in range(INPUT // 2))
    right_queue = deque(n + 1 for n in range(INPUT // 2, INPUT))
    while len(left_queue) + len(right_queue) > 1:
        right_queue.popleft()
        if len(left_queue) == len(right_queue):
            left_queue.append(right_queue.popleft())
        right_queue.append(left_queue.popleft())

    print(right_queue.pop())


main()
