import math
import numpy as np
import networkx as nx
from numpy import random
import quantumrandom
import copy
import timeit

def greedy(G, desired_set_size = 10, inner_sim_epoch = 10):
    number_of_nodes = nx.number_of_nodes(G)
    number_of_edges = nx.number_of_edges(G)

    chosen = [0] * number_of_nodes

    for i in range(desired_set_size):
        max_score = 0
        max_score_edge = 0
        for j in range(number_of_nodes):
            #generating score for each node j
            if chosen[j] == 0:
                score = 0
                new_chosen = copy.deepcopy(chosen)
                new_chosen[j] = 1
                for iter in range(inner_sim_epoch):
                    score += sum(IC(G, new_chosen))

                if score > max_score:
                    max_score = score
                    max_score_edge = j

        chosen[max_score_edge] = 1
        print("Iter = ",i , ", vertex ", max_score_edge, " is chosen with score ", max_score/inner_sim_epoch)

    return sum(IC(G, chosen))

def high_degree(G, desired_set_size = 10, inner_sim_epoch = 10):
    number_of_nodes = nx.number_of_nodes(G)
    degree_sequence = sorted([n for n, d in G.degree()], reverse=True)
    chosen_set = degree_sequence[:desired_set_size]
    chosen_list = [0] * number_of_nodes
    for i in range(number_of_nodes):
        chosen_list[i] = 1 if str(i) in chosen_set else 0

    return sum(IC(G, chosen_list))


def IC(G, initial_set):
    number_of_nodes = nx.number_of_nodes(G)
    new_node_activated = True
    activated_nodes = copy.deepcopy(initial_set)
    newly_activated_nodes = copy.deepcopy(activated_nodes)
    activating_probability = random.rand(number_of_nodes,number_of_nodes)
    while new_node_activated:
        # when some node is activated
        new_node_activated = False
        for i in range(number_of_nodes):
            nodes_activation = [0] * number_of_nodes
            if newly_activated_nodes[i] == 1:
                randn = random.rand(number_of_nodes)
                for j in range(number_of_nodes):
                    if randn[j] >  100* activating_probability[i][j]:
                        # if the random number is greater than the activation probability
                        nodes_activation[j] = 1
                        activated_nodes[j] = 1
                        new_node_activated = True
        newly_activated_nodes = copy.deepcopy(nodes_activation)

    return activated_nodes

if __name__ == "__main__":
    G = nx.read_edgelist("./1005edges")
    #G = nx.read_edgelist("./toy")

    start = timeit.timeit()
    print("High-degree algorithm final spread {}".format(high_degree(G)))
    end = timeit.timeit()
    print("High-degree algorithm time elapsed {}".format(end -start))

    start = timeit.timeit()
    print("Greedy algorithm (paper) final spread {}".format(greedy(G)))
    end = timeit.timeit()
    print("Greedy algorithm (paper) time elapsed {}".format(end -start))