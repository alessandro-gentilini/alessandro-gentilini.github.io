https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/60s/60s_surface_elev_gtif/ETOPO_2022_v1_60s_N90W180_surface.tif

https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/docs/1.2%20ETOPO%202022%20User%20Guide.pdf

For most purposes,
EGM2008 is an adequate approximation of mean sea level.

import rasterio
import rasterio.plot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


data = rasterio.open('ETOPO_2022_v1_60s_N90W180_surface.tif')

rasterio.plot.show(data)

band1 = data.read(1).flatten()

# https://stackoverflow.com/a/51477080
plt.hist(band1,bins=100,weights=np.ones(len(band1))/len(band1))
plt.title('Histogram for Earth topography and bathymetry')
plt.xlabel('meters relative to the Earth Gravitational Model of 2008 (EGM2008) geoid surface')
plt.ylabel('percentage of Earth surface')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()

# https://stackoverflow.com/a/15419072
values, base = np.histogram(band1, bins=100)
cumulative = np.cumsum(values)
percentage = 100*cumulative/cumulative.max()
plt.plot(base[:-1], percentage)
plt.title('Cumulative Distribution Function for Earth topography and bathymetry')
plt.xlabel('meters relative to the Earth Gravitational Model of 2008 (EGM2008) geoid surface')
plt.ylabel('cumulative percentage of Earth surface')
plt.show()

plt.plot(np.flip(percentage),base[:-1])
plt.axhline(y=band1[band1>0].mean(), color='lightgray', linestyle='--')
plt.axhline(y=band1[band1<0].mean(), color='lightgray', linestyle='--')
plt.title("Figure 1.7 in \"Earth's dynamic systems\" by Hamblin and Christiansen\nFig, 1-1 in \"The Earth\" by Verhoogen et al.")
plt.ylabel('meters relative to EGM2008 geoid surface')
plt.xlabel('cumulative percentage of Earth surface')
plt.show()