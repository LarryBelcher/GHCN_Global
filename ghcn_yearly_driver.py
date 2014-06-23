#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, datetime, sys
import numpy as np
#import _imaging



fdate = sys.argv[1]   #(expects format like: 2013)
yyyy = fdate
labeldate = fdate

imgsize = sys.argv[2]  #(expects 620, 1000, DIY, HD, or HDSD )

if(imgsize != 'DIY'): figdpi = 72
if(imgsize == 'DIY'): figdpi = 300

cmd = "/usr/bin/python ./ghcn_yearly_map.py "+fdate+" "+imgsize
os.system(cmd)

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	cmd = "/usr/bin/python ./ghcn_yearly_colorbar.py "+fdate+" "+imgsize
	os.system(cmd)

if not os.path.isdir('../Images/Yearly'):
	cmd = 'mkdir ../Images/Yearly'
	os.system(cmd)
if not os.path.isdir('../Images/Yearly/'+imgsize):
	cmd = 'mkdir ../Images/Yearly/'+imgsize.lower()
	os.system(cmd)


if(imgsize == '620' or imgsize == '1000'):
	im1 = Image.open("temporary_map.png")
	im2 = Image.open("temporary_cbar.png")
	im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
	im3.paste(im2, (0,im1.size[1]))
	im3.paste(im1, (0,0))
	imgw = str(im3.size[0])
	imgh = str(im3.size[1])
	img_path = '../Images/Yearly/'+imgsize+'/'
	img_name = 'tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'--'+yyyy+'-00-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im3.save(pngfile)


if(imgsize == 'DIY'):
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = '../Images/Yearly/'+imgsize.lower()+'/'
	img_name = 'tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'--'+yyyy+'-00-00.png'
	cmd = 'mv '+im1+' '+img_name
	os.system(cmd)
	im2 = "./temporary_cbar.eps"
	cbar_name = 'tempanomaly-annual-nnvl--'+yyyy+'-00-00_colorbar.eps'
	cmd = 'mv '+im2+' '+cbar_name
	os.system(cmd)	
	cmd1 = 'zip tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'--'+yyyy+'-00-00.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	os.system(cmd1)
	cmd2 = 'mv tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'--'+yyyy+'-00-00.zip '+img_path
	os.system(cmd2)
	cmd3 = 'rm '+img_name+' '+cbar_name
	os.system(cmd3)
	
if(imgsize == 'HD'):
	im1 = Image.open("temporary_map.png")
	imgw = str(im1.size[0])
	imgh = str(im1.size[1])
	draw = ImageDraw.Draw(im1)
	fntpath = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 25)
	draw.text((224,810), yyyy, (0,0,0), font=fnt1)
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Compared to 20th Century"
	draw.text((224,838), ttext, (0,0,0), font=fnt2)
	
	#Add the colorbar
	cbar_orig = Image.open('ANOM.colorbar_HD.png')
	bbox = (1,1,726,49)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	im1.paste(cbar_im, (596,865))
	
	fnt3 = ImageFont.truetype(fntpath, 48)
	text1 = "Cooler"
	text2 = "Warmer"
	draw.text((645,915), text1, (0,0,0), font=fnt3)
	draw.text((1100,915), text2, (0,0,0), font=fnt3)
	
	draw.polygon([(630,955), (615,945), (630,935)], fill="black", outline="black")
	draw.polygon([(1285,955), (1300,945), (1285,935)], fill="black", outline="black")
	
	img_path = '../Images/Yearly/'+imgsize.lower()+'/'
	img_name = 'tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'hd--'+yyyy+'-00-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im1.save(pngfile)
	
	
if(imgsize == 'HDSD'):
	im1 = Image.open("temporary_map.png")
	imgw = str(im1.size[0])
	imgh = str(im1.size[1])
	draw = ImageDraw.Draw(im1)
	fntpath = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 25)
	draw.text((408,642), yyyy, (0,0,0), font=fnt1)
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Compared to 20th Century"
	draw.text((408,670), ttext, (0,0,0), font=fnt2)
	
	#Add the colorbar
	cbar_orig = Image.open('ANOM.colorbar_HD.png')
	bbox = (1,1,726,49)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	im1.paste(cbar_im, (596,740))
	
	fnt3 = ImageFont.truetype(fntpath, 48)
	text1 = "Cooler"
	text2 = "Warmer"
	draw.text((645,791), text1, (0,0,0), font=fnt3)
	draw.text((1100,791), text2, (0,0,0), font=fnt3)
	
	draw.polygon([(630,830), (615,820), (630,810)], fill="black", outline="black")
	draw.polygon([(1285,830), (1300,820), (1285,810)], fill="black", outline="black")
	
	img_path = '../Images/Yearly/'+imgsize.lower()+'/'
	img_name = 'tempanomaly-annual-nnvl--'+imgw+'x'+imgh+'hdsd--'+yyyy+'-00-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im1.save(pngfile)

