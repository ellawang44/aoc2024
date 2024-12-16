import functools
import numpy as np
from collections import defaultdict

def flatten(xss):
    return [x for xs in xss for x in xs]

@functools.lru_cache(None)
def apply_rule(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        length = len(str(stone))
        return [int(str(stone)[:length//2]), int(str(stone)[length//2:])]
    else:
        return [stone*2024]

with open('data/input_day11.txt') as f:
    stones = [int(i) for i in f.readline().strip().split(' ')]

for _ in range(25):
    stones = flatten([apply_rule(stone) for stone in stones])

print('challenge 1', len(stones))

###############################

# write into dictionary, stone : repeats
current_stones = defaultdict(int)
ss, rr = np.unique(stones, return_counts=True)
for s, r in zip(ss, rr):
    current_stones[s] = r

# iterate
for _ in range(50):
    new_stones = defaultdict(int)
    for current_stone, current_repeat in current_stones.items():
        next_stones = apply_rule(current_stone)
        for s in next_stones:
            new_stones[s] += current_repeat
    current_stones = new_stones

print('challenge 2', np.sum(list(current_stones.values())))