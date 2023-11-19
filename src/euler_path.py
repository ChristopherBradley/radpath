import networkx as nx
import numpy as np
from scipy.spatial.distance import cosine
from functools import reduce
import operator

def euler_path(edges, double_edges):
    """Create a route through the graph that is easy to follow and avoids turning back on itself"""
    graph = create_multi_graph(edges, double_edges)
    last_edge = list(graph.edges)[0]
    ordered_edges = [last_edge[:2]]
    graph.remove_edge(last_edge[0], last_edge[1])
    insertion_index = 1
    loop_size = 0

    current_loop = ordered_edges.copy()
    intersections = []
    loops = []

    # Choose edges one at a time, and remove them from the graph.
    while(len(graph.edges())) > 0:
        possibilities = graph.adj[last_edge[1]]
        if len(possibilities) == 0:
            insertion_index, last_edge = backtrack(insertion_index, ordered_edges, graph.adj)
            possibilities = graph.adj[last_edge[1]]
            # Reset the current loop to wherever we were previously
            for i in range(len(intersections)):
                if insertion_index < intersections[i]:
                    current_loop = loops[i]
                    break
        possibilities = list(prioritise_double_edges(possibilities))
        next_node = choose_next_node(last_edge, possibilities)
        graph.remove_edge(last_edge[1], next_node)
        last_edge = (last_edge[1], next_node)
        ordered_edges.insert(insertion_index, last_edge)
        
        intersections = [index if index <= insertion_index else index + 1 for index in intersections]
        insertion_index += 1
        loop_size += 1

        # Start a new loop if we intersect with this loop and the intersection results in a loop larger than intersect_lenience + 1
        in_current_loop = next_node in {item for sublist in current_loop for item in sublist}
        intersect_lenience = 5
        in_last_n = next_node in {item for sublist in current_loop[-intersect_lenience:] for item in sublist}
        if in_current_loop and not in_last_n:
            intersections.append(insertion_index)
            loops.append(current_loop)
            current_loop = []
            continue
        current_loop.append(last_edge)

    intersections2 = [0] + sorted(intersections) + [len(ordered_edges)]
    diffs = np.diff(intersections2)
    colours = reduce(operator.concat, [[i]*length for i,length in enumerate(diffs)])
    return ordered_edges, colours

def prioritise_double_edges(possibilities):
    """Choose the double edges first to help avoid turning back on yourself"""
    doubled = [k for k, v in possibilities.items() if len(v) > 1]
    return doubled if len(doubled) > 0 else possibilities

def backtrack(insertion_index, ordered_edges, adjacencies):
    """Find the last node where we could have gone in a different direction"""
    while insertion_index > 0:
        insertion_index -= 1
        last_edge = ordered_edges[insertion_index]
        if len(adjacencies[last_edge[0]]) > 0:
            break
    if insertion_index == 0:
        last_edge = [last_edge[0], last_edge[0]]
    else:
        last_edge = ordered_edges[insertion_index - 1]
    return insertion_index, last_edge

def choose_next_node(last_edge, possibilities):
    """Choose the node that is most in a straight line"""
    current_gradient = np.array(last_edge[0]) - np.array(last_edge[1])
    possible_gradients = np.array(last_edge[1]) - possibilities
    similarities = [cosine(current_gradient, p) for p in possible_gradients]
    node_index = np.argmin(similarities)
    next_node = possibilities[node_index]
    return next_node

def create_multi_graph(edges, double_edges):
    """Combine the single and double edges into a graph"""
    graph = nx.MultiGraph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1])
    for edge in double_edges:
        graph.add_edge(edge[0], edge[1])
    return graph