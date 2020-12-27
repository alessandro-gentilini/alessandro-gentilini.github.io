import geopandas as gpd
import elevation
import matplotlib.pyplot as plt
import os
from rasterio.transform import from_bounds, from_origin
from rasterio.warp import reproject, Resampling
import rasterio
from rasterio.plot import show
import numpy as np

dem_path = '/Imola_DEM.tif'
output = os.getcwd() + dem_path

print(output)

com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/')
imola = com.loc[com['COMUNE']=='Imola']

bounds = imola.to_crs('WGS84').geometry.bounds
west = float(bounds.minx)
east = float(bounds.maxx)
north = float(bounds.maxy)
south = float(bounds.miny)

elevation.clip(bounds=(west,south,east,north), output=output, product='SRTM1') #SRTM3 does not work
dem_raster = rasterio.open('.' + dem_path)

print('DEM crs is '+str(dem_raster.crs))
print('DEM has '+str(dem_raster.count)+'  band(s)')

imola = imola.to_crs(dem_raster.crs)
print(imola)

fig, ax = plt.subplots()
imola.plot(ax=ax)
fig.savefig('confini_imola.png',bbox_inches='tight')

fig, ax = plt.subplots()
show(source=dem_raster.read(1),ax=ax,cmap='pink',transform=dem_raster.transform)
peak = np.unravel_index(dem_raster.read(1).argmax(),dem_raster.read(1).shape)
peak = dem_raster.xy(peak[0],peak[1])
ax.plot(peak[0],peak[1],'*')
fig.savefig('DEM_imola.png',bbox_inches='tight')





#src_shape = src_height, src_width = dem_raster.shape
#src_transform = from_bounds(west, south, east, north, src_width, src_height)
#source = dem_raster.read(1)

