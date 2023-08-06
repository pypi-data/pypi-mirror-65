import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d

def triangulo():
    fig, [[ax0,ax1,ax2],[ax3,ax4,ax5]]=plt.subplots(2,3,figsize=(15,10))
    ax0.axis("off")
    ax0.set_title('K0')

    ax1.plot(0.2,0.2,'bo')
    ax1.axis("off")
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    ax1.annotate("1",(0.16,0.15))
    ax1.set_title('K1')

    ax2.plot([0.2,0.5,0.8],[0.2,0.8,0.2],'bo')
    lc = mc.LineCollection([[(0.2,0.2),(0.5,0.8)]], colors='g')
    ax2.add_collection(lc)
    ax2.axis("off")
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])
    ax2.annotate("1",(0.16,0.15))
    ax2.annotate("2",(0.5,0.85))
    ax2.annotate("3",(0.84,0.15))
    ax2.set_title('K2')

    ax3.plot([0.2,0.5,0.8],[0.2,0.8,0.2],'bo')
    lc = mc.LineCollection([[(0.2,0.2),(0.5,0.8)],[(0.5,0.8),(0.8,0.2)],[(0.2,0.2),(0.8,0.2)]], colors='g')
    ax3.add_collection(lc)
    ax3.axis("off")
    ax3.set_xlim([0, 1])
    ax3.set_ylim([0, 1])
    ax3.annotate("1",(0.16,0.15))
    ax3.annotate("2",(0.5,0.85))
    ax3.annotate("3",(0.84,0.15))
    ax3.set_title('K3')

    ax4.plot([0.2,0.5,0.8],[0.2,0.8,0.2],'bo')
    lc = mc.LineCollection([[(0.2,0.2),(0.5,0.8)],[(0.5,0.8),(0.8,0.2)],[(0.2,0.2),(0.8,0.2)]], colors='g')
    ax4.add_collection(lc)
    ax4.add_patch(Polygon([[0.2,0.2], [0.5,0.8], [0.8,0.2]], closed=False))
    ax4.axis("off")
    ax4.set_xlim([0, 1])
    ax4.set_ylim([0, 1])
    ax4.annotate("1",(0.16,0.15))
    ax4.annotate("2",(0.5,0.85))
    ax4.annotate("3",(0.84,0.15))
    ax4.set_title('K4 o 2-simplex')

    ax5.axis("off")
    plt.show()



def tetraedro():
    fig = plt.figure( figsize=(30,30))
    axes = fig.add_subplot(331,projection='3d')
    axes.set_title("K0")
    axes.axis("off")

    axes = fig.add_subplot(332, projection='3d')
    axes.set_title("K1")
    x = [0, 0.87, 0]
    y = [0, 0.5, 1]
    z = [0, 0, 0]
    axes.text(-0.03, 0, 0,r"1")
    axes.text(0.9, 0.5, 0,r"2")
    axes.text(0, 1.02, 0,"3")
    axes.plot(x, y, z, 'ko')
    axes.axis("off")

    axes = fig.add_subplot(333, projection='3d')
    axes.set_title("K2")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87]
    y1=[0, 0.5]
    z1=[0, 0]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")


    axes = fig.add_subplot(334,projection='3d')
    axes.set_title("K3")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87]
    y1=[0, 0.5,1,0, 0.5,0.5]
    z1=[0, 0,0,0, 0.82,0]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    vertices = [[0, 1, 2]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('grey')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")

    axes = fig.add_subplot(335, projection='3d')
    axes.set_title("K4")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87,0,0.27]
    y1=[0, 0.5,1,0, 0.5,0.5,1,0.5]
    z1=[0, 0,0,0, 0.82,0,0,0.82]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    vertices = [[0, 1, 2]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('grey')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")

    axes = fig.add_subplot(336, projection='3d')
    axes.set_title("K5")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87,0,0.27]
    y1=[0, 0.5,1,0, 0.5,0.5,1,0.5]
    z1=[0, 0,0,0, 0.82,0,0,0.82]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    vertices = [[0, 1, 2], [1,2, 3]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('grey')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")

    axes = fig.add_subplot(337, projection='3d')
    axes.set_title(r"K6")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87,0,0.27]
    y1=[0, 0.5,1,0, 0.5,0.5,1,0.5]
    z1=[0, 0,0,0, 0.82,0,0,0.82]
    axes.text(-0.03, 0, 0,r"1")
    axes.text(0.9, 0.5, 0,r"2")
    axes.text(0, 1.02, 0,r"3")
    axes.text(0.27, 0.5, 0.85,r"4")
    vertices = [[0, 1, 2], [1,2, 3],[0,2,3]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('grey')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")


    axes = fig.add_subplot(338, projection='3d')
    axes.set_title("K7")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87,0,0.27]
    y1=[0, 0.5,1,0, 0.5,0.5,1,0.5]
    z1=[0, 0,0,0, 0.82,0,0,0.82]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    vertices = [[0, 1, 2], [1,2, 3],[0,2,3],[0,1,3]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('grey')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")

    axes = fig.add_subplot(339, projection='3d')
    axes.set_title("K7 o 3-simplex")
    x = [0, 0.87, 0, 0.27]
    y = [0, 0.5, 1, 0.5]
    z = [0, 0, 0, 0.82]
    x1=[0, 0.87,0,0, 0.27,0.87,0,0.27]
    y1=[0, 0.5,1,0, 0.5,0.5,1,0.5]
    z1=[0, 0,0,0, 0.82,0,0,0.82]
    axes.text(-0.03, 0, 0,"1")
    axes.text(0.9, 0.5, 0,"2")
    axes.text(0, 1.02, 0,"3")
    axes.text(0.27, 0.5, 0.85,"4")
    vertices = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    tupleList = list(zip(x, y, z))
    poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    tetra = art3d.Poly3DCollection(poly3d)
    tetra.set_alpha(0.2)
    tetra.set_color('blue')
    axes.add_collection3d(tetra)
    axes.plot(x, y, z, 'ko')
    axes.plot(x1, y1, z1, 'g')
    axes.axis("off")


    plt.show()

def tetracomplex():
    Tetrapre={}
    Tetrapre={"K0":[],"K1":[[1],[2],[3]],"K2":[[1,2],[4]],"K3":[[1,3],[2,3],[1,2,3],[1,4],[2,4]],"K4":[[3,4]],"K5":[[2,3,4]],"K6":[[1,3,4]],"K7":[[1,2,4]],"K8":[[1,2,3,4]] }
    Tetra={"K0":[]}
    for i in range(1,9):
        Tetra["K"+str(i)]=Tetra["K"+str(i-1)] + Tetrapre["K"+str(i)]
    return Tetra
	