# -*- coding: utf-8 -*-
"""
DP-SCREAM Diagnostics package

Main file to make plots and webpages for the DP-SCREAM
Diagnsotics package

This example script shows you how to plot several DP-SCREAM model simulations
against one another, in addition to comparing them to SAM LES
"""

## ==========================================================
## ==========================================================
## ==========================================================
# Begin User Defined Settings

# User defined name used for this comparison, this will be the name
#   given the directory for these diagnostics
casename="DP_SCREAM.MAGIC.test.001a"

# Directory where output files (i.e. *.eam.h0*) live
datadir="/pscratch/sd/b/bogensch/dp_scream/"

# Directory where output will be written to (plots, webpages, etc.)
outdir=datadir+"/dp_diags/"

# Here put the output files.  Currently there is a limit of
#   six cases, but this could be easily fixed if desired.

filelist_pre=["scream_dp_MAGIC.3km.001a",
              "scream_dp_MAGIC.100m.001a",
              "scream_dp_MAGIC.100m.L526.001a"]

filelist_append="2013-07-21-19620.nc"

# Easy ID for individual cases, for legends and plot titles
caselist=["3 km L128","100 m L128","100 m L526"]

# Pick your color scheme and line styles for each simulation
colorarr=["b","r","g"]
linesarr=["-","-","-"]

#################################
# OPTION FOR LES:

# If activating support for SAM LES then
#  provie the statistics file in *.nc form
LESmodel="SAM" # Set to "none" if no les desired
lesfile="/global/homes/b/bogensch/THREAD/SAM_LES/MAG3D.15A.20130720.1729_105h_128x128x460_LES.nc"
lestime_start=201.25 # Enter the staring time of your desired LES analysis (in units of your LES)
                     # Note that at the current time only units of "days" is supported

#################################
# OPTIONS FOR SET1: PROFILE PLOTS
# Make profile plots
makeprofiles=True
#  Averaging period
#  Enter "end" for average_end to end averaging at the end of the simulation
#  Simply enter "0" to start at the beginning of the simulation
prof_avg_start=[0.1] # units in days
prof_avg_end=[1.0] # units in days
# Top layer you would like to make your plots, in units of km (useful for
#   boundary layer cloud cases)
toplev_prof=4.0

# Time period legend
#  Optional: Append time period to the legend
timelist=[""]

# List variables to plot.  If you wish for ALL three dimensional variables in
#  your file to be plotted then submit as:
#  varstoplot_prof=["all"]
varstoplot_prof=["all"]

# If you selected "all" for the varstoplot_prof then you can add selected "derived" variables
#  to the output list.  Else set:
#  derived_prof=["none"]
derived_prof=["TOT_WQW","TOT_WTHL","THETAL","QT","TOT_W2","TOT_W3","TOT_THL2","TOT_QW2"]

#################################
# OPTIONS FOR SET2: 1D TIME SERIES PLOTS
# Make 1D timeseries plots
make1Dtime=True
#  1D time series plotting period
#  To plot entire simulation simply put 0 for start and "end" for end
time1d_start=0 # units in days
time1d_end=3.25 # units in days

time1d_xaxis="default"  # Specify "custom" if you want different units
# By default x-axis of the time series will be in days.  If you want
#  a different unit you can specify that here
time1d_xaxis_units="Local Time (hr)"
time1d_xaxis_mult=24
time1d_xaxis_start=6

#################################
# OPTIONS FOR SET3: 2D TIME SERIES PLOTS - CURRENTLY NOT SUPPORTED
# Make 2D timeseries plots
make2Dtime=False # NOT SUPPORTED AT THIS TIME
toplev_time2D=0.0

# Generate a webage for easier viewing?
makeweb=True

# Generate .tar file for webpage and output
maketar=True

# End User Defined Settings
## ==========================================================
## ==========================================================
## ==========================================================

# Import required packages
import DP_diagnostics_profiles
import DP_diagnostics_time
import DP_diagnostics_webpages
import os
import DP_diagnostics_functions

filelisth0=[];
filelisth1=[];
for f in range(0,len(filelist_pre)):
    filelisth0.append(filelist_pre[f]+"/run/"+filelist_pre[f]+'.eam.h0.'+filelist_append)
    filelisth1.append(filelist_pre[f]+"/run/"+filelist_pre[f]+'.eam.h1.'+filelist_append)

# Make case directory, remove and replace if it exists
casedir=outdir+casename
print("CaseDir", casedir)

if not os.path.exists(casedir):
    os.mkdir(casedir)

if makeprofiles:
    print("Making set1: Profile plots")
    profdir=casedir+'/set1'
    if not os.path.exists(profdir):
        os.mkdir(profdir)
    profwebvars=DP_diagnostics_profiles.plotprofiles(datadir,profdir,toplev_prof,\
                                                      prof_avg_start,prof_avg_end,timelist,\
                                                      filelisth0,caselist,varstoplot_prof,derived_prof,\
                                                      LES_model_opt=LESmodel,les_file_opt=lesfile,\
                                                      les_time_start_opt=lestime_start,\
                                                      colorarr=colorarr,linesarr=linesarr)

if make1Dtime:
    print("Making set2: 1D Time series")
    time1Ddir=casedir+'/set2'
    if not os.path.exists(time1Ddir):
        os.mkdir(time1Ddir)
    time1Dwebvars=DP_diagnostics_time.plot1Dtime(datadir,time1Ddir,time1d_start,time1d_end,\
                                                 filelisth1,caselist,LES_model_opt=LESmodel,les_file_opt=lesfile,\
                                                 les_time_start_opt=lestime_start,\
                                                 xaxis_opt=time1d_xaxis,xaxis_units=time1d_xaxis_units,\
						 xaxis_mult=time1d_xaxis_mult,xaxis_start=time1d_xaxis_start,
                                                 colorarr=colorarr,linesarr=linesarr)

if make2Dtime:
    print("Making set3: 2D Time series")
    time2Ddir=casedir+'/set3'
    if not os.path.exists(time2Ddir):
        os.mkdir(time2Ddir)
    time2Dwebvars=DP_diagnostics_time.plot2Dtimepanel(datadir,time2Ddir,toplev_time2D,\
                                    filelist,caselist)

## ============================
# Make Web Page

if makeweb:
    print("Making webpages")
    DP_diagnostics_webpages.main_web(casename,casedir)
    if (makeprofiles):
        DP_diagnostics_webpages.sets_web(casename,casedir,profwebvars,"set1",\
                                  "Set 1 - Profile Plots","354","268")
    if (make1Dtime):
        DP_diagnostics_webpages.sets_web(casename,casedir,time1Dwebvars,"set2",\
                                  "Set 2 - 1D Timeseries Plots","454","318")
    if (make2Dtime):
        DP_diagnostics_webpages.sets_web(casename,casedir,time2Dwebvars,"set3",\
                                  "Set 3 - 2D Timeseries Plots","454","318")

if maketar:
    print("Making tar file of case")
    DP_diagnostics_functions.make_tarfile(outdir+casename+'.tar',outdir+casename)

