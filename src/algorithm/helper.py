import networkx
from tangentsegment import *
from distributepoints import *
from discard_accept import *
from arbitrarychains import *
import math
from map.draw import *

def angle(vec1, vec2):
    dotp  = np.dot(vec1,vec2)
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    return math.acos(dotp/(norm_v1*norm_v2))

def translate(C, t):
    return [np.array(vertex) + t for vertex in C]

def getPrincipalAngle(C):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal Chain

    Returns
    -------
    the angle between start_end_line (first to last vertex)
    and the x-axis
    """
    if C[0].any() == C[-1].any():
        start_end_line = [C[-2][0]-C[0][0],C[-2][1]-C[0][1]]

    else:
        start_end_line = [C[-1][0]-C[0][0],C[-1][1]-C[0][1]]

    xaxis = [1,0]
    if C[-1][1] > 0:
        return 2*math.pi - angle(start_end_line, xaxis)

    return angle(start_end_line,xaxis)

def rotate(C, angle):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal Chain
    angle : float
        angle in radians

    Returns
    -------
    the rotated polygonal chain
    """
    rotationMatrix = [[math.cos(angle), -math.sin(angle)],
                      [math.sin(angle),  math.cos(angle)]]

    #rotatedC = zip(*rotatedC)
    return [np.dot(rotationMatrix, vertex) for vertex in C]


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

def computeShortcutsForPolygonalChain2(C,P,epsilon):
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
        j = determineSubchain(C,i)
        #if j-i > 2: print i,j
        subchain = C[0:j+1]
        P += addConstraintPointsFromChain(C,subchain)
        w_max, w_min, f, f_minmax = computeTangentSplitters(subchain,i)
        Pextended = C[j+1:]
        Pextended += P
        distributedPoints, representatives = distributePoints(f,i,Pextended,subchain,w_max,w_min)

        Si = subdivision(f,representatives,f_minmax)

        if not epsilon is None:
            shortcuts += [shortcut for shortcut in discard_and_accept(subchain, Si, i) if shortcutInEpsilonCorridor(subchain,shortcut,epsilon)]
        else:
            shortcuts += [shortcut for shortcut in discard_and_accept(subchain, Si, i)]
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

def addConstraintPointsFromChain(C, xMonotoneSubchain):
    from_ = C.index(xMonotoneSubchain[0])
    to_   = C.index(xMonotoneSubchain[-1])

    if len(C) == len(xMonotoneSubchain):
        return []
    elif from_ == 0:
        return C[to_:]
    elif to_ == len(C)-1:
        return C[0:from_+1]
    else:
        return C[:from_+1] + C[to_:]

def computeShortcutsForArbitraryChain(xMonotoneSubChains,C, P, epsilon):
    shortcuts = []
    for chain in xMonotoneSubChains:
        if len(chain) > 1:
            P += addConstraintPointsFromChain(C,chain)
            shortcuts += computeShortcutsForPolygonalChain(chain,P,epsilon)
    return shortcuts


def preprocess(C, points):
    t = -np.array(C[0])

    translatedC = translate(C,t)
    translatedP = translate(points, t)

    a = getPrincipalAngle(translatedC)

    rotatedC = rotate(translatedC,a)
    rotatedP = rotate(translatedP,a)
    return map(list, rotatedC), map(list,rotatedP)

def simplifyChain(C, points, epsilon, anim_flag):
    rotatedC, rotatedP = preprocess(C, points)

    #xMonotoneSubC = xMonotoneSubchains(rotatedC)
    #shortcuts = computeShortcutsForArbitraryChain(xMonotoneSubC, rotatedC, rotatedP, epsilon)

    rP = list(rotatedP)
    shortcuts = computeShortcutsForPolygonalChain2(rotatedC, rotatedP, epsilon)

    G = transformToGraph(rotatedC,shortcuts)
    s = getShortestPaths(rotatedC,G)

    if anim_flag == 1:
        animate(rotatedC,rP,shortcuts,s)

    return getSimplifiedPolygonalChain(C,s)

def simplify(polygonalChains, points, epsilon):
    shortcuts = []
    simplifiedC = []
    for chain in polygonalChains:
        #C = map(list, chain[1:][0])
        rotatedC, rotatedP = preprocess(C, points)

        xMonotoneSubC = xMonotoneSubchains(rotatedC)
        shortcuts.append(computeShortcutsForArbitraryChain(xMonotoneSubC, rotatedC, rotatedP, epsilon))


        G = transformToGraph(rotatedC,shortcuts[-1])
        s = getShortestPaths(rotatedC,G)

        simplifiedC.append(getSimplifiedPolygonalChain(C,s))

    return simplifiedC
