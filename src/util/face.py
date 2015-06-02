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
        return type(self.p) == list

    def maximalTangent(self):
        return self.maximal
