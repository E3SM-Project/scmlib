# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import os
import SCM_diagnostics_functions

def plotprofiles(datadir,plotdir,toplev,avg_start,avg_end,filelist,caselist): 
    
    colorarr=["r","b","g","c","m","y"]
    
    numfiles=len(filelist)
        
    ############################################################
    # Make the variable list for variables to plot
    # This will make profile plots for every variable possible
    
    # Initialize list
    varstoplot=[];
    SCM_diagnostics_functions.makevarlist(datadir,filelist,4,varstoplot)
    
    ############################################################
    # loop over the variables to plot
    for x in range(0,len(varstoplot)):
        
        varname=varstoplot[x]
    
        legendlist=[];
        # loop over the number of simulations to plot
        for f in range(0,numfiles):
            
            filename=filelist[f]
            file=datadir+filename
            
            # Read in file and the dataset information
            fh=Dataset(file,mode='r')
            
            # Read in appropriate coordinate variables
            time=fh.variables['time'][:]
            lev=fh.variables['lev'][:]
            ilev=fh.variables['ilev'][:]
            
            # Generate a list to see if variables are in there
            varsinfile=fh.variables.keys()
                
            if varname in varsinfile:
                vartoplot=fh.variables[varname][:]
                
                if (avg_end == "end"):
                    plottimes=np.squeeze(np.where(time >= avg_start))
                else:
                    plottimes=np.squeeze(np.where((time >= avg_start) & \
                                                  (time <= avg_end)))
          
                if (vartoplot.ndim == 4):
                    avgprof=np.mean(vartoplot[plottimes,:,:,:],axis=0)
                elif (vartoplot.ndim == 3):
                    avgprof=np.mean(vartoplot[plottimes,:,:],axis=0)
                
                if (len(avgprof) == len(lev)):
                    levarr=lev
                elif (len(avgprof) == len(ilev)):
                    levarr=ilev
            
                legendlist.append(caselist[f])
                
                # Exceptions for plotting ease
                theunits=fh.variables[varname].units
                if (theunits == "kg/kg"):
                    avgprof=avgprof*1000.
                    theunits="g/kg"
                
                
                # Only plot to top level
                plotlevs=np.where(levarr > toplev)
            
                plt.figure(x)
#                print("f",f,colorarr[f])
                plt.plot(np.squeeze(avgprof[plotlevs]),levarr[plotlevs],colorarr[f])   
        
                plt.ylim(max(levarr),toplev)
                plt.title(fh.variables[varname].long_name + '\n' + \
                '(' + varname + ')')
                plt.ylabel('P (hPa)')
                plt.xlabel('('+theunits+')')
                plt.grid(True)
                plt.ticklabel_format(style='sci', axis='x', scilimits=(-4,4))
                
        plt.legend(legendlist)        
        pylab.savefig(plotdir+'/'+varname+'.png')
        plt.close(x)
        
    return varstoplot
        
