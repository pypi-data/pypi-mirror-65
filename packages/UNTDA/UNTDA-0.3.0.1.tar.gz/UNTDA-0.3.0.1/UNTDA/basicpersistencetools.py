import pandas as pd
import numpy as np
from random import sample
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors

class Color:
    def __init__(self, d):
        self.d = d
        
    def colores(d):
        A=[]
        K=[]
        num=[]
        t=0
        for i in d.keys():
            num.append(len(d[i]))
            col=(len(d[i])-num[t-1])*(list(mcolors.CSS4_COLORS.keys())[t]+" ").split()
            col2=(len(d[i])-num[t-1])*(i+" ").split()
            t+=1
            A.extend(col) 
            K.extend(col2)
        return [A,K]
    
    def to_color(self,x):
        return ["background-color:"+i for i in Color.colores(self.d)[0]]
    
    def colorframe(self):
        DF=pd.DataFrame(self.d.values(),index=self.d.keys())
        CS=pd.DataFrame({"Simplex":pd.Series(DF.iloc[len(DF)-1]),"K":pd.Series(Color.colores(self.d)[1])},index=None)
        return CS.style.apply(self.to_color)

def operadorfrontera(d):
    B=[]
    for i in d[list(d)[len(d)-1]]:
        A=[]
        for j in d[list(d)[len(d)-1]]:
            if len(i)==len(j)-1:
                if(set(i).issubset(set(j))):
                    A.append(1)
                else:
                    A.append(0)
            else:
                A.append(0)
        B.append(A)
    return np.array(B)

def operadorfronteraDF(d):
    B=[]
    lista=[]
    for i in d[list(d)[len(d)-1]]:
        lista.append(str(i))
        A=[]
        for j in d[list(d)[len(d)-1]]:
            if len(i)==len(j)-1:
                if(set(i).issubset(set(j))):
                    A.append(1)
                else:
                    A.append(0)
            else:
                A.append(0)
        B.append(A)
    CDF=Color(d)
    print(B.append(Color.colores(d)[1]))
    DF=pd.DataFrame(data=B,columns=lista,index=lista+["$K$"])
    return DF.style.apply(CDF.to_color,axis=1)

def low(A):
    l=[]
    ls=[]
    for j in range(len(A)):
        l.append([i for i,e in enumerate(np.transpose(A)[j]) if e!=0])
        if len(l[j])==0:
            ls.append(0)
        else:
            ls.append(l[j][-1]+1)
    return ls

def reduction1(A):
    B=np.transpose(A)
    for j in range(len(A)):
        if low(A)[j]!=0:
            for i in range(j):
                if low(A)[i]==low(A)[j]:
                    B[j]=(B[i]+B[j])%2
    C=np.transpose(B)
    return C

def reduction(d):
    A=operadorfrontera(d)
    n1=len([i for i in low(reduction1(A)) if i!=0])
    n2=len(set([i for i in low(reduction1(A)) if i!=0]))
    while n1 != n2:
        A=reduction1(A)
        n1=len([i for i in low(reduction1(A)) if i!=0])
        n2=len(set([i for i in low(reduction1(A)) if i!=0]))
    return A

def generatefiltrationcomplexes():
    n=int(input("Cantidad de complejos no vacios:"))
    complexes={"K0":[]}
    for i in range(n):
        k=int(input("Cantidad de simplices adicionales en K"+str(i+1)+":"))
        ad=[]
        for j in range(k):
            news=np.fromstring(input("Ingrese la información del simplex adicional "+str(j+1)+", cada vértice debe estar separado por coma (,):"), dtype=int, sep=',')
            news=news.tolist()
            ad.append(news)
        complexes["K"+str(i+1)]=complexes["K"+str(i)+""]+ad
    CDF=Color(complexes)
    CDF.colorframe()
    return complexes

def etapa(ind,num):
    if num<=ind[0]:
        E=1
    else: 
        for i in range(len(ind)):
            if num>ind[i]:
                E=i+2
        
    return E 

def persistencepairs(d):
    LR=low(reduction(d))
    pairs=[]
    elements=[]
    ind=[]
    perspairs=[]
    K=list(d.values())[-1]
    Homology=[]
    
    for i in range(1,len(d)):
        ind.append(list(d.values())[i].index(list(d.values())[i][-1])+1)
        
    for i in range(len(LR)):
        if LR[i]!=0:
            elements.extend([LR[i],i+1])
            pairs.append((LR[i],i+1))
            if etapa(ind,LR[i])!=etapa(ind,i+1):
                perspairs.append((etapa(ind,LR[i]),etapa(ind,i+1)))
                Homology.append(len(K[LR[i]])-1)
    for i in range(1,len(LR)):
        if i not in elements:
            perspairs.insert(0,(i,len(d)+1))
            Homology.insert(0,len(K[LR[i]])-1)
            
    return perspairs, Homology

def persitencediagram(d): 
    HC=[]
    for i in persistencepairs(d)[1]:
        if i not in HC:
            HC.append(i)
    colors=sample(list(mcolors.TABLEAU_COLORS.keys()),max(persistencepairs(d)[1])+1)
    Homologycolors=[colors[i] for i in persistencepairs(d)[1]]
    plt.scatter(list(zip(*persistencepairs(d)[0]))[0],list(zip(*persistencepairs(d)[0]))[1],c=Homologycolors)
    n=len(d)
    plt.xlim(0,n)
    plt.ylim(0,n)
    plt.plot([0,n],[0,n])    
    LegendElement=[Line2D([0], [0], marker='o', color=colors[i], label='H'+str(i)) for i in HC]
    plt.legend(handles=LegendElement,fontsize=10)

def persitencebarcode(d): 
    V=np.array(persistencepairs(d)[1]).argsort()
    V2=[persistencepairs(d)[0][i] for i in V]
    V3=[persistencepairs(d)[1][i] for i in V]
    HC=[]
    
    for i in persistencepairs(d)[1]:
        if i not in HC:
            HC.append(i)
    colors=sample(list(mcolors.TABLEAU_COLORS.keys()),max(persistencepairs(d)[1])+1)
    Homologycolors=[colors[i] for i in V3]
    n=len(d)
    plt.xlim(0,n+1)
    plt.ylim(0,n)
    nn=len(persistencepairs(d)[0])
    for i in range(nn):
        plt.plot([V2[i][0],V2[i][1]],[i+1,i+1],c=Homologycolors[i])    
    LegendElement=[Line2D([0], [0], marker='o', color=colors[i], label='H'+str(i)) for i in HC]
    plt.legend(handles=LegendElement,fontsize=10)
    plt.yticks([])
    plt.show()