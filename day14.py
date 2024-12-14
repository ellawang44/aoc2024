import numpy as np
import matplotlib.pyplot as plt

class Bathroom:
    def __init__(self):
        self.init_pos, self.init_vel = self.read_input()
        self.map = (101, 103)

    def read_input(self):
        pos = []
        vel = []
        with open('data/input_day14.txt') as f:
            for line in f:
                line = line.strip().split(' ')
                p = [int(i) for i in line[0].split('=')[1].split(',')]
                v = [int(i) for i in line[1].split('=')[1].split(',')]
                pos.append(p)
                vel.append(v)
        return pos, vel

    def move(self, pos, vel, time=1):
        dist = vel[0]*time, vel[1]*time
        new_pos = (pos[0]+dist[0]) % self.map[0], (pos[1]+dist[1]) % self.map[1]
        return new_pos

    def move_all(self, time=1):
        new_pos = []
        for init_pos, init_vel in zip(self.init_pos, self.init_vel):
            new_pos.append(self.move(init_pos, init_vel, time=time))
        return new_pos

    def display(self, pos, filename=0, show=False):
        dis_map = np.zeros(self.map)
        for p in pos:
            dis_map[p[0], p[1]] += 1
        plt.imshow(dis_map.T)
        plt.savefig(f'img/{filename}.png')
        plt.close()

bathroom = Bathroom()
# move robots
new_pos = bathroom.move_all(time=100)
new_pos = np.array(new_pos)
# calculate quadrants
half_width = bathroom.map[0]//2
half_height = bathroom.map[1]//2
q1 = np.sum((new_pos[:,0] < half_width) & (new_pos[:,1] < half_height))
q2 = np.sum((new_pos[:,0] > half_width) & (new_pos[:,1] < half_height))
q3 = np.sum((new_pos[:,0] < half_width) & (new_pos[:,1] > half_height))
q4 = np.sum((new_pos[:,0] > half_width) & (new_pos[:,1] > half_height))
print('challenge 1', q1*q2*q3*q4)

#######
# I don't understand what a xmas tree looks like?
width = 20
for i in range(10000):
    new_pos = np.array(bathroom.move_all(time=i))
    if np.sum(new_pos[:,0] < width) + np.sum(new_pos[:,0] > (bathroom.map[0]-width)) < 150:
        bathroom.display(new_pos, filename=i)
# there's a bit of brute force, oh well.