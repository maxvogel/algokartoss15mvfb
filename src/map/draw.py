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


    #plt.show()


def plotSimplifiedAndOriginal(gml, gmlSimplified):

    plt.subplot(1, 2, 1)
    plt.xticks(()); plt.yticks(())
    plt.title("Simplified")
    drawMap(gmlSimplified.linesX, gmlSimplified.linesY,
        gml.pointsX,gml.pointsY,
        gmlSimplified.index,
        annotate=False)

    plt.subplot(1, 2, 2)
    plt.xticks(()); plt.yticks(())
    plt.title("Original")
    drawMap(gml.linesX,gml.linesY,
        gml.pointsX,gml.pointsY,
        gml.index,
        annotate=False)
    plt.tight_layout()

    plt.show()
