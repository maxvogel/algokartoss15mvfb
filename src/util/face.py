class face(object):
    def __init__(self, C, p, minmax):
        self.C = C  #polygonal chain
        self.p = p
        self.minmax = minmax

    def pointStored(self):
        """
        if there's a point associated with
        a face, return true
        """
        return self.p

    def maximalTangent(self):
        if self.minmax == "max":
            return True
        elif self.minmax == "min":
            return False

    def tangentSplitterVertex(self, index):
        return index == len(self.C)-1
