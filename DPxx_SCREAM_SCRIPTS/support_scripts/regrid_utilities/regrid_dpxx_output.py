# -*- coding: utf-8 -*-
"""
Process 2D & 3D fields and put them on an x & y grid.
Data will be placed in a folder called post_processed_output
in your case directory.

3D currently only works with data on the lev grid (as opposed to ilev).
This is because ilev currently doesn't appear to be written to to
output files for some reason.

This comes with no warranty and is provided as a convenience. 
"""

import netCDF4 as nc4
import numpy as np
import scipy as sp
import pylab
import os
import glob
import matplotlib.pyplot as plt

###### Start user input ################################################
# What variables do you want to process?  You have two options, you
#   can either list specific variables or simply put "all" to regrid every
#   2D & 3D variable in your output stream. Example below of selected vars.
#vartodo=["T_mid","IceWaterPath"]
vartodo=["all"]

# Supply the run directory, casename, and prefix of the output stream to process
casedir='/pscratch/sd/b/bogensch/dp_screamxx/'
casename='scream_dpxx_GATEIDEAL.3.2km.003a'
outstream='scream_dpxx_GATEIDEAL.3.2km.003a.scream.hourly.avg.AVERAGE.nhours_x1'

###### End user input
#######################################################################

def regrid_array(data, x_coords, y_coords):
    # Create dictionaries to map the coordinates to their indices
    unique_x = sorted(set(x_coords))
    unique_y = sorted(set(y_coords))
    
    x_index = {value: idx for idx, value in enumerate(unique_x)}
    y_index = {value: idx for idx, value in enumerate(unique_y)}
    
    # Determine the shape of the 2D array
    max_x = len(unique_x)
    max_y = len(unique_y)

    # Convert x_coords and y_coords to indices
    x_indices = np.array([x_index[x] for x in x_coords])
    y_indices = np.array([y_index[y] for y in y_coords])
    
    # Determine the number of slices (time or vertical levels)
    num_slices = data.shape[0]
    
    if (data.ndim == 2):
    
       # Create an empty 3D array with the determined shape
       arranged_array = np.empty((num_slices, max_y, max_x))
    
       # Use advanced indexing to place the data in the correct locations in one go
       arranged_array[:, y_indices, x_indices] = data
       
    if (data.ndim == 3):
       num_levs = data.shape[2]  # Assuming the 3rd dimension is the number of levels
    
       # Create an empty 4D array with the determined shape
       arranged_array = np.empty((num_slices, num_levs, max_y, max_x))

       # Vectorized operation to place data into 4D array
       # Use broadcasting to index array positions efficiently
       arranged_array[:, :, y_indices, x_indices] = data.transpose(0, 2, 1)
    
    # Create the appropriately arranged x and y coordinate arrays
    arranged_x_coords = np.array(unique_x)
    arranged_y_coords = np.array(unique_y)
    
    return arranged_array, arranged_x_coords, arranged_y_coords

################################

def SCREAM_get_cords(initfile):

   f=nc4.Dataset(initfile)
   time=f.variables['time'][:]
   lev=f.variables['lev'][:]
   crm_grid_x=f.variables['lon'][:]
   crm_grid_y=f.variables['lat'][:]
   
#   conversion_fac=(3.14/180.)
   conversion_fac=1.
   
   crm_grid_x=crm_grid_x*conversion_fac
   crm_grid_y=crm_grid_y*conversion_fac
   
   f.close()

   return time, lev, crm_grid_x, crm_grid_y

################################

def determine_var_dim(var,var_name,matching_vars,dimarr):

   # Check if the dimensions are ('time', 'ncol')
   if var.dimensions == ('time', 'ncol'):
      matching_vars.append(var_name)
      dimarr.append('2D')
   
   # Check if the dimensions are ('time', 'ncol')
   if var.dimensions == ('time', 'ncol','lev'):
      matching_vars.append(var_name)
      dimarr.append('3D')   

################################
   
