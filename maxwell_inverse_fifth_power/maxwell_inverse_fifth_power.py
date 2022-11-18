# Imports
# SciPy's numerical ODE solver
from scipy.integrate import odeint
# The fabulous numpy library:
import numpy as np
import matplotlib.pyplot as plt

# Parameters
G = 1
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

def F(s,t): return [s[2],s[3],
    G*s[0]/(s[0]**2 + s[1]**2)**(6/2),
    G*s[1]/(s[0]**2 + s[1]**2)**(6/2),
]

# We'll solve the system for the following values of t, namely
# 100 equally spaced values between 0 and 2.
t = np.linspace(0,5,100)

fig, ax = plt.subplots(1)
steps = [1,1.5,2,3,4,5,6,7,9]
Delta_x = .1

for i in steps:
    # Solve it!
    solution = odeint(F,[x0+i*Delta_x,y0,vx0,vy0],t)
    x = solution[:,0]
    y = solution[:,1]
    ax.plot(x,y, '-')
    ax.set_aspect('equal', 'box')

ax.plot([0],[0], '*')

G = 1000
t = np.linspace(0,5,100)

fig, ax = plt.subplots(1)
solution = odeint(F,[1.1,4.1,0,-1.5],t)
x = solution[:,0]
y = solution[:,1]
ax.plot(x,y, '-')
ax.set_aspect('equal', 'box')

solution = odeint(F,[1.8,4.1,0,-1.5],t)
x = solution[:,0]
y = solution[:,1]
ax.plot(x,y, '-')
ax.set_aspect('equal', 'box')

#ax.axline((1.1,9.4),(1.2,4.9),ls='--',color='C0')
ax.axline((1.1,9.4),(1.1,4.9),ls='--',color='C0')
ax.axline((2.7,4.9),(6.8,9.4),ls='--',color='C0')

#ax.axline((1.8,9.4),(1.9,4.9),ls='--',color='C1')
ax.axline((1.8,9.4),(1.8,4.9),ls='--',color='C1')
ax.axline((5.3,4.9),(7,6),ls='--',color='C1')


ax.plot([0],[0], '*')

plt.show()