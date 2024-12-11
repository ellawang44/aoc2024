def flatten(xss):
    return [x for xs in xss for x in xs]

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

for _ in range(50):
    stones = flatten([apply_rule(stone) for stone in stones])

print('challenge 2', len(stones))