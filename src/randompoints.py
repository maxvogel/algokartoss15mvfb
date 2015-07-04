import numpy as np

def randomPoints(bb_ul, bb_lr, num):
    """
    Parameters
    ----------
    bb_ul : point bounding box upper left
    bb_lr : point bounding box lower right
    num : number of points

    Returns
    num random points in bounding box
    -------
    """
    ptsX = map(lambda x: bb_ul[0]+x*(bb_lr[0]-bb_ul[0]), np.random.rand(num))
    ptsY = map(lambda y: bb_lr[1]+y*(bb_ul[1]-bb_lr[1]), np.random.rand(num))

    return zip(*(ptsX, ptsY))


def writeRandomPoints(randP_file, randP):

    with open(randP_file,"w") as file:
        base_str = """{}:<gml:Point srsName="EPSG:54004" xmlns:gml="http://www.opengis.net/gml"><gml:coordinates decimal="." cs="," ts=" ">{}</gml:coordinates> </gml:Point>\n"""
        for i,p in enumerate(randP):
            file.write(base_str.format(i," "+str(p[0])+str(" ")+str(p[1])))

bbleftupper  = [-8.17e+06,5.25e+06]
bbrightlower = [-7.85e+06,5.04e+06]
writeRandomPoints("randP.txt", randomPoints(bbleftupper, bbrightlower, 2000))
