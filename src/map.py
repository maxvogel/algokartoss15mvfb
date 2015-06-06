import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from parser.gml import GML
from map.draw import drawMap
from algorithm.tangentsegment import *
from algorithm.distributepoints import *
from algorithm.discard_accept import *
from util.face import *
import numpy as np

gml = GML()
gml.getLines("../data/lines_out.txt")
gml.getPoints("../data/points_out.txt")

#drawMap(gml.linesX,gml.linesY,
#        gml.pointsX,gml.pointsY,
#        gml.index,
#        annotate=True)
"""""
rot = []
for i in range(0,len(gml.linesX)):
    xy = zip(gml.linesX[i][1:], gml.linesY[i][1:])

    a = t.getPrincipalAngle(xy)

    #    print i, a, t.rotate(xy,a)
    r = t.rotate(xy,a)
    print r
    print "              "
    plt.plot(r[0],r[1])

"""""

polygonalChain = [[0,0],[10,20],[30,30],[45,22],[50,-5],[60,-10],[70,10],[75,-2],[90,15],[92,25]]  # -> paper
C = zip(*polygonalChain)
P = [[-5,0],[8,20],[10,7],[15,3],[20,8],[25,15],[40,-7],[70,-7],[70,2],[80,0],[90,5],[53,-5],[59,-7],[65,7],[53,3],[58,-1],[40,-6],[51,19],[60,17],[65,17],[19,26],[37,28],[75,6],[87,13],[90,20],[48,10]]

Ps = zip(*P)

i = 0
w_max, w_min, f = computeTangentSplitters(polygonalChain,i)
tangentSplitters = mc.LineCollection(w_max + w_min, linewidths=2, linestyles='dashed')

distributedPoints, representatives = distributePoints(f,i,P,polygonalChain,w_max,w_min)

rep = list(representatives)

if [] in rep:
        rep.remove([])

r = zip(*rep)


Si = [face(f[0],representatives[0],False),
      face(f[1],representatives[1],True),
      face(f[2],representatives[2],False),
      face(f[3],representatives[3],True)]

shortcuts = discard_and_accept(polygonalChain, Si, i)
shortcutlines = mc.LineCollection(shortcuts, linewidths=4, color='g')


points = [item for sublist in distributedPoints for item in sublist]
fig, ax = plt.subplots()
ax.add_collection(tangentSplitters)
ax.add_collection(shortcutlines)


plt.scatter(Ps[0], Ps[1], c=[[1,0,0] for x in Ps])
plt.scatter(zip(*points)[0],zip(*points)[1],c=[[0,1,0] for x in Ps])
plt.scatter(r[0], r[1],c=[[0,0,0] for x in polygonalChain])
plt.plot(C[0], C[1])
plt.show()
