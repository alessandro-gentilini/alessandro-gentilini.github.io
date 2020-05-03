import zipfile
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

# https://scipy-cookbook.readthedocs.io/items/EyeDiagram.html
def bres_segment_count_slow(x0, y0, x1, y1, grid):
    """Bresenham's algorithm.

    The value of grid[x,y] is incremented for each x,y
    in the line from (x0,y0) up to but not including (x1, y1).
    """

    if np.any(np.isnan([x0,y0,x1,y1])):
        return    

    nrows, ncols = grid.shape

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 0
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    sy = 0
    if y0 < y1:
        sy = 1
    else:
        sy = -1

    err = dx - dy

    while True:
        # Note: this test is moved before setting
        # the value, so we don't set the last point.
        if x0 == x1 and y0 == y1:
            break

        if 0 <= x0 < nrows and 0 <= y0 < ncols:
            grid[int(x0), int(y0)] += 1

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def bres_curve_count_slow(y, x, grid):
    for k in range(x.size - 1):
        x0 = x[k]
        y0 = y[k]
        x1 = x[k+1]
        y1 = y[k+1]
        bres_segment_count_slow(x0, y0, x1, y1, grid)

def linear_scale(x,src_min,src_max,dst_min,dst_max):
    return dst_min+(x-src_min)*(dst_max-dst_min)/(src_max-src_min)


lanes = []
stations = []

zips = glob.glob("./flussi_MTS/*.zip")
for z in zips:
    bn = os.path.basename(z)
    n = os.path.splitext(bn)[0]
    with zipfile.ZipFile(z, 'r') as zip_ref:
        zip_ref.extractall('.')
        new_name = 'RilevazioniPerCorsia-'+n+'.csv'
        os.rename('RilevazioniPerCorsia.csv',new_name)
        lanes.append(new_name)
        new_name = 'RilevazioniPerPostazione-'+n+'.csv'
        os.rename('RilevazioniPerPostazione.csv',new_name)
        stations.append(new_name)

tmp = []
for f in lanes:
    tmp.append(pd.read_csv(f,sep=';',thousands='.'))
    
df = pd.concat(tmp)
df['Giorno'] = pd.to_datetime(df['Giorno'],format="%d/%m/%Y")

df1 = df[df['Giorno']>='2020-02-01']
df1 = df1.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values='Transiti - Totale')
df1 = 100*df1/df1.max()
fig, ax = plt.subplots(1)
df1.plot(legend=False,colormap='Blues',ax=ax)
ax.set_title('Flussi di traffico Emilia Romagna\n(Traffic in Emilia Romagna)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('Emilia_Romagna_all_stations.png',bbox_inches='tight')

ys = []
L = []
for x in df1:
    L.append(len(df1[x]))
    ys.append(df1[x].values)



if all(x==L[0] for x in L):
    tmin = 0
    tmax = L[0]-1
    ymin = np.nanmin(ys)
    ymax = np.nanmax(ys)    
    t = np.linspace(0,L[0]-1,L[0])
    ys_d = []
    grid_W = 800
    grid_H = 600
    grid = np.zeros((grid_H, grid_W), dtype=np.int32)
    td = np.round(linear_scale(t,tmin,tmax,0,grid_W))
    for y in ys:
        ys_d.append(np.round(linear_scale(y,ymin,ymax,0,grid_H)))
    for y in ys_d:
        bres_curve_count_slow(td, y, grid)
    plt.figure()
    # Convert to float32 so we can use nan instead of 0.
    grid = grid.astype(np.float32)
    grid[grid==0] = np.nan
    plt.grid(color='w')
    #plt.imshow(grid.T[::-1,:], extent=[0,1,0,1], cmap=plt.cm.coolwarm, interpolation='gaussian')
    plt.imshow(grid,origin='lower',cmap=plt.cm.Blues_r)
    plt.grid(None)
    ax = plt.gca()
    ax.set_facecolor('k')
    # ax.set_xticks(linear_scale([0,1,2,3,4],tmin,tmax,0,grid_W))
    # ax.set_yticks(linear_scale([0,1,2,3,4,5,6,7,8],ymin,ymax,0,grid_H))
    # ax.set_xticklabels([0,1,2,3,4])
    # ax.set_yticklabels([0,1,2,3,4,5,6,7,8])
    plt.colorbar()
    fig = plt.gcf()        
    plt.savefig("persistence-diagram.png", bbox_inches='tight')



#c1 = (df['Postazione']==251) | (df['Postazione']==255) | (df['Postazione']==505) | (df['Postazione']==651)
#c1 = (df['Postazione']==156) | (df['Postazione']==252) | (df['Postazione']==600) | (df['Postazione']==52)
c1 = df['Postazione']==255
c2 = df['Giorno']>='2020-02-01'
df2 = df[c1&c2]

df3 = df2.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values='Transiti - Totale')
fig, ax = plt.subplots(1)
df3.plot(legend=True,ax=ax)
ax.set_title('Strada: SS 9 tra Castel San Pietro e Imola\n(Traffic along road Via Emilia)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri (number of daily transits)')
ax.set_xlabel('Data (date)')
ax.figure.savefig('station_255_Via_Emilia.png',bbox_inches='tight')

df3 = 100*df3/df3.max()
fig, ax = plt.subplots(1)
df3.plot(legend=True,ax=ax)
ax.set_title('Strada: SS 9 tra Castel San Pietro e Imola\n(Traffic along road Via Emilia)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('station_255_Via_Emilia_normalized.png',bbox_inches='tight')





