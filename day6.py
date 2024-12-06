class patrol:
    def __init__(self):
        self.guard_map = self.read_map()
        for row in range(len(self.guard_map)):
            if '^' in self.guard_map[row]:
                self.pos = row, self.guard_map[row].index('^')
        self.dir = 0 # ['up', 'right', 'down', 'left']
        self.max_map = len(self.guard_map) # square map
        self.status = True
        self.steps = 0
    
    def display(self):
        for row in self.guard_map:
            print(row)

    def read_map(self):
        '''read the map'''
        guard_map = []
        with open('input_day6.txt') as f:
            for line in f:
                guard_map.append(list(line.strip()))
        return guard_map

    def next_pos(self):
        if self.dir == 0:
            new_pos = self.pos[0]-1, self.pos[1]
        elif self.dir == 1:
            new_pos = self.pos[0], self.pos[1]+1
        elif self.dir == 2:
            new_pos = self.pos[0]+1, self.pos[1]
        else:
            new_pos = self.pos[0], self.pos[1]-1
        return new_pos

    def forward(self, new_pos):
        self.guard_map[self.pos[0]][self.pos[1]] = 'X'
        self.pos = new_pos
        self.steps += 1
    
    def turn(self):
        self.dir = (self.dir + 1) % 4

    def move(self):
        # check new position
        new_pos = self.next_pos()
        if new_pos[0] > -1 and new_pos[1] > -1 and new_pos[0] < self.max_map and new_pos[1] < self.max_map:
            if self.guard_map[new_pos[0]][new_pos[1]] == '#':
                self.turn()
                self.guard_map[self.pos[0]][self.pos[1]] = f'{self.dir}'
            else:
                self.forward(new_pos)
                self.guard_map[new_pos[0]][new_pos[1]] = f'{self.dir}'
        else:
            self.forward(new_pos)
            self.status = False

patrol_instance = patrol()
while patrol_instance.status:
    patrol_instance.move()

count = 0
for row in patrol_instance.guard_map:
    count += ''.join(row).count('X')

print('challenge 1', count)

###############################

pristine = patrol() # untouched map :3

def add_obs(pos):
    '''add an obstacle at the pos and run the code, return if the guard pathing terminates by exiting the map or not.'''
    flag = False
    patrol_instance = patrol()
    patrol_instance.guard_map[pos[0]][pos[1]] = '#'
    while patrol_instance.status:
        patrol_instance.move()
        if patrol_instance.steps > patrol_instance.max_map**2: # look I'm too lazy to figure out how to determine repeated pathing. I'm sorry.
            flag = True
            break
    return flag

count = 0
for row in range(pristine.max_map):
    for col in range(pristine.max_map):
        if pristine.pos[0] == row and pristine.pos[1] == col: # skip guard's current position
            continue
        if patrol_instance.guard_map[row][col] == 'X': # the guard will not interact with anything not in its path already
            if add_obs((row, col)):
                count += 1

print('challenge 2', count)