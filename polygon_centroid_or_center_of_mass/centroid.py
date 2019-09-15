import numpy as np
import math
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from shapely.geometry import Polygon

points = np.random.rand(30, 2)   # 30 random points in 2-D
hull = ConvexHull(points)



import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
#plt.plot(points[:,0], points[:,1], 'o')

plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r-', lw=2)
plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'o')

hull_pts = []
for i in xrange(0,len(hull.vertices)):
	hull_pts=hull_pts+[points[hull.vertices[i]]]
	plt.text(points[hull.vertices[i]][0],points[hull.vertices[i]][1],str(i))

def dist(p1,p2):
	return math.hypot(p1[0]-p2[0],p1[1]-p2[1])

from math import sqrt

# http://pyhyd.blogspot.com/2017/08/calculate-centroid-of-polygon-with.html 
def centroid(lstP):
    sumCx = 0
    sumCy = 0
    sumAc= 0
    for i in range(len(lstP)-1):
        cX = (lstP[i][0]+lstP[i+1][0])*(lstP[i][0]*lstP[i+1][1]-lstP[i+1][0]*lstP[i][1])
        cY = (lstP[i][1]+lstP[i+1][1])*(lstP[i][0]*lstP[i+1][1]-lstP[i+1][0]*lstP[i][1])
        pA = (lstP[i][0]*lstP[i+1][1])-(lstP[i+1][0]*lstP[i][1])
        sumCx+=cX
        sumCy+=cY
        sumAc+=pA
        #print(cX,cY,pA)
    ar = sumAc/2.0
    #print(ar)
    centr = ((1.0/(6.0*ar))*sumCx,(1.0/(6.0*ar))*sumCy)
    return centr	
	
D = 0
P = [0,0]
for i in xrange(1,len(hull.vertices)):
	p1 = points[hull.vertices[i-1]]
	p2 = points[hull.vertices[i]]
	d = dist(p1,p2)
	D = D + d
	p3 = d*(p1+p2)
	P = P + p3
	#print(i,d,p1+p2,p3)
	plt.plot(p3[0], p3[1], '+')
	plt.text(p3[0], p3[1], str(i-1)+str(i))
	O = [0,0]
	A = p1+p2
	L = [O,A]
	lc = LineCollection([L])
	plt.gca().add_collection(lc)
	#print(i,points[hull.vertices[i]],points[hull.vertices[i]][0],points[hull.vertices[i]][1])

perimetral_centroid = .5*P/D

print('perimetral_centroid: '+str(perimetral_centroid))

#print(hull_pts)

barycenter = centroid(hull_pts)

print('barycenter: '+str(barycenter))

P = Polygon(hull_pts)

print('shapely: '+str(P.centroid))

plt.plot(perimetral_centroid[0],perimetral_centroid[1],'x')
plt.show()