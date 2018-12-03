import math
import numpy as np
import networkx as nx
from numpy import random
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

def high_degree(G, activating_probability, desired_set_size = 10, inner_sim_epoch = 10):
    number_of_nodes = nx.number_of_nodes(G)
    degree_sequence = sorted(G.degree, key=lambda x: x[1], reverse=True)
    chosen_set = [name for (name, degree) in degree_sequence[:desired_set_size]]
    chosen_list = [0] * number_of_nodes
    for i in range(number_of_nodes):
        chosen_list[i] = 1 if str(i) in chosen_set else 0
    
    return sum(IC(G, chosen_list, activating_probability))
        
def hdGreedy(G, k):
    #degree_sequence = sorted([d for n, d in G.degree()])
    g=[]
    S=[]
    for i in range(k):
        X=G.subgraph(G.nodes()-g)
        degree_sequence=sorted(X.degree, key=lambda x: x[1], reverse=True)
        v=degree_sequence[0][0]
        #print(degree_sequence[0])
        S.append(v)
        T=runIC(X, [v])
        g=g+T
        
        print(len(g))
    return len(g)


def IC(G, initial_set,activating_probability):
    number_of_nodes = nx.number_of_nodes(G)
    new_node_activated = True
    activated_nodes = copy.deepcopy(initial_set)
    newly_activated_nodes = copy.deepcopy(activated_nodes)
    while new_node_activated:
        # when some node is activated
        new_node_activated = False
        nodes_activation = [0] * number_of_nodes
        for i in newly_activated_nodes:
            randn = random.rand(number_of_nodes)
            for j in G.neighbors(str(i)):
                if randn[int(j)] < activating_probability[int(i)][int(j)] and activated_nodes[int(j)] == 0:
                    # if the random number is greater than the activation probability
                    nodes_activation[int(j)] = 1
                    activated_nodes[int(j)] = 1
                    new_node_activated = True
        newly_activated_nodes = []
        for k in range(number_of_nodes):
            if nodes_activation[k] == 1:
                newly_activated_nodes.append(k)

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
