import math
import numpy as np
import networkx as nx
from numpy import random
import quantumrandom
import copy
import timeit

def greedy(G, desired_set_size = 10, inner_sim_epoch = 10):
    chosen = []
    for i in range(desired_set_size):
        max_score = 0
        max_score_edge = 0
        for j in G.nodes():
            #generating score for each node j
            if j not in chosen:
                score = 0
                new_chosen = copy.deepcopy(chosen)
                new_chosen.append(j)
                for iter in range(inner_sim_epoch):
                    score += len(IC(G, new_chosen))

                if score > max_score:
                    max_score = score
                    max_score_node = j

        chosen.append(max_score_node)
        print(chosen)

        print("Iter = ", i , ", vertex ", max_score_node, " is chosen with score ", max_score/inner_sim_epoch)

    return len(IC(G, chosen))

def high_degree(G, desired_set_size = 10, inner_sim_epoch = 10):
    number_of_nodes = nx.number_of_nodes(G)
    degree_sequence = sorted(G.degree, key=lambda x: x[1], reverse=True)
    chosen_set = [name for (name, degree) in degree_sequence[:desired_set_size]]

    return len(IC(G, chosen_set))


def IC(G, initial_set):
    new_node_activated = True
    activated_nodes = copy.deepcopy(initial_set)
    newly_activated_nodes = copy.deepcopy(activated_nodes)
    while new_node_activated:
        # when some node is activated
        new_node_activated = False
        nodes_activation = []
        for i in newly_activated_nodes:
            for j in G.neighbors(str(i)):
                if random.uniform(0,1) < G.edges[u, v]['weight'] and j not in activated_nodes:
                    # if the random number is greater than the activation probability
                    nodes_activation.append(j)
                    activated_nodes.append(j)
                    new_node_activated = True
        newly_activated_nodes = copy.deepcopy(nodes_activation)

    return activated_nodes


def hdGreedy(G, k):
    # degree_sequence = sorted([d for n, d in G.degree()])
    g = []
    S = []
    for i in range(k):
        X = G.subgraph(G.nodes() - g)
        degree_sequence = sorted(X.degree, key=lambda x: x[1], reverse=True)
        v = degree_sequence[0][0]
        # print(degree_sequence[0])
        S.append(v)
        T = IC(X, [v])
        g = g + T

        print(len(g))
    return len(g)


if __name__ == "__main__":
    G = nx.read_edgelist("./1005edges")
    #G = nx.read_edgelist("./toy")
    for u,v,e in G.edges(data = True):
        e['weight'] = random.uniform(0,1)/100

    start = timeit.timeit()
    print("High-degree algorithm final spread {}".format(high_degree(G)))
    end = timeit.timeit()
    print("High-degree algorithm time elapsed {}".format(end -start))

    start = timeit.timeit()
    print("Greedy algorithm (paper) final spread {}".format(greedy(G)))
    end = timeit.timeit()
    print("Greedy algorithm (paper) time elapsed {}".format(end -start))

    start = timeit.timeit()
    print("High-degree greedy algorithm final spread {}".format(hdGreedy(G)))
    end = timeit.timeit()
    print("High-degree greedy algorithm time elapsed {}".format(end -start))
