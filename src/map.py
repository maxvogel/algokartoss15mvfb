import matplotlib.pyplot as plt
from parser.gml import GML
from map.draw import drawMap

gml = GML()
gml.getLines("../data/lines_out.txt")
gml.getPoints("../data/points_out.txt")



drawMap(gml.linesX,gml.linesY,
        gml.pointsX,gml.pointsY,
        gml.index,
        annotate=True)


