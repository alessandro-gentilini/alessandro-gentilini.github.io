# coding=utf-8

# trick per evitare errore
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 3: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
import math
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import geopandas as gpd
from pathlib import Path
import pickle
import unicodedata
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import json

def shorten(address,provincia,regione):
    parts = address.split(',')
    result = []
    for p in parts:
        if p.lstrip() not in (provincia,regione,'Italia'):
            result.append(p)
    return ','.join(result)



def normalize(s):
    t = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')
    t = t.replace(' ','_')
    t = t.replace("'",'')
    return t

def query_nga(lat,lon):
    distance,index = nbrs.kneighbors([[math.pi*lat/180,math.pi*lon/180]])
    # print(distance[0][0],nga.iloc[index[0][0]].FULL_NAME_RO,nga.iloc[index[0][0]].LAT,nga.iloc[index[0][0]].LONG)
    return nga.iloc[index[0][0]].FULL_NAME_RO

def query_nominatim_cache(query):
    if query not in nominatim_cache:
        return query
    if hasattr(nominatim_cache[query],'address'):
        return nominatim_cache[query].address
    else:
        return nominatim_cache[query]

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

def analyze(comune):
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
    obj['regione_full'] = prov[prov.COD_PROV_Storico==c.COD_PROV.values[0]].DEN_REG.values[0]
    obj['regione']= obj['regione_full'][0:3].upper()
    obj['PRO_COM_T'] = c.PRO_COM_T.values[0]

    print(obj['PRO_COM_T'])

    obj['comune_lat'] = None
    obj['comune_lon'] = None

    for x in comune_lat_lon:
        if int(x[u'istat']) == int(obj['PRO_COM_T']):
            lat = float(x[u'lat'])
            lon = float(x[u'lng'])
            obj['comune_lat'] = lat
            obj['comune_lon'] = lon
            break    

    basename = obj['regione']+'-'+obj['plate']+'-'+obj['norm_name']
    dem_path = '/tif/'+basename+'-DEM.tif'

    dem_raster = rasterio.open('.'+dem_path)
    
    nda = dem_raster.read(1)

    peak_idx = np.unravel_index(nda.argmax(),nda.shape)
    peak_lon_lat = dem_raster.xy(peak_idx[0],peak_idx[1])
    peak_lon = peak_lon_lat[0]
    peak_lat = peak_lon_lat[1]

    nga_nearest = query_nga(peak_lat,peak_lon)
    
    query_decimals = 6
    query = str(round(peak_lat,query_decimals))+' '+str(round(peak_lon,query_decimals))
    nominatim_nearest = shorten(query_nominatim_cache(query),obj['provincia'],obj['regione_full'])

    title = comune + ', ' + obj['provincia'] + ', ' + obj['regione_full']
    title = title + '\n'
    title = title + 'NGA: ' + nga_nearest
    title = title + '\n'
    title = title + 'Nominatim: ' + nominatim_nearest
    my_plot(comune,dem_raster,nda,title,obj['comune_lon'],obj['comune_lat'],peak_lon,peak_lat)




