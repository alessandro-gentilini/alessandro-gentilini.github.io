import math
import numpy as np
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
rho = 2650
fill_factor = .6
rho_w = 1000
h = 1
phi=15

rho_b = fill_factor*rho
c = 0#rho_b*g*h
thetas = [x * 0.5 for x in range(2, 141)]
thetas = np.arange(1, 70, 0.5)
FS_asciutto = []
for theta in thetas:
    FS_asciutto.append(asciutto(rho_b,g,h,theta,c,phi))


rho_b = fill_factor*rho+(1-fill_factor)*rho_w
c = 0#rho_b*g*h
FS_bagnato = []
for theta in thetas:
    FS_bagnato.append(bagnato(rho_b,g,h,theta,c,phi,rho_w))

rho_b = fill_factor*rho+((1-fill_factor)*rho_w)/2
c = 0#rho_b*g*h
FS_semi_asciutto = []
for theta in thetas:
    FS_semi_asciutto.append(bagnato(rho_b,g,h,theta,c,phi,rho_w))

plt.plot(thetas, FS_asciutto, color='brown')
plt.plot(thetas, FS_semi_asciutto, color='tab:green')
plt.plot(thetas, FS_bagnato, color='tab:blue')
plt.xlabel(r'$\vartheta$/°')
plt.ylabel(r'FS')
plt.axhline(1, color='gray')
plt.show()