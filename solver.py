#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from numba import jit


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
        dict = {'index': i-1, 'value' : int(parts[0]),'weight' : int(parts[1])}
        items.append(dict)
    return capacity, items

def dy_matrix(capacity, items):
    matrix = [[0 for j in items] for i in range(capacity+1)]
    for w in range(capacity + 1):
        matrix[w][0] = 0 if w < items[0]['weight'] else items[0]['value']
        for i, item in enumerate(items[1:]):
            ind = i + 1
            if item['weight'] > w:
                matrix[w][ind] = matrix[w][ind - 1]
            else:
                matrix[w][ind] = max(matrix[w][ind - 1],\
                                     matrix[w-item['weight']][ind-1]+item['value'])
    return matrix

def trace_back(matrix,items):
    row = len(matrix) - 1
    col = len(matrix[0]) - 1
    taken = {}
    for item in reversed(items):
        if col >= 1 and row >=0 and matrix[row][col] == matrix[row][col-1]:
            taken[item['index']] = 0
        elif row == 0 or col== 0:
            taken[item['index']] = 1 if matrix[row][col] == item['value'] else 0
        else:
            taken[item['index']] = 1
            row -=  item['weight']
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
    t1 = time.clock()
    with open('data/ks_100_0','r') as input_data_file:
        input_data = input_data_file.read()
        capacity, items = data_parser(input_data)

    matrix = dy_matrix(capacity, items)
    take = trace_back(matrix,items)
    t2 = time.clock()
    print('run time:%f s'%(t2-t1))

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
