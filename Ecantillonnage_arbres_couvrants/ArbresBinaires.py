import random
import collections
import matplotlib.pyplot as plt
import numpy as np

# Fonction donnant le nombre de sommets d'un graphe

def Nb_sommets(list_edges, list_nodes):
    N=0
    for i in range(len(list_nodes)):
        N=N+len(list_nodes[i])
    return N

# Fonction testant si un graphe est un arbre ou non

def arbre(list_edges, list_nodes):
    return (len(list_nodes)==1 and (len((suppr_arete(list_edges, list_nodes, list_edges[0][0]))[1]))>=2)
    
# Fonction testant si un arbre est un arbre binaire

    