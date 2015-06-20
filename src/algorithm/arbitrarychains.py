import math
import numpy as np
from util.planargeometry import *

def isValid(C,i,j):
    a1 = angle([C[i][0]-C[j][0],C[i][1]-C[j][1]],[C[j+1][0]-C[j][0],C[j+1][1]-C[j][1]])
    a2 = angle([C[i][0]-C[j][0],C[i][1]-C[j][1]],[C[j-1][0]-C[j][0],C[j-1][1]-C[j][1]])
    if a2 < a1 and a1 < math.pi:
        return True
    else:
        return math.pi < a1 and a1 < a2

def diminishInterval(C,i,I,j):
    for angle in I:
        halfline = [C[i], [10**6*math.cos(angle), 10**6*math.sin(angle)]]
        if intersect(C[j-1],C[j],halfline[0],halfline[1]):
            I.remove(angle)
    return I

def determineSubchain(C,i):
    if i >= len(C)-3:
        return len(C)-1
    j = i+2
    Interval = np.linspace(-math.pi, math.pi, 500)
    Interval = Interval.tolist()
    vivj = [C[j][0]- C[i][0],C[j][1]- C[i][1]]
    angle_vivj = angle([1,0], vivj)

    if angle_vivj in Interval:
        Interval.remove(angle_vivj)

    while j < len(C)-2 and isValid(C,i,j) and Interval:
        j +=1
        I = diminishInterval(C, i, Interval, j)
    if not Interval:
        return j-1
    else:
        return j

def isLeftTurn(C, i):
    """
    Returns
    -------

    true if there's a 'left turn' at index i
    """
    if i == 0 or i == len(C)-1: return False
    return C[i-1][0] < C[i][0] and C[i+1][0] < C[i][0]

def isRightTurn(C, i):
    """
    Returns
    -------

    true if there's a 'right turn' at index i
    """
    if i == 0 or i == len(C)-1: return False
    return C[i-1][0] > C[i][0] and C[i+1][0] > C[i][0]

def startsToRight(C,i):
    while i < len(C)-1 and C[i][0] > C[i+1][0]:
        i = i+1
    return i

def isXmonotone(C):
    for i in range(len(C)-2):
        if C[i][0] > C[i+1][0]:
            return False
    return True

def isSamePoint(p1,p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) < 10**-9

def xMonotoneSubchains(C):
    """
    Returns
    -------

    a list of all x-monotone subchain, which are
    defined by left and right turns of the polygonal chain
    """
    if C[0] == C[-1]:
        print("polygonal chain is a cycle")

    if isXmonotone(C): return [C]

    i = 0; subchains = []

    while i < len(C):
        x = []

        if i == 0:
            i = startsToRight(C,i)

        while i < len(C) and not isLeftTurn(C,i):
            x.append(C[i])
            i = i+1

        while i < len(C) and not isRightTurn(C,i):
            i = i+1

        if x:
            subchains.append(x)

    if subchains:
        print "split into {} subchains".format(len(subchains))
        return subchains
