#include <iostream>

int main() {
    long a = 1, b = 0, c = 0, d = 0, e = 0, f = 0;

    goto csd;
begin:
    b = 1;
begin2:
    d = 1;

    if (f % b == 0 && f/b >= d) {
        a += b;
    }
    d = f + 1;

    b++;
    c = (b > f);
    if (b > f) goto out;
    else goto begin2;

csd: 
    f += 2;
    f = 11*19*f*f;
    c = 6 + (c+1)*22;
    f += c;
    if (a == 0) goto begin;
    switch (a) {
        case 1: c = 27;
        case 2: c *= 28;
        case 3: c += 29;
        case 4: c *= 30;
        case 5: c *= 14;
        case 6: c *= 32;
        case 7: f += c;
        case 8: a = 0;
        case 9: goto begin;
    }

out: 
    std::cout << a << " " << b << " "
        << c << " "<< d << " "
        << e << " " << f << std::endl;
}