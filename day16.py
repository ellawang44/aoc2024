import numpy as np
from collections import defaultdict

class Trail:
    def __init__(self):
        self.maze = self.read_maze()
        self.max_length = self.maze.shape[0] # map is square
        start = np.where(self.maze == 'S')
        self.start = start[0][0], start[1][0]
        end = np.where(self.maze == 'E')
        self.end = end[0][0], end[1][0]

    def read_maze(self):
        data = []
        with open('data/input_day16.txt') as f:
            for line in f:
                data.append([i for i in line.strip()])
        return np.array(data)

    def all_trails(self):
        end = []
        trails = [[self.start]]
        while len(trails) != 0:
            new_trails = []
            for trail in trails:
                extend_trail = self.make_trail(trail)
                for t in extend_trail:
                    if t[-1] == self.end:
                        end.append(t)
                    else:
                        new_trails.append(t)
            trails = new_trails
        return end

    def make_trail(self, trail):
        next_pos = self.next_tile(trail[-1])
        trails = []
        for pos in next_pos:
            if pos not in trail:
                new_trail = trail[:]
                new_trail.append(pos)
                trails.append(new_trail)
        return trails

    def next_tile(self, curr_pos):
        new_poss = []
        # up
        new_pos_up = (curr_pos[0], curr_pos[1]-1)
        if self.legal_move(new_pos_up):
            new_poss.append(new_pos_up)
        # down
        new_pos_down = (curr_pos[0], curr_pos[1]+1)
        if self.legal_move(new_pos_down):
            new_poss.append(new_pos_down)
        # left
        new_pos_left = (curr_pos[0]-1, curr_pos[1])
        if self.legal_move(new_pos_left):
            new_poss.append(new_pos_left)
        # right
        new_pos_right = (curr_pos[0]+1, curr_pos[1])
        if self.legal_move(new_pos_right):
            new_poss.append(new_pos_right)
        return new_poss

    def legal_move(self, pos):
        if not self.out_of_bounds(pos) and self.maze[pos[0], pos[1]] != '#':
            return True
        else:
            return False

    def out_of_bounds(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.max_length-1 or pos[1] > self.max_length-1:
            return True
        else:
            return False

    def score(self, trail):
        debug = 'E'
        dir = 'E'
        tot = 0
        for t1, t2 in zip(trail[:-1], trail[1:]):
            next_dir = self.get_dir(t1, t2)
            debug = debug + next_dir
            if dir == next_dir:
                tot += 1
            elif dir == 'E' and next_dir == 'W':
                tot += 2001
            else:
                tot += 1001
            dir = next_dir
        #print(tot, debug)
        return tot

    def get_dir(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            return 'E'
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
            return 'W'
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
            return 'S'
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            return 'N'

trail = Trail()
trails = trail.all_trails()
min_score = np.inf
for t in trails:
    new_score = trail.score(t)
    if new_score < min_score:
        min_score = new_score
print('challenge 1', min_score)