from util.planargeometry import *
from util.face import *


def discardShortcuts(from_, Q, slope):
    if from_ == "front":
        while angle(Q[i]) > slope:
            Q.pop(0)

    elif from_ == "back":
        while angle(Q[i]) < slope:
            Q.pop(len(Q)-1)

    return Q

def discard_and_accept(C, Si, i):
    """
    Parameters
    ----------


    Returns
    -------

    """
    accept = []
    xaxis = [1,0]
    Qplus = [[C[i],Cj] for Cj in C[i+1:] if Cj[1] >= 0]
    Qmin  = [[C[i],Cj] for Cj in C[i+1:] if Cj[1] <  0]
    j = i
    Qplus.sort(key=lambda x: angle(x[1],xaxis), reverse=True)
    Qmin.sort(key=lambda x: angle(x[1],xaxis), reverse=False)
    Q = Qplus + Qmin

    for face in Si:
        if face.pointStored():
            slope = angle(C[i], face.p)
            if face.maximalTangent():
                discardShortcuts("front", Q, slope)
            else:
                discardShortcuts("back", Q, slope)

            while not face.tangentSplitterVertex(j):
                j = j+1
                if [C[i],C[j]] in Q:
                    accept.append([C[i],C[j]])
                    Q.remove([C[i],C[j]])
