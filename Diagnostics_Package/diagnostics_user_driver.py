from diagnostics import run_diagnostics
import os

##########################################################
# ARM/ASR diagnostics package for E3SM Single Column Model (SCM)
#  or doubly-periodic EAMxx (DP-EAMxx).

# Please make a copy of this driver file and modify it for your case/needs.

# This driver file should provide sufficient documentation on user
#  defined settings, but more details exist in the README.md file.

# For detailed documentation on input data requirements and how to
#  add supported observational/LES data sets please see the documentation
# (to be released very soon).

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?  Provide path.
output_dir = "/global/cfs/cdirs/e3sm/www/bogensch/Official_Example_Diags"

# User-specified general ID for this diagnostic set
general_id = "MAGIC_dpxx_bug_fix"  # Change as needed

######## Begin manage input datasets

datasets=[]

# Define each dataset and its associated metadata.
# - REQUIRED Input:
#   1) filename = the path and filename of the output dataset to be considered.
#   2) short_id = ID used in the diagnostics package for legends etc.
#   3) line_color and line_style: used for profile and 1D time series plots.

# below stuff useful to define if recycled by many datasets, but not required as it is just used
#  to define the filename metadata for E3SM/DP-SCREAM output (i.e. you can explicity just declare path
#  and file for each filename if you prefer when adding each case).
simulation_dir = "/pscratch/sd/b/bogensch/dp_screamxx" # directory for model simulations
caseappend = ".horiz_avg.AVERAGE.nmins_x15.2013-07-21-19620.nc" # file suffix for model simulations

# Path to observational datasets
obs_dir = "/global/cfs/cdirs/e3sm/diagnostics/observations/Atm/scm_dpxx_datasets/DP_EAMxx"

# Add datasets (can have as many as you want, minimum of one)
# Please list model (E3SM/SCREAM) datasets first, before LES/OBS.

# SCREAM control simulation
casename="scream_dpxx_MAGIC.prefix.001a"
datasets.append({
"filename": os.path.join(simulation_dir, casename, "run", f"{casename}{caseappend}"),
"short_id": "EAMxx 3 km Control",
"line_color": "blue",
"line_style": "-"
})

# SCREAM simulation with a bug fix
casename="scream_dpxx_MAGIC.fix.001a"
datasets.append({
"filename": os.path.join(simulation_dir, casename, "run", f"{casename}{caseappend}"),
"short_id": "EAMxx 3 km Bug Fix",
"line_color": "green",
"line_style": "--"
})

# SAM LES
datasets.append({
"filename": os.path.join(obs_dir,"MAGIC.les.dpxx.SAM.dpxx_format.nc"),
"short_id": "SAM-LES",
"line_color": "black",
"line_style": "-"
})

# 1D observation dataset
datasets.append({
"filename": os.path.join(obs_dir,"MAGIC.obs.1dvars.dpxx_format.nc"),
"short_id": "OBS",
"line_color": "gray",
"line_style": "--"
})

# Sounding observation dataset
datasets.append({
"filename": os.path.join(obs_dir,"MAGIC.obs.sounding.dpxx_format.nc"),
"short_id": "OBS",
"line_color": "gray",
"line_style": "--"
})

# KAZR observation dataset
datasets.append({
"filename": os.path.join(obs_dir,"MAGIC.obs.kazr.dpxx_format.nc"),
"short_id": "OBS-Kazr",
"line_color": "gray",
"line_style": "--"
})

# End add datasets.

######## End manage input datasets

# PROFILE PLOT AVERAGING WINDOWS:
# Define averaging windows for profile plots as numerical values in days.  You can have
#  as many averaging windows as you would like.  Each index for these arrays corresponds
#  to an averaging window.  This example does daily averaging for three days.
profile_time_s = [0.0,1.0,2.0]  # Starting times for averaging
profile_time_e = [1.0,2.0,3.0]  # Ending times for averaging

# Note that time series and time-height plots will by default plot the entire range
#  in your simulation.  If you want to modify this, then please see the optional
#  user defined settings below.

# END: MANDATORY USER DEFINED SETTINGS
##########################################################
##########################################################
# BEGIN: OPTIONAL user defined settings

# Do time-height plots? These can take a bit longer to make
do_timeheight=True

# Choose vertical plotting coordinate; can be pressure or height.
#  -If height then the variable Z3 (E3SM) or z_mid (EAMxx) needs to be in your output file.
#  -If pressure then PS (E3SM) or ps (EAMxx) should be in your output file.  If it is not then
#    the package will use hybrid levels to plot, which may not be accurate compared to observations.
height_cord = "z"  # p = pressure; z = height

# Optional: Maximum y-axis height for profile plots (in meters or mb; depending on vertical coordinate)
max_height_profile = 3000  # Set to desired height in meters or mb, or None for automatic scaling

# Optional: Maximum y-axis height for time-height (in meters or mb; depending on vertical coordinate)
max_height_timeheight = 3000  # Set to desired height in meters or mb, or None for automatic scaling

# linewidth for curves
linewidth = 4

# Optional: Time range for time series plots in days
time_series_time_s = 0  # Starting time for time series, None for default (entire range)
time_series_time_e = 3.25  # Ending time for time series, None for default (entire range)

# Optional: Time range for time-height plots in days
time_height_time_s = 0  # Starting time for time-height plots, None for default (entire range)
time_height_time_e = 3.25  # Ending time for time-height plots, None for default (entire range)

# Do Diurnal Composite Analysis?  Must have at least three days worth of data and each
#  day must have at least 4 output time slices for this analysis to be considered.
do_diurnal_composites = True
diurnal_start_day = 0  # Starting day for diurnal composite stats, None for default (entire range)
diurnal_end_day = 3.0    # Ending day for diurnal composite stats, None for default (entire range)

# Define the colormap for time height contourf plots.  Default is "viridis_r".
time_height_cmap = "viridis_r"

# Optional arguments to define tick size and label size for plots.  Default is 14.
ticksize=14
labelsize=14

# END: OPTIONAL user defined settings
##########################################################
##########################################################

# Call the diagnostics function with user-defined settings
run_diagnostics(
    output_dir,
    general_id,
    datasets,
    profile_time_s,
    profile_time_e,
    do_timeheight,
    height_cord,
    max_height_profile,
    max_height_timeheight,
    linewidth,
    time_series_time_s,
    time_series_time_e,
    time_height_time_s,
    time_height_time_e,
    do_diurnal_composites=do_diurnal_composites,
    diurnal_start_day=diurnal_start_day,
    diurnal_end_day=diurnal_end_day,
    usercmap=time_height_cmap,
    ticksize=ticksize,
    labelsize=labelsize
)

