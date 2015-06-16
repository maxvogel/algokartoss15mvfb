import math
import numpy as np
from util.planargeometry import *

x = 0; y = 1

def minMaxTangent(C, i, j):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain
    i : int
        vertex vi
    j : int
        vertex vj

    Returns
    -------
    0  if vivj is minimal tangent
    1  if vivj is maximal tangent
   -1  else
    """
    if j == len(C)-1:  # special case: last vertex is always max or min
        if C[j-1][y] < C[j][y]:
            return 1
        else:
            return 0

    dx = C[j][x]-C[i][x]
    dy = C[j][y]-C[i][y]
    normal_vec = [-dy,dx]

    vivj_pre  = [C[j-1][x]-C[i][x], C[j-1][y]-C[i][y]]   # vector from vi to vj-1
    vivj_post = [C[j+1][x]-C[i][x], C[j+1][y]-C[i][y]]   # vector from vi to vj+1

    dotvj_pre  = np.dot(normal_vec, vivj_pre)
    dotvj_post = np.dot(normal_vec, vivj_post)

    # vj-1 and vj+1 are on the same site of vij
    # <=> the dotproduct of those two vectors
    # with the normal vector of vij has the same sign

    if dotvj_pre * dotvj_post > 0:  # same sign
        #vij is tangent
        if C[j-1][y] < C[j][y]:
            return 1
        elif C[j-1][y] > C[j][y]:
            return 0
    return -1


def buildface(C, k, v_y, w):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain with n vertices
    k : int
        starting index of C for face
    v_y : int
          end index of C for face
    w : list of x/y coordinates
        w_min or w_max

    Returns
    -------
    a minimal or maximal face
    """
    if w:
        predecessor = w[-1]

        if predecessor[0] in C[k:v_y+1]:
            idx = C.index(predecessor[0])
            return [predecessor[1]] + C[idx:v_y+1]

    return C[k:v_y+1]


def computeTangentSplitters(C,i):
    """
    Parameters
    ----------
    C : list of x/y coordinates
        polygonal chain with n vertices
    i : int
        1 <= i <= n

    Returns
    -------
    tangent splitters of C with respect to vertex i
    and the corresponding faces
    """
    w_max = []
    w_min = []
    face = []
    minmax = []
    v_y = 0

    for j in range(i+1,len(C)):

        if minMaxTangent(C,i,j) == 1:
            v_y = j
            k = j-1
            lij = [C[i], C[j]+10.0**6*(np.array(C[j])-np.array(C[i]))]
            while not intersect(lij[0],lij[1],C[k-1],C[k]):
                k = k-1
                if minMaxTangent(C,i,k) == 1:
                    pass         #TODO
                else:
                    pass
            interP = intersectionPoint(lij[0],lij[1],C[k-1],C[k])

            #face.append([interP] + C[k:v_y+1])
            face.append([interP] + buildface(C,k,v_y,w_max))
            w_max.append([C[j], interP])
            minmax.append("max")

        elif minMaxTangent(C,i,j) == 0:
            v_y = j
            k = j-1
            lij = [C[i], C[j]+10.0**6*(np.array(C[j])-np.array(C[i]))]
            while not intersect(lij[0],lij[1],C[k-1],C[k]):
                k = k-1
                if minMaxTangent(C,i,k) == 0:
                    pass         #TODO
                else:
                    pass
            interP = intersectionPoint(lij[0],lij[1],C[k-1],C[k])

            #face.append([interP] + C[k:v_y+1])
            face.append([interP] + buildface(C,k,v_y,w_min))
            w_min.append([C[j], interP])
            minmax.append("min")

    return w_max, w_min, face, minmax
