import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl


def drawMap(linesX, linesY, pointsX, pointsY, index, annotate):
    for i in range(0,len(linesX)):
        plt.plot(linesX[i][1:], linesY[i][1:])

    for i in range(0,len(pointsX)):
        plt.scatter(pointsX, pointsY)

    if annotate:
        middlePointsX = [linesX[i][int(len(linesX[i])/2)]
                 for i in range(len(linesX))]
        middlePointsY = [linesY[i][int(len(linesY[i])/2)]
                 for i in range(len(linesY))]

        for label, x, y in zip(index, middlePointsX, middlePointsY):
            plt.annotate(
                label,
                xy = (x, y), xytext = (-20, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
            )


    plt.show()


