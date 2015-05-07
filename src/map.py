import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
from parser.gml import GML

gml = GML()
gml.getLines("../data/lines_out.txt")
gml.getPoints("../data/points_out.txt")


# middlePoints of lines for annotation
middlePointsX = [gml.linesX[i][int(len(gml.linesX[i])/2)]
                 for i in range(len(gml.linesX))]
middlePointsY = [gml.linesY[i][int(len(gml.linesY[i])/2)]
                 for i in range(len(gml.linesY))]


for i in range(0,len(gml.linesX)):
    plt.plot(gml.linesX[i][1:], gml.linesY[i][1:])

for label, x, y in zip(gml.index, middlePointsX, middlePointsY):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
    )


for i in range(0,len(gml.pointsX)):
    plt.scatter(gml.pointsX[i], gml.pointsY[i])


plt.show()



