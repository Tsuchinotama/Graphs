# To execute the code, launch Simulation()

import random
import collections
import matplotlib.pyplot as plt
import numpy as np

global list_edges_G, list_nodes_G, list_edges_ST, list_nodes_ST, i, j

# Ladder with 2 steps
# list_edges_G=[[(1,2),(1,3),(2,3),(2,4),(3,6),(4,5),(4,6),(5,6)]]
# list_nodes_G=[[1,2,3,4,5,6]]

# Graph K4 (triangle)
list_edges_G=[[(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]]
list_nodes_G=[[1,2,3,4]] 
# Number of permutations considered
i=25
# Number of try on one permutation
j=25
# List of Nodes and Edges of the Spanning Tree
list_edges_ST=[]
list_nodes_ST=[]

# Function creating a random order on the edges of the graph

def GenAle():
    l=len(list_edges_G[0])
    compt = [1 for i in range(l)]
    list_alea = []
    while any(compt):
        j=random.randint(0, l-1)
        if compt[j] == 1:
            compt[j] = 0
            list_alea.append(list_edges_G[0][j])
    return list_alea      

# Function inserting an edge to the graph

def insert(edge_in):
    
    insert=0
    merge=0
    smerge=0
    a=edge_in[0]
    b=edge_in[1]
    # case 1  origin or extremity (not both) in the list_nodes_ST:  smerge=1
    # case 2  both in the list_nodes_ST:  merge=1
    # case 3  none in the list_nodes_ST:  insert=1
     
    # looking for case 1 or 2
    for ln in list_nodes_ST:
        if a in ln and b in ln:
    # case 2 detected with i=j
            i=list_nodes_ST.index(ln)
            j=i
            merge=1
            break
             
        elif a in ln and b not in ln:
            i=list_nodes_ST.index(ln)
    # case 1a check for case 2  a is before b   
            for ln1 in list_nodes_ST:
                if b in ln1:
    # case 2 detected   
                    j=list_nodes_ST.index(ln1)
                    merge=1
                    break
             
    #       break  ????
    # case 1a
            if merge==0:
                ln.append(b)
                if a<b:
                    list_edges_ST[i].append((a,b))
                else:
                    list_edges_ST[i].append((b,a))
                smerge=1
            break
             
        elif a not in ln and b  in ln:
    # case 1b
            i=list_nodes_ST.index(ln)
    # case 1a check for case 2      b is before a 
            for ln1 in list_nodes_ST:
                if a in ln1:
    # case 2 detected: inverse i and j
                     
                    j=list_nodes_ST.index(ln1)
                    merge=1
                    break
             
    # case 1b
            if merge==0:
                ln.append(a)
                if a<b:
                    list_edges_ST[i].append((a,b))
                else:
                    list_edges_ST[i].append((b,a))
                smerge=1
            break
             
        else:
            continue
             
    #  case 3 detected :  will have to insert new lists     
    if merge==0 and smerge==0:
        insert=1
         
    #  dealing wih case 3 detected :  new  items in the lists   
    if insert==1:
            if a==b:
                list_nodes_ST.append([a])
            else:
                if a<b:
                    list_nodes_ST.append([a,b])
                else:
                    list_nodes_ST.append([b,a])
            if a<b:
                list_edges_ST.append([(a,b)])
            else:
                list_edges_ST.append([(b,a)])
         
    #  dealing with case 2:  merge elements i and j if they are different   i<j
    if merge==1:
        if i!=j:
            list_nodes_ST[i]=list_nodes_ST[i]+list_nodes_ST[j]
            list_nodes_ST.pop(j)
            list_edges_ST[i]=list_edges_ST[i]+list_edges_ST[j]
            if a<b:
                list_edges_ST[i].append((a,b))
            else:
                list_edges_ST[i].append((b,a))
            list_edges_ST.pop(j)
        elif i==j:
    #  dealing with case 2:  merge edges only   
            if a<b:
                list_edges_ST[i].append((a,b))
            else:
                list_edges_ST[i].append((b,a))
    #print(list_edges_ST)00
    
    
    
    #print(list_nodes_ST)
    
# Function checking if there is a cycle et returnind his length before adding an edge
# Use a Breadth First Search

def Detect_cycle(edge_in):
    a=edge_in[0]
    b=edge_in[1]
    # Mise à jour d'une variable disant si l'on a ou non trouvé un cycle
    # Updating the variable showing if a cycle have been found or not
    boolcycle=False
    # Cycle is given as a list of edges
    cycle=[]
    for i in range(len(list_nodes_ST)):
        if a in list_nodes_ST[i] and b in list_nodes_ST[i]:
            # If both the 2 incident nodes of the added edge are in the same connex component, we have a cycle
            boolcycle=True
            # We color nodes with :
            # - white if they have not been processed
            # - grey if they are in the queue area
            # - black if they have been processed
            couleur=dict()
            for x in list_nodes_ST[i]:
                couleur[x]='blanc'
            # Remembering which node is parent of another in the tree with root a with a dictionnary P
            P=dict()
            P[a]=None
            couleur[a]='gris'
            Q=[a]
            # Looping while we didn't arrive to b : if the tree is a simple trail,
            # checking if the queue area is empty
            while couleur[b]=='blanc':
                u=Q[0]
                for j in range(0, len(list_edges_ST[i])):
                    # If u is incident to an edge, coloring in grey and let u be his parent
                    if u==list_edges_ST[i][j][0]:
                        if couleur[list_edges_ST[i][j][1]]=='blanc':
                            P[list_edges_ST[i][j][1]]=u
                            couleur[list_edges_ST[i][j][1]]='gris'
                            Q.append(list_edges_ST[i][j][1])
                    elif u==list_edges_ST[i][j][1]:
                        if couleur[list_edges_ST[i][j][0]]=='blanc':
                            P[list_edges_ST[i][j][0]]=u
                            couleur[list_edges_ST[i][j][0]]='gris'
                            Q.append(list_edges_ST[i][j][0])
                # Coloring u in black and removing it from queue area : u has been processed
                Q.remove(u)
                couleur[u]='noir'
            cycle=[(a,b),(b,u)]
            # Going to b from a following the parents
            while u!=a:
                cycle.append((u,P[u]))
                u=P[u]
            break
    return [boolcycle, cycle, len(cycle)]
    

#  Function deleting an edge from a cycle (if there is a new one) random uniformly after adding the edge in parameter

def Suppr_unif(edge_in):
    # Detect if there is a cycle or not
    ans=Detect_cycle(edge_in) 
    # inserting
    insert(edge_in)
    # if there is a cycle, deleting an edge of it random uniformly
    if ans[0]:
        p=random.randint(0, ans[2]-1)
        for q in range(len(list_edges_ST)):
            if tuple(ans[1][p]) in list_edges_ST[q]:
                list_edges_ST[q].remove(tuple(ans[1][p]))
                break
            if (tuple(ans[1][p][l] for l in [1,0])) in list_edges_ST[q]:
                list_edges_ST[q].remove(tuple(ans[1][p][l] for l in [1,0]))
                break
    #print(list_edges_ST)
    #print(list_nodes_ST)
    
# Definition de la fonction rajoutant un arbre à un dictionnaire
# comptant le nombre d'occurences de chaque arbre
# Function adding a tree to a dictionnary that counts appearances of each tree

def Rajoute_ST(dict_ST, ST):
    if ST in dict_ST:
        dict_ST[ST]=dict_ST.get(ST)+1
    else:
        dict_ST[ST]=1


def Simulation():
    dico={}
    # if len(list_nodes_G)>1:
    #    print("Le graphe n'est pas connexe")
    # else:
    for m in range(i):
        list_alea=GenAle()
        # list_alea=[(5,6),(4,5),(1,2),(6,7),(3,4),(2,3),(3,6),(7,8),(2,7)]
        # list_alea.reverse()
        # print(list_alea)
        for n in range(j):
            global list_nodes_ST, list_edges_ST
            list_edges_ST=[]
            list_nodes_ST=[]
            for k in range(len(list_alea)):
                Suppr_unif(list_alea[k])
            (list_edges_ST[0]).sort()
            Rajoute_ST(dico, tuple(list_edges_ST[0]))
    for key in dico.keys():
        dico[key]=dico[key]/(i*j)
    l=sorted(dico.items())
    fig, ax = plt.subplots()
    ax.bar(range(len(l)), [t[1] for t in l]  , align="center")
    ax.set_xticks(range(len(l)))
    ax.set_xticklabels([t[0] for t in l])
    fig.autofmt_xdate()
    plt.show()
            
