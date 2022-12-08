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
import DP_diagnostics_functions

def plot1Dtime(datadir,plotdir,time_start,time_end,filelist,caselist): 
    
    colorarr=["r","b","g","c","m","y"]
    
    numfiles=len(filelist)
    
    ############################################################
    # Make the variable list for variables to plot
    # This will make profile plots for every variable possible
    
    # Initialize list of variables to plot
    varstoplot=[];
    
    # temporarily limit to searching just the first file for speed
    listtodo=filelist[0]
    DP_diagnostics_functions.makevarlist(datadir,listtodo,3,varstoplot)
    
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
            
            # Generate a list to see if variables are in there
            varsinfile=fh.variables.keys()
                
            if varname in varsinfile:
                vartoplot=fh.variables[varname][:]
                
                if (time_end == "end"):
                    plottimes=np.squeeze(np.where(time >= time_start))
                else:
                    plottimes=np.squeeze(np.where((time >= time_start) & \
                                                  (time <= time_end)))

                if (vartoplot.ndim == 3):                    
                    vartoplot2=np.squeeze(vartoplot[plottimes,:,:])
                elif (vartoplot.ndim == 2):
                    vartoplot2=np.mean(vartoplot[plottimes,:],axis=1)
            
                plt.figure(x)
#                plt.plot(time[plottimes],np.squeeze(vartoplot[plottimes,:,:]),colorarr[f])   
                plt.plot(time[plottimes],vartoplot2,colorarr[f])
                
                legendlist.append(caselist[f])
        
                plt.title(fh.variables[varname].long_name + '\n' + \
                '(' + varname + ')')
                plt.xlabel('time (days)')
                if hasattr(fh.variables[varname],'units'):
                    plt.ylabel('('+fh.variables[varname].units+')')
                plt.grid(True)
                
        plt.legend(legendlist)       
        pylab.savefig(plotdir+'/'+varname+'.png')
        plt.close(x)

    return varstoplot

################################################################
### Plot the 2 dimensional timeseries

def plot2Dtime(datadir,plotdir,toplev,filelist,caselist): 
    
    numfiles=len(filelist)
    
    # Make list of variables to plot
    varstoplot=[];
    DP_diagnostics_functions.makevarlist(datadir,filelist,4,varstoplot)
    
    ############################################################
    # loop over the variables to plot
    for x in range(0,len(varstoplot)):
        
        varname=varstoplot[x]
    
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
                
                avgprof=np.mean(vartoplot,axis=0)
                
                if (len(avgprof) == len(lev)):
                    levarr=lev
                elif (len(avgprof) == len(ilev)):
                    levarr=ilev
            
                # Only plot to top level
                plotlevs=np.where(levarr > toplev)

                plt.figure(x)  
                vartoplot=np.squeeze(vartoplot[:,plotlevs])
                vartoplot=np.rot90(vartoplot)
                levarr=levarr[plotlevs]
                rev_lev=levarr[::-1]
                sc=plt.contourf(time,rev_lev,vartoplot)
                plt.ylim(max(rev_lev),toplev)
        
                plt.title(fh.variables[varname].long_name + \
                ' (' + varname + ')' '\n' + caselist[f])
                plt.ylabel('P (hPa)')
                plt.xlabel('time (days)')
                clb=plt.colorbar(sc)
                clb.set_label('('+fh.variables[varname].units+')')
                
                pylab.savefig(plotdir+'/'+varname+caselist[f]+'.png')
                plt.close(x)
                
    return

################################################################
### Plot the 2 dimensional timeseries