def my_plot(comune,dem_raster,nda,title,comune_lon,comune_lat,peak_lon,peak_lat):
    H = nda.shape[0]
    W = nda.shape[1]
    dpi = 60.

    my_cmap = cut_terrain_map

    max_elev = nda.max()

    norm = FixPointNormalize(sealevel=0, 
    vmin=nda.min(),
    vmax=max_elev if max_elev > 100 else 100
    )

    #fig, ax = plt.subplots()
    #show(source=nda,ax=ax,cmap=my_cmap,transform=dem_raster.transform)


    # https://stackoverflow.com/a/63043659
    #fig, ax = plt.subplots(figsize=(W/dpi,H/dpi))
    fig, ax = plt.subplots(figsize=(18,10))
    # use imshow so that we have something to map the colorbar to
    image_hidden = ax.imshow(nda, 
                            norm = norm,
                            cmap=my_cmap)


    tl = dem_raster.xy(0,0)
    tr = dem_raster.xy(0,nda.shape[1])
    bl = dem_raster.xy(nda.shape[0],0)
    br = dem_raster.xy(nda.shape[0],nda.shape[1])


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


    ax.plot([bl1[0],br1[0]],[bl1[1],br1[1]], 'k-', linewidth=3)
    ax.plot([bl1[0],br1[0]],[bl1[1],br1[1]], 'w-', linewidth=1)

    txt = ax.text((bl1[0]+br1[0])/2,bl1[1]*1.00005,scale_label,
            color='w',
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=15
            )        
    txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
    # todo scegliere automaticamente il posto migliore per evitare che si sovrapponga ai punti notevoli

    ax.plot(peak_lon,peak_lat,'^')
    if comune_lat != None and comune_lon != None:
        ax.plot(comune_lon,comune_lat,'s',color='red')
    ax.axhline(peak_lat,color='w',linewidth=.5)
    ax.axvline(peak_lon,color='w',linewidth=.5)
    
    # plot on the same axis with rio.plot.show
    image = show(nda,
                transform=dem_raster.transform, 
                ax=ax, 
                norm = norm,
                cmap=my_cmap)


    # add colorbar using the now hidden image
    axins = inset_axes(ax,
                   width="5%",  # width = 5% of parent_bbox width
                   height="75%",  # height : 50%
                   loc='lower left',
                   bbox_to_anchor=(1.05, 0., 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0,
                   )    
    clb = fig.colorbar(image_hidden, ax=ax, cax=axins)
    clb.ax.set_title('meters\n(SRTM-1)')        

    ax.set_xlabel('Longitude - EAST')
    ax.set_ylabel('Latitude - NORTH')
    ax.set_title(title)
    fig.savefig(comune+'.png',bbox_inches='tight')

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





# todo https://doi.org/10.5066/F7PR7TFT
# todo https://www.istat.it/storage/cartografia/confini_amministrativi/non_generalizzati/Limiti01012020.zip https://www.istat.it/it/archivio/222527
# todo https://www.istat.it/it/archivio/156224#AltitudinideicomunitramiteDEM-1
# todo https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel/blob/master/italy_geo.json ma anche descritto nel pdf https://www.istat.it/it/files//2018/10/Descrizione-dei-dati-geografici-2020-03-19.pdf


print('Load cache...')
cache_path = 'cache2.p'
nominatim_cache = dict()
if Path(cache_path).exists():
    nominatim_cache = pickle.load(open(cache_path, 'rb'))

print('Load NGA data...')
nga = pd.read_csv('it.txt',sep='\t',encoding='utf-8',dtype={'ADM1':str,'TRANSL_CD':str,'F_TERM_DT':str})
X = math.pi*nga[['LAT','LONG']]/180
nbrs = NearestNeighbors(n_neighbors=1, metric='haversine').fit(X)

print('Load shp...')
com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/',encoding='utf-8')

print('Load province...')
prov = pd.read_csv('codici_statistici_e_denominazioni_delle_ripartizioni_sovracomunali.txt',sep=';',skiprows=3,encoding='utf-8',keep_default_na=False,na_values=['_'])

print('Load comune lat lon...')
with open('italy_geo.json') as f:
   comune_lat_lon = json.load(f)


# analyze(u'Roma')
# analyze(u'Lipari')
# analyze(u'Boretto')
# analyze(u'Isole Tremiti')
# analyze(u'Courmayeur')
# analyze(u'Valtournenche')
# analyze(u'Atrani')
# analyze(u'Bologna')
# analyze(u'Imola')
# analyze(u'Mordano')
# analyze(u'Brisighella')
# analyze(u'Stelvio')
# analyze(u'Barbariga')
# analyze(u'Castel del Rio')
analyze(u'Malé')
#analyze(u'Malè')
analyze(u"Sant'Angelo in Vado")


#plt.show()