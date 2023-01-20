# https://geopandas.org/en/stable/gallery/geopandas_rasterio_sample.html
import geopandas
import rasterio
import matplotlib.pyplot as plt
from shapely import LineString
import pandas as pd
from rasterio.plot import show
import rasterio.mask
import numpy as np
from matplotlib.patches import Polygon

# https://geohack.toolforge.org/geohack.php?language=it&pagename=Monte_Bianco&params=45.832905_N_6.864688_E_type:mountain
monte_bianco = (334162,5077700)

crop_side = 1000

# https://github.com/rasterio/rasterio/issues/1343#issuecomment-389971813
geoms = [{'type': 'Polygon', 'coordinates': [
        [
            (monte_bianco[0]-crop_side/2,monte_bianco[1]-crop_side/2), 
            (monte_bianco[0]+crop_side/2,monte_bianco[1]-crop_side/2),
            (monte_bianco[0]+crop_side/2,monte_bianco[1]+crop_side/2),
            (monte_bianco[0]-crop_side/2,monte_bianco[1]+crop_side/2),
            (monte_bianco[0]-crop_side/2,monte_bianco[1]-crop_side/2)
        ]]}]

# https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
with rasterio.open("Pleiades_Mont-Blanc_2017-10-25_DEM_5m.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, geoms, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("pleiades.masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)


dem = rasterio.open('pleiades.masked.tif')


# https://www.istat.it/storage/cartografia/confini_amministrativi/non_generalizzati/Limiti01012022.zip
boundary_it=geopandas.read_file('Limiti01012022/Com01012022/Com01012022_WGS84.shp')
boundary_it = boundary_it.loc[boundary_it['COMUNE']=="Courmayeur"]
boundary_it = boundary_it.to_crs(epsg=dem.crs.to_epsg())

# https://wxs.ign.fr/x02uy2aiwjo9bm8ce5plwqmr/telechargement/prepackage/ADMINEXPRESS_SHP_TERRITOIRES_PACK_2022-12-20$ADMIN-EXPRESS_3-1__SHP_LAMB93_FXX_2022-12-20/file/ADMIN-EXPRESS_3-1__SHP_LAMB93_FXX_2022-12-20.7z
boundary_fr=geopandas.read_file('ADMIN-EXPRESS_3-1__SHP_LAMB93_FXX_2022-12-20/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2022-12-20/ADE_3-1_SHP_LAMB93_FXX/COMMUNE.shp')
boundary_fr = boundary_fr.loc[(boundary_fr['NOM']=='Saint-Gervais-les-Bains') | (boundary_fr['NOM']=='Chamonix-Mont-Blanc')]
boundary_fr = boundary_fr.to_crs(epsg=dem.crs.to_epsg())

boundary = pd.concat([boundary_it['geometry'],boundary_fr['geometry']])

fig, ax = plt.subplots()

# transform rasterio plot to real world coords
extent=[dem.bounds[0], dem.bounds[2], dem.bounds[1], dem.bounds[3]]
ax = rasterio.plot.show(dem, extent=extent, ax=ax, cmap='plasma')

#ax.axhline(y=monte_bianco[1], color='gray', linestyle='-',linewidth=.1)
#ax.axvline(x=monte_bianco[0], color='gray', linestyle='-',linewidth=.1)

xlim = ([monte_bianco[0]-crop_side/2, monte_bianco[0]+crop_side/2])
ylim = ([monte_bianco[1]-crop_side/2, monte_bianco[1]+crop_side/2])

# https://gis.stackexchange.com/a/442136
ax.set_xlim(xlim)
ax.set_ylim(ylim)

raw_dem=dem.read()[0]
if np.any(raw_dem == -9999):
    raw_dem[raw_dem == -9999] = np.nan

qcs = plt.contour(raw_dem,levels = list(range(4000, 5000, 25)))    

meter_per_px_x = abs(dem.transform[0])
meter_per_px_y = abs(dem.transform[4])

idx = 0
lw = .1
for collection in qcs.collections:
    if int(qcs.levels[idx]) % 100 == 0:
        lw=.3
    else:
        lw=.000000001
    for path in collection.get_paths():
        for polygon in path.to_polygons(): 
            polygon[:,0]=meter_per_px_x*(polygon[:,0]-raw_dem.shape[0]/2)
            polygon[:,1]=meter_per_px_y*(polygon[:,1]-raw_dem.shape[1]/2)
            polygon[:,0]=polygon[:,0]+monte_bianco[0]
            polygon[:,1]=polygon[:,1]+monte_bianco[1]
            ax.add_patch(Polygon(polygon,fill=None,closed=False,linewidth=lw))
    idx = idx+1

t = ax.text(monte_bianco[0],monte_bianco[1],'Monte Bianco',{'ha': 'center', 'va': 'center'},rotation=45)
renderer = fig.canvas.get_renderer()
bbox = plt.gca().transData.inverted().transform_bbox(t.get_window_extent(renderer))


boundary.plot(ax=ax,facecolor="none", edgecolor=["blue","red","red"],linestyle='-.')

#boundary_fr.plot(ax=ax,facecolor="none", edgecolor="black")
#boundary_it.plot(ax=ax,facecolor="none", edgecolor="black")