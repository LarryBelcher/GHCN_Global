#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import shapefile, os, subprocess, urllib, time, sys, Image, ImageOps
import matplotlib.font_manager as font_manager


def int2str(mm):
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms


infile = sys.argv[1] #expecting a filename like: ANOM.monthly.201307.color.png
fdate = infile.split('.')[2]
yyyy = fdate[0:4]
outpng = "../Images/Yearly/1000/GHCN_yearly_temperature_anom_"+yyyy+"_1000.png"

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)



#Define some figure properties
figxsize = 13.87
figysize = 8.38

figdpi = 72
logo_image = './noaa_logo_620.png'
logo_x = 946
logo_y = 56
cbar_image = './ANOM.colorbar_620.png'
cbar_x = 371
cbar_y = 21

fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=True, axisbg='#F5F5F5')


# define projection (use -98.5 to center on North America)
m = Basemap(projection='hammer',lon_0=0,resolution='l',area_thresh=10000, ax=ax1)
m.drawmapboundary(color='#787878', linewidth=0.4)


orig = Image.open(infile)
bg = Image.new("RGB", orig.size, (211,211,211))
bg.paste(orig,orig)
bg.save("./tmp.png")
im = m.warpimage("./tmp.png")


# draw coastlines and boundaries
m.drawcoastlines(color='#787878',linewidth=0.2,)
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
bbox = (1,1,257,12)
cbar_orig = cbar_orig.crop(bbox)
old_size = cbar_orig.size
new_size = (old_size[0]+2,old_size[1]+2)
cbar_im = Image.new("RGB", new_size)
cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
#cbar_im = ImageOps.expand(cbar_orig,border=1,fill='#505050')
# We need a float array between 0-1, rather than
# a uint8 array between 0-255 for the logo
cbar_im = np.array(cbar_im).astype(np.float) / 255
fig.figimage(cbar_im, cbar_x, cbar_y, zorder=10)


#ax2 = fig.add_axes([0.0,0.0,1.0,0.13], frameon=True, axisbg='#FFFFFF')
ax2 = fig.add_axes([0.0,0.0,1.0,0.085])
ax2.set_frame_on(False)
#ax2.spines['top'].set_color('#FFFFFF')
#ax2.spines['bottom'].set_color('#FFFFFF')
#ax2.spines['left'].set_color('#FFFFFF')
#ax2.spines['right'].set_color('#FFFFFF')
ax2.set_xticks([])
ax2.set_xticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])

plt.text(0.362, 0.15, '-11', fontproperties=propr, size=12, color='#333333')
plt.text(0.5, 0.15, '0', fontproperties=propr, size=12, color='#333333')
plt.text(0.623, 0.15, '11', fontproperties=propr, size=12, color='#333333')
plt.text(0.382, 0.72, 'Difference from average temperature', fontproperties=propb, size=12, color='#333333')
plt.text(0.595, 0.73, '($^\circ$F)', fontproperties=propr, size=12, color='#333333')
plt.text(0.005, 0.77, yyyy, fontproperties=propr, size=11, color='#8d8d8d')
plt.text(0.938, 0.77, 'Climate.gov', fontproperties=propr, size=11, color='#8d8d8d')
plt.text(0.94, 0.55, 'Data: NCDC', fontproperties=propr, size=11, color='#8d8d8d')



#Save figure w/ grey behind the globe ***For testing only now!!!
#plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01, facecolor='#787878')

#Save figure w/o grey behind the globe
plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01)

#clean up
cmd = "rm tmp.png"
os.system(cmd)

