# Estimation of the Epicentral Coordinates of a Seismic Event
# TARANTOLA, Albert. Inverse problem theory and methods for model parameter estimation. Society for Industrial and Applied Mathematics, 2005.


import numpy as np
import cuqi
from cuqi.model import Model
from cuqi.geometry import Continuous1D, Discrete
from cuqi.distribution import Gaussian, Uniform, JointDistribution
from cuqi.sampler import MH
import time
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



v = 5
x = np.array([3,3,4,4,5,5])
y = np.array([15,16,15,16,15,16])
t = np.array([3.12,3.26,2.98,3.12,2.84,2.98])

def forward_arrival_time(wrt):
    X = wrt[0]
    Y = wrt[1]
    t = ((x-X)**2+(y-Y)**2)**(1/2)/v
    return t

def jacobian_arrival_time(wrt):
    X = wrt[0]
    Y = wrt[1]
    dAdX = (x-X)/(v*((x-X)**2+(y-Y)**2)**(1/2))
    dAdY = (y-Y)/(v*((x-X)**2+(y-Y)**2)**(1/2))
    J = np.vstack([dAdX,dAdY]).T
    return J

par_names = ['X','Y']
n = len(par_names)
m = len(x)

domain_geometry = Discrete(par_names)
range_geometry = Continuous1D(m)
model = Model(forward=forward_arrival_time, jacobian=jacobian_arrival_time, range_geometry=range_geometry, domain_geometry=domain_geometry)


prior = cuqi.distribution.Uniform(np.array([-30,-30]),np.array([30,30]))
data_std = .1
gg = Gaussian(model(prior),sqrtcov=data_std)

posterior = JointDistribution(prior,gg)(gg=t)

# Metropolis-Hastings sampling
x_init= np.array(prior.sample(), dtype=np.float64)
np.random.seed(1000000)
MHsampler = MH(posterior)#, x0 = x_init)

t_start = time.time()
samplesMH = MHsampler.sample_adapt(1000000, 100000)
print("--- %s seconds ---" % (time.time() - t_start))

fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.plot(samplesMH.samples[0,:], samplesMH.samples[1,:], '.')

df = pd.DataFrame({'X':samplesMH.samples[0,:],'Y':samplesMH.samples[1,:]})

ax = sns.kdeplot(data=df.sample(1000),x='X',y='Y',fill=True)
ax.plot(x,y,'.')
ax.axis('equal')
ax.set(xlim=(0, 20), ylim=(0, 20))
ax.figure.savefig('sns_kde.png')

fig, ax = plt.subplots(nrows = 1, ncols = 1)
df2 = df.sample(1000)
ax.plot(df2['X'],df2['Y'],'.',alpha=.1)
ax.plot(x,y,'.')
ax.axis('equal')
ax.set(xlim=(0, 20), ylim=(0, 20))
ax.figure.savefig('tarantola.png')
