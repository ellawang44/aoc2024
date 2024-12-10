import numpy as np
from itertools import combinations
import copy

class Antenna:
    def __init__(self):
        self.antennas = self.read_antennas()
        self.anti_nodes = np.zeros(self.antennas.shape)
        self.max_length = len(self.antennas) # square

    def display(self):
        c = copy.deepcopy(self.antennas)
        for ind, line in enumerate(self.anti_nodes):
            c[ind][line == 1] = '#'
            print(c[ind])

    def read_antennas(self):
        data = []
        with open('data/input_day8.txt') as f:
            for line in f:
                data.append(list(line.strip()))
        data = np.array(data)
        return data

    def find_all_nodes(self):
        for sym in np.unique(self.antennas):
            if sym != '.':
                self.find_nodes_for_sym(sym)

    def find_nodes_for_sym(self, sym):
        inds = np.array(np.where(self.antennas == sym)).T
        ind_pairs = list(combinations(inds, 2))
        for ind1, ind2 in ind_pairs:
            self.find_pair_node(ind1, ind2)

    def find_pair_node(self, ind1, ind2):
        row_dist = ind2[0] - ind1[0]
        col_dist = ind2[1] - ind1[1]
        new1 = (ind1[0]-row_dist, ind1[1]-col_dist)
        new2 = (ind2[0]+row_dist, ind2[1]+col_dist)
        if new1[0] >= 0 and new1[1] >= 0 and new1[0] < self.max_length and new1[1] < self.max_length:
            self.anti_nodes[new1[0]][new1[1]] = 1
        if new2[0] >= 0 and new2[1] >= 0 and new2[0] < self.max_length and new2[1] < self.max_length:
            self.anti_nodes[new2[0]][new2[1]] = 1

ant = Antenna()
ant.find_all_nodes()
print('challenge 1', np.sum(ant.anti_nodes))

###############################

class Antenna:
    def __init__(self):
        self.antennas = self.read_antennas()
        self.anti_nodes = np.zeros(self.antennas.shape)
        self.max_length = len(self.antennas) # square

    def display(self):
        c = copy.deepcopy(self.antennas)
        for ind, line in enumerate(self.anti_nodes):
            c[ind][line == 1] = '#'
            print(c[ind])

    def read_antennas(self):
        data = []
        with open('data/input_day8.txt') as f:
            for line in f:
                data.append(list(line.strip()))
        data = np.array(data)
        return data

    def find_all_nodes(self):
        for sym in np.unique(self.antennas):
            if sym != '.':
                self.find_nodes_for_sym(sym)

    def find_nodes_for_sym(self, sym):
        inds = np.array(np.where(self.antennas == sym)).T
        ind_pairs = list(combinations(inds, 2))
        for ind1, ind2 in ind_pairs:
            self.find_pair_node(ind1, ind2)

    def find_pair_node(self, ind1, ind2):
        row_dist = ind2[0] - ind1[0]
        col_dist = ind2[1] - ind1[1]
        # set antennas themselves as nodes
        self.anti_nodes[ind1[0]][ind1[1]] = 1
        self.anti_nodes[ind2[0]][ind2[1]] = 1
        # direction 1
        new1 = (ind1[0]-row_dist, ind1[1]-col_dist)
        while new1[0] >= 0 and new1[1] >= 0 and new1[0] < self.max_length and new1[1] < self.max_length:
            self.anti_nodes[new1[0]][new1[1]] = 1
            new1 = (new1[0]-row_dist, new1[1]-col_dist)
        # direction 2
        new2 = (ind2[0]+row_dist, ind2[1]+col_dist)
        while new2[0] >= 0 and new2[1] >= 0 and new2[0] < self.max_length and new2[1] < self.max_length:
            self.anti_nodes[new2[0]][new2[1]] = 1
            new2 = (new2[0]+row_dist, new2[1]+col_dist)

ant = Antenna()
ant.find_all_nodes()
print('challenge 2', np.sum(ant.anti_nodes))