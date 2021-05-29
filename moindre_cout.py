import numpy as np
import copy
import time
def transform(distances):
    edge=[]
    for i in range(0,np.size(distances,0)):
        for j in range(i+1,np.size(distances,0)):
            edge.append([i+1,j+1,distances[i,j]])
    return edge

def cycle(aret, arr, n,m):

    sommet1 = arr[0]
    sommet2 = arr[1]
    cyc=copy.deepcopy(aret)
    courant=copy.deepcopy(sommet1)
    fin=False
    flat_list=np.array(cyc)

    while not fin:
        ind=np.where(flat_list==courant)[0]

        if np.size(ind)==0:
            fin=True
            boole=True
        else:
            if ind[0]%2==0 :
                courant=flat_list[ind[0]+1]
                flat_list=np.delete(flat_list,[ind[0],ind[0]+1])
            elif ind[0]%2==1 :
                courant=flat_list[ind[0]-1]
                flat_list=np.delete(flat_list,[ind[0],ind[0]-1])
            if courant==sommet2:
                fin=True
                if(len(aret)<2*n-2):boole=False
                else :boole=True
    return boole


def degre(arete, arr,n):
    sommet1 = arr[0]
    sommet2 = arr[1]
    deg1 = 0
    deg2 = 0
    bool = True
    for i in arete:
        if i== sommet1:
            deg1 = deg1 + 1
        elif i == sommet2:
            deg2 = deg2 + 1
        if (deg1 > 1 or deg2 > 1) :
            bool = False
            break
    return bool

def tolist(tab):

    sommet1 = tab[0]
    cyc=copy.deepcopy(tab)
    courant=copy.deepcopy(sommet1)
    fin=False
    flat_list=np.array(cyc)
    root=[]
    root.append(sommet1)
    while not fin:
        ind=np.where(flat_list==courant)[0]
        if np.size(ind)==0:
            fin=True
        else:
            if ind[0]%2==0 :
                root.append(flat_list[ind[0]+1])
                courant=flat_list[ind[0]+1]
                flat_list=np.delete(flat_list,[ind[0],ind[0]+1])
            elif ind[0]%2==1 :
                root.append(flat_list[ind[0]-1])
                courant=flat_list[ind[0]-1]
                flat_list=np.delete(flat_list,[ind[0],ind[0]-1])
    return root

def moindre_cout(distances):
    startTime = time.time()
    n=np.size(distances,0)
    edgelist=transform(distances)
    dist_min = 0
    arete = []
    dist = copy.deepcopy(edgelist)
    dist.sort(key = lambda dist: dist[2])
    for key in dist:
        if  degre(arete, key,n) :
            if cycle(arete, key,n,len(arete)):
                arete.append(key[0])
                arete.append(key[1])
                dist_min = dist_min + key[2]
                if len(arete) == 2*n:
                    break
    finishTime=time.time()
    return  dist_min, list(np.array(tolist(arete))-1),finishTime-startTime
