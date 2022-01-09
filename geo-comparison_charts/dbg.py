from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import json
import sys

from numpy import Infinity

data = json.loads(sys.stdin.read())

min_x = Infinity
max_x = 0
min_y = Infinity
max_y = 0

def to_polygon(vector_of_vector):
    polygon = []
    for p in vector_of_vector:
        global min_x, max_x, min_y, max_y
        min_x = min(min_x,p[0])
        max_x = max(max_x,p[0])
        min_y = min(min_y,p[1])
        max_y = max(max_y,p[1])        
        polygon.append((p[0],p[1]))
    return polygon

fig, ax = plt.subplots(3,1)

for p in data['full']:
    ax[0].add_patch(Polygon(to_polygon(p),facecolor='none',edgecolor='blue'))

ax[0].set_xlim(0,600)
ax[0].set_ylim(0,600)
ax[0].axis('square')

#fig, ax = plt.subplots(1,1)

for p in data['full']:
    ax[1].add_patch(Polygon(to_polygon(p),facecolor='none',edgecolor='blue'))

ax[1].add_patch(Polygon(to_polygon(data['candidate'])))

ax[1].set_xlim(0,600)
ax[1].set_ylim(0,600)
ax[1].axis('square')

#fig, ax = plt.subplots(1,1)

for p in data['full']:
    ax[2].add_patch(Polygon(to_polygon(p),facecolor='none',edgecolor='blue'))

for p in data['subset']:
    ax[2].add_patch(Polygon(to_polygon(p),facecolor='none',edgecolor='red'))    

ax[2].add_patch(Polygon(to_polygon(data['candidate'])))

ax[2].set_xlim(0,600)
ax[2].set_ylim(0,600)
ax[2].axis('square')

plt.show()

