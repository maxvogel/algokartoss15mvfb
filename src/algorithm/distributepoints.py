import math
import numpy as np
from tangentsegment import angle, intersect
from util.planargeometry import *
import Queue

def distributePoints(Si, i, P, C):
	#print(P)
	Pdash = [p for p in P if p[0] > C[i][0]]
	#print(Pdash)
	Pdash += C[i+1:]
	#print(Pdash)
	#for p in Pdash:
	#	print(angle([C[i][0],C[i][1]+1],p))
	Pdash.sort(key=lambda x: angle([C[i][0],C[i][1]+10],[x[0]-C[i][0],x[1]-C[i][1]]))
	#print("the queue is:\t{0}".format(Pdash))
	#T binary search tree
	T = []
	distributedPoints = [[] for x in C]
	for j in range(0,len(Pdash)):
		p = Pdash[j]
		if p in C:
			idx = C.index(p)
			#print("point {0} of queue is in polygonal chain: update search tree with edges of the point".format(p))
			if idx > 0 and not [C[idx-1],C[idx]] in T:
				T += [[C[idx-1],C[idx]]]
			if idx < len(C)-1 and not [C[idx],C[idx+1]] in T:
				T += [[C[idx],C[idx+1]]]
		else:
			# sort by x-coordinate of the "left" point of the edge
			T.sort(key=lambda x: x[0][0])
			#print("find the left most edge e in T such that e is on the right side of {0} with regards to the sweep line".format(p))
			e = findLeftMostEdgeRightOfP(T,p,C[i])
			if e:
				idx = C.index(e[0])
				distributedPoints[idx] += [p]
				#print("attaching point {0} to edge {1}".format(p,e))
			#e = linkeste Kante v_k bis v_k+1 in T rechts von p auf sweep line 
			#speichere p an e
	return distributedPoints

def getSweepLine(Ci,p):
	return [Ci,[Ci[0]+100*(p[0]-Ci[0]),Ci[1]+100*(p[1]-Ci[1])]]

def dotProduct(a,b):
	line = [a[1][0]-a[0][0],a[1][1]-a[0][1]]
	point = [b[0]-a[0][0],b[1]-a[0][1]]
	return line[0]*point[1]-line[1]*point[0]

def debugPoints(p):
	lO = [[37,28],[10,7],[51,19]]
	lTw = [[37,28],[70,-7],[40,-7]]
	lTh = [[87,13],[20,8],[53,-5],[59,-7]]
	if p in lTh:
		return True
	return False

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
			#print(int(intersection[0]) == sweepline[0][0])
			#print(int(intersection[1]) == sweepline[0][1])
			if intersection[0] > p[0]:
				#if not int(intersection[0]) == Ci[0] and not int(intersection[1]) == Ci[1]:
				#print("returning edge:\t{0}".format(T[i]))
				found = True
				result = T[i]
		else:
			#print("\tremoving edge from T:\t{0}".format(T[i]))
			#if T[i] == [[70, 10], [75, -2]]: 
			#	foo = 2
			#else:
			toDelete.append(T[i])
		i+=1
	for e in toDelete:
		try:
			T.remove(e)
		except ValueError:
			print("\ttried to delete edge e from T that is not in T:\t{0}".format(e))
	#print("-----------------------")
	return result