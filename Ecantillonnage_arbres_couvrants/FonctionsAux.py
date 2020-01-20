import math 
import sys

def coeff_binomial(n, k):
    if n==k:
        return(1)
    elif k==1:         # see georg's comment
        return(n)
    elif k>n:          # will be executed only if y != 1 and y != x
        return(0)
    else:                # will be executed only if y != 1 and y != x and x <= y
        a=math.factorial(n)
        b=math.factorial(k)
        c=math.factorial(n-k)  # that appears to be useful to get the correct result
        return(a//(b*c))

# A partir de la liste des arêtes, renvoie celle-ci et la liste des noeuds correspondantes

def edges_to_nodes (list_edges):
    l=len(list_edges)
    list_nodes=[]
    for i in range(l):
        list_nodes.append([])
        for j in range(len(list_edges[i])):
            if list_edges[i][j][0] not in list_nodes[i]:
                list_nodes[i].append(list_edges[i][j][0])
            if list_edges[i][j][1] not in list_nodes[i]:
                list_nodes[i].append(list_edges[i][j][1])
    return(list_edges,list_nodes) 
   
# Renvoie si les 2 listes (d'arêteset de sommets) correspondent au même graphe (cohérence entre les listes)
    
def coher_edges_nodes(list_edges, list_nodes):
    l=edges_to_nodes(list_edges)[1]
    egal=True
    for i in range(len(list_nodes)):
        if list_nodes[i] not in l:
            egal=False
            break
    if egal:
        for j in range(len(l)):
            if l[j] not in list_nodes:
                egal=False
                break
    return egal

# A partir de maintenant, sauf indication contraire, on suppose les listes cohérentes
    
# Fonction renvoyant si la 1ère liste est bien dans la 2ème (les listes sont quelconques)
    
def included(l1, l2):
    inc=True
    for i in range(len(l1)):
        if l1[i] not in l2:
            inc=False
            break
    return inc

# Suppression d'une arete d'un graphe en supposant que les composantes des 2 listes (arêtes et sommets) se correspondent 

def suppr_arete(list_edges, list_nodes, arete):
    l=len(list_nodes)
    for i in range(len(list_nodes)):
        if arete[0] in list_nodes[i]:
            break
    j=list_edges[i].index(arete)
    list_edges[i].remove(arete)
    list_nodes[i].remove(arete[0])
    ls=list_nodes[i]
    la=list_edges[i]
    list_nodes[i]=[arete[0]]
    list_edges[i]=[]
    couleur=dict()
    for s in ls:
        couleur[s]='blanc'
    Q=[ls[0]]
    couleur[ls[0]]='gris'
    finparcours=False
    coupe=True
    while Q:
        bouge=False
        for a in la:
            if a[0] in list_nodes[i]:
                if a[1] in ls:
                    list_nodes[i].append(a[1])
                    ls.remove(a[1]) 
                list_edges[i].append(a)
                la.remove(a)
                couleur[a[0]]='gris'
                Q.append(a[0])
                bouge=True
            elif a[1] in list_nodes[i]:
                list_nodes[i].append(a[0])
                list_edges[i].append(a)
                la.remove(a)
                ls.remove(a[0])
                couleur[a[1]]='gris'
                Q.append(a[1])
                bouge=True
        couleur[Q[0]]='noir'
        Q.pop(0)
        if couleur[arete[1]]=='gris':
            coupe=False
            break
    if coupe:
        list_nodes.append(ls)
        list_edges.append(la)
    return(list_edges,list_nodes)
        
# Supression d'un sommet et des aretes le touchant

def suppr_sommet(list_edges, list_nodes, sommet):
    for i in range(len(list_nodes)):
        if sommet in list_nodes[i]:
            break
    list_nodes[i].remove(sommet)
    li=[]
    for j in range(len(list_edges[i])):
        if not ((list_edges[i][j][0]==sommet) or (list_edges[i][j][1]==sommet)):
            li.append(list_edges[i][j])
        j=j+1
    list_edges[i]=li
    ls=list_nodes[i]
    la=list_edges[i]
    l=len(list_nodes)-1
    list_nodes[i]=list_nodes[l]
    list_nodes.pop(l)
    list_edges[i]=list_edges[l]
    list_edges.pop(l)
    nbcoupe=0
    couleur=dict()
    for s in ls:
        couleur[s]='blanc'
    while ls:
        Q=[ls[0]]
        couleur[ls[0]]='gris'
        list_nodes.append([ls[0]])
        list_edges.append([])
        trouve=False
        while Q:
            for a in la:
                if a[0] in list_nodes[l+nbcoupe] and not a[1] in list_nodes[l+nbcoupe]:
                    list_nodes[l+nbcoupe].append(a[1])
                    list_edges[l+nbcoupe].append(a)
                    if a[1]==Q[0]:
                        trouve=True
                    la.remove(a)
                    ls.remove(a[1])
                    couleur[a[0]]='gris'
                    Q.append(a[0])
                elif a[1] in list_nodes[l+nbcoupe] and not a[0] in list_nodes[l+nbcoupe]:
                    list_nodes[l+nbcoupe].append(a[0])
                    list_edges[l+nbcoupe].append(a)
                    if a[0]==Q[0]:
                        trouve=True
                    la.remove(a)
                    ls.remove(a[0])
                    couleur[a[1]]='gris'
                    Q.append(a[1])
            couleur[Q[0]]='noir'
            Q.pop(0)
        if not trouve:
            ls.pop(0)
        nbcoupe=nbcoupe+1
    return(list_edges, list_nodes)
            
# Fonction vérifiant si le 1er graphe donné est un sous-graphe du 2ème                
    
def ss_graphe(list_edges1, list_nodes1, list_edges2, list_nodes2):
    list_nodes1bis=[]
    list_nodes2bis=[]
    list_edges1bis=[]
    list_edges2bis=[]
    for i in range(len(list_nodes1)):
        for j in range(len(list_nodes1[i])):
            list_nodes1bis.append(list_nodes1[i][j])
    for i in range(len(list_nodes2)):
        for j in range(len(list_nodes2[i])):
            list_nodes2bis.append(list_nodes2[i][j])
    for i in range(len(list_nodes1)):
        for j in range(len(list_nodes1[i])):
            list_nodes1bis.append(list_nodes1[i][j])
    for i in range(len(list_edges1)):
        for j in range(len(list_edges1[i])):
            list_edges1bis.append(list_edges1[i][j])
    for i in range(len(list_edges2)):
        for j in range(len(list_edges2[i])):
            list_edges2bis.append(list_edges2[i][j])
    return included(list_nodes1bis, list_nodes2bis) and included(list_edges1bis, list_edges2bis)
   
# Fonction bis, en supposant les listes de chaque graphe se correspondant

def ss_graphe_bis(list_edges1, list_nodes1, list_edges2, list_nodes2):
    inc=True
    for i in range(len(list_nodes1)):
        trouvesommet=False
        for j in range(len(list_nodes2)):
            if list_nodes1[i][0] in list_nodes2[j]:
                trouvesommet=True
                for k in range(1, len(list_nodes1[i])):
                    for l in range(len(list_edges1[i])):
                        if not list_nodes1[i][k] in list_nodes2[j] or not list_edges1[i][l] in list_edges2[j]:
                            inc=False
                            break
                    break  
        if not trouvesommet:
            break
    return inc and trouvesommet
    
# Fonction vérifiant si le 1er graphe donné est un sous-graphe induit du 2ème

def ss_graphe_induit(list_edges1, list_nodes1, list_edges2, list_nodes2):
    inc=True
    for i in range(len(list_nodes1)):
        trouvesommet=False
        for j in range(len(list_nodes2)):
            if list_nodes1[i][0] in list_nodes2[j]:
                trouvesommet=True
                for k in range(1, len(list_nodes1[i])):
                    for l in range(len(list_edges1[i])):
                        for m in range(len(list_edges2[j])):
                            if list_edges2[j][m][0] in list_nodes1[i] and list_edges2[j][m][1] in list_nodes1[i]:
                                if not list_edges2[j][m] in list_edges1[i]:
                                    inc=False
                                    break
                        if not list_nodes1[i][k] in list_nodes2[j] or not list_edges1[i][l] in list_edges2[j]:
                            inc=False
                            break
                    break  
        if not trouvesommet:
            break
    return inc and trouvesommet                    
        
# Fonction renvoyant le complémentaire d'un graphe, en supposant les listes se correspondant

def complementaire(list_edges, list_nodes):
    la=[]
    ln=[]
    listlinarete=[]
    if len(list_nodes)>=2:
        for i in range(len(list_edges)):
            for j in range(len(list_edges[i])):
                listlinarete.append(list_edges[i][j])
        ln[0].append(list_nodes[0][0])
        for i in range(1, len(list_nodes[0])):
            ln[0].append(list_nodes[0][i])
            for j in ln[0]:
                if not list_nodes[0][i]==j and not (j,list_nodes[0][i]) in listlinarete and not (list_nodes[0][i],j) in listlinarete:
                    la[0].append((j,list_nodes[0][i]))
        for i in range(1, len(list_nodes)):
            for j in range(len(list_nodes[i])):
                ln[0].append(list_nodes[i][j])
                for k in ln[0]:
                    if not list_nodes[i][j]==k and not (k,list_nodes[i][j]) in listlinarete and not (list_nodes[i][j],k) in listlinarete:
                        la[0].append((k,list_nodes[i][j]))
    else:
        listlinsommets=list_nodes[0]
        for i in range(len(listlinsommets)):
            for j in range(i+1,len(listlinsommets)):
                if not (listlinsommets[i],listlinsommets[j]) in list_edges[0] and not (listlinsommets[j],listlinsommets[i]) in list_edges[0]:
                    listlinarete.append((listlinsommets[i],listlinsommets[j]))
        nbCC=0
        while listlinsommets:
            la.append([])
            ln.append([])
            Q=[listlinsommets[0]]
            ln[nbCC].append(listlinsommets[0])
            listlinsommets.pop(0)
            while Q:
                u=Q[0]
                for i in range(len(listlinarete)):
                    if i<len(listlinarete):
                        if u==listlinarete[i][0]:
                            la[nbCC].append(listlinarete[i])
                            if not listlinarete[i][1] in ln[nbCC]:
                                ln[nbCC].append(listlinarete[i][1])
                                listlinsommets.remove(listlinarete[i][1])
                                Q.append(listlinarete[i][1])
                            listlinarete.remove(listlinarete[i])
                        elif u==listlinarete[i][1]:
                            la[nbCC].append(listlinarete[i])
                            if not listlinarete[i][0] in ln[nbCC]:
                                ln[nbCC].append(listlinarete[i][0])
                                listlinsommets.remove(listlinarete[i][0])
                                Q.append(listlinarete[i][0])
                            listlinarete.remove(listlinarete[i])
                Q.pop(0)
            nbCC=nbCC+1
    return(la,ln)

# Definition de la fonction verifiant si l'on a un cycle et renvoyant sa longueur
# avant le rajout d'une arete, on utilise un parcours en largeur

def Detect_cycle(edge_in):
    a=edge_in[0]
    b=edge_in[1]
    # Mise à jour d'une variable disant si l'on a ou non trouvé un cycle
    boolcycle=False
    # Le cycle est donné sous la forme d'une liste d'arêtes
    cycle=[]
    for i in range(len(list_nodes_ST)):
        if a in list_nodes_ST[i] and b in list_nodes_ST[i]:
            # Si les 2 éxtrémités de l'arête ajoutée sont dans la même CC, on a un cycle
            boolcycle=True
            # On colorie les noeuds par:
            # -blanc s'ils n'ont pas été traités, ni vus
            # -gris s'ils sont dans la fle d'attente Q, càd vus mais pas encore traités
            # -noir s'ils ont été traités
            couleur=dict()
            for x in list_nodes_ST[i]:
                couleur[x]='blanc'
            # On retient qui est le parent d'un noeud dans le parcours de l'arbre enraciné en a gràce à P
            P=dict()
            P[a]=None
            couleur[a]='gris'
            Q=[a]
            # On boucle tant qu'on n'a pas atteint b: si l'arbre est un chemin, on vérifie que la file d'attente est vide
            while couleur[b]=='blanc':
                u=Q[0]
                for j in range(0, len(list_edges_ST[i])):
                    # Si u est éxtrémité d'une arête, on colorie l'autre éxtrémité en gris et on met u comme son parent
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
                # On colorie u en noir et on l'enlève de la file d'attente ; u a bien été traité
                Q.remove(u)
                couleur[u]='noir'
            cycle=[(a,b),(b,u)]
            # On remonte de b jusqu"à a en suivant les parents
            while u!=a:
                cycle.append((u,P[u]))
                u=P[u]
            break
    return [boolcycle, cycle, len(cycle)]

# Fonction testant si un graphe est un arbre ou non

def arbre(list_edges, list_nodes):
    return (len(list_nodes)==1) and (len(list_edges[0])==len(list_nodes[0])-1)
    
# Fonction renvoyant tous les sommets sous la forme d'une liste

def liste_sommets(list_nodes):
    l=[]
    for i in range(len(list_nodes)):
        for j in range(len(list_nodes[i])):
            l.append(list_nodes[i][j])
    return l
    
def liste_aretes(list_edges):
    l=[]
    for i in range(len(list_edges)):
        for j in range(len(list_edges[i])):
            l.append(list_edges[i][j])
    return l

def partiesliste_taille(taille, liste):
    l=[]
    i=0
    imax=2**len(liste)-1
    while i<=imax:
        s=[]
        j=0
        jmax=len(liste)-1
        while j<=jmax:
            if (i>>j)&1 == 1:
                s.append(liste[j])
            j += 1
        if len(s)==taille:
            l.append(s)
        i += 1 
    return l
            
def nb_scheeger(list_nodes, list_edges):
    ls=liste_sommets(list_nodes)
    la=liste_aretes(list_edges)
    ns=len(ls)
    na=len(la)
    nb_sch=0
    partition=partiesliste_taille(math.floor(ns/2), ls)
    for ss_ens in partition:
        nb_prov=0
        for arete in la:
            if ((arete[0] in ss_ens) and (not arete[1] in ss_ens)) or ((arete[1] in ss_ens) and (not arete[0] in ss_ens)):
                nb_prov=nb_prov+1
        if nb_prov<nb_sch:
            nb_sch=nb_prov
    return nb_sch


    
    


        


     

                    
            
            
         
    
    
    