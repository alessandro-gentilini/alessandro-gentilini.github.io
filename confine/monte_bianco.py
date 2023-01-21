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
import math
import matplotlib.font_manager

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
fig2, ax2 = plt.subplots()

# transform rasterio plot to real world coords
extent=[dem.bounds[0], dem.bounds[2], dem.bounds[1], dem.bounds[3]]
ax = rasterio.plot.show(dem, extent=extent, ax=ax, cmap='plasma')
ax2 = rasterio.plot.show(dem, extent=extent, ax=ax2, cmap='plasma')

#ax.axhline(y=monte_bianco[1], color='gray', linestyle='-',linewidth=.1)
#ax.axvline(x=monte_bianco[0], color='gray', linestyle='-',linewidth=.1)

xlim = ([monte_bianco[0]-crop_side/2, monte_bianco[0]+crop_side/2])
ylim = ([monte_bianco[1]-crop_side/2, monte_bianco[1]+crop_side/2])

# https://gis.stackexchange.com/a/442136
ax.set_xlim(xlim)
ax.set_ylim(ylim)

ax2.set_xlim(xlim)
ax2.set_ylim(ylim)

raw_dem=dem.read()[0]
if np.any(raw_dem == -9999):
    raw_dem[raw_dem == -9999] = np.nan

qcs = plt.contour(raw_dem,levels = list(range(4000, 5000, 25)))    

meter_per_px_x = abs(dem.transform[0])
meter_per_px_y = abs(dem.transform[4])

# https://codereview.stackexchange.com/a/28210
def shortest_distance(node, nodes):
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return {'sqdist':np.min(dist_2),'p':nodes[np.argmin(dist_2)]}

main_contour = False
for idx,collection in enumerate(qcs.collections):
    if int(qcs.levels[idx]) % 100 == 0:
        main_contour=True
    else:
        main_contour=False

    for path in collection.get_paths():
        for polygon in path.to_polygons(): 
            polygon[:,0]=meter_per_px_x*(polygon[:,0]-raw_dem.shape[0]/2)
            polygon[:,1]=meter_per_px_y*(polygon[:,1]-raw_dem.shape[1]/2)
            polygon[:,0]=polygon[:,0]+monte_bianco[0]
            polygon[:,1]=polygon[:,1]+monte_bianco[1]

            if main_contour and polygon.shape[0]>100:
                t = ax2.text(monte_bianco[0],monte_bianco[1],str(qcs.levels[idx]),{'ha': 'center', 'va': 'center'},rotation=0)
                renderer = fig.canvas.get_renderer()
                bbox = plt.gca().transData.inverted().transform_bbox(t.get_window_extent(renderer))      
                min_distance = np.inf
                min_p = polygon[0]
                min_angle = 0
                min_R = polygon[0]
                min_L = polygon[0]
                for i,p in enumerate(polygon):
                    L=np.array([p[0]-bbox.width/2,p[1]])
                    R=np.array([p[0]+bbox.width/2,p[1]])
                    for d in range(0,360):
                        L_0 = L-p
                        R_0 = R-p
                        theta = math.radians(d)
                        M = np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
                        L_rot = np.dot(M,L_0)+p
                        R_rot = np.dot(M,R_0)+p
                        pp = np.vstack([polygon[0:i],polygon[i+1:]])
                        d_L = shortest_distance(L_rot,pp)
                        d_R = shortest_distance(R_rot,pp)
                        if d_L['sqdist']+d_R['sqdist']<min_distance:
                            min_distance = d_L['sqdist']+d_R['sqdist']
                            min_p = p
                            min_angle = d
                            min_R = d_R['p']
                            min_L = d_L['p']
                    #ax.plot(p[0],p[1],'.',color='black')

                #ax.plot(min_R[0],min_R[1],'o',color='red')
                #ax.plot(min_L[0],min_L[1],'x',color='blue')
                #ax.plot(min_p[0],min_p[1],'+',color='green')

                # mi piacerebbe usare il font ITC Zapf Chancery ma al momento non va perché ha estensione .afm che dà errore
                # questo è un minimum working sample che dà errore:
                # import matplotlib.font_manager as fm
                # font_path ="/usr/share/fonts/type1/gsfonts/z003034l.afm"
                # font_name = fm.FontProperties(fname=font_path).get_name()
                # RuntimeError: In FT2Font: Can not load face.  Unknown file format.

                ax.text(min_p[0],min_p[1],str(qcs.levels[idx]),{'ha': 'center', 'va': 'center','family':'serif'},rotation=min_angle)         
                
            if main_contour:                 
                ax.add_patch(Polygon(polygon,fill=None,closed=False,linewidth=.3))
            else:
                ax.add_patch(Polygon(polygon,fill=None,closed=False,linewidth=.1))

boundary.plot(ax=ax,facecolor="none", edgecolor=["blue","red","red"],linestyle='-.')

#boundary_fr.plot(ax=ax,facecolor="none", edgecolor="black")
#boundary_it.plot(ax=ax,facecolor="none", edgecolor="black")