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

def xmonotoneSubchains(C):
    """
    Returns
    -------

    a list of all x-monotone subchain, which are
    defined by left and right turns of the polygonal chain
    """

    i = 0; subchains = []

    while i < len(C):
        x = []
        if not isLeftTurn(C,i):
            x.append(C[i])
        else:
            subchain.append(x)
            while not isRightTurn:
                i = i+1

    return subchains
