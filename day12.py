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

    def get_surrounding(self, pos):
        return [self.move(pos, dir) for dir in ['down', 'left', 'up', 'right']]

    def fence(self, pos, region):
        if self.out_of_bounds(pos):
            return 1
        elif self.garden[pos[0], pos[1]] != region:
            return 1
        else:
            return 0

    def find_region(self, region, in_region, to_explore):
        if len(to_explore) == 0:
            return in_region
        else:
            # explore one position
            pos = min(to_explore)
            if self.garden[pos[0], pos[1]] == region:
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
                    region = self.garden[row, col]
                    patch = self.find_region(region, {pos}, set([p for p in self.get_surrounding(pos) if not self.out_of_bounds(p)]))
                    traversed.extend(patch)
                    patches.append(patch)
        return patches

    def area(self, patch):
        return len(patch)

    def perimeter_one(self, pos, region):
        return self.fence((pos[0], pos[1]-1), region) + self.fence((pos[0], pos[1]+1), region) + self.fence((pos[0]-1, pos[1]), region) + self.fence((pos[0]+1, pos[1]), region)

    def perimeter(self, patch):
        pos = min(patch)
        region = self.garden[pos[0], pos[1]]
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

    def sides(self, patch):
        return 0

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