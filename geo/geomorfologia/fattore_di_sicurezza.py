import math
import numpy as np
import matplotlib.pyplot as plt

def FS(rho,g,h,theta,c,phi,fill_factor, saturation, rho_w):
    rho_b = fill_factor*rho+saturation*(1-fill_factor)*rho_w
    sigma = rho_b*g*h*math.cos(math.radians(theta))
    u = saturation*rho_w*g*h*math.cos(math.radians(theta))
    S = c+(sigma-u)*math.tan(math.radians(phi))
    tau = rho_b*g*h*math.sin(math.radians(theta))
    return S/tau



g = 9.8
rho = 2650
fill_factor = .6
rho_w = 1000
h = 1
phi=15
thetas = np.arange(1, 70, 0.5)


c = 0#rho_b*g*h
saturation = 0
FS_asciutto = []
for theta in thetas:
    FS_asciutto.append(FS(rho,g,h,theta,c,phi,fill_factor,saturation,rho_w))



c = 0#rho_b*g*h
saturation = 1
FS_bagnato = []
for theta in thetas:
    FS_bagnato.append(FS(rho,g,h,theta,c,phi,fill_factor,saturation,rho_w))


c = 0#rho_b*g*h
saturation = .5
FS_semi_asciutto = []
for theta in thetas:
    FS_semi_asciutto.append(FS(rho,g,h,theta,c,phi,fill_factor,saturation,rho_w))

plt.plot(thetas, FS_asciutto, color='brown')
plt.plot(thetas, FS_semi_asciutto, color='tab:green')
plt.plot(thetas, FS_bagnato, color='tab:blue')
plt.xlabel(r'$\vartheta$/°')
plt.ylabel(r'FS')
plt.axhline(1, color='gray')
plt.show()