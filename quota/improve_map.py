import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from geopy import distance

dem_raster = rasterio.open('./EMI-BO-Imola-DEM.tif')
print(dem_raster.crs)

nda = dem_raster.read(1)

fig, ax = plt.subplots()
show(source=nda,ax=ax,cmap='pink',transform=dem_raster.transform)


# https://stackoverflow.com/a/63043659
fig, ax = plt.subplots()
# use imshow so that we have something to map the colorbar to
image_hidden = ax.imshow(nda, 
                         cmap='pink')

x_0=nda.shape[0]/10
x_1=x_0
y_0=nda.shape[1]/10
y_1=y_0+nda.shape[0]/5

p0 = dem_raster.xy(x_0,y_0)
print(p0)
p1 = dem_raster.xy(x_1,y_1)
print(p1)

dist = distance.distance(p0,p1).meters
print('Distance: '+str(dist))


#ax.plot(peak_bb[0],peak_bb[1],'*')
#ax.plot([L[0],R[0]],[L[1],R[1]], 'k-')                                
ax.plot([p0[0],p1[0]],[p0[1],p1[1]], 'k-', linewidth=5)      
ax.plot([p0[0],p1[0]],[p0[1],p1[1]], 'w-', linewidth=2)   
txt = ax.text((p0[0]+p1[0])/2,p1[1]*1.00005,str(int(round(dist)))+'m',
        color='w',
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=15
        )                          
txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])
plt.draw()

# plot on the same axis with rio.plot.show
image = show(nda,
             transform=dem_raster.transform, 
             ax=ax, 
             cmap='pink')

               

# add colorbar using the now hidden image
clb = fig.colorbar(image_hidden, ax=ax)
clb.ax.set_title('meters\n(SRTM-1)')


# https://doi.org/10.5066/F7PR7TFT


plt.show()