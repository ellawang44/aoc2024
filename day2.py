import numpy as np

# challenge 1
safe = 0
with open('data/input_day2.txt') as f:
    for line in f:
        line = np.int64(line.strip().split(' '))
        diff = line[1:] - line[:-1]
        if not ((diff > 0).all() or (diff < 0).all()): # monotonic
            continue
        elif not (np.abs(diff) < 4).all(): # jump
            continue
        else:
            safe += 1

print('challenge 1', safe)

# challenge 2
def safe(level):
    '''level is safe'''
    diff = level[1:] - level[:-1]
    if not ((diff > 0).all() or (diff < 0).all()): # monotonic
        return False
    elif not (np.abs(diff) < 4).all(): # jump
        return False
    else:
        return True

def tol_safe(level):
    '''safe allowing 1 level to be removed'''
    for i in range(len(level)):
        if safe(np.array([*level[:i], *level[i+1:]])):
            return True
    return False

num = 0
with open('data/input_day2.txt') as f:
    for line in f:
        line = np.int64(line.strip().split(' '))
        if safe(line):
            num += 1
        elif tol_safe(line):
            num += 1
        else:
            continue

print('challenge 2', num)