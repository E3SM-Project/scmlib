#!/bin/csh -fe

#######################################################################
#######################################################################
#######  Script to run SCREAMv1 in doubly periodic (DP) mode (DP-EAMxx)
#######  RACORO
#######  Continental liquid boundary layer clouds at ARM SGP site
#######
#######  Script Author: P. Bogenschutz (bogenschutz1@llnl.gov)
#######  Forcing provided by: Shuaiqi Tang and Shaocheng Xie

#######  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#######  WARNING READ FIRST BEFORE RUNNING:
#######
#######  October 22, 2024 Update:
#######  Beta testing for the C++/Kokkos version of DP-SCREAM (commonly referred
#######  to as DPxx) has been going well and the code base has been stable for a
#######	 while now (i.e. no new issues found in over a month from a large user base).
#######	 Please feel free to use DPxx if you wish. Please send Peter Bogenschutz
#######	 (bogenschutz1@llnl.gov) an email if you do so that I can add you to the
#######	 DPxx beta testing mailing list in case there are any important updates to
#######	 the code or scripts. We anticipate that DPxx will become the official and
#######	 validated version of DP-SCREAM in a few months. At this time DP-SCREAMv0
#######	 (Fortran version) will no longer be supported. Thus, the time to transition is upon us.
#######
#######  IMPORTANT:
#######    - PLEASE make sure your SCREAM master is dated September 30, 2024 or after for most cases.
#######    - If running RCE case you MUST use master dated November 21, 2024 or after as there was a
#######      major bug fix related to that compset prior to that date.
#######
#######  Exciting news:
#######    - It is now possible to get horizontally averaged output in DPxx.  Very useful to reduce
#######      the amount of data written and post-processing times.  For guidance on how to produce this
#######      please see the script in the scmlib repo directory (your master should be current):
#######      DPxx_SCREAM_SCRIPTS/regrid_utilities/generate_dpxx_horiz_avg_weights.py
#######
#######  Known issues (Nov 21, 2024):
#######    - None at the moment
#######  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#######################################################
#######  BEGIN USER DEFINED SETTINGS
####### NOTE: beyond this section you will need to configure your
#######  ouput yaml file(s).  Please do a search for "yaml" and you will
#######  be brought to the correct location.
####### See the example yaml file in the DPxx_SCREAM_SCRIPTS/yaml_file_example
#######  of the scmlib repo to get you started.

  # Set the name of your case here
  setenv casename scream_dpxx_RACORO

  # Set the case directory here
  setenv casedirectory /pscratch/sd/b/bogensch/dp_screamxx

  # Directory where code lives
  setenv code_dir /pscratch/sd/b/bogensch/dp_scream/codes

  # Code tag name
  setenv code_tag SCREAM_master

  # Name of machine you are running on (i.e. pm-cpu, anvil, etc)
  setenv machine pm-cpu

  # Compiler (pm-cpu should use "gnu"; pm-gpu should use "gnugpu"; LC should use "intel";
  #           frontier should use "crayclang-scream")
  #   more machine compiler defaults will be added as they are tested/validated.
  setenv compiler gnu

  # Name of project to run on, if submitting to queue
  setenv projectname e3sm


  # Set to debug queue?
  # - Some cases are small enough to run on debug queues
  # - Setting to true only supported for NERSC and Livermore Computing,
  #   else user will need to modify script to submit to debug queue
  setenv debug_queue false

  # Set number of processors to use, should be less than or equal
  #   to the total number of elements in your domain.  Note that if you are running
  #   on pm-gpu you will want to set this to either "4" or "8" if running the standard
  #   domain size and resolution (RCE excluded).
  set num_procs = 96

  # set walltime
  set walltime = '05:00:00'

  ## SET DOMAIN SIZE AND DYNAMICS RESOLUTION:
  # - Note that these scripts are set to run with dx=dy=3.33 km
  # which is the default SCREAM resolution.

  # To estimate dx (analogous for dy):
  # dx = domain_size_x / (num_ne_x * 3)
  # (there are 3x3 unique dynamics columns per element, hence the "3" factor)

  # Set number of elements in the x&y directions
  set num_ne_x = 10
  set num_ne_y = 10

  # Set domain length [m] in x&y direction
  set domain_size_x = 100000
  set domain_size_y = 100000

  # BELOW SETS RESOLUTION DEPENDENT SETTINGS
  # (Note that all default values below are appropriate for dx=dy=3.33 km and do not
  #  need to be modified if you are not changing the resolution)

  # SET MODEL TIME STEPS
  #  -NOTE that if you change the model resolution,
  #  it is likely the physics and dynamics time steps will need to be adjusted.
  #  See below for guidance on how to adjust both.

  # model/physics time step [s]:
  #  As a rule, a factor of 2 increase in resolution should equate to a factor of 2
  #  decrease of the model/physics step.  This needs to be an integer number.
  set model_dtime = 100

  # dynamics time step [s]:
  #  should divide evenly into model_dtime.  As a general rule of thumb, divide
  #   model_dtime by 12 to get your dynamics time step.
  set dyn_dtime = 8.3333333333333

  # SET SECOND ORDER VISCOSITY NEAR MODEL TOP
  #  NOTE that if you decrease resolution you will also need to reduce
  #  the value of "nu_top" (second-order viscosity applied only near model top).
  #  Rule of thumb is that a factor of 2 increase in resolution should equate to a
  #  factor of 2 decrease for this value

  # second order visocosity near model top [m2/s]
  set nu_top_dyn = 1e4

