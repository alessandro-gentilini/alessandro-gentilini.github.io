import glob
import pandas as pd
import matplotlib.pyplot as plt
import pystan
import utm
#import arviz
import numpy as np


from matplotlib.transforms import offset_copy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt



# dis = glob.glob("./*.DIS")
# displacements = pd.DataFrame()
# cnt = 0
# for f in dis:
#     station = f.split('.')[2]
#     df = pd.read_csv(f,skiprows=50,header=None,names=[station])
#     displacements = pd.concat([displacements, df], axis=1)
#     cnt=cnt+1

# displacements = displacements.reindex(sorted(displacements.columns), axis=1)
# displacements.plot(subplots=True, layout=(cnt,1), ylim=[-.0005,.0005],title='dis')


# vel = glob.glob("./*.VEL")
# velocities = pd.DataFrame()
# cnt = 0
# for f in vel:
#     station = f.split('.')[2]
#     df = pd.read_csv(f,skiprows=50,header=None,names=[station])
#     velocities = pd.concat([velocities, df], axis=1)
#     cnt=cnt+1

# velocities = velocities.reindex(sorted(velocities.columns), axis=1)
# velocities.plot(subplots=True, layout=(cnt,1),title='vel')

acc = glob.glob("./*.DAT")
accelerations = pd.DataFrame()
cnt = 0
for f in acc:
    station = f.split('.')[2]
    df = pd.read_csv(f,skiprows=50,header=None,names=[station],nrows=10e3)
    accelerations = pd.concat([accelerations, df], axis=1)
    cnt=cnt+1

accelerations = accelerations.reindex(sorted(accelerations.columns), axis=1)
accelerations.plot(subplots=True, layout=(cnt,1),title='acc')



station_latitude = {}
station_longitude = {}
station_elevation = {}
for f in acc:
    station = f.split('.')[2]
    with open(f) as myfile:
        for line in myfile:
            name, var = line.partition(':')[::2]
            if name=='STATION_LATITUDE_DEGREE':
                station_latitude[station] = float(var)
            if name=='STATION_LONGITUDE_DEGREE':
                station_longitude[station] = float(var)
            if name=='STATION_ELEVATION':      
                station_elevation[station] = float(var)                

print(station_latitude)
print(station_longitude)
print(station_elevation)

SAMPLING_INTERVAL_S = .01

#plt.show()

times_of_arrival = {
    'ACATE':3212,
    'CEL':2902,
    'EMCN':2808,
    'ENIC':2795,
    'EVRN':2829,
    'HVZN':3044,
    'JOPP':2768,
    'SCIAR':1679,
    'T1573':2452
}

# https://gist.github.com/graydon/11198540
lat_min = 35.2889616
lat_max = 47.0921462
lon_min = 6.6272658	
lon_max = 18.7844746

print(utm.from_latlon(lat_min,lon_min))
print(utm.from_latlon(lat_min,lon_max))
print(utm.from_latlon(lat_max,lon_min))
print(utm.from_latlon(lat_max,lon_max))

my_model="""
data{
    vector[9] t;
    real v[9];
    real y[9];
    real x[9];
    real t0[9];
}
parameters{
    real<lower=-10e6,upper=10e6> x0;
    real<lower=-10e6,upper=10e6> y0;
}
model{
    vector[9] mu;
    y0 ~ uniform( -10e6 , 10e6 );
    x0 ~ uniform( -10e6 , 10e6 );
    for ( i in 1:9 ) {
        mu[i] = t0[i] + sqrt((x[i] - x0)^2 + (y[i] - y0)^2)/v[i];
    }
    t ~ normal( mu , .01 );
}"""

my_model="""
data{
    vector[9] t;
    real y[9];
    real x[9];
    real t0[9];
}
parameters{
    real<lower=-10e6,upper=10e6> x0;
    real<lower=-10e6,upper=10e6> y0;
    real<lower=500,upper=10000> v;
}
model{
    vector[9] mu;
    y0 ~ uniform( -10e6 , 10e6 );
    x0 ~ uniform( -10e6 , 10e6 );
    v ~ uniform(500,10000);
    for ( i in 1:9 ) {
        mu[i] = t0[i] + sqrt((x[i] - x0)^2 + (y[i] - y0)^2)/v;
    }
    t ~ normal( mu , .01 );
}"""


    

easting=[]
northing=[]
zone_number=[]
zone_letter=[]
for key in sorted(times_of_arrival):
    u = utm.from_latlon(station_latitude[key], station_longitude[key])
    print(key,u)
    easting.append(u[0])
    northing.append(u[1])
    zone_number.append(u[2])
    zone_letter.append(u[3])


print(easting)
print(northing)

times=[]
for key in sorted(times_of_arrival):
    times.append(SAMPLING_INTERVAL_S*times_of_arrival[key])

my_data={
     't':times,
     'x':easting,
     'y':northing,
     't0':[0,0,0,0,0,0,0,0,0],
     'v':[5000,5000,5000,5000,5000,5000,5000,5000,5000]
}    

sm = pystan.StanModel(model_code=my_model)
fit = sm.sampling(data=my_data, iter=1000000, chains=4)
print(fit)
fit.plot()
#arviz.plot_trace(fit)

means = np.mean(fit.get_posterior_mean(),1)

epicentre_x = means[0]
epicentre_y = means[1]

utm_ale = utm.to_latlon(epicentre_x,epicentre_y,zone_number[0],zone_letter[1])
print('Ale: ',utm_ale)
# (39.03898131649315, 13.819875262386265) cattivo?
# (39.03878690943342, 13.820042144461398) buono!





# Create a Stamen terrain background instance.
stamen_terrain = cimgt.Stamen('terrain-background')

fig = plt.figure()

# Create a GeoAxes in the tile's projection.
ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)

# Limit the extent of the map to a small longitude/latitude range.
ax.set_extent([11, 18, 36, 41], crs=ccrs.Geodetic())

# Add the Stamen data at zoom level 8.
ax.add_image(stamen_terrain, 8)

def add_point(ax,lon,lat,name,marker):
    # Add a marker for the Eyjafjallajökull volcano.
    ax.plot(lon,lat,  marker=marker, color='red', #markersize=12,
            alpha=0.7, transform=ccrs.Geodetic())

    # Use the cartopy interface to create a matplotlib transform object
    # for the Geodetic coordinate system. We will use this along with
    # matplotlib's offset_copy function to define a coordinate system which
    # translates the text by 25 pixels to the left.
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=-10)

    # Add text 25 pixels to the left of the volcano.
    ax.text(lon,lat, name,
            verticalalignment='center', horizontalalignment='right',
            transform=text_transform,
            bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))

for key in sorted(times_of_arrival):
    add_point(ax,station_longitude[key],station_latitude[key],key,'o')

EVENT_LATITUDE_DEGREE = 38.6957
EVENT_LONGITUDE_DEGREE = 13.8490

add_point(ax,EVENT_LONGITUDE_DEGREE,EVENT_LATITUDE_DEGREE,'INGV','*')
add_point(ax,utm_ale[1],utm_ale[0],'ALE','*')

plt.show()





