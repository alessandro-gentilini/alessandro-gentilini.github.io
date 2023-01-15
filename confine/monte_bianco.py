# https://geopandas.org/en/stable/gallery/geopandas_rasterio_sample.html
import geopandas
import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
from rasterio.plot import show
import rasterio.mask

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
ax = rasterio.plot.show(dem, extent=extent, ax=ax)#, cmap='terrain')

ax.axhline(y=monte_bianco[1], color='gray', linestyle='-')
ax.axvline(x=monte_bianco[0], color='gray', linestyle='-')

xlim = ([monte_bianco[0]-crop_side/2, monte_bianco[0]+crop_side/2])
ylim = ([monte_bianco[1]-crop_side/2, monte_bianco[1]+crop_side/2])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

boundary.plot(ax=ax,facecolor="none", edgecolor=["red","black","blue"])

#boundary_fr.plot(ax=ax,facecolor="none", edgecolor="black")
#boundary_it.plot(ax=ax,facecolor="none", edgecolor="black")