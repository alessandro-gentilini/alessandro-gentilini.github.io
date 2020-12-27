import geopandas as gpd
import elevation
import matplotlib.pyplot as plt
import os
from rasterio.transform import from_bounds, from_origin
from rasterio.warp import reproject, Resampling
import rasterio
from rasterio.plot import show
import numpy as np
import rasterio.mask

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
peak_idx = np.unravel_index(dem_raster.read(1).argmax(),dem_raster.read(1).shape)
peak = dem_raster.xy(peak_idx[0],peak_idx[1])
ax.plot(peak[0],peak[1],'*')
fig.savefig('DEM_bounding_box_imola.png',bbox_inches='tight')

out_image, out_transform = rasterio.mask.mask(dem_raster,imola.geometry,crop=True)
out_meta = dem_raster.meta
out_image[out_image==-32768]=0
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("DEM_masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)

dem_masked = rasterio.open("DEM_masked.tif")
fig, ax = plt.subplots()
show(source=dem_masked.read(1),ax=ax,cmap='pink',transform=dem_masked.transform)
peak_idx = np.unravel_index(dem_masked.read(1).argmax(),dem_masked.read(1).shape)
peak = dem_masked.xy(peak_idx[0],peak_idx[1])
ax.plot(peak[0],peak[1],'*')
fig.savefig('DEM_imola.png',bbox_inches='tight')