#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import shapefile, os, subprocess, urllib, time, sys, glob
from PIL import Image
from PIL import ImageOps
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


fdate = sys.argv[1]   #(expects format like: 2013)
yyyy = fdate
labeldate = fdate

if(yyyy == '0000'): labeldate = 'No Data'

imgsize = sys.argv[2]  #(expects 620, 1000, DIY, HD, or HDSD)

if(yyyy != '0000'):
	#Define the path to the original images
	path2orig = '/Users/belcher/Desktop/NOAA_CSC/GHCN_Global/Images/Yearly/Orig/'
	infile = glob.glob(path2orig+'ANOM.yearly.*'+yyyy+'*.color.png')[0]


outpng = './temporary_map.png'

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)



#Define some figure properties

if(imgsize == '620'):
	figxsize = 8.5
	figysize = 5.8
	figdpi = 72
	logo_image = './noaa_logo_42.png'
	logo_x = 568
	logo_y = 1
	mproj = 'HA'
	mlw = 0.2

if(imgsize == '1000'):
	figxsize = 13.78
	figysize = 7.5
	figdpi = 72
	logo_image = './noaa_logo_42.png'
	logo_x = 948
	logo_y = 2
	mproj = 'HA'
	mlw = 0.2


if(imgsize == 'DIY'):
	figxsize = 13.657
	figysize = 6.817
	figdpi = 300
	mproj = 'CE'
	mlw = 0.5

if(imgsize == 'HD'):
	figxsize = 26.67
	figysize = 15
	figdpi = 72
	logo_image = './noaa_logo_100.png'
	logo_x = 1596
	logo_y = 228
	mproj = 'RB'
	mlw = 0.5

if(imgsize == 'HDSD'):
	figxsize = 26.67
	figysize = 15
	figdpi = 72
	logo_image = './noaa_logo_70.png'
	logo_x = 1442
	logo_y = 394
	mproj = 'RB'
	mlw = 0.5


fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=False, axisbg='#F5F5F5')
if(imgsize == 'HD'):
	ax1 = fig.add_axes([0.12,0.2199,0.76,0.679], frameon=False, axisbg='#F5F5F5')
if(imgsize == 'HDSD'):
	ax1 = fig.add_axes([0.15,0.367,0.7,0.513], frameon=False, axisbg='#F5F5F5')

if(mproj == 'HA'):
	# define projection (use -98.5 to center on North America)
	m = Basemap(projection='hammer',lon_0=0,resolution='l',area_thresh=10000, ax=ax1)
	m.drawmapboundary(color='#787878', linewidth=0.4)

if(mproj == 'CE'):
	# define projection
	m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,area_thresh=10000,\
	llcrnrlon=-180,urcrnrlon=180,resolution='l')

if(mproj == 'RB'):
	m = Basemap(projection='robin',lon_0=0,resolution='l')

if(yyyy != '0000'):
	orig = Image.open(infile)
	bg = Image.new("RGB", orig.size, (211,211,211))
	bg.paste(orig,orig)
	bg.save("./tmp.png")
	im = m.warpimage("./tmp.png")

#orig = np.array(orig).astype(np.float) / 255
#fig.figimage(orig, logo_x, logo_y, zorder=10)

# draw coastlines and boundaries
m.drawcoastlines(color='#787878',linewidth=mlw)
m.drawcountries(color='#787878',linewidth=mlw)


#Add the NOAA logo (except for DIY)
if(imgsize != 'DIY'):
	logo_im = Image.open(logo_image)
	height = logo_im.size[1]
	# We need a float array between 0-1, rather than
	# a uint8 array between 0-255 for the logo
	logo_im = np.array(logo_im).astype(np.float) / 255
	fig.figimage(logo_im, logo_x, logo_y, zorder=10)

if(imgsize == '620' or imgsize == '1000'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.06)

if(imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi,orientation='landscape', bbox_inches='tight', pad_inches=0.01)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng,dpi=figdpi,orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)

#clean up
cmd = "rm tmp.png"
subprocess.call(cmd,shell=True)

