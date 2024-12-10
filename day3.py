def parse(line):
    count = 0
    mul_chunk = get_mul(line)
    for chunk in mul_chunk:
        num1, num2 = parse_chunk(chunk)
        count += num1*num2
    return count

def get_mul(line):
    '''split out chunks of mul'''
    return line.split('mul')

def parse_chunk(chunk):
    '''remove wrong stuff, return the numbers'''
    if chunk[0] != '(': # start with (
        return 0, 0
    if ')' not in chunk: # needs to end with )
        return 0, 0
    if ',' not in chunk: # needs comma somewhere
        return 0, 0

    blobs = chunk[1:].split(',')
    # check first number
    num1 = blobs[0]
    if not num1.isdigit(): # needs to be all digits
        return 0, 0
    if len(num1) > 3: # needs to be less than 3 digits
        return 0, 0
    # check second number
    num2 = blobs[1].split(')')[0]
    if not num2.isdigit(): # needs to be all digits
        return 0, 0
    if len(num2) > 3: # needs to be less than 3 digits
        return 0, 0
    return int(num1), int(num2)

def read_chunk(chunk):
    blobs = chunk.split(',')
    blobs[0].isdigit()

with open('data/input_day3.txt') as f:
    stuff = ''
    for line in f:
        stuff = stuff + line
    count = parse(stuff)

print('challenge 1', count)

##########################

def dodont(line):
    '''cut the string where there is a don't'''
    dos = line.split('do()')
    # for each do chunk, if you find a don't, remove the rest of the string
    new_line = ''
    for do in dos:
        valid = do.split("don't()")
        new_line = new_line + valid[0]
    return new_line

with open('data/input_day3.txt') as f:
    stuff = ''
    for line in f:
        stuff = stuff + line
    count = parse(dodont(stuff))

print('challenge 2', count)