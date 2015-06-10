import numpy as np
import math

x = 0; y = 1

def angle(vec1, vec2):
    dotp  = np.dot(vec1,vec2)
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    return math.acos(dotp/(norm_v1*norm_v2))

def intersectionPoint(a,b,c,d):
    """
    Parameters
    ----------
    a b c d : list
        x/y coordinates

    Returns
    -------
    intersection point of line ab and cd
    """
    a = map(float,a)

    Sx = ((a[x]*b[y]-a[y]*b[x])*(c[x]-d[x])-(a[x]-b[x])*(c[x]*d[y]-c[y]*d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))
    Sy = ((a[x]*b[y]-a[y]*b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]*d[y]-c[y]*d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))

    return [Sx,Sy]

def counterClockwise(a,b,c):
    return (c[y]-a[y])*(b[x]-a[x]) > (b[y]-a[y])*(c[x]-a[x])

def intersect(a,b,c,d):
    """
    Returns
    -------
    true if line segments ab and cd intersect
    """
    return counterClockwise(a,c,d) != counterClockwise(b,c,d) and \
           counterClockwise(a,b,c) != counterClockwise(a,b,d)

def distancePointLine(C,line, p):
    y = (line[1][1]-line[0][1])
    x = (line[1][0]-line[0][0])
    distance = abs(y*p[0] - x*p[1] + line[1][0]*line[0][1] - line[1][1]*line[0][0])
    distance /= math.sqrt(y**2 + x**2)
    return distance