def plot2Dtimepanel(datadir,plotdir,toplev,filelist,caselist): 
    
    numfiles=len(filelist)
    
    # Make list of variables to plot
    varstoplot=[];
    DP_diagnostics_functions.makevarlist(datadir,filelist,4,varstoplot)
    
    ############################################################
    # loop over the variables to plot
    for x in range(0,len(varstoplot)):
        
        varname=varstoplot[x]
        varsinpanel=0
    
        # loop over the number of simulations to plot
        for f in range(0,numfiles):
            
            filename=filelist[f]
            file=datadir+filename
            
            # Read in file and the dataset information
            fh=Dataset(file,mode='r')
            
            # Generate a list to see if variables are in there
            varsinfile=fh.variables.keys()
                
            if varname in varsinfile:      
                varsinpanel=varsinpanel+1
                
        # start loop again and make in panel
         # loop over the number of simulations to plot
         
        plt.figure(x)
        if varsinpanel > 0: 
            if varsinpanel == 1:
                fig,axes=plt.subplots()
            elif (varsinpanel > 1) & (varsinpanel <= 4):
                fig,axes=plt.subplots(varsinpanel,sharex=True)
            elif (varsinpanel > 4) & (varsinpanel % 2 == 0):
                fig,axes=plt.subplots(varsinpanel/2.,2,sharey=True,sharex=True)
            elif (varsinpanel > 4) & (varsinpanel % 2 != 0):
                fig,axes=plt.subplots(varsinpanel/2.+1,2,sharey=True,sharex=True)
                
#            fig.tight_layout()
            
            pcount=0
#            plt.figure(x) 
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
                    
                    avgprof=np.mean(vartoplot,axis=0)
                    
                    if (len(avgprof) == len(lev)):
                        levarr=lev
                    elif (len(avgprof) == len(ilev)):
                        levarr=ilev
                
                    # Only plot to top level
                    plotlevs=np.where(levarr > toplev)
                       
                    vartoplot=np.squeeze(vartoplot[:,plotlevs])
                    vartoplot=np.rot90(vartoplot)
                    vartoplot=np.flipud(vartoplot)
                    levarr=levarr[plotlevs]
                    rev_lev=levarr
                    if pcount == 0:
                        fig.suptitle(fh.variables[varname].long_name + \
                    ' (' + varname + ')',y=1.01)
                    if varsinpanel == 1:
                        sc=axes.contourf(time,rev_lev,vartoplot)
                        axes.set_ylim(max(rev_lev),toplev)
                        axes.set_title(caselist[f])
                        axes.set_ylabel('P (hPa)')
                    elif (varsinpanel > 1) & (varsinpanel <= 4):
                        sc=axes[pcount].contourf(time,rev_lev,vartoplot)
                        axes[pcount].set_ylim(max(rev_lev),toplev)
                        axes[pcount].set_title(caselist[f])
                        axes[pcount].set_ylabel('P (hPa)')
                    elif (varsinpanel > 4) & (pcount % 2 == 0):
                        sc=axes[pcount/2,0].plt.contourf(time,rev_lev,vartoplot)
                        axes[pcount/2,0].set_ylim(max(rev_lev),toplev)
                        axes[pcount/2,0].set_title(caselist[f])
                        axes[pcount/2,0].set_ylabel('P (hPa)')                        
                    elif (varsinpanel > 4) & (pcount % 2 != 0):
                        sc=axes[pcount/2,1].plt.contourf(time,rev_lev,vartoplot)
                        axes[pcount/2,1].set_ylim(max(rev_lev),toplev)
                        axes[pcount/2,1].set_title(caselist[f])
                        axes[pcount/2,1].set_ylabel('P (hPa)') 
                        
                    # get unit info here because next file may not have it
                    if hasattr(fh.variables[varname],'units'):
                        theunits=fh.variables[varname].units
                    else:
                        theunits="-"
                    
                    pcount=pcount+1
            
#            plt.ylabel('P (hPa)')
            plt.xlabel('time (days)')
            
            fig.tight_layout()

            if (varsinpanel > 1):
                clb=fig.colorbar(sc,ax=axes.ravel().tolist())
            else:
                clb=fig.colorbar(sc)

            clb.set_label(theunits)
            
#            fig.subplots_adjust(top=0.9,left=0.1,bottom=0.1)
            
            pylab.savefig(plotdir+'/'+varname+'.png',bbox_inches='tight')
            plt.close(x)                    
                
    return varstoplot
