class face(object):
    """
    Attributes
    ----------
    C : list of x/y coordinates
        polygonal chain
    p : bool
        true if a point is associated with this face
    minimax: string
             'max' for maximal face
             'min' for minimal face
    """
    def __init__(self, C, p, minmax):
        self.C = C  #polygonal chain
        self.p = p
        self.minmax = minmax

    def pointStored(self):
        """
        Returns
        -------
        true if there's a point associated with
        this face
        """
        return self.p

    def maximalTangent(self):
        if self.minmax == "max":
            return True
        elif self.minmax == "min":
            return False

    def tangentSplitterVertex(self, index):
        return index == len(self.C)-1
