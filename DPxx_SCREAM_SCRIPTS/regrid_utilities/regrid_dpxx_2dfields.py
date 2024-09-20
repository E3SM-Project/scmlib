# -*- coding: utf-8 -*-
"""
Process 2D fields and put them on an x & y grid.
Data will be placed in a folder called post_processed_output/2D
in your case directory.

This comes with no warranty and is provided as a convenience. 
"""

import netCDF4 as nc4
import numpy as np
import scipy as sp
import pylab
import os
import glob
import matplotlib.pyplot as plt

###### User input

# What variables do you want to process?
vartodo=["LiqWaterPath","IceWaterPath"]

# Supply the run directory, casename, and prefix of the output files to process
rundir='/pscratch/sd/b/bogensch/dp_screamxx/'
casename='scream_dpxx_GATEIDEAL.400m.003a'
outfilepre='scream_dpxx_GATEIDEAL.400m.003a.scream.5minute.2d.instant.INSTANT.nmins_x5'

#######################################################################

def arrange_3d_array(data, x_coords, y_coords):
    # Create dictionaries to map the coordinates to their indices
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    x_index = {value: idx for idx, value in enumerate(unique_x)}
    y_index = {value: idx for idx, value in enumerate(unique_y)}
    
    # Determine the shape of the 2D array
    max_x = len(unique_x)
    max_y = len(unique_y)
    
    # Determine the number of slices (time or vertical levels)
    num_slices = data.shape[0]
    
    # Create an empty 3D array with the determined shape
    array_3d = np.empty((num_slices, max_y, max_x))
    
    # Convert x_coords and y_coords to indices
    x_indices = np.array([x_index[x] for x in x_coords])
    y_indices = np.array([y_index[y] for y in y_coords])
    
    # Use advanced indexing to place the data in the correct locations
    for t in range(num_slices):
        array_3d[t, y_indices, x_indices] = data[t]
    
    # Create the appropriately arranged x and y coordinate arrays
    arranged_x_coords = np.array(unique_x)
    arranged_y_coords = np.array(unique_y)
    
    return array_3d, arranged_x_coords, arranged_y_coords

def SCREAM_get_cords(initfile):

   f=nc4.Dataset(initfile)
   time=f.variables['time'][:]
   crm_grid_x=f.variables['lon'][:]
   crm_grid_y=f.variables['lat'][:]
   
#   conversion_fac=(3.14/180.)
   conversion_fac=1.
   
   crm_grid_x=crm_grid_x*conversion_fac
   crm_grid_y=crm_grid_y*conversion_fac
   
   f.close()

   return time, crm_grid_x, crm_grid_y

##############################################################################
# Begin main function

# Check to see if post process directory exists; if not create it
postpath=rundir+casename+'/post_processed_output/'
ishere=os.path.isdir(postpath)

# Make directory for post processing
if not ishere:
   os.system('mkdir '+postpath)

# Check to see if post process directory exists for 2d output; if not create it
postpath_h2=rundir+casename+'/post_processed_output/2D/'
ishere=os.path.isdir(postpath_h2)

# Make directory for post processing
if not ishere:
   os.system('mkdir '+postpath_h2)
   
############################################################
#

# Make a list of files to process
filedir=rundir+casename+'/run/'+outfilepre
filelist=sorted(glob.glob(filedir+'*.nc'))
print(filedir)
# Get coordinates and timing information
# open first file
time_in, crm_grid_x, crm_grid_y = SCREAM_get_cords(filelist[0])

# arrange the coordinates
unique_x = sorted(set(crm_grid_x))
unique_y = sorted(set(crm_grid_y))

# Create the appropriately arranged x and y coordinate arrays
arranged_x_coords = np.array(unique_x)
arranged_y_coords = np.array(unique_y)

# figure out number of times in files
numfiles=len(filelist)
numtimes=len(time_in)

# figure out number of times for output file
ntimes=numtimes*(numfiles-1.)

# figure out number of times in last file
if (numfiles > 1):
   time_in, crm_grid_x, crm_grid_y = SCREAM_get_cords(filelist[len(filelist)-1])
   ntimes=ntimes+len(time_in)

numvars=len(vartodo)

#############################################################
# Process each variable one at a time
for v in range(0,numvars):

   print('Doing variable: ',vartodo[v])
   outputfile=postpath_h2+casename+'_2D_'+vartodo[v]+'.nc'   
   
   ishere=os.path.isfile(outputfile)
   print('Making output file ',outputfile)
   if ishere:
      os.system('rm '+outputfile)
   f=nc4.Dataset(outputfile,'w',format='NETCDF4')
   f.createDimension('x',len(arranged_x_coords))
   f.createDimension('y',len(arranged_y_coords))
   f.createDimension('time',ntimes)

   x=f.createVariable('x','f4','x')
   y=f.createVariable('y','f4','y')
   time=f.createVariable('time','f4','time')
   out_var=f.createVariable(vartodo[v],'f4',('time','y','x'))

   x[:]=arranged_x_coords
   x.units='m'
   x.long_name='x coordinate'

   y[:]=arranged_y_coords
   y.units='m'
   y.long_name='y coordinate'

   time.units='days'
   time.long_name='time'

   out_var.long_name=vartodo[v]
   
   # Now loop over each file
   ts=0
   te=numtimes
   for thefile in filelist:
   
      print("Processing file: ", thefile)
      
      fi=nc4.Dataset(thefile,mode='r')
      time_in=fi.variables['time'][:]
      var=fi.variables[vartodo[v]][:]
   
      var_arranged,dummyx,dummyy=arrange_3d_array(var, crm_grid_x, crm_grid_y)
   
      te=ts+len(time_in)
      time[ts:te]=time_in
      out_var[ts:te,:,:]=var_arranged
      ts=te
   
      del(var)
      del(var_arranged)
   
      fi.close()

   f.close()