####### END (mandatory) USER DEFINED SETTINGS, but see above about output
###########################################################################
###########################################################################
###########################################################################

# Case specific information kept here
  set lat = 36.6 # latitude
  set lon = 262.5 # longitude
  set do_iop_srf_prop = true # Use surface fluxes in IOP file?
  set do_iop_nudge_tq = false # Relax T&Q to observations?
  set do_iop_nudge_uv = true # Relax U&V to observations?
  set do_iop_nudge_coriolis = false # Nudge to geostrophic winds?
  set do_iop_subsidence = false # compute LS vertical transport?
  set startdate = 2009-05-01 # Start date in IOP file
  set start_in_sec = 84585 # start time in seconds in IOP file
  set stop_option = ndays
  set stop_n = 26
  set iop_file = RACORO_iopfile_4scam.nc #IOP file name
  set do_turnoff_swrad = false # Turn off SW calculation (if false, keep false)
# End Case specific stuff here

  # Location of IOP file
  set iop_path = atm/cam/scam/iop

  set PROJECT=$projectname
  set E3SMROOT=${code_dir}/${code_tag}

  cd $E3SMROOT/cime/scripts

  set compset=FIOP-SCREAMv1-DP

  # Note that in DP-SCREAM the grid is set ONLY to initialize
  #  the model from these files
  set grid=ne30pg2_ne30pg2

  set CASEID=$casename

  set CASEDIR=${casedirectory}/$CASEID

  set run_root_dir = $CASEDIR
  set temp_case_scripts_dir = $run_root_dir/case_scripts

  set case_scripts_dir = $run_root_dir/case_scripts
  set case_build_dir   = $run_root_dir/build
  set case_run_dir     = $run_root_dir/run

# Create new case
  ./create_newcase -case $casename --script-root $temp_case_scripts_dir -mach $machine -project $PROJECT -compset $compset -res $grid --compiler $compiler
  cd $temp_case_scripts_dir

  ./xmlchange JOB_WALLCLOCK_TIME=$walltime
  
 ./xmlchange SCREAM_CMAKE_OPTIONS="`./xmlquery -value SCREAM_CMAKE_OPTIONS | sed 's/SCREAM_NUM_VERTICAL_LEV [0-9][0-9]*/SCREAM_NUM_VERTICAL_LEV 128/'`"  

# Define executable and run directories
  ./xmlchange --id EXEROOT --val "${case_build_dir}"
  ./xmlchange --id RUNDIR --val "${case_run_dir}"

# Set to debug, only on certain machines
  if ($debug_queue == 'true') then
    if ($machine =~ 'pm*') then
      ./xmlchange --id JOB_QUEUE --val 'debug'
    endif

    if ($machine == 'quartz' || $machine == 'syrah' || $machine == 'ruby') then
      ./xmlchange --id JOB_QUEUE --val 'pdebug'
    endif
  endif

# need to use single thread
  set npes = $num_procs
  foreach component ( ATM LND ICE OCN CPL GLC ROF WAV )
    ./xmlchange  NTASKS_$component=$npes,NTHRDS_$component=1,ROOTPE_$component=0
  end

# Compute maximum allowable number for processes (number of elements)
  set dyn_pes_nxny = `expr $num_ne_x \* $num_ne_y`

  set ELM_CONFIG_OPTS="-phys elm"
  ./xmlchange ELM_CONFIG_OPTS="$ELM_CONFIG_OPTS"

