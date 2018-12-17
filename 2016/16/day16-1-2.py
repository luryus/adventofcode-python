#!/usr/bin/env python3

INPUT = list(map(int, "01111001100111011"))
DISK_LEN_P1 = 272
DISK_LEN_P2 = 35651584


def main(disk_len: int):
    data = INPUT

    while len(data) < disk_len:
        new_data = data[::-1]
        new_data = [1 if a == 0 else 0 for a in new_data]
        data += [0] + new_data

    checksum = list(data[:disk_len])
    while len(checksum) % 2 == 0:
        new_cs = []
        for pair in zip(checksum[::2], checksum[1::2]):
            new_cs.append(1 if pair[0] == pair[1] else 0)
        checksum = new_cs

    print('Checksum:', ''.join(map(str, checksum)))


print('Part 1:', end=" ")
main(DISK_LEN_P1)
print('Part 2:', end=" ")
main(DISK_LEN_P2)
