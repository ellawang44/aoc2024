import numpy as np
from collections import defaultdict

def flatten(xss):
    return [x for xs in xss for x in xs]

class Trail:
    def __init__(self):
        self.topo_map = self.read_map()
        self.max_length = self.topo_map.shape[0] # map is square

    def read_map(self):
        data = []
        with open('data/input_day10.txt') as f:
            for line in f:
                data.append([int(i) for i in line.strip()])
        return np.array(data)

    def get_trailhead(self):
        return list(np.array(np.where(self.topo_map == 0)).T)

    def all_trails(self, trail_head):
        trails = [[trail_head]]
        for _ in range(9):
            new_trails = []
            for trail in trails:
                new_trails.extend(self.make_trail(trail))
            trails = new_trails
        return trails

    def make_trail(self, trail):
        next_pos = self.next_tile(trail[-1], len(trail)-1)
        trails = []
        for pos in next_pos:
            new_trail = trail[:]
            new_trail.append(pos)
            trails.append(new_trail)
        return trails

    def get_trail(self, head_pos):
        paths = {}
        height_dict = defaultdict(list)
        height = 0
        curr_pos = [head_pos]
        while height < 10:
            next_pos = [self.next_tile(pos, height) for pos in curr_pos]
            for pos, n_pos in zip(curr_pos, next_pos):
                paths[(pos[0], pos[1])] = n_pos
            flatten_pos = flatten(next_pos)
            height_dict[height].extend(flatten_pos)
            height_dict[height] = list(set(height_dict[height])) # remove duplicates
            curr_pos = flatten_pos
            height += 1
        return height_dict, paths

    def next_tile(self, curr_pos, curr_height):
        new_poss = []
        # up
        new_pos_up = (curr_pos[0], curr_pos[1]-1)
        if self.criteria(new_pos_up, curr_height+1):
            new_poss.append(new_pos_up)
        # down
        new_pos_down = (curr_pos[0], curr_pos[1]+1)
        if self.criteria(new_pos_down, curr_height+1):
            new_poss.append(new_pos_down)
        # left
        new_pos_left = (curr_pos[0]-1, curr_pos[1])
        if self.criteria(new_pos_left, curr_height+1):
            new_poss.append(new_pos_left)
        # right
        new_pos_right = (curr_pos[0]+1, curr_pos[1])
        if self.criteria(new_pos_right, curr_height+1):
            new_poss.append(new_pos_right)
        return new_poss

    def criteria(self, pos, height):
        if not self.out_of_bounds(pos) and self.topo_map[pos[0], pos[1]] == height:
            return True
        else:
            return False

    def out_of_bounds(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.max_length-1 or pos[1] > self.max_length-1:
            return True
        else:
            return False

trail = Trail()
trailheads = trail.get_trailhead()
tot = 0
for head in trailheads:
    height_dict, paths = trail.get_trail(head)
    tot += len(height_dict[8])

print('challenge 1', tot)

########################
tot = 0
for head in trailheads:
    trails = trail.all_trails(head)
    tot += len(trails)

print('challenge 2', tot)
