# coding=utf-8

# https://github.com/pandas-dev/pandas/issues/25287#issuecomment-494428308
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import geopandas as gpd
import elevation
import matplotlib.pyplot as plt
import os
import rasterio
from rasterio.plot import show
import numpy as np
import rasterio.mask
from geopy.geocoders import Nominatim
import unicodedata
import pandas as pd

def lon_lat(p):
    return 'lon: '+ str(p[0]) + ' lat: '+ str(p[1])

def normalize(s):
    t = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')
    t = t.replace(' ','_')
    t = t.replace("'",'')
    return t

def quota_max(comune):
    obj = {}
        
    normalized_comune = normalize(comune)
    obj['norm_name']=normalized_comune

    dem_path = '/'+normalized_comune+'_DEM.tif'
    output = os.getcwd() + dem_path

    c = com.loc[com['COMUNE']==comune]
    obj['COMUNE']=c.COMUNE
    obj['COD_PROV']=c.COD_PROV
    obj['provincia']=prov[prov.COD_PROV_Storico==c.COD_PROV.values[0]].DEN_UTS.values[0]

    bounds = c.to_crs('WGS84').geometry.bounds
    west = float(bounds.minx)
    east = float(bounds.maxx)
    north = float(bounds.maxy)
    south = float(bounds.miny)

    elevation.clip(bounds=(west,south,east,north), output=output, product='SRTM1') #SRTM3 does not work
    dem_raster = rasterio.open('.' + dem_path)

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
    obj['lon_bb']=peak_bb[0]
    obj['lat_bb']=peak_bb[1]
    obj['elev_bb']=dem_raster.read(1).max()
    obj['addr_bb']=location.address
    title = comune+' ('+obj['provincia']+')'+'\nBounding box: '+lon_lat(peak_bb)+' elevation: '+str(obj['elev_bb'])+'\naddress: '+location.address
    ax.set_title(title)
    fig.savefig(normalized_comune+'_DEM_bb.png',bbox_inches='tight')

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
    obj['lon']=peak[0]
    obj['lat']=peak[1]
    obj['elev']=dem_masked.read(1).max()
    obj['addr']=location.address     
    title = comune+' ('+obj['provincia']+')'+'\nMasked: '+lon_lat(peak)+ ' elevation: '+str(obj['elev'])+'\naddress: '+location.address
    ax.set_title(title)
    fig.savefig(normalized_comune+'_DEM.png',bbox_inches='tight')

    plt.close('all')
    return obj

geolocator = Nominatim(user_agent="Alessandro")    
com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/',encoding='utf-8')
prov = pd.read_csv('codici_statistici_e_denominazioni_delle_ripartizioni_sovracomunali.txt',sep=';',skiprows=2,encoding='utf-8')


objs = []

o = quota_max(u'Imola')
objs.append(o)

o = quota_max(u'Castel del Rio')
objs.append(o)

o = quota_max(u'Malé')
objs.append(o)

o = quota_max(u"Sant'Angelo in Vado")
objs.append(o)

campione = com.sample(10,random_state=19760106)
for c in campione.COMUNE:
    print('\n\nProcessing '+c)
    o = quota_max(c)
    objs.append(o)

print(objs)    
