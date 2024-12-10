import numpy as np
import copy

class Format:
    def __init__(self):
        self.dense_data = self.read_dense()

    def read_dense(self):
        with open('input_day9.txt') as f:
            dense = f.readline().strip()
        return dense

    def display(self):
        print(self.dense_data)
        print(self.file_dict)
        print(self.free_dict)
        print(self.block_format)

    def parse_dense(self):
        l = len(self.dense_data)
        self.file_dict = {}
        self.free_dict = {}
        ind = 0
        for i in range(l):
            if i % 2 == 0:
                file_length = int(self.dense_data[i])
                self.file_dict[i//2] = file_length
                ind += file_length
            else:
                empty_length = int(self.dense_data[i])
                if empty_length > 0:
                    self.free_dict[ind] = empty_length
                ind += empty_length

    def init_block(self):
        self.block_format = []
        ind = 0
        for key in range(len(self.file_dict)):
            # puts file in format
            file_length = self.file_dict[key]
            self.block_format.extend([key]*file_length)
            ind += file_length
            # put free space in format
            if ind in self.free_dict.keys():
                self.block_format.extend([-1]*self.free_dict[ind])
                ind += self.free_dict[ind]
        self.block_format = np.array(self.block_format)

    def move_one(self):
        if self.block_format[-1] == -1:
            self.block_format = self.block_format[:-1]
        else:
            ind = np.where(self.block_format == -1)[0][0]
            val = self.block_format[-1]
            self.block_format[ind] = val
            self.block_format = self.block_format[:-1]

    def condense1(self):
        while -1 in self.block_format:
            self.move_one()

    def move_block(self, key):
        file_length = self.file_dict[key]
        file_ind = np.where(self.block_format == key)[0][0]
        free_dict_inds = []
        for ind, val in self.free_dict.items():
            if ind < file_ind and val >= file_length:
                free_dict_inds.append(ind)
        if len(free_dict_inds) > 0:
            free_dict_ind = min(free_dict_inds)
            # move the file
            self.block_format[free_dict_ind:free_dict_ind+file_length] = np.array([key]*file_length)
            self.block_format[file_ind:file_ind+file_length] = np.array([-1]*file_length)
            # update free space
            orig_free_length = self.free_dict[free_dict_ind]
            del self.free_dict[free_dict_ind]
            if orig_free_length - file_length > 0:
                self.free_dict[free_dict_ind+file_length] = orig_free_length - file_length

    def condense2(self):
        for key in list(range(len(self.file_dict)))[1:][::-1]:
            self.move_block(key)

    def checksum(self):
        block_format = copy.deepcopy(self.block_format)
        block_format[np.where(block_format == -1)[0]] = 0
        return np.sum(block_format*np.arange(len(block_format)))

format = Format()
format.parse_dense()
format.init_block()
format.condense1()
print('challenge 1', format.checksum())

############################

format = Format()
format.parse_dense()
format.init_block()
format.condense2()
print('challenge 2', format.checksum())