import geopandas as gpd
import elevation
import matplotlib.pyplot as plt
import os
import rasterio
from rasterio.plot import show
import numpy as np
import rasterio.mask
from geopy.geocoders import Nominatim

def lon_lat(p):
    return 'lon: '+ str(p[0]) + ' lat: '+ str(p[1])

def normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')

def quota_max(comune):
    normalized_comune = comune.replace(' ','_')
    dem_path = '/'+normalized_comune+'_DEM.tif'
    output = os.getcwd() + dem_path

    c = com.loc[com['COMUNE']==comune]

    bounds = c.to_crs('WGS84').geometry.bounds
    west = float(bounds.minx)
    east = float(bounds.maxx)
    north = float(bounds.maxy)
    south = float(bounds.miny)

    elevation.clip(bounds=(west,south,east,north), output=output, product='SRTM1') #SRTM3 does not work
    dem_raster = rasterio.open('.' + dem_path)

    print('DEM crs is '+str(dem_raster.crs))
    print('DEM has '+str(dem_raster.count)+'  band(s)')

    c = c.to_crs(dem_raster.crs)

    fig, ax = plt.subplots()
    c.plot(ax=ax)
    fig.savefig(normalized_comune+'_limits.png',bbox_inches='tight')

    fig, ax = plt.subplots()
    show(source=dem_raster.read(1),ax=ax,cmap='pink',transform=dem_raster.transform)
    peak_idx = np.unravel_index(dem_raster.read(1).argmax(),dem_raster.read(1).shape)
    peak_bb = dem_raster.xy(peak_idx[0],peak_idx[1])
    ax.plot(peak_bb[0],peak_bb[1],'*')
    location = geolocator.reverse(str(peak_bb[1])+' '+str(peak_bb[0]))
    title = 'Bounding box: '+lon_lat(peak_bb)+' elevation: '+str(dem_raster.read(1).max())+'\naddress: '+location.address
    ax.set_title(title)
    fig.savefig(normalized_comune+'_DEM_bb.png',bbox_inches='tight')
    print(title)

    out_image, out_transform = rasterio.mask.mask(dem_raster,c.geometry,crop=True)
    out_meta = dem_raster.meta
    out_image[out_image==-32768]=0
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    masked_tif = normalized_comune+'_DEM_masked.tif'
    with rasterio.open(masked_tif, 'w', **out_meta) as dest:
        dest.write(out_image)

    dem_masked = rasterio.open(masked_tif)
    fig, ax = plt.subplots()
    show(source=dem_masked.read(1),ax=ax,cmap='pink',transform=dem_masked.transform)
    peak_idx = np.unravel_index(dem_masked.read(1).argmax(),dem_masked.read(1).shape)
    peak = dem_masked.xy(peak_idx[0],peak_idx[1])
    ax.plot(peak[0],peak[1],'*')
    location = geolocator.reverse(str(peak[1])+' '+str(peak[0]))
    title = 'Masked: '+lon_lat(peak)+ ' elevation: '+str(dem_masked.read(1).max())+'\naddress: '+location.address
    ax.set_title(title)
    fig.savefig(normalized_comune+'_DEM.png',bbox_inches='tight')
    print(title)

geolocator = Nominatim(user_agent="Alessandro")    
com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/',encoding='utf-8')

quota_max('Imola')
quota_max('Castel del Rio')
