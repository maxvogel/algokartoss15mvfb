import numpy as np
import math

x = 0; y = 1

def angle(vec1, vec2):
    """
    Parameters
    ----------
    vec1, vec2 : two 2D vectors (i.e. two list with two elements each)

    Returns
    -------
    The angle between the vectors measured counterclockwise
    """
    dotp  = np.dot(vec1,vec2)
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    return math.acos(round(dotp/(norm_v1*norm_v2),10))

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
    a = map(float,a); b = map(float,b)

    if a == d:
        return a
    elif b == c:
        return b

    Sx = ((a[x]*b[y]-a[y]*b[x])*(c[x]-d[x])-(a[x]-b[x])*(c[x]*d[y]-c[y]*d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))
    Sy = ((a[x]*b[y]-a[y]*b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]*d[y]-c[y]*d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))

    return [Sx,Sy]

def counterClockwise(a,b,c):
    return (c[y]-a[y])*(b[x]-a[x]) >= (b[y]-a[y])*(c[x]-a[x])

def between(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)

    if abs(np.cross(b-a, c-a)) > 0.005:
        return False

    dotp = np.dot(c-a, c-a)
    if dotp < 0:
        return False

    d_ab = (np.linalg.norm(a-b))**2
    if dotp > d_ab:
        return False

    return True

def intersect(a,b,c,d):
    """
    Returns
    -------
    true if line segments ab and cd intersect
    """
    return (counterClockwise(a,c,d) != counterClockwise(b,c,d) and \
           counterClockwise(a,b,c) != counterClockwise(a,b,d)) or \
           between(a,b,c) or between(a,b,d)

def distancePointLine(line, p):
    """
    Parameters
    ----------
    line : two list of two each elements each defining a line in a 2D space
    p : a list of two values defining a point
    
    Returns
    -------
    The distance between the given line `line`and the given point `p`
    """
    y = (line[1][1]-line[0][1])
    x = (line[1][0]-line[0][0])
    distance = abs(y*p[0] - x*p[1] + line[1][0]*line[0][1] - line[1][1]*line[0][0])
    distance /= math.sqrt(y**2 + x**2)
    return distance
