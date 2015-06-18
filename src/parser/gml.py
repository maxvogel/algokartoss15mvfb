from shapely.geometry import LineString
from osgeo import ogr


class GML(object):
    """
    Attributes
    ----------

    index : list
    linesX,linesY : list of lists; every list is a path
    pointsX,pointsY : list x/y coordinates
    """

    def __init__(self):
        self.index = []
        self.linesX = []
        self.linesY = []

        self.pointsX = []
        self.pointsY = []

    def readLines(self, pathToFile):

        with open(pathToFile) as txt:
            lines = txt.readlines()

        for i, line in enumerate(lines):
            comma = line.find(":")
            self.index.append(line[:comma])
            lines[i] = line[comma+1:]

        for l in lines:
            linestr = ogr.CreateGeometryFromGML(l)
            xcoord = []; ycoord = []
            for i in range(0, linestr.GetPointCount()):
                if i ==  0:
                    xcoord.append(self.index[len(self.linesX)])
                    ycoord.append(self.index[len(self.linesX)])

                pt = linestr.GetPoint(i)
                xcoord.append(pt[0])
                ycoord.append(pt[1])
            self.linesX.append(xcoord)
            self.linesY.append(ycoord)


    def readPoints(self, pathToFile):

        with open(pathToFile) as txt:
            points = txt.readlines()

        for i, point in enumerate(points):
            comma = point.find(":")
            # self.index.append(line[:comma])
            points[i] = point[comma+1:]


        for p in points:

            ppp = ogr.CreateGeometryFromGML(p)

            pt = ppp.GetPoint(0)
            self.pointsX.append(pt[0])
            self.pointsY.append(pt[1])

    def getListOfPoints(self):
        return zip(self.pointsX, self.pointsY)

    def getListOfLines(self):
        lines = []
        for i in range(0,len(self.index)):
            lines.append((self.index[i],zip(self.linesX[i][1:],self.linesY[i][1:])))
        return lines
