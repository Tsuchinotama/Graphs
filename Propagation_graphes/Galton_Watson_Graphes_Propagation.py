import numpy as np
import math
from numpy.random import rand
from numpy.random import randint

def generation_growth(m,imax):
    g=np.zeros(imax+1,int)
    i=0
    g[i]=1
    while ((not g[i]==0) and i<imax):
        for j in range(g[i]):
              if rand()<m/2:
                  g[i+1]=g[i+1]+2
        i=i+1
    if i<imax:
        for k in range(i+1,imax+1)   :
            g[k]=0
    return g

def active_growth(m,tmax):
    x=np.zeros(tmax+1,int) 
    t=0
    x[t]=1
    while ((not x[t]==0) and t<tmax):
        x[t+1]=x[t]-1
        if rand()<m/2:
            x[t+1]=x[t+1]+2
        t=t+1
    if t<tmax:
        for k in range(t+1,tmax+1)   :
            x[k]=0
    return x
    
def estimate_generation(m,imax,n):
    g=np.zeros(imax+1)
    for i in range(n):
        g=g+generation_growth(m,imax)
    return g/n

def estimate_active(m,tmax,n):
    x=np.zeros(tmax+1)
    for i in range(n):
        x=x+active_growth(m,tmax)
    return x/n
          
def estimate_extinction(m,tmax,n):
    ext=0
    for i in range(n):
        if active_growth(m,tmax)[tmax]==0:
            ext=ext+1
    return ext/n
    
def pext_bim_exact(list_m):
    pext=[]
    for m in list_m:
        if not m==0:
            pext.append((1-(1-m*(2-m))**0.5)/m)
        else:
             pext.append(1)
    return pext
    
def estimate_mult_extinction(list_m,tmax,n):
    list_ext=[]
    for m in list_m:
        ext=0
        for i in range(n):
            if active_growth(m,tmax)[tmax]==0:
                ext=ext+1
        list_ext.append(ext/n)
    return list_ext
