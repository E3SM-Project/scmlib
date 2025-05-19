from iop_diagnostics import run_diagnostics

##########################################################
# Quick diagnostics package for E3SM Single Column Model (SCM)
#  or doubly-periodic EAMxx (DP-EAMxx).
# NOTE that for DP-EAMxx this program only works on output
#  streams that contain horizontally averaged output.

# Will produce time averaged profile plots, time series plots,
#  and time height plots.
# Finally, will produce .tar file with plots and html viewer.

# This package is currently still in development and thus is
#  considered to be in beta testing mode.  At this point there
#  is limited to no documentation and comes with no warranty.

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?  Provide path.
output_dir = "/global/cfs/cdirs/e3sm/www/bogensch/IOP_diags"

# User-specified general ID for this diagnostic set
general_id = "MAGIC_e3sm"  # Change as needed

######## Begin manage simulation output

# Where are simulation case directories stored?
#   This program assumes that all output is in the run directory for each case.
simulation_dir = "/pscratch/sd/b/bogensch/dp_scream3"

# User-specified list of casenames and corresponding short IDs
casenames = ["e3sm_scm_MAGIC.v2.001a",
             "e3sm_scm_MAGIC.v2.5m.001a"]  # Example casenames

# All cases should end with this appendix for the output stream to be considered
caseappend = ".eam.h0.2013-07-21-19620.nc"

######## End manage simulation output
######## Begin manage LES and observation output

# Directory and file for LES (large eddy simulation) data.  If none, state None
les_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/les_data/SAM_MAGIC.les.e3sm.nc"

# Directory and file for Observation data.  If none, state None
obs_file = None

######## End manage LES and observation output

# short IDs used in legend; be sure to include LES and OBS if added.
short_ids = ["CNTL","dz = 5m","SAM-LES"]

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
time_series_time_e = None  # Ending time for time series, None for default (entire range)

# Optional: Time range for time-height plots in days
time_height_time_s = None  # Starting time for time-height plots, None for default (entire range)
time_height_time_e = None  # Ending time for time-height plots, None for default (entire range)

# Do Diurnal Composite Analysis?  Must have at least three days worth of data and each
#  day must have at least 4 output time slices for this analysis to be considered.
do_diurnal_composites = False
diurnal_start_day = None  # Starting day for diurnal composite stats, None for default (entire range)
diurnal_end_day = None    # Ending day for diurnal composite stats, None for default (entire range)

# Define the colormap for time height contourf plots.  Default is "viridis_r".
time_height_cmap = "viridis_r"

# Optional arguments to define line color and style for profile and time series plots.
#  The number of entries MUST match the number of short_ids for each.  If None is specified
#  then will default to python defaults.
line_colors=None
line_styles=None

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
    simulation_dir,
    casenames,
    les_file,
    obs_file,
    short_ids,
    caseappend,
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
    line_colors=line_colors,
    line_styles=line_styles,
    ticksize=ticksize,
    labelsize=labelsize
)

