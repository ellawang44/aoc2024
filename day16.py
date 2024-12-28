import re
import numpy as np
import heapq


class TrailBase:
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

    def cost(self, dir, pos1, pos2):
        new_dir = self.get_dir(pos1, pos2)
        if dir == new_dir:
            return 1
        elif dir in ['E', 'W'] and new_dir in ['E', 'W']:
            return 2001
        elif dir in ['N', 'S'] and new_dir in ['N', 'S']:
            return 2001
        else:
            return 1001

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


trail = TrailBase()
# only works if maze is small enough
if trail.max_length < 20:
    trails = trail.all_trails()
    min_score = np.inf
    for t in trails:
        new_score = trail.score(t)
        if new_score < min_score:
            min_score = new_score
    print('brute force', min_score)


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

    def next_tile(self, curr_pos):
        new_poss = []
        # up
        new_pos_up = (curr_pos[0], curr_pos[1]-1)
        if self.legal_move(new_pos_up):
            new_poss.append(('W', new_pos_up))
        # down
        new_pos_down = (curr_pos[0], curr_pos[1]+1)
        if self.legal_move(new_pos_down):
            new_poss.append(('E', new_pos_down))
        # left
        new_pos_left = (curr_pos[0]-1, curr_pos[1])
        if self.legal_move(new_pos_left):
            new_poss.append(('N', new_pos_left))
        # right
        new_pos_right = (curr_pos[0]+1, curr_pos[1])
        if self.legal_move(new_pos_right):
            new_poss.append(('S', new_pos_right))
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

    def cost(self, dir, new_dir, pos1, pos2):
        if dir == new_dir:
            return 1
        elif dir in ['E', 'W'] and new_dir in ['E', 'W']:
            return 2001
        elif dir in ['N', 'S'] and new_dir in ['N', 'S']:
            return 2001
        else:
            return 1001

    def dij(self, heap):
        heapq.heapify(heap)
        current_cost, dir, pos = heapq.heappop(heap)
        seen = {pos}
        while pos != self.end:
            #print(current_cost, dir, pos)
            # add
            next_pos = self.next_tile(pos)
            for n_dir, n_pos in next_pos:
                n_cost = self.cost(dir, n_dir, pos, n_pos)
                # skip seen
                if n_pos not in seen:
                    heapq.heappush(heap, (n_cost+current_cost, n_dir, n_pos))
            #print(heap)
            # next point
            current_cost, dir, pos = heapq.heappop(heap)
            seen.add(pos)
            #if current_cost > 3000:
            #    break
        return current_cost

    def sit(self, target):
        cost_table = {}
        heap = [(0, 'E', [self.start])]
        heapq.heapify(heap)
        paths = set()
        while len(heap) > 0:
            # next point to investigate
            current_cost, dir, path = heapq.heappop(heap)
            pos = path[-1]
            cost_table[pos, dir] = current_cost
            # end
            if pos == self.end:
                paths.update(path)
                continue
            # add
            next_pos = self.next_tile(pos)
            for n_dir, n_pos in next_pos:
                # loop
                if n_pos in path:
                    continue
                n_cost = self.cost(dir, n_dir, pos, n_pos)+current_cost
                # cost too high
                if n_cost > target:
                    continue
                # cost table
                if (n_pos, n_dir) in cost_table and cost_table[n_pos, n_dir] < n_cost:
                    #print(path, n_pos, n_cost, cost_table[n_pos])
                    continue
                heapq.heappush(heap, (n_cost, n_dir, [*path, n_pos]))
            #print(heap)
            #if current_cost > 3000:
            #    break
        return len(paths)


trail = Trail()
best_score = trail.dij([(0, 'E', trail.start)])
print('challenge 1', best_score)
num_tile = trail.sit(best_score)
print('challenge 2', num_tile)