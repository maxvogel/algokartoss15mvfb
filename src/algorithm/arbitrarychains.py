def isLeftTurn(C, i):
    """
    Returns
    -------

    true if there's a 'left turn' at index i
    """
    if i == 0 or i == len(C)-1: return False
    return C[i-1][0] < C[i][0] and C[i+1][0] < C[i][0]

def isRightTurn(C, i):
    """
    Returns
    -------

    true if there's a 'right turn' at index i
    """
    if i == 0 or i == len(C)-1: return False
    return C[i-1][0] > C[i][0] and C[i+1][0] > C[i][0]

def startsToRight(C,i):
    while i < len(C)-1 and C[i][0] > C[i+1][0]:
        i = i+1
    return i

def isXmonotone(C):
    for i in range(len(C)-2):
        if C[i][0] > C[i+1][0]:
            return False
    return True

def xMonotoneSubchains(C):
    """
    Returns
    -------

    a list of all x-monotone subchain, which are
    defined by left and right turns of the polygonal chain
    """

    i = 0; subchains = []

    while i < len(C):
        x = []

        if i == 0:
            i = startsToRight(C,i)

        while i < len(C) and not isLeftTurn(C,i):
            x.append(C[i])
            i = i+1

        while i < len(C) and not isRightTurn(C,i):
            i = i+1

        if x:
            subchains.append(x)

    if subchains:
        return subchains