def find_variables(filename,varlist_in):
    # Open the NetCDF file
    dataset = nc4.Dataset(filename)

    # Initialize a list to store variable names that match the criteria
    matching_vars = []
    dimarr = []

    for var_entry in varlist_in:

       # If all variables are done, search for variables in file
       if (var_entry == "all"): 

          # Iterate over all the variables in the NetCDF file
          for var_name in dataset.variables:
             var = dataset.variables[var_name]
             determine_var_dim(var,var_name,matching_vars,dimarr)		
       else:

          # user specified output
          var = dataset.variables[var_entry]
          determine_var_dim(var,var_entry,matching_vars,dimarr)

    # Close the dataset
    dataset.close()

    return matching_vars, dimarr

################################

def check_path(dim):
   
   # Check to see if post process directory exists for 2d output; if not create it
   postpath_dim=casedir+casename+'/post_processed_output/'+dim+'/'
   ishere=os.path.isdir(postpath_dim)

   # Make directory for post processing
   if not ishere:
      os.system('mkdir '+postpath_dim)
      
   return postpath_dim

##############################################################################  
##############################################################################
##############################################################################
# Begin main function

# Check to see if post process directory exists; if not create it
postpath=casedir+casename+'/post_processed_output/'
ishere=os.path.isdir(postpath)

# Make directory for post processing
if not ishere:
   os.system('mkdir '+postpath)
   
############################################################
#

# Make a list of files to process
filedir=casedir+casename+'/run/'+outstream
filelist=sorted(glob.glob(filedir+'*.nc'))
print(filedir)
# Get coordinates and timing information
# open first file
time_in, lev_in, crm_grid_x, crm_grid_y = SCREAM_get_cords(filelist[0])

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
   time_in, lev_in, crm_grid_x, crm_grid_y = SCREAM_get_cords(filelist[len(filelist)-1])
   ntimes=ntimes+len(time_in)

# Are we doing all variables or selected variables?
vartodo,dimarr=find_variables(filelist[0],vartodo)

numvars=len(vartodo)

#############################################################
# Process each variable one at a time
for v in range(0,numvars):

   # Make sure output directory has been created
   postpath_dim=check_path(dimarr[v])

   print('PROCESSING VARIABLE: ',vartodo[v])
   outputfile=postpath_dim+casename+'_'+dimarr[v]+'_'+vartodo[v]+'.nc'   
   
   ishere=os.path.isfile(outputfile)
   print('Making output file ',outputfile)
   if ishere:
      os.system('rm '+outputfile)
   f=nc4.Dataset(outputfile,'w',format='NETCDF4')
   f.createDimension('x',len(arranged_x_coords))
   f.createDimension('y',len(arranged_y_coords))
   f.createDimension('time',ntimes)
   if (dimarr[v] == '3D'):
      f.createDimension('lev',len(lev_in))

   x=f.createVariable('x','f4','x')
   y=f.createVariable('y','f4','y')
   time=f.createVariable('time','f4','time')
   if (dimarr[v] == '2D'):
      out_var=f.createVariable(vartodo[v],'f4',('time','y','x'))
   if (dimarr[v] == '3D'):
      lev=f.createVariable('lev','f4','lev')
      out_var=f.createVariable(vartodo[v],'f4',('time','lev','y','x'))
      
   x[:]=arranged_x_coords
   x.units='m'
   x.long_name='x coordinate'

   y[:]=arranged_y_coords
   y.units='m'
   y.long_name='y coordinate'
   
   if (dimarr[v] == '3D'):
      lev[:]=lev_in
      lev.units='mb'
      lev.long_name='hybrid level at midpoints'      

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

      var_arranged,dummyx,dummyy=regrid_array(var, crm_grid_x, crm_grid_y)
   
      te=ts+len(time_in)
      time[ts:te]=time_in
      if (dimarr[v] == '2D'):
         out_var[ts:te,:,:]=var_arranged
      if (dimarr[v] == '3D'):
         out_var[ts:te,:,:,:]=var_arranged
      ts=te
   
      del(var)
      del(var_arranged)
   
      fi.close()

   f.close()
