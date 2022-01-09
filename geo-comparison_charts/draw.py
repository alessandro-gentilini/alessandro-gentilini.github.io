from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import json
import sys

from numpy import Infinity

pp = json.loads(sys.stdin.read())

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

fig, ax = plt.subplots(1,1)

for p in pp:
    ax.add_patch(Polygon(to_polygon(p)))

ax.set_xlim(min_x,max_x)
ax.set_ylim(min_y,max_y)
ax.axis('square')
ax.figure.savefig('chart.png',bbox_inches='tight')
plt.show()

