import numpy as np

class Fence:
    def __init__(self):
        self.read_plot()

    def read_plot(self):
        soil = []
        with open('data/input_day12.txt') as f:
            for line in f:
                soil.append([i for i in line.strip()])
        self.garden = np.array(soil)
        self.max_length = self.garden.shape[0] # square

    def out_of_bounds(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.max_length-1 or pos[1] > self.max_length-1:
            return True
        else:
            return False

    def get_region(self, pos):
        return self.garden[pos[0], pos[1]]

    def get_surrounding(self, pos):
        return [self.move(pos, dir) for dir in ['down', 'left', 'up', 'right']]

    def fence(self, pos, region):
        if self.out_of_bounds(pos):
            return 1
        elif self.get_region(pos) != region:
            return 1
        else:
            return 0

    def find_region(self, region, in_region, to_explore):
        if len(to_explore) == 0:
            return in_region
        else:
            # explore one position
            pos = min(to_explore)
            if self.get_region(pos) == region:
                in_region.add(pos)
                # add to explore list
                for new_pos in self.get_surrounding(pos):
                    if not self.out_of_bounds(new_pos) and new_pos not in in_region:
                        to_explore.add(new_pos)
            to_explore.remove(pos)
            in_region = self.find_region(region, in_region, to_explore)
        return in_region

    def get_patches(self):
        traversed = []
        patches = []
        for row in range(self.max_length):
            for col in range(self.max_length):
                pos = (row, col)
                if pos not in traversed:
                    region = self.get_region(pos)
                    patch = self.find_region(region, {pos}, set([p for p in self.get_surrounding(pos) if not self.out_of_bounds(p)]))
                    traversed.extend(patch)
                    patches.append(patch)
        return patches

    def area(self, patch):
        return len(patch)

    def perimeter_one(self, pos, region):
        return sum([self.fence(pos, region) for pos in self.get_surrounding(pos)])

    def perimeter(self, patch):
        pos = min(patch)
        region = self.get_region(pos)
        tot = 0
        for pos in patch:
            tot += self.perimeter_one(pos, region)
        return tot

    def move(self, pos, direction):
        if direction == 'up':
            return (pos[0]-1, pos[1])
        elif direction == 'down':
            return (pos[0]+1, pos[1])
        elif direction == 'left':
            return (pos[0], pos[1]-1)
        else:
            return (pos[0], pos[1]+1)

    def convex(self, pos, region):
        verticies = 0
        fences = [self.fence(self.move(pos, 'up'), region), self.fence(self.move(pos, 'right'), region), self.fence(self.move(pos, 'down'), region), self.fence(self.move(pos, 'left'), region)]
        for f1, f2 in zip(fences[:-1], fences[1:]):
            if f1+f2 == 2:
                verticies += 1
        if fences[0] + fences[-1] == 2:
            verticies += 1
        return verticies

    def concave(self, pos, region):
        verticies = 0
        for dir1, dir2 in [['up', 'left'], ['left', 'down'], ['down', 'right'], ['right', 'up']]:
            # check in bounds
            pos1 = self.move(pos, dir1)
            pos2 = self.move(pos, dir2)
            if not self.out_of_bounds(pos1) and not self.out_of_bounds(pos2):
                diag = self.move(pos1, dir2)
                if self.get_region(pos1) == region and self.get_region(pos2) == region and self.get_region(diag) != region:
                    verticies += 1
        return verticies

    def sides(self, patch):
        region = self.get_region(min(patch))
        all_verticies = 0
        for pos in patch:
            all_verticies += self.convex(pos, region) + self.concave(pos, region)
        return all_verticies

garden = Fence()
patches = garden.get_patches()
price = 0
for patch in patches:
    price += garden.area(patch) * garden.perimeter(patch)

print('challenge 1', price)

price = 0
for patch in patches:
    price += garden.area(patch) * garden.sides(patch)

print('challenge 2', price)