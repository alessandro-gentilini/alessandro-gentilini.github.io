import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt
import contextily as ctx
from geopy.geocoders import Nominatim
import time


gdf = gpd.read_file('hybas_eu_lev00_v1c.shp')

#Monte_Bianco = Point(6.867222,45.833333)
Dobbiaco = Point(12.216667,46.733333)
#Dobbiaco = Point(287350,5179294)


d = gdf.distance(Dobbiaco)


gdf = gdf.to_crs(epsg=3857)


fig, ax = plt.subplots()
ax = gdf[d<.15].plot(figsize=(10, 10), alpha=0.25, edgecolor='k')
ctx.add_basemap(ax)

plt.show()


ax = gdf[d<.15].plot("MAIN_BAS",figsize=(10, 10), alpha=0.25, edgecolor='k',legend=True)
ctx.add_basemap(ax)

plt.show()

df = gdf[d<.15]

ax = df.plot("DIST_MAIN", alpha=0.25, edgecolor='k',legend=True)

# https://stackoverflow.com/questions/38899190/geopandas-label-polygons
df.apply(lambda x: ax.annotate(text=x.MAIN_BAS, xy=x.geometry.centroid.coords[0], ha='center'), axis=1);

ctx.add_basemap(ax)



mb = gdf[gdf.HYBAS_ID.isin(df.MAIN_BAS.unique())]
sinks = mb.centroid.to_crs(epsg=4326)

geolocator = Nominatim(user_agent="bel_paese.py")

info = ''
for i in range(0,len(sinks)):
    s = sinks.iloc[i]
    info += str(mb.iloc[i].HYBAS_ID) + ': ' +str(geolocator.reverse((s.y,s.x))) + '\n'
    time.sleep(3)

ax.set_title(info)
plt.show()

#ax = mb.plot(figsize=(10, 10), alpha=0.25, edgecolor='k')
#ctx.add_basemap(ax)
#plt.show()
