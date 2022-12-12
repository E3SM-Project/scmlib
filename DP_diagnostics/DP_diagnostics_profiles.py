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

def plotprofiles(datadir,plotdir,toplev,avg_start,avg_end,timelist,filelist,caselist,derived_prof):
    
    colorarr=["r","b","g","c","m","y","k"] # standard
    
    numfiles=len(filelist)
    numtimes=len(avg_start)
        
    ############################################################
    # Make the variable list for variables to plot
    # This will make profile plots for every variable possible
    
    # Initialize list
    varstoplot=[];
    
    # temporarily limit to searching just the first file for speed
    listtodo=filelist[0]
    DP_diagnostics_functions.makevarlist(datadir,listtodo,4,varstoplot)

    # append the derived variables to the list
    numderived=len(derived_prof)
    for d in range(0,numderived):
        varstoplot.append(derived_prof[d])

    print('Now Plotting Profiles')
    ############################################################
    # loop over the variables to plot
    for x in range(0,len(varstoplot)):
        
        varname=varstoplot[x]
    
        legendlist=[];
        # loop over the number of simulations to plot
        for f in range(0,numfiles):

            Rd=287.15 # gas constant for air
            grav=9.81 # gravity
            
            filename=filelist[f]
            file=datadir+filename
            
            # Read in file and the dataset information
            fh=Dataset(file,mode='r')
            
            # Read in appropriate coordinate variables
            lat=fh.variables['lat'][:]
            lon=fh.variables['lon'][:]
            time=fh.variables['time'][:]
            lev=fh.variables['lev'][:]
            ilev=fh.variables['ilev'][:]

	    # Compute heights
            temp=fh.variables['T'][:]

            z_mid=np.zeros(lev.size)
            z_int=np.zeros(ilev.size)

            T_avg=np.mean(temp,axis=2)

	    # Guess the bottom edge
            z_int[-1]=0.0
            z_mid[-1]=10.0
            for k in range(len(lev)-2,-1,-1):
                z_mid[k] = z_mid[k+1] + Rd*T_avg[0,k]/grav*np.log(lev[k+1]/lev[k])

            for k in range(len(ilev)-2,-1,-1):
                z_int[k] = z_int[k+1] + Rd*T_avg[0,k]/grav*np.log(ilev[k+1]/ilev[k])

            # Convert from meters to kilometers
            z_mid=z_mid/1000.
            z_int=z_int/1000.

            # End compute heights
            
            # Generate a list to see if variables are in there
            varsinfile=fh.variables.keys()
                
            # The True check is a temporary hack
            if (varname in varsinfile or True):
