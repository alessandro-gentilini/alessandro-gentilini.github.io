from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import json
import sys

pp = json.loads(sys.stdin.read())

def to_polygon(vector_of_vector):
    polygon = []
    for p in vector_of_vector:
        polygon.append((p[0],p[1]))
    return polygon

fig, ax = plt.subplots(1,1)

for p in pp:
    ax.add_patch(Polygon(to_polygon(p)))

plt.xlim(-500,500)
plt.ylim(-500,500)
plt.axis('square')

plt.show()