# Modify the run start and duration parameters for the desired case
  ./xmlchange RUN_STARTDATE="$startdate",START_TOD="$start_in_sec",STOP_OPTION="$stop_option",STOP_N="$stop_n"

# Compute number of columns needed for component model initialization
  set comp_mods_nx = `expr $num_ne_x \* $num_ne_y \* 4`

# Modify the latitude and longitude for the particular case
  ./xmlchange PTS_MULTCOLS_MODE="TRUE",PTS_MODE="TRUE",PTS_LAT="$lat",PTS_LON="$lon"
  ./xmlchange MASK_GRID="USGS",PTS_NX="${comp_mods_nx}",PTS_NY=1
  ./xmlchange ICE_NX="${comp_mods_nx}",ICE_NY=1
  ./xmlchange CALENDAR="GREGORIAN"


# Set model timesteps

  @ ncpl = 86400 / $model_dtime
  ./xmlchange ATM_NCPL=$ncpl
  ./xmlchange ELM_NAMELIST_OPTS="dtime=$model_dtime"
  
  ./case.setup

# Get local input data directory path
  set input_data_dir = `./xmlquery DIN_LOC_ROOT -value`


# Set relevant namelist modifications  
  ./atmchange se_ne_x=$num_ne_x
  ./atmchange se_ne_y=$num_ne_y
  ./atmchange se_lx=$domain_size_x
  ./atmchange se_ly=$domain_size_y
  ./atmchange dt_remap_factor=2
  ./atmchange cubed_sphere_map=2
  ./atmchange target_latitude=$lat
  ./atmchange target_longitude=$lon
  ./atmchange iop_file=$input_data_dir/$iop_path/$iop_file
  ./atmchange nu=0.216784
  ./atmchange nu_top=$nu_top_dyn
  ./atmchange se_ftype=2
  ./atmchange se_tstep=$dyn_dtime
  ./atmchange rad_frequency=3
  ./atmchange iop_srf_prop=$do_iop_srf_prop
  ./atmchange iop_dosubsidence=$do_iop_subsidence
  ./atmchange iop_nudge_uv=$do_iop_nudge_uv
  ./atmchange iop_nudge_tq=$do_iop_nudge_tq
  ./atmchange iop_coriolis=$do_iop_nudge_coriolis

# Allow for the computation of tendencies for output purposes
  ./atmchange physics::mac_aero_mic::shoc::compute_tendencies=T_mid,qv
  ./atmchange physics::mac_aero_mic::p3::compute_tendencies=T_mid,qv
  ./atmchange physics::rrtmgp::compute_tendencies=T_mid
  ./atmchange homme::compute_tendencies=T_mid,qv
  
 # configure yaml output
 # See the example yaml file in the DPxx_SCREAM_SCRIPTS/yaml_file_example
 # Note that you can have as many output streams (yaml files) as you want!
 # Here we just have one, but see commented lines to show how to add a second and third output stream
 #   (you would want to do this if you also wanted daily or timestep output for example).
cp /global/homes/b/bogensch/dp_scream_scripts_xx/dpxx_outputfiles/scream_hourly_avg_output.yaml .
#cp /global/homes/b/bogensch/dp_scream_scripts_xx/dpxx_outputfiles/second_output_stream.yaml .
#cp /global/homes/b/bogensch/dp_scream_scripts_xx/dpxx_outputfiles/third_output_stream.yaml .
./atmchange output_yaml_files="./scream_hourly_avg_output.yaml"
#./atmchange output_yaml_files+="./second_output_stream.yaml"
#./atmchange output_yaml_files+="./third_output_stream.yaml"

# avoid the monthly cice file from writing as this
#   appears to be currently broken for SCM
cat <<EOF >> user_nl_cice
  histfreq='y','x','x','x','x'
EOF

# Turn on UofA surface flux scheme
cat <<EOF>> user_nl_cpl
  ocn_surface_flux_scheme = 2
EOF

if ($do_turnoff_swrad == 'true') then
  set solar_angle = 180 # turns off incoming solar radiation
else
  set solar_angle = -1 # Interactive SW radiation
endif

# Note that this call will be disabled for RCE
cat <<EOF>> user_nl_cpl
  constant_zenith_deg = $solar_angle
EOF

  ./case.setup

# Write restart files at the end of model simulation
  ./xmlchange PIO_TYPENAME="pnetcdf"

# Build the case
  ./case.build

# Submit the case
  ./case.submit

  exit