#            if (varname in varsinfile):
            
                # If derived variable search first for that
                # If you want to add dervied variables, this is the place
                if (varname == "CLDLIQICE"):
                    vartoplot1=fh.variables['CLDLIQ'][:]
                    vartoplot2=fh.variables['CLDICE'][:]
                    vartoplot=vartoplot1+vartoplot2
                    theunits="kg/kg"
                    thelongname="Liquid + Ice Condensate"
                elif (varname == "TOT_WQW"):
                    vartoplot1=fh.variables['WQW_RES'][:]
                    vartoplot2=fh.variables['WQW_SEC'][:]
                    vartoplot=vartoplot1+vartoplot2
                    theunits="W/m2"
                    thelongname="Total (Resolved + SGS) Moisture Flux"
                elif (varname == "TOT_WTHL"):
                    vartoplot1=fh.variables['WTHL_RES'][:]
                    vartoplot2=fh.variables['WTHL_SEC'][:]
                    vartoplot=vartoplot1+vartoplot2
                    theunits="W/m2"
                    thelongname="Total (Resolved + SGS) Heat Flux"
                elif (varname == "THETAL"):
                    vartoplot1=fh.variables['T'][:]
                    vartoplot2=fh.variables['CLDLIQ'][:]
                    Ps=fh.variables['PS'][:]
                    hyam=fh.variables['hyam'][:]
                    hybm=fh.variables['hybm'][:]
                    vartoplot=compute_thetal(vartoplot1,vartoplot2,Ps,hyam,hybm)
                    theunits="K"
                    thelongname="Liquid Water Potential Temperature"
                elif (varname == "QT"):
                    vartoplot1=fh.variables['Q'][:]
                    vartoplot2=fh.variables['CLDLIQ'][:]
                    vartoplot3=fh.variables['CLDICE'][:]
                    vartoplot=(vartoplot1+vartoplot2+vartoplot3)*1000.
                    theunits="g/kg"
                    thelongname="Total Water Mixing Ratio"
                else:
                    # DEFAULT GOES HERE
                    vartoplot=fh.variables[varname][:]
                    theunits=fh.variables[varname].units
                    #theunits="dummy"
                    thelongname=fh.variables[varname].long_name

                # Are we plotting several different time periods?
                for t in range(0,numtimes):

                    if (avg_end == "end"):
                        plottimes=np.squeeze(np.where(time >= avg_start[t]))
                    else:
                        plottimes=np.squeeze(np.where((time >= avg_start[t]) & \
                                                      (time <= avg_end[t])))
                    if (vartoplot.ndim == 4):
                        avgprof=np.mean(vartoplot[plottimes,:,:,:],axis=0)
                        if (plottimes.size == 1):
                            avgprof=vartoplot[plottimes,:,0,0]
                    elif (vartoplot.ndim == 3):
                        if (plottimes.size == 1):
                            avgprof=vartoplot[plottimes,:,:]
                        else:
                            avgprof=np.mean(vartoplot[plottimes,:,:],axis=0)
                        if (lat.size > 1):
                            avgprof=np.mean(avgprof[:,1:lat.size-1],axis=1)
                    elif (vartoplot.ndim == 2):
                        avgprof=np.mean(vartoplot[plottimes,:],axis=0)

                    if (len(avgprof) == len(lev)):
                       levarr=z_mid
                    elif (len(avgprof) == len(ilev)):
                       levarr=z_int

                    #legendlist.append(caselist[f+t])
                    legendstr=caselist[f]+" "+timelist[t]
                    legendlist.append(legendstr)

                    # Exceptions for plotting ease
                    if (theunits == "kg/kg"):
                        avgprof=avgprof*1000.
                        plottheunits="g/kg"

                    if (varname == "WQW_SEC"):
                        thelongname="SGS Moisture Flux"

                    if (varname == "WQW_RES"):
                        thelongname="Resolved Moisture Flux"

                    if (varname == "WTHL_SEC"):
                        thelongname = "SGS Heat Flux"

                    if (varname == "WTHL_RES"):
                        thelongname = "Resolved Heat Flux"

                    # Copy units into a temporary arry in case manipulation needs to be done
                    #   on these variables with similar units (like convert kg/kg to g/kg)
                    plottheunits=theunits
                    # Only plot to top level
                    plotlevs=np.where(levarr < toplev)

                    plt.figure(x)
                    plt.plot(np.squeeze(avgprof[plotlevs]),levarr[plotlevs],colorarr[f+f+t],linewidth=3)

                    #plt.ylim(max(levarr),toplev)
                    plt.ylim(0,toplev)
                    plt.title(thelongname + '\n' + \
                    '(' + varname + ')',fontsize=16)
                    plt.ylabel('height (km)',fontsize=14)
                    plt.xlabel('('+plottheunits+')',fontsize=14)
                    plt.grid(True)
                    plt.ticklabel_format(style='sci', axis='x', scilimits=(-4,4))
                    plt.xticks(fontsize=14)
                    plt.yticks(fontsize=14)
                
        plt.legend(legendlist)        
        pylab.savefig(plotdir+'/'+varname+'.png',bbox_inches='tight',pad_inches=0.05)
        plt.close(x)
        
    return varstoplot

def compute_thetal(temp,cldliq,Ps,hyam,hybm):

    rgas = 287.058
    Cp = 1004.0
    R_over_Cp = 0.286
    latvap = 2.5*10**6
    Cp = 1004.0
    P0 = 1000.0

    theshape=np.shape(temp)
    timedim=theshape[0]
    levdim=theshape[1]
    ptsdim=theshape[2]
    
    pottemp=np.zeros((timedim,levdim,ptsdim))
    Psavg=np.mean(Ps,axis=1)/100.
    
    # Compute thetal
    for t in range(0,timedim):
        for k in range(0,levdim):

            levarr=P0*hyam[k]+Psavg[t]*hybm[k]
            pottemp[t,k,:] = (temp[t,k,:]*(Psavg[t]/levarr)**(R_over_Cp)) - \
            ((latvap/Cp)*cldliq[t,k,:])
	    
    vartoplot = pottemp
    return vartoplot
        
