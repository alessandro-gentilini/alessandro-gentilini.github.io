# Section "An Example of Ordinary Kriging" at page 290 of the book:
# ISAAKS, Edward and SRIVASTAVA, Mohan. An Introduction to Applied Geostatistics. Oxford University Press, 1989. 

import pandas as pd
import numpy as np
import math

df=pd.read_csv('table_12.1.csv')

X_0=65
Y_0=137

xx=[X_0]+df.X.values.tolist()
yy=[Y_0]+df.Y.values.tolist()

distances=np.zeros((len(xx),len(xx)))

def euclidean_distance(x1,x2,y1,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2) # but have a look at math.hypot

for i in range(0,len(xx)):
    for j in range(0,len(xx)):
        distances[i,j]=euclidean_distance(xx[i],xx[j],yy[i],yy[j])

def C_tilde(h):
    return 10*math.exp(-0.3*abs(h))   

C=np.ones((len(xx),len(xx)))    
C[len(xx)-1,len(xx)-1]=0

for i in range(1,len(xx)):
    for j in range(1,len(xx)):
        C[i-1,j-1]=C_tilde(distances[i,j])

D=np.ones((len(xx),1))  

for i in range(1,len(xx)):
    D[i-1,0]=C_tilde(distances[i,0])

C_inverse = np.linalg.inv(C)

w = np.matmul(C_inverse,D)

v_0_hat = np.dot(w[:-1,0],df.V.values)