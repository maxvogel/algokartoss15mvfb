import math
import numpy as np

x = 0; y = 1

def angle(vec1, vec2):
    dotp  = np.dot(vec1,vec2)
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    return math.acos(dotp/(norm_v1*norm_v2))


def getPrincipalAngle(C):
    # C = [[x,y], [], [] .... ]
    start_end_line = [C[-1][0]-C[0][0],C[-1][1]-C[0][1]]
    xaxis = [1,0]
    return angle(start_end_line,xaxis)


def rotate(C, angle):
    """
    """
    rotationMatrix = [[math.cos(angle), -math.sin(angle)],
                      [math.sin(angle),  math.cos(angle)]]

    newC = []
    for vertex in C:
        rotate = np.dot(rotationMatrix, vertex)
        newC.append(rotate)

    newC = zip(*newC)
    return newC


def minMaxTangent(C, i, j):
    """
    returns
    0  if vivj is minimal tangent
    1  if vivj is maximal tangent
   -1  else
    """
    dx = C[j][0]-C[i][0]
    dy = C[j][1]-C[i][1]
    normal_vec = [-dy,dx]

    dotvj_pre  = np.dot(normal_vec,C[j-1])
    dotvj_post = np.dot(normal_vec,C[j+1])

    # vj-1 and vj+1 are on the same site of vij
    # <=> the dotproduct of those two vectors
    # with the normal vector of vij has the same sign

    if dotvj_pre * dotvj_post > 0:  # same sign
        #vij is tangent
        if C[j-1][y] < C[j][y]:
            return 1
        else:
            return 0
    return -1

def intersectionPoint(a,b,c,d):
    """
    returns intersection point of line ab and cd
    """
    Sx = ((a[x]*b[y]-c[x]-d[x])-(a[x]-b[x])*(c[x]*d[y]-c[y]-d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))
    Sy = ((a[x]*b[y]-c[y]-d[y])-(a[y]-b[y])*(c[x]*d[y]-c[y]-d[x]))/ \
    ((a[x]-b[x])*(c[y]-d[y])-(a[y]-b[y])*(c[x]-d[x]))

    return [Sx,Sy]

def counterClockwise(a,b,c):
    return (c[y]-a[y])*(b[x]-a[x]) > (b[y]-a[y])*(c[x]-a[x])

def intersect(a,b,c,d):
    """
    returns true if line segments ab and cd intersect
    """
    return counterClockwise(a,c,d) != counterClockwise(b,c,d) and \
           counterClockwise(a,b,c) != counterClockwise(a,b,d)


def computeTangentSplitters(C,i):
    """
    """
    for j in range(i+1,len(C)+1):
        if minMaxTangent(C,i,j) == 1:
            k = j-1
            lij = [C[i], C[j]+100*(C[j]-C[i])]
            while not intersect(lij[0],lij[1],C[k-1],C[k]):
                k = k-1
                if minMaxTangent(C,i,k) == 1:
                    pass
                else:
                    k = k-1
            w = intersectionPoint(lij[0],lij[1],C[k-1],C[k])
            #TODO
