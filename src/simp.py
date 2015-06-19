import sys
import os

from algorithm.helper import *
from parser.gml import GML
from map.draw import plotSimplifiedAndOriginal
import map

def readData(file_lines, file_points):
        gml = GML()
        gml.readLines(file_lines)
        gml.readPoints(file_points)
        return (gml, gml.getListOfLines(), gml.getListOfPoints())


def writeData(file_simple,polygonal_chains):
	with open(file_simple,"w") as file:
		base_str = """{}:<gml:LineString srsName="EPSG:54004" xmlns:gml="http://www.opengis.net/gml"><gml:coordinates decimal="." cs="," ts=" ">{}</gml:coordinates></gml:LineString>\n"""
		for chain in polygonal_chains:
                        chainFlattened = list(sum(chain[1], ()))
			chainStr = [" ".join([str(p) for p in chainFlattened])]
			file.write(base_str.format(chain[0]," ".join(chainStr)))

def runMain(args):
        plot_flag = 0
        if len(args) == 6 and args[1] == '--plot':
                plot_flag = 1

        try:
		# TODO: maybe check manually if the given paths are actually files. currently, there is Error raised if wrong file(path)s are given
		gml, polygonalChains, points = readData(args[2+plot_flag],args[3+plot_flag])
                print "Successfully read lines from file {}, and points from file {}.".format(args[2+plot_flag],args[3+plot_flag])

	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)


	k = int(args[1+plot_flag])
	simplified_chains = []

	for idx,pc in polygonalChains:

		shortcut = simplifyChain(pc, points, 10**10)  #computeSimplifiedChain(pc,points,None)
		if k > 0 and len(shortcut) > k:
			print("ERROR: polygonal chain with index {} could not be simplified".format(idx))
		else:
			if k == 0: print("simplified polygonal chain with index {} from {} to {} segments".format(idx,len(pc),len(shortcut)))
			simplified_chains.append((idx,shortcut))
	writeData(args[4+plot_flag],simplified_chains)

        if plot_flag == 1:
                gmlSimplified = GML()
                gmlSimplified.readLines(args[4+plot_flag])
                gmlSimplified.readPoints(args[3+plot_flag])
                plotSimplifiedAndOriginal(gml, gmlSimplified)


if __name__ == "__main__":
	if not (len(sys.argv) == 5 or len(sys.argv) == 6):
		print("ERROR: wrong number of parameters")
		print("Usage:\npython[2] simp.py MaxEdgesToKeep LineInputFilePath PointInputFilePath OutputFilePath")
	else:
 		runMain(sys.argv)
