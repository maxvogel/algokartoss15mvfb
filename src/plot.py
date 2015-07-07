import numpy as np
from map.draw import plotSimplifiedAndOriginal, drawMap
import matplotlib.pyplot as plt
from parser.gml import *
import sys

if __name__ == "__main__":

    if not (len(sys.argv) == 3 or len(sys.argv) == 4):
        print("""
        Usage:

        python plot.py LineInputFilePath PointInputFilePath
        or:
        python plot.py LineInputFilePath PointInputFilePath SimplifiedLineInputFilePath

        """)

        exit()

    gml = GML()
    lines = sys.argv[1]
    points = sys.argv[2]
    gml.readLines(lines)
    gml.readPoints(points)

    if len(sys.argv) == 3:
        drawMap(gml.linesX, gml.linesY,
                gml.pointsX,gml.pointsY,
                gml.index,
                annotate=False)
        plt.show()

    elif len(sys.argv) == 4:
        gmlSimplified = GML()
        lines_simp = sys.argv[3]
        gmlSimplified.readLines(lines_simp)
        gmlSimplified.readPoints(points)

        plotSimplifiedAndOriginal(gml, gmlSimplified)
