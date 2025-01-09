from iop_diagnostics import run_diagnostics

##########################################################
# Quick diagnostics package for E3SM Single Column Model (SCM)
#  or doubly-periodic EAMxx (DP-EAMxx).
# NOTE that for DP-EAMxx this program only works on output
#  streams that contain horizontally averaged output.

# Will produce time averaged profile plots, time series plots,
#  and time height plots.
# Finally, will produce .tar file with plots and html viewer.

# This is a work in progress that will be routinely updated.
# Upcoming features: ability to plot against ARM observations
#  and LES!

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?  Provide path.
output_dir = "dpxx_quickdiags"

# User-specified general ID for this diagnostic set
general_id = "MAGIC_development"  # Change as needed

# Where are simulation case directories stored?
#   This program assumes that all output is in the run directory for each case.
base_dir = "/pscratch/sd/b/bogensch/dp_screamxx_conv/"

# User-specified list of casenames and corresponding short IDs
casenames = ["scream_dpxx_MAGIC.cntl.001a",
             "scream_dpxx_MAGIC.conv.001a",
             "scream_dpxx_MAGIC.conv.001b",
	     "SAM_MAGIC.les.001a"]  # Example casenames
# short IDs used in legend
short_ids = ["CNTL","All Mods","Rfrac Only","SAM-LES"]

# All cases should end with this appendix for the output stream to be considered
caseappend = ".horiz_avg.AVERAGE.nmins_x5.2013-07-21-19620.nc"

# Define start and end times for averaging for profiles as numerical values in days
profile_time_s = [0.0,1.0]  # Starting times for averaging
profile_time_e = [3.0,2.0]  # Ending times for averaging (put "end" to average to end of simulation)

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

# END: OPTIONAL user defined settings
##########################################################
##########################################################

# Call the diagnostics function with user-defined settings
run_diagnostics(
    output_dir,
    general_id,
    base_dir,
    casenames,
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
    time_height_time_e
)

