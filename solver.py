#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def data_parser(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
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

def dy_matrix(capacity, items):
    matrix = [[0 for j in items] for i in range(capacity+1)]
    for w in range(capacity+1):
        matrix[w][0] = 0 if w < items[0].weight else items[0].value
        for item in items[1:]:
            if item.weight > w:
                matrix[w][item.index] = matrix[w][item.index-1]
            else:
                not_taken = matrix[w][item.index-1]
                taken = matrix[w - item.weight][item.index-1] + item.value
                matrix[w][item.index] = max(taken, not_taken)
    return matrix


def trace_back(matrix,items):
    row = len(matrix) -1
    col = len(matrix[0]) -1
    taken = {}
    for item in items[::-1]:
        #print('col:', col, 'row:', row)
        if row == 0 or col== 0:
            taken[item.index] = 1 if matrix[row][col] == item.value else 0

        elif matrix[row][col] == matrix[row][col-1] and col >= 1 and row >=0:
            taken[item.index] = 0
        else:
            taken[item.index] = 1
            row -=  item.weight
        col -= 1
    return taken




def solve_it(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    matrix = [[0 for j in items] for i in range(capacity+1)]
    for w in range(capacity+1):
        matrix[w][0] = 0 if w < items[0].weight else items[0].value
        for item in items[1:]:
            if item.weight > w:
                matrix[w][item.index] = matrix[w][item.index-1]
            else:
                not_taken = matrix[w][item.index-1]
                taken = matrix[w - item.weight][item.index-1] + item.value
                matrix[w][item.index] = max(taken, not_taken)

    row = len(matrix) -1
    col = len(matrix[0]) -1
    take = {}
    for item in items[::-1]:
        if row == 0 or col== 0:
            take[item.index] = 1 if matrix[row][col] == item.value else 0
        elif matrix[row][col] == matrix[row][col-1] and col >= 1 and row >=0:
            take[item.index] = 0
        else:
            take[item.index] = 1
            row -=  item.weight
        col -= 1


    output_data = str(matrix[-1][-1]) + ' ' + str(0) + '\n'
    for i in sorted(list(take.keys()), reverse=False):
        output_data += str(take[i]) + ' '
    return output_data





    # # a trivial greedy algorithm for filling the knapsack
    # # it takes items in-order until the knapsack is full
    # value = 0
    # weight = 0
    # taken = [0]*len(items)
    #
    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight
    #
    # # prepare the solution in the specified output format
    # output_data = str(value) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, taken))
    # return output_data


if __name__ == '__main__':
    # with open('./data/ks_30_0','r') as input_data_file:
    #     input_data = input_data_file.read()
    #     capacity, items = data_parser(input_data)
    #
    # matrix = dy_matrix(capacity, items)
    # take = trace_back(matrix,items)
    # print(matrix[-1][-1])
    # print(take)


    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
        #     input_data = input_data_file.read()
        #     capacity, items = data_parser(input_data)
        #
        # matrix = dy_matrix(capacity, items)
        # take = trace_back(matrix, items)
            solve_it(input_data_file)



        # print(data_parser(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

