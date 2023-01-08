
# https://geopandas.org/en/stable/gallery/geopandas_rasterio_sample.html
import geopandas
import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import Point

gdf=geopandas.read_file('Limiti01012022/Com01012022/Com01012022_WGS84.shp')
gdf = gdf.loc[gdf['COMUNE']=="Courmayeur"]
src = rasterio.open('Pleiades_Mont-Blanc_2017-10-25_DEM_5m.tif')

from rasterio.plot import show

fig, ax = plt.subplots()

# transform rasterio plot to real world coords
extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
ax = rasterio.plot.show(src, extent=extent, ax=ax)#, cmap='terrain')
gdf.plot(ax=ax,facecolor="none", edgecolor="black")

# from pysheds.grid import Grid
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import colors
# import seaborn as sns

# grid = Grid.from_raster('Pleiades_Mont-Blanc_2017-10-25_DEM_5m.tif')
# dem = grid.read_raster('Pleiades_Mont-Blanc_2017-10-25_DEM_5m.tif')

# fig, ax = plt.subplots(figsize=(8,6))
# fig.patch.set_alpha(0)

# plt.imshow(dem, extent=grid.extent, cmap='terrain', zorder=1)
# plt.colorbar(label='Elevation (m)')
# plt.grid(zorder=0)
# plt.title('Digital elevation map', size=14)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.tight_layout()

# # Condition DEM
# # ----------------------
# # Fill pits in DEM
# pit_filled_dem = grid.fill_pits(dem)

# # Fill depressions in DEM
# flooded_dem = grid.fill_depressions(pit_filled_dem)
    
# # Resolve flats in DEM
# inflated_dem = grid.resolve_flats(flooded_dem)

# fig, ax = plt.subplots(figsize=(8,6))
# fig.patch.set_alpha(0)

# plt.imshow(inflated_dem, extent=grid.extent, cmap='terrain', zorder=1)
# plt.colorbar(label='Elevation (m)')
# plt.grid(zorder=0)
# plt.title('Digital elevation map', size=14)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.tight_layout()