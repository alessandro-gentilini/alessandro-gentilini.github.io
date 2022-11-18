# taken from "Motion in a central field" https://marksmath.org/visualization/orbits/CentralOrbit.html by Mark McClure
# Imports
# SciPy's numerical ODE solver
from scipy.integrate import odeint
# The fabulous numpy library:
import numpy as np
import matplotlib.pyplot as plt
import math

def p2ld(x0,y0,x1,y1,x2,y2):
    return abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)

# Parameters
k = 1
x0 = 0
y0 = 3
vx0 = 0
vy0 = -1

# In the following definition of F, s is a state vector whose components represent the following:
#   s[0]: Horizontal or x position
#   s[1]: Vertical or y position
#   s[2]: Horizontal velocity
#   s[3]: Vertical velocity
# In general, F can depend upon time t as well. Although our F is independent of t, we still need to
# indicate that it is a possible variable.

def Fun(s,t): return [s[2],s[3],
    k*s[0]/(s[0]**2 + s[1]**2)**(6/2),
    k*s[1]/(s[0]**2 + s[1]**2)**(6/2),
]

# We'll solve the system for the following values of t, namely
# 100 equally spaced values between 0 and 2.
t = np.linspace(0,5,100)

fig, ax = plt.subplots(1)
steps = [1,1.5,2,3,4,5,6,7,9]
Delta_x = .1

for i in steps:
    # Solve it!
    solution = odeint(Fun,[x0+i*Delta_x,y0,vx0,vy0],t)
    x = solution[:,0]
    y = solution[:,1]
    ax.plot(x,y, '-')
    ax.set_aspect('equal', 'box')

ax.plot([0],[0], '*')

k = 1000
t = np.linspace(0,5,100)
# v1
A = (1.1,9.4)
B = (1.1,4.9)

# d1
C = (2.7,4.9)
D = (6.8,9.4)

# v2
E = (1.8,9.4)
F = (1.8,4.9)

# d2
G = (5.3,4.9)
H = (7,6)

fig, ax = plt.subplots(1)
solution = odeint(Fun,[1.1,4.1,0,-1.5],t)
x = solution[:,0]
y = solution[:,1]
#ax.plot(x,y, '-')
ax.set_aspect('equal', 'box')

accum = 0
for r in solution:
    v1 = p2ld(r[0],r[1],A[0],A[1],B[0],B[1])
    d1 = p2ld(r[0],r[1],C[0],C[1],D[0],D[1])
    if v1 < d1:
        accum = accum + v1
        ax.plot(r[0],r[1], 'd',color='C0')
    else:
        accum = accum + d1
        ax.plot(r[0],r[1], 'x',color='C0')

solution = odeint(Fun,[1.8,4.1,0,-1.5],t)
x = solution[:,0]
y = solution[:,1]
#ax.plot(x,y, '-')
ax.set_aspect('equal', 'box')

accum = 0
for r in solution:
    v2 = p2ld(r[0],r[1],E[0],E[1],F[0],F[1])
    d2 = p2ld(r[0],r[1],G[0],G[1],H[0],H[1])
    if v2 < d2:
        accum = accum + v2
        ax.plot(r[0],r[1], 'd',color='C1')
    else:
        accum = accum + d2
        ax.plot(r[0],r[1], 'x',color='C1')



#ax.axline((1.1,9.4),(1.2,4.9),ls='--',color='C0')
ax.axline(A,B,ls='--',color='C0')
ax.axline(C,D,ls='--',color='C0')

#ax.axline((1.8,9.4),(1.9,4.9),ls='--',color='C1')
ax.axline(E,F,ls='--',color='C1')
ax.axline(G,H,ls='--',color='C1')


ax.plot([0],[0], '*')





plt.show()