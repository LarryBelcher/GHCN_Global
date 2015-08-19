#!/usr/bin/python

###This module builds a c-shell script to reprocess monthly and/or yearly images

import numpy as np
import os, subprocess

'''
ofilename = 'catchup.csh'
ofile = open(ofilename,'w')
ofile.write('#!/bin/csh')
ofile.write("\n")

sname = 'ghcn_monthly_driver.py'
#years = ['2015']
#months = ['01', '02', '03', '04', '05', '06']
#imgsize = ['620', '1000', 'DIY', 'HD', 'HDSD']
years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
imgsize = ['620', '1000', 'DIY']

for i in range(len(years)):
	yyyy = years[i]
	for j in range(len(months)):
		for k in range(len(imgsize)):
			cmd = "/usr/bin/python "+sname+' '+yyyy+months[j]+" "+imgsize[k]
			ofile.write(cmd)
			ofile.write("\n")

ofile.close()

cmd = 'chmod 755 '+ofilename
subprocess.call(cmd, shell=True)


'''

###Yearly driver
ofilename = 'catchup.csh'
ofile = open(ofilename,'w')
ofile.write('#!/bin/csh')
ofile.write("\n")

sname = 'ghcn_yearly_driver.py'
years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
imgsize = ['620', '1000', 'DIY']# 'HD', 'HDSD']

for i in range(len(years)):
	yyyy = years[i]
	for k in range(len(imgsize)):
		cmd = "/usr/bin/python "+sname+' '+yyyy+" "+imgsize[k]
		ofile.write(cmd)
		ofile.write("\n")

ofile.close()

cmd = 'chmod 755 '+ofilename
subprocess.call(cmd, shell=True)

