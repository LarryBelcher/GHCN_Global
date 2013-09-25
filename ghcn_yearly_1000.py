#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import shapefile, os, subprocess, urllib, time, sys, Image, ImageOps
import matplotlib.font_manager as font_manager



infile = sys.argv[1] #expecting a filename like: ANOM.yearly.2012.color.png
fdate = infile.split('.')[2]
yyyy = fdate[0:4]
labeldate = yyyy
outpng = "../Images/Yearly/GHCN_yearly_temperature_anom_"+fdate+"_1000.png"

path = '/usr/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)



#Define some figure properties
figxsize = 9.7
figysize = 13
figdpi = 100
logo_image = './noaa_logo_1000.png'
logo_x = 905
logo_y = 62
cbar_image = './ANOM.colorbar_1000.png'
cbar_x = 294
cbar_y = 35

fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax = fig.add_axes([0.0,0.1,1.0,0.85])

## define projection (use -98.5 to center on North America)
m = Basemap(projection='hammer',lon_0=0,resolution='l',area_thresh=10000)
m.drawmapboundary(color='#787878', linewidth=0.5)
#m.fillcontinents(color='#E3E3E3')

orig = Image.open(infile)
bg = Image.new("RGB", orig.size, (211,211,211))
bg.paste(orig,orig)
bg.save("./tmp.png")
im = m.warpimage("./tmp.png")


# draw coastlines and boundaries
m.drawcoastlines(color='#787878',linewidth=0.2)
m.drawcountries(color='#787878',linewidth=0.2)


#Add the NOAA logo
logo_im = Image.open(logo_image)
height = logo_im.size[1]
# We need a float array between 0-1, rather than
# a uint8 array between 0-255 for the logo
logo_im = np.array(logo_im).astype(np.float) / 255
fig.figimage(logo_im, logo_x, logo_y, zorder=10)

#Add the colorbar
cbar_orig = Image.open(cbar_image)
cbar_im = ImageOps.expand(cbar_orig,border=1,fill='#454545')
#height = cbar_im.size[1]
# We need a float array between 0-1, rather than
# a uint8 array between 0-255 for the logo
cbar_im = np.array(cbar_im).astype(np.float) / 255
fig.figimage(cbar_im, cbar_x, cbar_y, zorder=10)


ax2 = fig.add_axes([0.0,0.275,1.0,0.4])
ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_xticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])
plt.text(0.275, 0.0, '-11', fontproperties=propr, size=11)
plt.text(0.5, 0.0, '0', fontproperties=propr, size=11)
plt.text(0.705, 0.0, '11', fontproperties=propr, size=11)
plt.text(0.35, 0.09, 'Difference from average temperature', fontproperties=propb, size=11)
plt.text(0.63, 0.09, '($^\circ$F)', fontproperties=propr, size=11)
plt.text(0.005, 0.04, labeldate, fontproperties=propr, size=11, color='#787878')
plt.text(0.9, 0.04, 'Climate.gov', fontproperties=propr, size=11, color='#787878')
plt.text(0.9, 0.0, 'Data: NCDC', fontproperties=propr, size=11, color='#787878')



#plt.savefig(outpng, dpi=310, bbox_inches='tight', pad_inches=0)
#plt.savefig(outpng, dpi=figdpi,orientation='landscape',transparent='True',bbox_inches='tight',pad_inches=0.75)
plt.savefig(outpng,dpi=figdpi,orientation='landscape',bbox_inches='tight',pad_inches=0.15)
#plt.savefig(outpng, dpi=figdpi, orientation='landscape', transparent='True', pad_inches=0.75)
#plt.savefig(outpng, dpi=figdpi, orientation='landscape', pad_inches=0.75)
