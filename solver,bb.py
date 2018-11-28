#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import copy
from collections import namedtuple
from collections import deque
from numba import jit

Item = namedtuple("Item", ['index', 'value', 'weight','unit_v'])

@jit
def data_parser(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), int(parts[0])/int(parts[1])))
    return capacity, item_count, items


class Node(object):
    def __init__(self, depth, value, room, bound, take):
        self.depth = depth
        self.value = value
        self.room = room
        self.bound = bound
        self.take = take

class Stack(object):
    def __init__(self):
        self.buffer = deque()

    def push(self, node):
        self.buffer.append(node)

    def pop(self):
        return self.buffer.pop()

    def __len__(self):
        return len(self.buffer)


def solve_it(sorted_items):
    def cal_bound(room, depth):
        """upper bound of current node
            the optimistic value"""
        bound = 0.0
        weight = 0.0
        for item in sorted_items[depth:]:
            if weight + item.weight <= room:
                bound += item.value
                weight += item.weight
            else:
                bound += (float(room) - weight) *item.unit_v
                break
        return bound

    max_bound = cal_bound(capacity, 0)  # root relaxation
    best_value = 0
    best_taken = [0 for i in range(item_count +1)]
    current_taken = [0 for i in range(item_count +1)]
    root = Node(0, 0, capacity, max_bound, 0) # depth, value, room, bound, take
    stack = Stack()
    stack.push(root)

    while len(stack) > 0:
        current = stack.pop()

        if current.room < 0 or current.bound < best_value: # pruning
            continue
        elif current.depth < item_count:
            next_item = sorted_items[current.depth]
            left_node = Node(current.depth+1, \
                             current.value + next_item.value,\
                             current.room - next_item.weight ,\
                             current.bound, 1)
            right_node = Node(current.depth +1, current.value, current.room,\
                              current.value + cal_bound(current.room, current.depth+1), 0)
            stack.push(right_node)
            stack.push(left_node)
            if current.depth != 0:
                current_taken[sorted_items[current.depth-1].index] = current.take

        elif current.depth == item_count:
            if current.value > best_value and current.room >= 0:
                best_value = current.value
                current_taken[sorted_items[current.depth-1].index] = current.take
                best_taken = copy.deepcopy(current_taken)

    output_data = str(best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_taken[:-1]))
    return output_data

if __name__ == '__main__':
    with open('data/ks_60_0','r') as input_data_file:
        input_data = input_data_file.read()
        capacity, item_count, items = data_parser(input_data)

    time1 = time.clock()
    sorted_items = sorted(items, key=lambda x: x.unit_v, reverse=True)
    solve_it(sorted_items)
    time2 = time.clock()
    print('run time %fs'%(time2-time1))



    #
    # import sys
    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    #     with open(file_location, 'r') as input_data_file:
    #     #     input_data = input_data_file.read()
    #     #     capacity, items = data_parser(input_data)
    #     #
    #     # matrix = dy_matrix(capacity, items)
    #     # take = trace_back(matrix, items)
    #         solve_it(input_data_file)
    #
    #
    #
    #     # print(data_parser(input_data))
    # else:
    #     print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
    #
