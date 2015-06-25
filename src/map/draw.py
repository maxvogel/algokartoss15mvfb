import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
from matplotlib import collections  as mc

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

    plt.tight_layout()


def plotSimplifiedAndOriginal(gml, gmlSimplified):
    fig = plt.figure(1)

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


def plotChain(C, color, width):
    plt.plot(zip(*C)[0],zip(*C)[1],color,linewidth=width)

import time
fig = plt.figure(0)

def animate(C, points, shortcuts, shortestPath):
    # plt.ion()

    ax = fig.add_subplot(111)
    plt.xticks([]); plt.yticks([]);

    plotChain(C,'b', 2)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    plt.scatter(zip(*points)[0], zip(*points)[1])

    if shortcuts:
        for s in shortcuts:
            x = []; y = []
            x.append(zip(*s)[0][0]); x.append(zip(*s)[0][1]); x.append(None)
            y.append(zip(*s)[1][0]); y.append(zip(*s)[1][1]); y.append(None)

            plt.plot(x,y,'g')
            axes = plt.gca()
            axes.set_xlim([xmin,xmax])
            axes.set_ylim([ymin,ymax])

            plt.draw()
            time.sleep(0.05)
            plt.pause(0.0001)

        shortestC = [C[i] for i in shortestPath]
        plotChain(shortestC,'r', 5)
        plt.pause(0.001)

        plt.clf()
