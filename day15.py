import numpy as np

def flatten(xss):
    return [x for xs in xss for x in xs]

class Warehouse:
    def __init__(self):
        self.map = []
        self.instructions = []
        with open('data/input_day15.txt') as f:
            row = 0
            for line in f:
                line = [i for i in line.strip()]
                if len(line) == 0:
                    continue
                elif line[0] in ['<', '^', 'v', '>']:
                    self.instructions.extend(line)
                else:
                    if '@' in line:
                        col = line.index('@')
                        self.init_pos = row, col
                        line = line[:]
                        line[col] = '.'
                    self.map.append(line)
                row += 1

    def display(self, pos=(-1,-1)):
        # reset pos
        if pos == (-1, -1):
            pos = self.init_pos
        # challenge 1
        for ind, line in enumerate(self.map):
            if ind == pos[0]:
                line = line[:]
                line[pos[1]] = '@'
            print(line)
        print('------------')

    def get_sym(self, pos):
        return self.map[pos[0]][pos[1]]

    def get_pos(self, pos, dir):
        if dir == '^':
            return pos[0]-1, pos[1]
        elif dir == '<':
            return pos[0], pos[1]-1
        elif dir == 'v':
            return pos[0]+1, pos[1]
        else:
            return pos[0], pos[1]+1

    def move(self, pos, dir):
        next_pos = self.get_pos(pos, dir)
        next_sym = self.get_sym(next_pos)
        if next_sym == '#':
            return pos
        elif next_sym == '.':
            return next_pos
        elif next_sym == 'O':
            return self.move_boxes(pos, dir)

    def move_boxes(self, pos, dir):
        # how many boxes
        sym = 'O'
        start = self.get_pos(pos, dir)
        end = start
        while sym == 'O':
            end = self.get_pos(end, dir)
            sym = self.get_sym(end)
        if sym == '.':
            self.update_map(start, end)
            return start
        elif sym == '#':
            return pos

    def update_map(self, start, end):
        self.map[start[0]][start[1]] = '.'
        self.map[end[0]][end[1]] = 'O'

    def exe_instructions(self):
        pos = self.init_pos
        for dir in self.instructions:
            pos = self.move(pos, dir)

    def GPS(self):
        boxes = np.array(list(np.where(np.array(self.map) == 'O'))).T
        return np.sum(boxes[:,0]*100+boxes[:,1])

warehouse = Warehouse()
warehouse.exe_instructions()
print('challenge 1', warehouse.GPS())

######################

class Warehouse2:
    def __init__(self):
        self.walls = []
        self.boxes = {}
        self.instructions = []
        box_id = 0
        with open('data/input_day15.txt') as f:
            for row, line in enumerate(f):
                line = [i for i in line.strip()]
                if len(line) == 0:
                    continue
                elif line[0] in ['<', '^', 'v', '>']:
                    self.instructions.extend(line)
                else:
                    for col, sym in enumerate(line):
                        if sym == '#':
                            self.walls.extend([(row, col*2), (row, col*2+1)])
                        elif sym == 'O':
                            self.boxes[box_id] = row, col*2
                            box_id += 1
                        elif sym == '@':
                            self.robot = row, col*2
        self.map_size = self.walls[-1][0]+1, self.walls[-1][1]+1

    def display(self):
        # create map
        map = []
        for row in range(self.map_size[0]):
            map.append(['.']*self.map_size[1])
        # draw walls
        for wall in self.walls:
            map[wall[0]][wall[1]] = '#'
        # draw boxes
        for box_id in self.boxes.keys():
            coord = self.boxes[box_id]
            map[coord[0]][coord[1]] = '['
            map[coord[0]][coord[1]+1] = ']'
        # draw robot
        map[self.robot[0]][self.robot[1]] = '@'
        # draw
        for row in map:
            print(''.join(row))
        print('------------')

    def get_box_coord(self, box_id):
        box_left = self.boxes[box_id]
        box_right = self.get_pos(box_left, '>')
        return [box_left, box_right]

    def get_box(self, pos):
        for box_id in self.boxes.keys():
            box_left, box_right = self.get_box_coord(box_id)
            if box_left == pos or box_right == pos:
                return box_id
        return -1

    def get_pos(self, pos, dir):
        if dir == '^':
            return pos[0]-1, pos[1]
        elif dir == '<':
            return pos[0], pos[1]-1
        elif dir == 'v':
            return pos[0]+1, pos[1]
        else:
            return pos[0], pos[1]+1

    def move(self, pos, dir):
        next_pos = self.get_pos(pos, dir)
        box_id = self.get_box(next_pos)
        if next_pos in self.walls:
            return pos
        elif box_id != -1:
            boxes = self.move_boxes([], dir, [box_id])
            if len(boxes) == 0:
                return pos
            else:
                self.increment_boxes(boxes, dir)
                return next_pos
        else:
            return next_pos

    def move_boxes(self, boxes, dir, check_boxes):
        if len(check_boxes) == 0:
            return list(set(boxes))
        else:
            new_check_boxes = []
            for box_id in check_boxes:
                boxes.append(box_id)
                box_left, box_right = self.get_box_coord(box_id)
                box_left = self.get_pos(box_left, dir)
                box_right = self.get_pos(box_right, dir)
                # failed
                if box_left in self.walls or box_right in self.walls:
                    return []
                # box
                left_box_id = self.get_box(box_left)
                right_box_id = self.get_box(box_right)
                if left_box_id != -1 and left_box_id != box_id:
                    new_check_boxes.append(left_box_id)
                if right_box_id != -1 and right_box_id != box_id:
                    new_check_boxes.append(right_box_id)
            return self.move_boxes(list(set(boxes)), dir, list(set(new_check_boxes)))

    def increment_boxes(self, boxes, dir):
        for box_id in boxes:
            new_coord = self.get_pos(self.boxes[box_id], dir)
            self.boxes[box_id] = new_coord

    def exe_instructions(self):
        num = 0
        for dir in self.instructions:
            self.robot = self.move(self.robot, dir)
            if 20 <= num and num <= 0:
                print(dir)
                self.display()
            num += 1

    def GPS(self):
        boxes = np.array(list(self.boxes.values()))
        return np.sum(boxes[:,0]*100+boxes[:,1])

warehouse = Warehouse2()
#warehouse.display()
warehouse.exe_instructions()
#warehouse.display()
print('challenge 2', warehouse.GPS())