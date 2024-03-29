# taken from "Motion in a central field" https://marksmath.org/visualization/orbits/CentralOrbit.html by Mark McClure
# Imports
# SciPy's numerical ODE solver
from scipy.integrate import odeint
import scipy.optimize as spo
# The fabulous numpy library:
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from matplotlib import collections as mc

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

def Fun(s,t,k): return [s[2],s[3],
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
    solution = odeint(Fun,[x0+i*Delta_x,y0,vx0,vy0],t,args=(k,))
    x = solution[:,0]
    y = solution[:,1]
    ax.plot(x,y, '-')
    ax.set_aspect('equal', 'box')

ax.plot([0],[0], '*')

k = 1000
t = np.linspace(0,5,100)
# v1
A = (1.1,10.9-1.5)
B = (1.1,10.9-6)

# d1
C = (2.7,10.9-6)
D = (6.8,10.9-1.5)

# v2
E = (1.8,10.9-1.5)
F = (1.8,10.9-6)

# d2
G = (5.3,10.9-6)
H = (7,10.9-4.9)

#fig, ax = plt.subplots(1)
solution = odeint(Fun,[1.1,4.1,0,-1.2],t,args=(k,))
#x = solution[:,0]
#y = solution[:,1]
#ax.plot(x,y, '-')
#ax.set_aspect('equal', 'box')

accum = 0
for r in solution:
    v1 = p2ld(r[0],r[1],A[0],A[1],B[0],B[1])
    d1 = p2ld(r[0],r[1],C[0],C[1],D[0],D[1])
    if v1 < d1:
        accum = accum + v1
        #ax.plot(r[0],r[1], 'd',color='C0')
    else:
        accum = accum + d1
        #ax.plot(r[0],r[1], 'x',color='C0')

solution = odeint(Fun,[1.8,4.1,0,-1.2],t,args=(k,))
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
        #ax.plot(r[0],r[1], 'd',color='C1')
    else:
        accum = accum + d2
        #ax.plot(r[0],r[1], 'x',color='C1')








def tenta(args):
    vy0 = args[0]
    k = args[1]
    fig, ax = plt.subplots(1)

    #ax.axline((1.1,9.4),(1.2,4.9),ls='--',color='C0')
    ax.axline(A,B,ls='--',color='C0')
    ax.axline(C,D,ls='--',color='C0')

    #ax.axline((1.8,9.4),(1.9,4.9),ls='--',color='C1')
    ax.axline(E,F,ls='--',color='C1')
    ax.axline(G,H,ls='--',color='C1')

    ax.plot([0],[0], '*')

    cost = 0
    t = np.linspace(0,5,100)
    solution = odeint(Fun,[1.1,4.1,0,vy0],t,args=(k,))
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
    cost = cost + accum

    solution = odeint(Fun,[1.8,4.1,0,vy0],t,args=(k,))
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
    cost = cost + accum

    ax.set_aspect('equal', 'box')
    ax.set_title('cost={0:f} vy0={1:f} k={2:f}'.format(cost,vy0,k))
    timestamp = datetime.datetime.now().isoformat().replace(":","-")
    fig.savefig(timestamp+'.png', dpi=fig.dpi)


    return cost

# print(tenta(-1.1,1000))
# print(tenta(-1.2,1000))
# print(tenta(-1.3,1000))
# print(tenta(-1.4,1000))
# print(tenta(-1.5,1000))
# print(tenta(-1.6,1000))

guess = [-1.5,1000]
#spo.basinhopping(tenta,guess,niter=1)

rranges = (slice(-2, -1, 0.5), slice(900, 1000, 50))
#spo.brute(tenta,rranges)


fig, ax = plt.subplots()
scale = 362/188
fig.set_size_inches(scale*6.4,scale*4.8)
# -1.26665 k=1062.093506
x0s = [1.1, 1.8, 2.3, 3.4, 4.4, 5.3, 6.4, 7.7, 9.7]
t = np.linspace(0,7,100)

for x0 in steps:
    # Solve it!
    solution = odeint(Fun,[x0,4.1,0,-1.26665],t,args=(1062.093506,))
    x = solution[:,0]
    y = solution[:,1]
    ax.plot(x,y, '-')
    ax.set_aspect('equal', 'box')

lines = []
colors = []
styles = []
for x0 in steps:
    lines.append([(x0,4.1),(x0,10.9)])
    colors.append('gray')
    styles.append('--')

ax.add_collection(mc.LineCollection(lines,colors=colors,linestyle=styles))

lines = [[(0,0),(0,4.1)],[(0,4.1),(0,10.9)]]
ax.add_collection(mc.LineCollection(lines,colors=['black','black'],linestyle=['--','-']))

ax.plot([0],[0],'*',color='black')
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.savefig('result.png', dpi=fig.dpi)
print(fig.dpi,fig.get_size_inches())
print(ax.transData.transform([(0,9.7),(9.7,0)])-ax.transData.transform((0,0)))

pixels = np.array([56,82,101,141,177,214,254,303,376])-15




