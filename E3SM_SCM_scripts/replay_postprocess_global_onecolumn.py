#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 9 16:11:48 2024

@author: bogenschutz1
"""
# -*- coding: utf-8 -*-
"""
Post process output generated to "replay" an E3SM column in SCM mode

This script assumes that all replay data is in one file.  This script extracts one 
column from the file to generate forcing data to run in E3SM SCM.  
This script is provided as an example and can be modified to meet
the users individual needs.
"""

import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate
import netCDF4 as nc4
import numpy as np
import scipy as sp
import pylab
import os

###################################
##### Begin user input

# Directory where output lives
datadir='/pscratch/sd/b/bogensch/SCM_sims/E3SM_SCMv3.F2010.replay.001a.ne30pg2_oECv3.pm-cpu/run/'

# Name of the case
casename='E3SM_SCMv3.F2010.replay.001a'

# File append information for the file to process
fileappend='.ne30pg2_oECv3.pm-cpu.eam.h1.0001-01-01-00000.nc'

# select lat and lon column to extract
lat_ex=0.0
lon_ex=0.0

# the lon and lat bounds of subset replay data; for global data keep blank
lonlat=''

# Specify desired location of processed output file
#   by default set to the input directory
outdir='/global/homes/b/bogensch/acme_scripts_scm001/'

###### End user input
####################################

# define input file
inputfile=datadir+casename+fileappend

# define output file
outputfile=outdir+casename+'.lon'+str(lon_ex)+'_lat'+str(lat_ex)+'.replaydata_for_SCM.nc'

# does output file already exist?  if so delete and start fresh
if os.path.isfile(outputfile):
   os.system('rm '+outputfile)
   
# Open input file
f_in=nc4.Dataset(inputfile,mode='r')

# Open output file
f_out=nc4.Dataset(outputfile,mode='w',format='NETCDF4')

############################ INPUT FILE READ INS
# Read in dimension of input file
ncol_dyn=f_in.dimensions['ncol_d'+lonlat]
ncol_phys=f_in.dimensions['ncol'+lonlat]
nlev=f_in.dimensions['lev']
nilev=f_in.dimensions['ilev']
ntime=f_in.dimensions['time']
nbnd=f_in.dimensions['nbnd']

# Read in coordinates of input file
lat_dyn=f_in.variables['lat_d'+lonlat]
lon_dyn=f_in.variables['lon_d'+lonlat]
lat_phys=f_in.variables['lat'+lonlat]
lon_phys=f_in.variables['lon'+lonlat]
lev_in=f_in.variables['lev']
ilev_in=f_in.variables['ilev']
time_in=f_in.variables['time']
tsec_in=f_in.variables['tsec']

############################ OUTPUT FILE CREATES
# Define dimensions for output file
f_out.createDimension('ncol',1)
f_out.createDimension('time',ntime.size)
f_out.createDimension('lev',nlev.size)
f_out.createDimension('ilev',nilev.size)
f_out.createDimension('nbnd',nbnd.size)

# Define coordinates for outputfile
lat=f_out.createVariable('lat','f4','ncol')
lon=f_out.createVariable('lon','f4','ncol')
lev=f_out.createVariable('lev','f4','lev')
ilev=f_out.createVariable('ilev','f4','ilev')
time=f_out.createVariable('time','f4','time')
tsec=f_out.createVariable('tsec','f4','time')
bdate=f_out.createVariable('bdate','i4')

############################ Copy coordinate information
lat[:]=lat_ex
lat.units=lat_dyn.units
lat.long_name=lat_dyn.long_name

lon[:]=lon_ex
lon.units=lon_dyn.units
lon.long_name=lon_dyn.long_name

time[:]=time_in[:]
time.units=time_in.units
time.long_name=time_in.long_name

tsec[:]=tsec_in[:]
tsec.units='s'
tsec.long_name=tsec_in.long_name

lev[:]=lev_in[:]
lev.units=lev_in.units
lev.long_name=lev_in.long_name

ilev[:]=ilev_in[:]
ilev.units=ilev_in.units
ilev.long_name=ilev_in.long_name

bdate[0]=20000101
bdate.units='yyyymmdd'
bdate.long_name='base date'

############################ Find column to extract for both physics and dynamics

testval=abs(lat_dyn[:] - lat_ex)+abs(lon_dyn[:] - lon_ex)
dy_col=np.where(testval == np.min(testval))

testval=abs(lat_phys[:] - lat_ex)+abs(lon_phys[:] - lon_ex)
phys_col=np.where(testval == np.min(testval))

print(lat_dyn[dy_col])
print(lon_dyn[dy_col])

print(dy_col)
print(np.size(testval))
#searchva=np.min(lat_test+lon_test)

############################## Process relevant variables

# Loop over inputdata to search for variables with specific dimensions
indata = nc4.Dataset(inputfile)
# list of vars w dimenions 'time' and 'hru'
wanted_vars = []

# loop thru all the variables
for v in indata.variables:
  # set filling flag to false by default
  fillvar=False

  print(indata.variables[v].dimensions)


  # process variables that are 3D and on dynamics grid
  #  These variables do NOT have to be remapped
  if indata.variables[v].dimensions == ('time','lev','ncol_d'+lonlat):
     fillvar=True
     current_name=indata.variables[v].name
     current_var=f_in.variables[current_name]
     current_var_out=f_out.createVariable(current_name,'f4',('time','lev','ncol'))
     print(np.shape(current_var),dy_col[0])
     current_var_out[:]=current_var[:,:,dy_col[0]]
  
  # process 2D variables on dynamics grid   
  if indata.variables[v].dimensions == ('time','ncol_d'+lonlat):
     fillvar=True
     current_name=indata.variables[v].name
     current_var=f_in.variables[current_name]
     current_var_out=f_out.createVariable(current_name,'f4',('time','ncol'))
     current_var_out[:]=current_var[:,dy_col[0]]

  # process 2D variables on physics grid - Needs to be remapped  
  if indata.variables[v].dimensions == ('time','ncol'+lonlat):
     fillvar=True
     current_name=indata.variables[v].name
     current_var=f_in.variables[current_name]
     current_var_out=f_out.createVariable(current_name,'f4',('time','ncol'))
     current_var_out[:]=current_var[:,phys_col[0]]
     
  # process 3D variables on physics grid - Needs to be remapped  
  if indata.variables[v].dimensions == ('time','lev','ncol'+lonlat):
     fillvar=True
     current_name=indata.variables[v].name
     current_var=f_in.variables[current_name]
     current_var_out=f_out.createVariable(current_name,'f4',('time','lev','ncol'))
     current_var_out[:]=current_var[:,:,phys_col[0]]     
     
  if (fillvar):
     print('Processing variable: ',current_name)    
     # Fill the information for this variable
     current_var_out.unit=current_var.units
     current_var_out.long_name=current_var.long_name

# Close both the input and output files
f_in.close()
f_out.close()

# Add this attribute, which is needed for E3SM REPLAY runs
thecmd ='ncatted -h -a E3SM_GENERATED_FORCING,global,o,c,"create SCM IOP dataset" '+outputfile
os.system(thecmd)
