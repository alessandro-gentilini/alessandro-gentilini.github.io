import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from geopy import distance
import geopy
from palettable.scientific.sequential import Oleron_20
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def my_distance(lat1,lon1,lat2,lon2):
    return distance.distance((lat1,lon1),(lat2,lon2)).meters

def nearest_scale(m):
    if m < 50:
        return 50,'50m'
    elif m < 100:
        return 100,'100m'
    elif m < 500:
        return 500,'500m'
    elif m < 1000:
        return 1000,'1km'
    elif m < 5000:
        return 5000,'5km'
    elif m < 10000:
        return 10000,'10km'
    else:
        return 50000,'50km'

# https://stackoverflow.com/a/40952872
class FixPointNormalize(matplotlib.colors.Normalize):
    """ 
    Inspired by https://stackoverflow.com/questions/20144529/shifted-colorbar-matplotlib
    Subclassing Normalize to obtain a colormap with a fixpoint 
    somewhere in the middle of the colormap.

    This may be useful for a `terrain` map, to set the "sea level" 
    to a color in the blue/turquise range. 
    """
    def __init__(self, vmin=None, vmax=None, sealevel=0, col_val = 0.21875, clip=False):
        # sealevel is the fix point of the colormap (in data units)
        self.sealevel = sealevel
        # col_val is the color value in the range [0,1] that should represent the sealevel.
        self.col_val = col_val
        matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
        return np.ma.masked_array(np.interp(value, x, y))        

# Combine the lower and upper range of the terrain colormap with a gap in the middle
# to let the coastline appear more prominently.
# inspired by https://stackoverflow.com/questions/31051488/combining-two-matplotlib-colormaps
colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 56))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 200))
# combine them and build a new colormap
colors = np.vstack((colors_undersea, colors_land))
cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)        

piratello = (44.3704275, 11.6713168)
monumento = (44.3605792, 11.6950927)

piratello2= (11.6713168,44.3704275)
monumento2= (11.6950927,44.3605792)

one_km = distance.distance(kilometers=2.188484)
piratello_hat = one_km.destination(point=monumento, bearing=292)
#print('piratello',piratello)
#print('stima',piratello_hat)
#print(my_distance(piratello[0],piratello[1],piratello_hat[0],piratello_hat[1]))
#print(distance.distance(piratello,piratello_hat))




#dem_raster = rasterio.open('./tif/LAZ-RM-Roma-DEM.tif')
#dem_raster = rasterio.open('./tif/SIC-ME-Lipari-DEM.tif')
#dem_raster = rasterio.open('./tif/EMI-RE-Boretto-DEM.tif')
dem_raster = rasterio.open('./tif/PUG-FG-Isole_Tremiti-DEM.tif')
#dem_raster = rasterio.open('./tif/VAL-AO-Courmayeur-DEM.tif')
#dem_raster = rasterio.open('./tif/VAL-AO-Valtournenche-DEM.tif')
#dem_raster = rasterio.open('./tif/CAM-SA-Atrani-DEM.tif')
#dem_raster = rasterio.open('./tif/EMI-BO-Bologna-DEM.tif')
#dem_raster = rasterio.open('./tif/EMI-BO-Imola-DEM.tif')
#dem_raster = rasterio.open('./tif/EMI-BO-Mordano-DEM.tif')
#dem_raster = rasterio.open('./tif/EMI-RA-Brisighella-DEM.tif')
#dem_raster = rasterio.open('./tif/TRE-BZ-Stelvio-DEM.tif')
#print(dem_raster.crs)

nda = dem_raster.read(1)

my_cmap = Oleron_20.mpl_colormap
#my_cmap = 'gist_earth'
my_cmap = plt.cm.terrain
my_cmap = cut_terrain_map

norm = FixPointNormalize(sealevel=0, 
vmin=nda.min(),
vmax=nda.max())

fig, ax = plt.subplots()
show(source=nda,ax=ax,cmap=my_cmap,transform=dem_raster.transform)


# https://stackoverflow.com/a/63043659
fig, ax = plt.subplots()
# use imshow so that we have something to map the colorbar to
image_hidden = ax.imshow(nda, 
                         norm = norm,
                         cmap=my_cmap)

x_0=nda.shape[0]/10
x_1=x_0
y_0=nda.shape[1]/10
y_1=y_0+nda.shape[0]/5

p0 = dem_raster.xy(x_0,y_0)
#print(p0)
p1 = dem_raster.xy(x_1,y_1)
#print(p1)

tl = dem_raster.xy(0,0)
tr = dem_raster.xy(0,nda.shape[1])
bl = dem_raster.xy(nda.shape[0],0)
br = dem_raster.xy(nda.shape[0],nda.shape[1])

H = nda.shape[0]
W = nda.shape[1]
bl1 = dem_raster.xy(.97*H,0.03*W)
br1 = dem_raster.xy(.97*H,.97*W)
H_meter = my_distance(bl[1],bl[0],br[1],br[0])
scale_L = H_meter/10
print(H_meter)
scale_value,scale_label = nearest_scale(scale_L)


my_scale_distance = distance.distance(kilometers=scale_value/1000)
EAST = 90
tmp = my_scale_distance.destination(point=geopy.Point(latitude=bl1[1], longitude=bl1[0]), bearing=EAST)
br1 = (tmp[1],tmp[0])


print('bl',bl)
print('br',br)

dist = distance.distance(p0,p1).meters
#print('Distance: '+str(dist))


#ax.plot(peak_bb[0],peak_bb[1],'*')
#ax.plot([L[0],R[0]],[L[1],R[1]], 'k-')                                
#ax.plot([p0[0],p1[0]],[p0[1],p1[1]], 'k-', linewidth=5)
#ax.plot([p0[0],p1[0]],[p0[1],p1[1]], 'w-', linewidth=2)
#ax.plot(tl[0],tl[1],'r*')
#ax.plot(tr[0],tr[1],'g*')
#ax.plot(bl[0],bl[1],'w*')
#ax.plot(br[0],br[1],'b*')
#ax.plot(piratello[1],piratello[0],'o')
#ax.plot(monumento[1],monumento[0],'o')
#ax.plot([piratello[1],monumento[1]],[piratello[0],monumento[0]], 'w-', linewidth=2)
ax.plot([bl1[0],br1[0]],[bl1[1],br1[1]], 'k-', linewidth=3)
ax.plot([bl1[0],br1[0]],[bl1[1],br1[1]], 'w-', linewidth=1)
#d2 = my_distance(piratello[0],piratello[1],monumento[0],monumento[1])
#d3 = my_distance(monumento[0],monumento[1],piratello[0],piratello[1])

#txt = ax.text(piratello[1],piratello[0],str(d2)+'m',
        #color='w',
        #horizontalalignment='center',
        #verticalalignment='bottom',
        #fontsize=15
        #)
# txt = ax.text((p0[0]+p1[0])/2,p1[1]*1.00005,str(int(round(dist)))+'m',
#         color='w',
#         horizontalalignment='center',
#         verticalalignment='bottom',
#         fontsize=15
#         )
txt = ax.text((bl1[0]+br1[0])/2,bl1[1]*1.00005,scale_label,
        color='w',
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=15
        )        
txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])


# plot on the same axis with rio.plot.show
image = show(nda,
             transform=dem_raster.transform, 
             ax=ax, 
             norm = norm,
             cmap=my_cmap)

               

# add colorbar using the now hidden image
clb = fig.colorbar(image_hidden, ax=ax)
clb.ax.set_title('meters\n(SRTM-1)')


# https://doi.org/10.5066/F7PR7TFT


plt.show()