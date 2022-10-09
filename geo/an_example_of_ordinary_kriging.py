# Section "An Example of Ordinary Kriging" at page 290 of the book:
# ISAAKS, Edward and SRIVASTAVA, Mohan. An Introduction to Applied Geostatistics. Oxford University Press, 1989. 

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# Table 12.1 at page 291.
df=pd.read_csv('table_12.1.csv')



# Point where to estimate V, it is written in Table 12.1 at page 291.
X_0=65
Y_0=137

def estimate_at(X_0,Y_0,df):
    xx=[X_0]+df.X.values.tolist()
    yy=[Y_0]+df.Y.values.tolist()

    # Create table 12.2 at page 293.
    distances=np.zeros((len(xx),len(xx)))

    def euclidean_distance(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2) # but have a look at math.hypot

    for i in range(0,len(xx)):
        for j in range(0,len(xx)):
            distances[i,j]=euclidean_distance(xx[i],xx[j],yy[i],yy[j])

    # Formula (12.25) at page 293.
    def C_tilde(h):
        return 10*math.exp(-0.3*abs(h))   

    # Create matrix C at page 294.
    C=np.ones((len(xx),len(xx)))    
    C[len(xx)-1,len(xx)-1]=0

    for i in range(1,len(xx)):
        for j in range(1,len(xx)):
            C[i-1,j-1]=C_tilde(distances[i,j])

    # Create vector D at page 294.
    D=np.ones((len(xx),1))  

    for i in range(1,len(xx)):
        D[i-1,0]=C_tilde(distances[i,0])

    # Inverse of matrix C at page 294.
    C_inverse = np.linalg.inv(C)

    # Parameters w at page 295
    w = np.matmul(C_inverse,D)

    # Estimate at page 295
    v_0_hat = np.dot(w[:-1,0],df.V.values)
    return v_0_hat

print(estimate_at(X_0,Y_0,df))

x_list = df['X']
y_list = df['Y']
z_list = df['V']

# f will be a function with two arguments (x and y coordinates),
# but those can be array_like structures too, in which case the
# result will be a matrix representing the values in the grid 
# specified by those arguments
f = interp2d(x_list,y_list,z_list,kind="linear")

x_coords = np.arange(-3+min(x_list),max(x_list)+3)
y_coords = np.arange(-3+min(y_list),max(y_list)+3)
Z = f(x_coords,y_coords)

fig = plt.imshow(Z,
           extent=[-3+min(x_list),max(x_list)+3,-3+min(y_list),max(y_list)+3],
           origin="lower")

# Show the positions of the sample points, just to have some reference
#fig.axes.set_autoscale_on(False)
fig.axes.scatter(x_list,y_list,facecolors='black')
