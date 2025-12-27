from math import exp, sin, sqrt
import matplotlib.pyplot as plt

kappa = 37.2
theta_max = 10
theta_min = -15
theta_r = theta_max-theta_min
omega = 2*3.1415



def theta(z,t):
    s = sqrt(omega/(2*kappa))
    return .5*theta_r*exp(-z*s)*sin(omega*t-z*s)

x1 = []
y1 = []
N = 1000
for i in range(0,1+N):
    t = 3*i/N
    x1.append(t)
    y1.append(theta(1,t))

x2 = []
y2 = []
N = 1000
for i in range(0,1+N):
    t = 3*i/N
    x2.append(t)
    y2.append(theta(10,t))

plt.plot(x1,y1,label='z=1m')
plt.plot(x2,y2,label='z=10m')
plt.legend()
plt.show()

xx = []
yy = []
labels = []

for i in range(0,11):
    N = 100
    t = i/10
    x = []
    y = []
    labels.append(f't={t:.1f}')
    for j in range(0,1+N):
        z = 20*j/N
        x.append(z)
        y.append(theta(z,t))
    xx.append(x)
    yy.append(y)




plt.figure()
for i in range(0,11):
    plt.plot(xx[i],yy[i],label=labels[i])
plt.xlabel('z')
plt.legend(loc='upper right')
plt.show()