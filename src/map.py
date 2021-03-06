import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from parser.gml import GML
from map.draw import drawMap, plotSimplifiedAndOriginal
from algorithm.tangentsegment import *
from algorithm.distributepoints import *
from algorithm.discard_accept import *
from util.planargeometry import distancePointLine
from util.face import *
import numpy as np
import networkx
from algorithm.arbitrarychains import *
from algorithm.helper import *
from simp import writeData

gml = GML()
gml.readLines('../data/lines_out.txt')
gml.readPoints('../data/points_out.txt')


simp = simplify(gml.getListOfLines(), gml.getListOfPoints(), 10**6)
#writeData('result.txt', simp)

#gmlSimplified = GML()
#gmlSimplified.readLines('./result.txt')
#gmlSimplified.readPoints('../data/points_out.txt')



#plotSimplifiedAndOriginal(gml,gmlSimplified)


#################
#################


polygonalChain = [[0,0],[10,20],[30,30],[45,22],[50,-5],[60,-10],[70,10],[75,-2],[90,15],[92,25]]  # -> paper
C = zip(*polygonalChain)
P = [[-5,0],[8,20],[10,7],[15,3],[20,8],[25,15],[40,-7],[70,-7],[70,2],[80,0],[90,5],[53,-5],[59,-7],[65,7],[53,3],[58,-1],[40,-6],[51,19],[60,17],[65,17],[19,26],[37,28],[75,6],[87,13],[90,20],[48,10]]
#P = []

Ps = zip(*P)

i = 0

w_max, w_min, f, f_minmax = computeTangentSplitters(polygonalChain,i)
tangentSplitters = mc.LineCollection(w_max + w_min, linewidths=2, linestyles='dashed')

distributedPoints, representatives = distributePoints(f,i,P,polygonalChain,w_max,w_min)


rep = list(representatives)

if [] in rep:
        rep.remove([])

r = zip(*rep)


Si = subdivision(f,representatives,f_minmax)

#shortcuts = discard_and_accept(polygonalChain, Si, i)
shortcuts =  computeShortcutsForPolygonalChain(polygonalChain,P,200.0)
shortcutlines = mc.LineCollection(shortcuts, linewidths=3, color='g')

G = transformToGraph(polygonalChain,shortcuts)
s = getShortestPaths(polygonalChain,G)
#print s

s = getSimplifiedPolygonalChain(polygonalChain,s)
#shortpath = mc.LineCollection([[s[i],s[i+1]] for i in range(0,len(s)-1)], linewidths=4, colors=[[1,.5,0] for i in range(0,len(s)-1)])


points = [item for sublist in distributedPoints for item in sublist]
fig, ax = plt.subplots()
ax.add_collection(tangentSplitters)
ax.add_collection(shortcutlines)
#ax.add_collection(shortpath)

if len(Ps) > 0: plt.scatter(Ps[0], Ps[1], c=[[1,0,0] for x in Ps])
if len(points) > 0: plt.scatter(zip(*points)[0],zip(*points)[1],c=[[0,1,0] for x in Ps])
if len(r) > 0: plt.scatter(r[0], r[1],c=[[0,0,0] for x in polygonalChain])
plt.plot(C[0], C[1])
#plt.show()
