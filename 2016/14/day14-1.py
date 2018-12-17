#!/usr/bin/env python3

import re
from hashlib import md5


SALT = "zpqevtbw"
REPEAT3_REGEX = re.compile(r"(.)\1\1")
REPEAT5_REGEX = re.compile(r"(.)\1{4}")


def main():
    ready_hashes = []
    testing_hashes = []
    counter = 0

    while len(ready_hashes) < 64:
        to_hash = (SALT + str(counter)).encode()
        hashed = md5(to_hash).hexdigest()
        m3 = REPEAT3_REGEX.search(hashed)
        if m3:
            testing_hashes.append((counter, m3.group(1), hashed))
        m5 = REPEAT5_REGEX.finditer(hashed)
        for m in m5:
            rep_chr = m.group(1)
            for hash3 in testing_hashes:
                if (hash3[0] < counter <= hash3[0] + 1000
                        and hash3[1] == rep_chr):
                    ready_hashes.append(hash3)
                    if len(ready_hashes) == 64:
                        break
            testing_hashes = [h for h in testing_hashes
                              if (h not in ready_hashes
                                  or counter > h[0] + 1000)]

        counter += 1

    print('64th hash counter', ready_hashes[-1][0])


main()
