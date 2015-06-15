import networkx
from tangentsegment import *
from distributepoints import *
from discard_accept import *


def subdivision(faces, representatives, f_minmax):
  return [face(faces[i],representatives[i], f_minmax[i]) for i in range(len(faces))]

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
    w_max, w_min, f, f_minmax = computeTangentSplitters(C,i)
    distributedPoints, representatives = distributePoints(f,i,P,C,w_max,w_min)

    Si = subdivision(f,representatives,f_minmax)

    if not epsilon is None:
      shortcuts += [shortcut for shortcut in discard_and_accept(C, Si, i) if shortcutInEpsilonCorridor(C,shortcut,epsilon)]
    else:
      shortcuts += [shortcut for shortcut in discard_and_accept(C, Si, i)]
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
  G = networkx.DiGraph()
  G.add_edges_from([(i,i+1) for i in range(len(C)-1)])
  G.add_edges_from([(C.index(s[0]), C.index(s[1])) for s in shortcuts])

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

def computeSimplifiedChain(C,P,epsilon):
  shortcuts = computeShortcutsForPolygonalChain(C,P,epsilon)
  G = transformToGraph(C,shortcuts)
  s = getShortestPaths(C,G)
  sp = getSimplifiedPolygonalChain(C,s)
  return sp