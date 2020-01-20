

import random

# Definition de la fonction verifiant si l'on a un cycle et renvoyant sa longueur
# avant le rajout d'une arete

def Detect_cycle(edge_in, list_edges, list_nodes):
    a=edge_in[0]
    b=edge_in[1]
    lg=-1
    ncycle=False
    cycle=[]
    for ln in list_nodes:
        if a in ln and b in ln:
            lg=0
            ncycle=True
            couleur=dict()
            for x in ln:
                couleur[x]='blanc'
            P=dict()
            P[a]=None
            couleur[a]='gris'
            Q=[a]
            i=list_nodes.index(ln)
            while couleur[b]=='blanc' and Q:
                lg=lg+1
                u=Q[0]
                for j in range(0, len(list_edges[i])-1):
                    if u==list_edges[i][j][0]:
                        if couleur[list_edges[i][j][1]]=='blanc':
                            P[list_edges[i][j][1]]=u
                            couleur[list_edges[i][j][1]]='gris'
                            Q.append(list_edges[i][j][1])
                    elif u==list_edges[i][j][1]:
                        if couleur[list_edges[i][j][0]]=='blanc':
                            P[list_edges[i][j][0]]=u
                            couleur[list_edges[i][j][0]]='gris'
                            Q.append(list_edges[i][j][0])
                Q.remove(u)
                couleur[u]='noir'
            cycle=[(a,b),(b,u)]
            while u!=a :
                cycle.append((u,P[u]))
                u=P[u]
            # print('Le cycle cree est :', cycle)
            # print('Sa longueur est :', lg+1)
            break
    # if not ncycle:
        # print('Pas de nouveau cycle cree')
    return [ncycle, cycle, lg+1]

# Definition de la suppression d'une arete d'un cycle de maniere uniforme

def Suppr_unif(edge_in, list_edges, list_nodes):
    ans=Detect_cycle(edge_in, list_edges, list_nodes)
    if ans[1]:
        j=random.randint(0, ans[2]-1)
        for i in range(0, len(list_edges)-1):
            if ans[1][j] in list_edges[i]:
                list_edges[i].remove(ans[1][j])
                break
    print('List_edges =', list_edges)
    print('List_nodes =', list_nodes)
        
            
            
            
     
                
                
            


     
    
    
