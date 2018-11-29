from collections import namedtuple
import xpress as xp
import sys

Item = namedtuple("Item", ['index', 'value', 'weight'])

def data_parser(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = {}
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items[i-1] = {'index':i-1, 'value':int(parts[0]), 'weight':int(parts[1])}
    return capacity, item_count, items

def solve_it(input_data):
    capacity, item_count, items = data_parser(input_data)
    m = xp.problem()
    x = {i: xp.var(vartype = xp.binary) for i in range(item_count)}
    m.addVariable(x)
    obj = xp.Sum(x[i]*items[i]['value'] for i in range(item_count))
    m.setObjective(obj, sense=xp.maximize)
    m.addConstraint(xp.Sum(x[i]*items[i]['weight'] for i in range(item_count)) <= capacity)
    m.controls.outputlog = 0
    m.solve()
    output_data = str(int(m.getObjVal())) + ' ' + str(0) + '\n'
    for v in x:
        output_data += str(int(m.getSolution(v))) + ' '
    return output_data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            solve_it(input_data)

    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
