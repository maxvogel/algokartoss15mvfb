from util.planargeometry import *
from util.face import *
from tangentsegment import *

def slope(vec1,vec2):
    if float(vec1[0])-vec2[0] == 0:
        return 10**10
    else:
        return (vec1[1]-vec2[1])/(float(vec1[0])-vec2[0])

def discardShortcuts(from_, Q, m):
    if from_ == "front":
        while Q and slope(Q[0][0],Q[0][1]) > m:
            #print("discarding {} from front".format(Q[0]))
            Q.pop(0)

    elif from_ == "back":
        while Q and slope(Q[len(Q)-1][0], Q[len(Q)-1][1]) < m:
            #print("discarding {} from back".format(Q[len(Q)-1]))
            Q.pop(len(Q)-1)

    return Q

def discard_and_accept(C, Si, i):
    """
    Parameters
    ----------


    Returns
    -------

    """
    accept = []
    j = i

    Q = [[C[i],Cj] for Cj in C[i+2:]]
    Q.sort(key=lambda v: slope(v[0],v[1]), reverse=True)
    #print Q

    for k in range(0,len(Si)):
        face = Si[k]
        #if i == 0: print face.C, face.maximalTangent(), face.p
        if face.pointStored():
            m = slope(C[i], face.p)
            #if i == 0: print m
            if face.maximalTangent():
                discardShortcuts("front", Q, m)
            else:
                discardShortcuts("back", Q, m)

        while not (minMaxTangent(C, i, j) == 1 or minMaxTangent(C, i, j) == 0):

            if [C[i],C[j]] in Q:
                accept.append([C[i],C[j]])
                Q.remove([C[i],C[j]])

            j = j+1

    return accept
