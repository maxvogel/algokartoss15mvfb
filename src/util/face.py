class face(object):
    def __init__(self, C, p, maximal):
        self.C = C  #polygonal chain
        self.p = p
        self.maximal = maximal

    def pointStored(self):
        """
        if there's a point associated with
        a face, return true
        """
        return self.p

    def maximalTangent(self):
        return self.maximal

    def tangentSplitterVertex(self, index):
        return index == len(self.C)-1
