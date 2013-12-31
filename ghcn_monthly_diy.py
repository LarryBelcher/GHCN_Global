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
mm = fdate[4:]
ms = int2str(mm)
labeldate = ms+' '+yyyy
outpng = "../Images/Monthly/4096/GHCN_monthly_temperature_anom_"+fdate+"_4096.png"

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)



#Define some figure properties
figxsize = 56.875
figysize = 28.435

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


# define projection
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,area_thresh=10000,\
            llcrnrlon=-180,urcrnrlon=180,resolution='l')

orig = Image.open(infile)
bg = Image.new("RGB", orig.size, (211,211,211))
bg.paste(orig,orig)
bg.save("./tmp.png")
im = m.warpimage("./tmp.png")
im = m.warpimage("./tmp.png")

# draw coastlines and boundaries
m.drawcoastlines(color='#787878',linewidth=0.75,)
m.drawcountries(color='#787878',linewidth=0.75)



#Save figure w/ grey behind the globe ***For testing only now!!!
#plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01, facecolor='#787878')

#Save figure w/o grey behind the globe
plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01)

#clean up
cmd = "rm tmp.png"
os.system(cmd)

