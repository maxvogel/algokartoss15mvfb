import matplotlib.pyplot as plt
from parser.gml import GML
from map.draw import drawMap
from algorithm.tangentsegment import *
import numpy as np

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

polygonalChain = [[0,0],[10,20],[30,30],[45,22],[50,-5],[60,-10],[70,10],[75,-2],[90,15],[92,25]]  # -> paper
C = zip(*polygonalChain)

print minMaxTangent(polygonalChain,0,7)
print computeTangentSplitters(polygonalChain,0)


plt.plot(C[0], C[1])
plt.show()
