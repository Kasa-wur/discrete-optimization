#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight'])

def data_parser(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    return capacity, items


def ny_matrix(capacity, items):
    matrix = np.zeros((capacity+1,len(items)))
    for w in range(capacity + 1):
        matrix[w,0] = 0 if w < items[0].weight else items[0].value
        for item in items[1:]:
            if item.weight > w:
                matrix[w,item.index] = matrix[w, item.index-1]
            else:
                not_taken = matrix[w,item.index - 1]
                taken = matrix[w - item.weight,item.index - 1] + item.value
                matrix[w,item.index] = max(taken, not_taken)
    return matrix

def trace_back(matrix,items):
    (row, col) = tuple(map(lambda x: x-1,matrix.shape))
    taken = {}
    for item in items[::-1]:
        if row == 0 or col== 0:
            taken[item.index] = 1 if matrix[row,col] == item.value else 0
        elif matrix[row,col] == matrix[row,col-1] and col >= 1 and row >=0:
            taken[item.index] = 0
        else:
            taken[item.index] = 1
            row -=  item.weight
        col -= 1
    return taken


#
# def solve_it(input_data):
#
#
#
#     output_data = str(matrix[-1][-1]) + ' ' + str(0) + '\n'
#     for i in sorted(list(take.keys()), reverse=False):
#         output_data += str(take[i]) + ' '
#     return output_data







if __name__ == '__main__':
    with open('./data/ks_50_0','r') as input_data_file:
        input_data = input_data_file.read()
        capacity, items = data_parser(input_data)

    # matrix = dy_matrix(capacity, items)
    # take = trace_back(matrix,items)
    # print(matrix[-1][-1])
    # print(take)

    np_mat = ny_matrix(capacity, items)
    print(np_mat)
    print('total value:', np_mat[-1,-1])
    take = trace_back(np_mat, items)

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
