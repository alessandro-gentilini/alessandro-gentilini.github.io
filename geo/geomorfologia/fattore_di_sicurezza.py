import math
import matplotlib.pyplot as plt

def FS(rho_b,g,h,theta,c,phi,rho_w):
    sigma = rho_b*g*h*math.cos(math.radians(theta))
    u = rho_w*g*h*math.cos(math.radians(theta))
    S = c+(sigma-u)*math.tan(math.radians(phi))
    tau = rho_b*g*h*math.sin(math.radians(theta))
    return S/tau

def bagnato(rho_b,g,h,theta,c,phi,rho_w):
    return FS(rho_b,g,h,theta,c,phi,rho_w)

def asciutto(rho_b,g,h,theta,c,phi):
    return FS(rho_b,g,h,theta,c,phi,0)

g = 9.8
rho_b = 1650
h = 1
phi=15
c = rho_b*g*h

thetas = range(1,70)
FS_asciutto = []
for theta in thetas:
    FS_asciutto.append(asciutto(rho_b,g,h,theta,c,phi))

plt.plot(thetas,FS_asciutto)
plt.axhline(1)
plt.show()