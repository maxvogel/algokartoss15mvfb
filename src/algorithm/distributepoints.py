import math
import numpy as np
from tangentsegment import angle, intersect
from util.planargeometry import *
import Queue

def distributePoints(Si, i, P, C, w_max, w_min):
	Pdash = [p for p in P if p[0] > C[i][0]]
	Pdash += C[i+1:]
	Pdash.sort(key=lambda x: angle([0,1],[x[0]-C[i][0],x[1]-C[i][1]]))
	#print("the queue for the point {0} is:\t{1}".format(C[i],Pdash))
	#T binary search tree
	T = []
	distributedPoints = [[] for x in C]
	for j in range(0,len(Pdash)):
		p = Pdash[j]
		if p in C:
			idx = C.index(p)
			#print("point {0} of queue is in polygonal chain: update search tree with edges of the point".format(p))
			if idx > i and not [C[idx-1],C[idx]] in T:
				T += [[C[idx-1],C[idx]]]
			if idx < len(C)-1 and not [C[idx],C[idx+1]] in T:
				T += [[C[idx],C[idx+1]]]
		else:
			# sort by x-coordinate of the "left" point of the edge
			# it probably would be cheaper to keep T sorted i.e. inserting an edge at the correct position
			# rather than sorting it everytime
			T.sort(key=lambda x: x[0][0])
			#print("find the left most edge e in T such that e is on the right side of {0} with regards to the sweep line".format(p))
			e = findLeftMostEdgeRightOfP(T,p,C[i])
			if e:
				idx = C.index(e[0])
				distributedPoints[idx] += [p]
				#print("attaching point {0} to edge {1}".format(p,e))
	filteredPoints = [[] for p in Si]
	trackedPoints = []
	for face in Si:
		for p in range(0,len(face)-1):
			if not face[p] in trackedPoints and face[p] in C:
				trackedPoints += [face[p]]
				if len(distributedPoints[C.index(face[p])]) > 0:
					for o in distributedPoints[C.index(face[p])]:
						if not filteredPoints[Si.index(face)]:
							filteredPoints[Si.index(face)] = o
						elif isFaceOrientation(face,w_min):
							filteredPoints[Si.index(face)] = min(o,filteredPoints[Si.index(face)], key=lambda x: angle([0,1],[x[0]-C[i][0],x[1]-C[i][1]]))
						elif isFaceOrientation(face,w_max):
							filteredPoints[Si.index(face)] = max(o,filteredPoints[Si.index(face)], key=lambda x: angle([0,1],[x[0]-C[i][0],x[1]-C[i][1]]))
						else:
							print("face has neither min or max orientation")
		#print("face {} with point {}".format(Si.index(face),filteredPoints[Si.index(face)]))
	#print("----------------------------")
	return distributedPoints, filteredPoints

def isFaceOrientation(face,w):
	for line in w:
		if line[0] in face and line[1] in face:
			return True
	return False

def getSweepLine(Ci,p):
	return [Ci,[Ci[0]+100*(p[0]-Ci[0]),Ci[1]+100*(p[1]-Ci[1])]]

def findLeftMostEdgeRightOfP(T,p,Ci):
	sweepline = getSweepLine(Ci,p)
	#print("checking point:\t{0}".format(p))
	#print("\tT:\t{0}".format(T))
	#print("\tsweepline:\t{0}".format(sweepline))		
	toDelete = []
	result = None
	found = False
	i = 0
	while not found and i < len(T):
		#print("\ttesting edge:\t{0}".format(T[i]))
		if intersect(sweepline[0],sweepline[1],T[i][0],T[i][1]):
			intersection = intersectionPoint(sweepline[0],sweepline[1],T[i][0],T[i][1])
			#print("\tintersectionPoint:\t{0}".format(intersection))
			if intersection[0] > p[0]:
				#print("returning edge:\t{0}".format(T[i]))
				found = True
				result = T[i]
		else:
			#print("\tremoving edge from T:\t{0}".format(T[i]))
			toDelete.append(T[i])
		i+=1
	for e in toDelete:
		try:
			T.remove(e)
		except ValueError:
			print("\ttried to delete edge e from T that is not in T:\t{0}".format(e))
	#print("-----------------------")
	return result