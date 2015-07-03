import networkx
from tangentsegment import *
from distributepoints import *
from discard_accept import *
from arbitrarychains import *
from util.planargeometry import angle
import math
from map.draw import *

def translate(C, t):
    """
    Parameters
    ----------
    C : list of x/y coordinates defining the polygonal chain
    t : a numpy array 

    Returns
    -------
    the translated polygonal chain
    """
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
    """
    Parameters
    ----------
    faces : list of list of points defining the faces
    representatives : a list of points where one corresponds to a face
    f_minmax : a list of strings where one corresponds to a face specifying whether its a min a or max face
    
    Returns
    -------
    a proper subdivision as a list of face objects
    """
    return [face(faces[i],representatives[i], f_minmax[i]) for i in range(len(faces))]

def shortcutInEpsilonCorridor(C,shortcut,epsilon):
    """
    Parameters
    ----------
    C : list of points defining the polygonal chain
    shortcut : list of points defining the shortcut
    epsilon : maximum allowed distance between a shortcut and the points from the polygonal chain

    Returns
    -------
    Boolean stating whether the shortcut lies within the epslion corridor or not
    """
    startIdx = C.index(shortcut[0])
    endIdx = C.index(shortcut[1])
    for i in range(startIdx+1,endIdx):
        dist = distancePointLine(shortcut,C[i])
        if (dist > epsilon): return False
    return True

def computeShortcutsForPolygonalChain(C,P,epsilon):
    """
    Computes a list of shortcuts for a polygonal chain C. The returned shortcuts are valid within the following two criteria:
    - The orientation of nearby points P (i.e. right or left of C) won't change.
    - All short-cut points lie within the epsilon corridor of the shortcut.

    Parameters
    ----------
    C : list of points defining the polygonal chain
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
    C : list of points defining the polygonal chain
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
        subchain = C[i:j+1]
        P += addConstraintPointsFromChain(C,subchain)
        w_max, w_min, f, f_minmax = computeTangentSplitters(subchain,0)
        #Pextended = C[j+1:]
        Pextended = P
        distributedPoints, representatives = distributePoints(f,0,Pextended,subchain,w_max,w_min)

        Si = subdivision(f,representatives,f_minmax)

        if not epsilon is None:
            shortcuts += [shortcut for shortcut in discard_and_accept(subchain, Si, 0) if shortcutInEpsilonCorridor(subchain,shortcut,epsilon)]
        else:
            shortcuts += [shortcut for shortcut in discard_and_accept(subchain, Si, 0)]
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
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain with n vertices    
    xMonotoneSubChains : list of list of x/y coordinates
        list of subchain which make up the polygonal chain C

    Returns
    -------
    a list of points which consists of C without xMonotoneSubchain
    """
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
    """
    Parameters
    ----------
    xMonotoneSubChains : list of list of x/y coordinates
        list of subchain which make up the polygonal chain C
    C : list of x/y coordinates
        polygonal chain with n vertices
    points : list of x/y coordinates
        points constraining the degree of the simplification
    epsilon : float
        shortcuts of the simplification have to lie within the specified epsilon corridor

    Returns
    -------
    the simplified polygonal chain
    """
    shortcuts = []
    for chain in xMonotoneSubChains:
        if len(chain) > 1:
            P += addConstraintPointsFromChain(C,chain)
            shortcuts += computeShortcutsForPolygonalChain(chain,P,epsilon)
    return shortcuts


def preprocess(C, points):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain with n vertices
    points : list of x/y coordinates
        points constraining the degree of the simplification

    Returns
    -------
    the input parameters, but translated to the view/axis of C[0]
    """
    t = -np.array(C[0])

    translatedC = translate(C,t)
    translatedP = translate(points, t)

    a = getPrincipalAngle(translatedC)

    rotatedC = rotate(translatedC,a)
    rotatedP = rotate(translatedP,a)
    return map(list, rotatedC), map(list,rotatedP)

def simplifyChain(C, points, epsilon, anim_flag):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain with n vertices
    points : list of x/y coordinates
        points constraining the degree of the simplification
    epsilon : float
        shortcuts of the simplification have to lie within the specified epsilon corridor
    anim_flag : bool
        true, if the simplification of the polygonal chain should be animated

    Returns
    -------
    the simplified polygonal chain
    """
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