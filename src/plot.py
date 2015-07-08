import numpy as np
from map.draw import plotSimplifiedAndOriginal, drawMap
import matplotlib.pyplot as plt
from parser.gml import *
import sys

if __name__ == "__main__":

    if not (len(sys.argv) >= 2 and len(sys.argv) <= 4):
        print("""
        Usage:
        python plot.py LineInputFilePath (without points)
        or:
        python plot.py LineInputFilePath PointInputFilePath
        or:
        python plot.py LineInputFilePath SimplifiedLineInputFilePath PointInputFilePath

        """)

        exit()

    if len(sys.argv) == 2:
        gml = GML()
        lines = sys.argv[1]
        gml.readLines(lines)
        drawMap(gml.linesX, gml.linesY,
                gml.pointsX,gml.pointsY,
                gml.index,
                annotate=False)
        plt.show()

    if len(sys.argv) > 2:
        gml = GML()
        lines = sys.argv[1]
        points = sys.argv[-1]
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
            lines_simp = sys.argv[2]
            gmlSimplified.readLines(lines_simp)
            gmlSimplified.readPoints(points)

            plotSimplifiedAndOriginal(gml, gmlSimplified)
