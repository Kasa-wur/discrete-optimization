import networkx as nx
import matplotlib.pyplot as plt

def data_parser(input_data):
    '''edges: list of tuples'''
    lines = input_data.split('\n')
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edges = []
    # return edges list
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # return graph dictionary   {node:[neighbor_nodes_list]}
    graph = {i:[] for i in range(node_count)}
    for (node1, node2) in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)
    return node_count, edge_count, edges, graph

def solve_it(graph):
    """welsh——powell algorithm (greedy) """
    # sort node by number of its neighbors
    nodes = sorted(graph, key = lambda x: len(graph[x]), reverse = True)

    color_map = {}
    for node in nodes:
        neighbor_colors = set(color_map.get(neighbor) for neighbor in graph[node])
        # next 巧用
        color_map[node] = next(color for color in range(len(graph)) \
                                                            if color not in neighbor_colors)
    output_data = str(len(graph)) + ' ' + str(0) +'\n'
    output_data += ' '.join(map(str, list(map(lambda x: color_map[x], color_map))))

    return color_map, output_data

def draw_graph(edges, color_map, node_count):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    colors = [color_map.get(node) for node in G.nodes()]
    nx.draw(G, pos, with_labels= True, node_color = colors, edge_color = 'black')



if __name__ == '__main__':
    file_location = 'data/gc_20_1'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    node_count, edge_count, edges, graph = data_parser(input_data)

    color_map = solve_it(graph)[0]

    draw_graph(edges, color_map, node_count)
    plt.show()


    # import sys
    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    #     with open(file_location, 'r') as input_data_file:
    #         input_data = input_data_file.read()
    #         node_count, edge_count, edges, graph = data_parser(input_data)
    #     print(solve_it(graph))
    # else:
    #     print(
    #         'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
