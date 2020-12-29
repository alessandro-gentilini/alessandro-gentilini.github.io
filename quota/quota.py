# coding=utf-8

# https://www.istat.it/it/files//2018/10/Descrizione-dei-dati-geografici-2020-03-19.pdf

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
import traceback
import logging
import json
import pickle
import time
from pathlib import Path

def query_geocoder_server(query):
    time.sleep(1) # https://operations.osmfoundation.org/policies/nominatim/
    return geolocator.reverse(query).address

def get_address(query):
    if query not in cache:
        cache[query] = query_geocoder_server(query)
    return cache[query]

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

    c = com.loc[com['COMUNE']==comune]
    if len(c)<1:
        logging.error(u'Comune not found: '+comune)
        return obj

    if len(c)>1:
        logging.error(u'Duplicated comune: '+comune)
        return obj

    obj['plate']=prov[prov.COD_PROV_Storico==c.COD_PROV.values[0]].Sigla_automobilistica.values[0]
    obj['COMUNE']=c.COMUNE.values[0]
    obj['COD_PROV']=c.COD_PROV.values[0]
    obj['provincia']=prov[prov.COD_PROV_Storico==c.COD_PROV.values[0]].DEN_UTS.values[0]
    obj['regione']=prov[prov.COD_PROV_Storico==c.COD_PROV.values[0]].DEN_REG.values[0][0:3].upper()

    basename = obj['regione']+'-'+obj['plate']+'-'+obj['norm_name']
    dem_path = '/'+basename+'-DEM.tif'
    output = os.getcwd() + dem_path        

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
    fig.savefig(basename+'-limits.png',bbox_inches='tight')

    fig, ax = plt.subplots()
    show(source=dem_raster.read(1),ax=ax,cmap='pink',transform=dem_raster.transform)
    peak_idx = np.unravel_index(dem_raster.read(1).argmax(),dem_raster.read(1).shape)
    peak_bb = dem_raster.xy(peak_idx[0],peak_idx[1])
    ax.plot(peak_bb[0],peak_bb[1],'*')
    query = str(round(peak_bb[1],6))+' '+str(round(peak_bb[0],6))
    print(query)
    address = get_address(query)
    obj['lon_bb']=peak_bb[0]
    obj['lat_bb']=peak_bb[1]
    obj['elev_bb']=np.float64(dem_raster.read(1).max()) # https://ellisvalentiner.com/post/serializing-numpyfloat32-json/
    obj['addr_bb']=address
    title = comune+' ('+obj['provincia']+')'+'\nBounding box: '+lon_lat(peak_bb)+' elevation: '+str(obj['elev_bb'])+'\naddress: '+obj['addr_bb']
    ax.set_title(title)
    fig.savefig(basename+'-DEM-bb.png',bbox_inches='tight')

    out_image, out_transform = rasterio.mask.mask(dem_raster,c.geometry,crop=True)
    out_meta = dem_raster.meta
    out_image[out_image==-32768]=0
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    masked_tif = basename+'-DEM-masked.tif'
    with rasterio.open(masked_tif, 'w', **out_meta) as dest:
        dest.write(out_image)

    dem_masked = rasterio.open(masked_tif)
    fig, ax = plt.subplots()
    show(source=dem_masked.read(1),ax=ax,cmap='pink',transform=dem_masked.transform)
    peak_idx = np.unravel_index(dem_masked.read(1).argmax(),dem_masked.read(1).shape)
    peak = dem_masked.xy(peak_idx[0],peak_idx[1])
    ax.plot(peak[0],peak[1],'*')
    query = str(round(peak[1],6))+' '+str(round(peak[0],6))
    print(query)
    address = get_address(query)
    obj['lon']=peak[0]
    obj['lat']=peak[1]
    obj['elev']=np.float64(dem_masked.read(1).max()) # https://ellisvalentiner.com/post/serializing-numpyfloat32-json/
    obj['addr']=address     
    title = comune+' ('+obj['provincia']+')'+'\nMasked: '+lon_lat(peak)+ ' elevation: '+str(obj['elev'])+'\naddress: '+obj['addr']
    ax.set_title(title)
    fig.savefig(basename+'-DEM.png',bbox_inches='tight')

    plt.close('all')
    return obj


print('Load cache...')
cache_path = 'cache.p'
cache = dict()
if Path(cache_path).exists():
    cache = pickle.load(open(cache_path, 'rb'))

print('Create geolocator...')
geolocator = Nominatim(user_agent="Alessandro")    
print('Load shp...')
com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/',encoding='utf-8')
print('Load province...')
prov = pd.read_csv('codici_statistici_e_denominazioni_delle_ripartizioni_sovracomunali.txt',sep=';',skiprows=3,encoding='utf-8',keep_default_na=False,na_values=['_'])


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
    o = {}
    try:
        o = quota_max(c)
    except Exception as e:
        logging.error(traceback.format_exc())
    objs.append(o)

i = 0
i_begin = int(sys.argv[1])
i_end = int(sys.argv[2])
sz = i_end-i_begin
objs = []
for j in range(i_begin,i_end):
    c = com.iloc[j].COMUNE
    print('\n\nProcessing '+c+' '+str(i)+' '+str((100.*i)/sz))
    o = {}
    try:
        o = quota_max(c)
    except Exception as e:
        logging.error(c)
        logging.error(traceback.format_exc())
    objs.append(o)
    json_str = json.dumps(o,indent=2)
    with open('result_{:04d}.json'.format(j), 'w') as text_file:
        text_file.write(json_str)    
    i=i+1

json_str = json.dumps(objs,indent=2)
with open('result_{:04d}-{:04d}.json'.format(i_begin,i_end), 'w') as text_file:
    text_file.write(json_str)

pickle.dump( objs, open( 'result_{:04d}-{:04d}.p'.format(i_begin,i_end), 'wb' ) )    
pickle.dump(cache, open(cache_path, 'wb'))

# legenda quote
# km
# fonti
# geojson
# disegnare su DEM il confine del comune
# toponimi IGM (scaricarli regione per regione)