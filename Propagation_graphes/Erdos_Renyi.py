import numpy as np
import math
from numpy.random import rand
from numpy.random import randint

def erdos_renyi(n,p):
    graphe=[]
    for i in range(n):
        graphe.append([])
    for i in range(n):
        for j in range(i+1,n):
            if rand()<p:
                graphe[i].append(j)
                graphe[j].append(i)
    return graphe
            
def size_components(l):
    non_vus=list(range(len(l)))
    CC_Taille=[]
    while (not non_vus==[]):
        Q=[non_vus[0]]
        CC=[non_vus[0]]
        taille=1
        while (not Q==[]):
            for v in l[Q[0]]:
                if v in non_vus:
                    CC.append(v)
                    taille=taille+1
                    non_vus.remove(v)
                    Q.append(v)
            if Q[0] in non_vus:
                non_vus.remove(Q[0])                
            Q.remove(Q[0])
        CC_Taille.append((CC,taille))   
    return CC_Taille 
     
# def size_infection(n,p):
#     taille_infection=1
#     infectes_actuels=[0]
#     while (not n==0):
#         g=erdos_renyi(n,p)
#         for i in infectes_actuels:
#             for j in range(len(size_components(g))):
#                 if i in size_components(g)[j][0]:
#                     taille_infection=taille_infection+size_components(g)[j][1]-1
#                     n=n-
    
def is_connected_flemmard(l):
    return len(size_components(l))==1
    
def is_connected(l):
    racine=0
    non_vus=list(range(len(l)))
    Q=[0]
    while not (non_vus==[]) or not (Q==[]):
        for v in l[Q[0]]:
            if v in non_vus:
                Q.append(v)
                non_vus.remove(v)
        if Q[0] in non_vus:
            non_vus.remove(Q[0])
        Q.remove(Q[0])
    return non_vus==[]
        
                
                    
                