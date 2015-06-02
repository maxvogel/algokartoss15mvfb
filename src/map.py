import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from parser.gml import GML
from map.draw import drawMap
from algorithm.tangentsegment import *
from algorithm.distributepoints import *
#from algorithm.discard_accept import *
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
P = [[-5,0],[8,20],[10,7],[15,3],[20,8],[25,15],[40,-7],[70,-7],[70,2],[80,0],[90,5],[53,-5],[59,-7],[65,7],[53,3],[58,-1],[40,-6],[51,19],[60,17],[65,17],[19,26],[37,28],[75,6],[87,13],[90,20],[48,10]]
Ps = zip(*P)

#print minMaxTangent(polygonalChain,0,7)
w_max, w_min, face = computeTangentSplitters(polygonalChain,0)

tangentSplitters = mc.LineCollection(w_max + w_min, linewidths=2, linestyles='dashed')
distributedPoints, representatives = distributePoints(face,0,P,polygonalChain,w_max,w_min)
r = zip(*representatives)

#print("w_max:\t{0}".format(w_max))
#print("w_min:\t{0}".format(w_min))
#print("number of faces:\t{0}".format(len(face)))
#for f in face:
#    print(f)




fig, ax = plt.subplots()
ax.add_collection(tangentSplitters)
pX = []
pY = []
tmpList = []
for e in distributedPoints:
	if len(e) > 0:
		for x in e:
			pX.append(x[0])
			pY.append(x[1])
        	tmpList += [x]
plt.scatter(Ps[0], Ps[1], c=[[1,0,0] for x in Ps])
plt.scatter(tuple(pX),tuple(pY),c=[[0,1,0] for x in Ps])
plt.scatter(r[0], r[1],c=[[0,0,0] for x in polygonalChain])
plt.plot(C[0], C[1])
plt.show()
