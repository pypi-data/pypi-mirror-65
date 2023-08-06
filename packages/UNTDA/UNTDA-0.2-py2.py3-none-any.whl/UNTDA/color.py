import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d

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