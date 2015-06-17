import sys
import os

from algorithm.helper import *
from parser.gml import GML
import map

def readData(file_lines, file_points):
	gml = GML()
	gml.readLines(file_lines)
	gml.readPoints(file_points)
	return (gml.getListOfLines(),gml.getListOfPoints())

def writeData(file_simple,polygonal_chains):
	with open(file_simple,"w") as file:
		base_str = """{}:<gml:LineString srsName="EPSG:54004" xmlns:gml="http://www.opengis.net/gml"><gml:coordinates decimal="." cs="," ts=" ">{}</gml:coordinates></gml:LineString>\n"""
		for chain in polygonal_chains:
			chainStr = [",".join([str(p) for p in point]) for point in chain]
			file.write(base_str.format(chain[0]," ".join(chainStr)))

def runMain(args):
	try:
		# TODO: maybe check manually if the given paths are actually files. currently, there is Error raised if wrong file(path)s are given
		polygonalChains, points = readData(args[2],args[3])
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	k = int(args[1])
	simplified_chains = []
	for idx,pc in polygonalChains:
		shortcut = computeSimplifiedChain(pc,points,None)
		if k > 0 and len(shortcut) > k:
			print("ERROR: polygonal chain with index {} could not be simplified".format(idx))
		else:
			if k == 0: print("simplified polygonal chain index {} from {} to {} segments".format(idx,len(pc),len(shortcut)))
			simplified_chains.append((idx,shortcut))
	writeData(args[4],simplified_chains)

if __name__ == "__main__":
	if not len(sys.argv) == 5:
		print("ERROR: wrong number of parameters")
		print("Usage:\npython[2] simp.py MaxEdgesToKeep LineInputFilePath PointInputFilePath OutputFilePath")
	else:
 		runMain(sys.argv)
