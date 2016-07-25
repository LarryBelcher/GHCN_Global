#!/usr/bin/python

'''******************************************************************************************************
Program: nnvlmaindriver.py

Usage: ./nnvlmaindriver.py [args]

Synopsis:
This script will retrieve NNVL monthly global temperature anomaly "original" images. If new data exist, 
the most recent monthly maps will be created. The user has the option to pass arguments in the form of
year and month to force the script to generate maps for a specific month (year). Otherwise, the
script will attempt to process the "previous" month's maps.

*********************************************************************************************************'''

import datetime, subprocess, sys, urllib, os
from dateutil.relativedelta import *


if __name__ == '__main__':


	
	if(len(sys.argv) == 1):
		date_last_month = datetime.datetime.now() - relativedelta(months=1)
		yyyy = date_last_month.year
		mm = date_last_month.month
		stryyyy = str(yyyy)
		if(mm < 10): strmm = '0'+str(mm)
		if(mm > 9): strmm = str(mm)
	if(len(sys.argv) == 2):
		stryyyy = sys.argv[1][:4]
		strmm = sys.argv[1][4:6]
	
	filename = 'ANOM.monthly.'+stryyyy+strmm+'.color.png'
	url = "ftp://ftp.nnvl.noaa.gov/View/ANOM/Images/Color/Monthly_Calculated_vs_1981_to_2010_Average/"
	result = os.popen("curl "+url+" | grep "+filename).read()
	
	if(len(result) == 0): 
		print " "
		print "Sorry! "+filename+" does not exist on the server"

	if(len(result) != 0):
		url = "ftp://ftp.nnvl.noaa.gov/View/ANOM/Images/Color/Monthly_Calculated_vs_1981_to_2010_Average/"+filename
		urllib.urlretrieve(url, "tmp.png")
		cmd = "mv tmp.png ../Images/Monthly/Orig/"+filename
		subprocess.call(cmd,shell=True)	
		isz = ['620', '1000', 'DIY', 'HD', 'HDSD']
		for i in xrange(len(isz)):
			cmd = 'python ghcn_monthly_driver.py '+stryyyy+strmm+' '+isz[i]
			subprocess.call(cmd, shell=True)
		cmd = "./UploadDsImages.csh"
		subprocess.call(cmd, shell=True)
		