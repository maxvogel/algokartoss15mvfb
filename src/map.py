import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from parser.gml import GML
from map.draw import drawMap
from algorithm.tangentsegment import *
from algorithm.distributepoints import *
from algorithm.discard_accept import *
from util.planargeometry import distancePointLine
from util.face import *
import numpy as np
#import networkx

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

  




def shortcutInEpsilonCorridor(C,shortcut,epsilon):
  startIdx = C.index(shortcut[0])
  endIdx = C.index(shortcut[1])
  for i in range(startIdx+1,endIdx):
    dist = distancePointLine(C,shortcut,C[i])
    if (dist > epsilon): return False
  return True

def computeShortcutsForPolygonalChain(C,P,epsilon):
  """
  Computes a list of shortcuts for a polygonal chain C. The returned shortcuts are valid within the following two criteria:
   - The orientation of nearby points P (i.e. right or left of C) won't change.
   - All short-cut points lie within the epsilon corridor of the shortcut.

  Parameters
  ----------
  C : list of points defining the the polygonal chain
  P : list of points constraining the number of consistent shortcuts
  epsilon : maximum allowed distance between a shortcut and the points from the polygonal chain

  Returns
  -------
  A list with shortcuts.

  """
  shortcuts = []
  for i in range(0,len(C)-1):
    w_max, w_min, f = computeTangentSplitters(C,i)
    distributedPoints, representatives = distributePoints(f,i,P,C,w_max,w_min)
    Si = [face(f[0],representatives[0],False),
      face(f[1],representatives[1],True),
      face(f[2],representatives[2],False),
      face(f[3],representatives[3],True)]
    shortcuts += [shortcut for shortcut in discard_and_accept(C, Si, i) if shortcutInEpsilonCorridor(C,shortcut,epsilon)]
  return shortcuts

def transformToGraph(C,shortcuts):
  """
  Constructs a networkX graph object from the given polygonal chain and the given shortcuts.

  Parameters
  ----------
  C : The polygonal chain
  shortcuts: a list of shortcuts

  Returns
  -------
  A networkX graph object.
  """
  G = networkx.digraph([i for i in range(0,len(C))])
  G.add_edges([(i,i+1) for i in range(0,len(C)-1)])
  for shortcut in shortcuts:
    G.add_edge(C.index(shortcut[0]),C.index(shortcut[1]))
  return G

def getShortestPaths(C,G):
  """
  Wraps the shortest path function from networkX

  Parameters
  ----------
  C : The polygonal chain to derive source and target vertex for the sssp calculation
  G : The networkX Graph object

  Returns
  -------
  A list of vertex ids representing the shortest path
  """
  return networkx.shortest_path(G,0,len(C)-1)

def getSimplifiedPolygonalChain(C,path):
  """
  Transforms a path in a polygonal chain.

  Parameters
  ----------
  C : the original polygonal chain
  path : the vertex ids of the shortest path

  Returns
  -------
  A list of points
  """
  return [C[p] for p in path]


polygonalChain = [[0,0],[10,20],[30,30],[45,22],[50,-5],[60,-10],[70,10],[75,-2],[90,15],[92,25]]  # -> paper
C = zip(*polygonalChain)
#P = [[-5,0],[8,20],[10,7],[15,3],[20,8],[25,15],[40,-7],[70,-7],[70,2],[80,0],[90,5],[53,-5],[59,-7],[65,7],[53,3],[58,-1],[40,-6],[51,19],[60,17],[65,17],[19,26],[37,28],[75,6],[87,13],[90,20],[48,10]]
P = []

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
#print(shortcuts)
#valid_shortcuts = [shortcut for shortcut in shortcuts if shortcutInEpsilonCorridor(polygonalChain,shortcut,10)]
#print(valid_shortcuts)
shortcutlines = mc.LineCollection(shortcuts, linewidths=4, color='g')


points = [item for sublist in distributedPoints for item in sublist]
fig, ax = plt.subplots()
ax.add_collection(tangentSplitters)
ax.add_collection(shortcutlines)


if len(Ps) > 0: plt.scatter(Ps[0], Ps[1], c=[[1,0,0] for x in Ps])
if len(points) > 0: plt.scatter(zip(*points)[0],zip(*points)[1],c=[[0,1,0] for x in Ps])
if len(r) > 0: plt.scatter(r[0], r[1],c=[[0,0,0] for x in polygonalChain])
plt.plot(C[0], C[1])
plt.show()
