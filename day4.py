import numpy as np

data = []
with open('input_day4.txt') as f:
    for line in f:
        data.append(list(line.strip()))
data = np.array(data)

def xmas_in_line(line):
    forward = ''.join(line)
    reverse = ''.join(line[::-1])
    return forward.count('XMAS') + reverse.count('XMAS')

def horizontal_max(data):
    tot = 0
    for line in data:
        tot += xmas_in_line(line)
    return tot

def get_diag(data):
    '''shift the rows around and pad with 0s to align diags'''
    l = data.shape[0]-1 # it is square
    arr = np.array(['0']*l)
    # pad with 0s
    new1 = []
    for ind, row in enumerate(data):
        new1.append([*arr[ind:], *row, *arr[:ind]])
    new1 = np.array(new1)
    # pad with 0s the other way
    new2 = []
    for ind, row in enumerate(data):
        new2.append([*arr[:ind], *row, *arr[ind:]])
    new2 = np.array(new2)
    return horizontal_max(new1.T) + horizontal_max(new2.T)

print('challenge 1', horizontal_max(data) + horizontal_max(data.T) + get_diag(data))

############################

def is_X(data, row, col):
    l = data.shape[0]
    if row == 0 or col == 0:
        return False
    if row == l-1 or col == l-1:
        return False
    d1 = [data[row-1][col-1], data[row+1][col+1]]
    d2 = [data[row-1][col+1], data[row+1][col-1]]
    if 'M' in d1 and 'S' in d1 and 'M' in d2 and 'S' in d2:
        return True
    return False

def cross_mas(data):
    l = data.shape[0] # it is square
    count = 0
    for row in range(l):
        for col in range(l):
            if data[row][col] == 'A' and is_X(data, row, col):
                count += 1
    return count

print('challenge 2', cross_mas(data))