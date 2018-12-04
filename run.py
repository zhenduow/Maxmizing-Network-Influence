import math
import numpy as np
import networkx as nx
from numpy import random
import quantumrandom
import copy
import timeit

def greedy(G, desired_set_size, simulation_round):
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
                for iter in range(simulation_round):
                    score += len(IC(G, new_chosen))

                if score > max_score:
                    max_score = score
                    max_score_node = j

        chosen.append(max_score_node)
        print(chosen)

        print("Iter = ", i , ", vertex ", max_score_node, " is chosen with score ", max_score/simulation_round)

    return len(IC(G, chosen))

def high_degree(G, desired_set_size, simulation_round):
    degree_sequence = sorted(G.degree, key=lambda x: x[1], reverse=True)
    for i in range(desired_set_size+1):
        chosen_set = [name for (name, degree) in degree_sequence[:i]]
        if i > 0:
            print(chosen_set)
            res = 0
            for iter in range(simulation_round):
                res += len(IC(G, chosen_set))
            print(res/simulation_round)
    return res/simulation_round


def ithnodeSpread(parameters):
    G,activated_nodes,nodes_activation,new_node_activated,j = parameters
    if random.uniform(0,1) < G.edges[u, v]['weight'] and j not in activated_nodes:
        # if the random number is greater than the activation probability
        nodes_activation.append(j)
        activated_nodes.append(j)
        new_node_activated = True
    return nodes_activation,activated_nodes,new_node_activated
    

def IC(G, initial_set):
    new_node_activated = True
    activated_nodes = copy.deepcopy(initial_set)
    newly_activated_nodes = copy.deepcopy(activated_nodes)
    while new_node_activated:
        # when some node is activated
        new_node_activated = False
        nodes_activation = []
        for i in newly_activated_nodes:

            import multiprocessing
            cores = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=cores)
            
            spreadlist = pool.map(ithnodeSpread,[(G,activated_nodes,nodes_activation,new_node_activated,j) for j in G.neighbors(str(i))])

            for nodes_activation_1,activated_nodes_1,new_node_activated_1 in spreadlist:
                if(new_node_activated==False and new_node_activated_1==True):
                    new_node_activated = True
                activated_nodes.extend(activated_nodes_1)
                nodes_activation.extend(nodes_activation_1)

            # for j in G.neighbors(str(i)):
            #     randn = random.uniform(0,1)
            #     if randn < G.edges[u, v]['weight'] and j not in activated_nodes:
            #         # if the random number is greater than the activation probability
            #         nodes_activation.append(j)
            #         activated_nodes.append(j)
            #         new_node_activated = True
        newly_activated_nodes = copy.deepcopy(nodes_activation)

    return activated_nodes

def hdGreedy2(G, k):
    #degree_sequence = sorted([d for n, d in G.degree()])
    S=[]
    print("num_node",nx.number_of_nodes(G))
    for i in range(k):
        X=G.subgraph(G.nodes()-S)
        dict = {}
        cc=0
        for j in range(200):
            g=runIC(G,S)
            cc+=len(g)
            for key in g:
                dict[key] = dict.get(key, 0) + 1
        #d = {k for k,v in dict.items() if v > 10+5*i}
        #dd=sorted(G.degree, key=lambda x: x[1], reverse=True)
        #dd=sorted(dict.iteritems(), key=lambda (k,v): (v,k))
        dd=sorted(dict.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)
        d=dd[:int(len(dd)/5)]
        print(d)
        print(cc/200,len(d))

        #print(d)
        #g=runIC(G,S)
        #ss=
        X=G.subgraph(X.nodes()-d)
            
        degree_sequence=sorted(X.degree, key=lambda x: x[1], reverse=True)
        v=degree_sequence[0][0]
        #if i==0:
        #    v='999'
        print("num_X", nx.number_of_nodes(X))
        print("choosen v",degree_sequence[0])
        #print(degree_sequence)
        S.append(v)       
        #print(len(g))
    xx=0    
    for i in range(100):
        xx+=(len(runIC(G,S)))
    print("activation nodes avg",xx/100)
    return xx/100    

def hdGreedy1(G, k):
    #degree_sequence = sorted([d for n, d in G.degree()])
    S=[]
    print("num_node",nx.number_of_nodes(G))
    for i in range(k):
        g=runIC(G,S)
        X=G.subgraph(G.nodes()-g)
        degree_sequence=sorted(X.degree, key=lambda x: x[1], reverse=True)
        v=degree_sequence[0][0]
        #if i==0:
        #    v='999'
        print("num_X", nx.number_of_nodes(X))
        print("choosen v",degree_sequence[0])
        #print(degree_sequence)
        S.append(v)       
        #print(len(g))
        print(len(runIC(G,S)))
    return len(g)
   
def hdGreedy(G, k):
    #degree_sequence = sorted([d for n, d in G.degree()])
    S=[]
    print("num_node",nx.number_of_nodes(G))
    for i in range(k):
        g=runIC(G,S)
        X=G.subgraph(G.nodes()-g)
        degree_sequence=sorted(X.degree, key=lambda x: x[1], reverse=True)
        v=degree_sequence[0][0]
        #if i==0:
        #    v='999'
        print("num_X", nx.number_of_nodes(X))
        print("choosen v",degree_sequence[0])
        #print(degree_sequence)
        S.append(v)       
        #print(len(g))
    xx=0    
    for i in range(100):
        xx+=(len(runIC(G,S)))
    print("activation nodes avg",xx/100)
    return xx/100  


if __name__ == "__main__":
    G = nx.read_edgelist("./1005edges")
    #G = nx.read_edgelist("./toy")
    for u,v,e in G.edges(data = True):
        e['weight'] = random.uniform(0,1)/20
    desired_set_size = 10
    simulation_round = 20
    start_time = timeit.default_timer()
    print("High-degree algorithm final spread {}".format(high_degree(G, desired_set_size, simulation_round)))
    print("High-degree algorithm time elapsed {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    print("Greedy algorithm (paper) final spread {}".format(greedy(G, desired_set_size, simulation_round)))
    print("Greedy algorithm (paper) time elapsed {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    print("High-degree greedy algorithm final spread {}".format(hdGreedy(G, desired_set_size)))
    print("High-degree greedy algorithm time elapsed {}".format(timeit.default_timer() - start_time))
