import math
import numpy as np
from tangentsegment import angle, intersect
import Queue

def distributePoints(Si, i, P, C):
	print(P)
	Pdash = [p for p in P if p[0] > C[i][0]]
	print(Pdash)
	Pdash += C[i+1:]
	print(Pdash)
	#for p in Pdash:
	#	print(angle([C[i][0],C[i][1]+1],p))
	Pdash.sort(key=lambda x: angle([C[i][0],C[i][1]+10],[x[0]-C[i][0],x[1]-C[i][1]]))
	print("the queue is:\t{0}".format(Pdash))
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
			#print("find the left most edge e in T such that e is on the right side of {0} with regards to the sweep line".format(p))
			e = findLeftMostEdgeRightOfP(T,p,C[i])
			if e:
				idx = C.index(e[0])
				distributedPoints[idx] += [p]
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
	if p in [[37,28],[10,7],[51,19]]:
		return True
	return False

def findLeftMostEdgeRightOfP(T,p,Ci):
	#print(Ci)
	sweepline = getSweepLine(Ci,p)
	#print(sweepline)
	found = False
	i = 0
	#print(T)
	if debugPoints(p):
		print("T:\t{0}".format(T))
		print("sweepline:\t{0}".format(sweepline))
	while not found and i < len(T):
		dotp  = dotProduct(sweepline,T[i][0])
		dotp2  = dotProduct(sweepline,T[i][1])
		if debugPoints(p):
			print("\tedge:\t{0}".format(T[i]))
			print("dotProducts:\t{0},{1}".format(dotp,dotp2))
		#print("{2}:\t{0}\t{1}".format(dotp, dotp2,type(dotp)))
		#if intersect(sweepline[0],sweepline[1],T[i][0],T[i][1]):
		if dotp < 0 and dotp2 < 0:
			found = True
			return T[i]
		i+=1
	return None

