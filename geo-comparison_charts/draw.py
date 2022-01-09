from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import json

polygon  = []
p1 = json.loads('[[100,100],[300,100],[300,300],[100,300]]')
#p1 = json.loads('[[0,141.421],[141.421,282.843],[0,424.264],[-141.421,282.843]]')
for p in p1:
    polygon.append((p[0],p[1]))

fig, ax = plt.subplots(1,1)
ax.add_patch(Polygon(polygon))
plt.xlim(-500,500)
plt.ylim(-500,500)
plt.axis('square')

plt.show()