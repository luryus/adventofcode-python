#include <iostream>
#include <list>
#include <map>

int main() {
    int nplayers = 463;
    unsigned long last_marble = 100 *71787;

    std::list<int> ring;
    std::map<int, unsigned long> scores;
    ring.push_back(0);
    int turn = 0;

    auto curr = ring.begin();

    for (unsigned long i = 1; i < last_marble + 1; ++i) {
        if (i % 100000 == 0) std::cout << i << std::endl; 
        if (i % 23 == 0) {
            scores[turn] += i;
            auto rem_pos = curr;
            for (int j = 0; j < 7; j++) {
                if (rem_pos == ring.begin()) rem_pos = ring.end();
                rem_pos--;
            }
            scores[turn] += *rem_pos;
            curr = ring.erase(rem_pos);
        } else {
            auto ins_pos = curr;
            for (int j = 0; j < 2; j++) {
                ins_pos++;
                if (ins_pos == ring.end()) ins_pos = ring.begin();
            }
            curr = ring.insert(ins_pos, i);
        }
        turn = (turn + 1) % nplayers;
    }

    unsigned long max_score = 0;

    for (auto a : scores) {
        if (a.second > max_score) {
            max_score = a.second;
        }
    }

    std::cout << max_score << std::endl;
}
