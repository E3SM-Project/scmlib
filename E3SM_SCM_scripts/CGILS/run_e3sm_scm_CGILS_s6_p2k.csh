#!/bin/csh

#######################################################################
#######################################################################
#######  Script to run E3SM in SCM for
#######  CGILS_s6_p2k
#######  Cumulus location - Plus 2 K SST
#######
#######  Script Author: P. Bogenschutz (bogenschutz1@llnl.gov)
#######  Forcing provided by: Yi Qin

#######################################################
#######  BEGIN USER DEFINED SETTINGS

  # Set the name of your case here
  setenv casename e3sm_scm_CGILS_s6_p2k

  # Set the case directory here
  setenv casedirectory $PSCRATCH/SCM_runs

  # Directory where code lives
  setenv code_dir $HOME/E3SM_code

  # Code tag name
  setenv code_tag E3SM_codetag

  # Name of machine you are running on (i.e. pm-cpu, anvil, chrysalis, compy, etc)
  setenv machine mach_name

  # Name of project to run on, if submitting to queue
  setenv projectname proj_name

  # Aerosol specification
  # Options include:
  #  1) cons_droplet (sets cloud liquid and ice concentration
  #                   to a constant)
  #  2) prescribed (uses climatologically prescribed aerosol
  #                 concentration)
  setenv init_aero_type prescribed


  # What version of E3SM? (v1, v2, v3, or master)
  #  Select "v1" if you are running with E3SMv1 RELEASE code
  #  Select "v2" if you are running with E3SMv2 RELEASE code
  #  If you want to run "v3" then select "master".
  #    This will work with official release v3 codes or for E3SM master branch.

  setenv e3sm_version master

  # Set the dynamical core
  #   1) Select "Eulerian" ONLY if you are running E3SMv1 release code
  #
  #   2) Select "SE" IF you are running code from recent E3SM master or v2
  setenv dycore SE
  #  WARNING:  EULERIAN DYCORE SCM IS NO LONGER SUPPORTED. You are only safe
  #  to use Eulerian dycore SCM if you are using E3SMv1 release code.  Else,
  #  user be(very)ware

# User enter any needed modules to load or use below
#  EXAMPLE:
#  module load python/2.7.5

####### END USER DEFINED SETTINGS
####### Likely POSSIBLE EXCEPTION (not limited to):
#######  - If the user wants to add addition output, for example, the EAM
#######	   namelist (user_nl_eam) should be modified below to accomodate for this
###########################################################################
###########################################################################
###########################################################################

# Case specific information kept here
  set lat = 17.0 # latitude
  set lon = 211.0 # longitude
  set do_iop_srf_prop = .false. # Use surface fluxes in IOP file?
  set do_scm_relaxation = .false. # Relax case to observations?
  set do_turnoff_swrad = .false. # Turn off SW calculation
  set do_turnoff_lwrad = .false. # Turn off LW calculation
  set do_turnoff_precip = .false. # Turn off precipitation
  set micro_nccons_val = 100.0D6 # cons_droplet value for liquid
  set micro_nicons_val = 0.0001D6 # cons_droplet value for ice
  set startdate = 2003-07-15 # Start date in IOP file
  set start_in_sec = 0 # start time in seconds in IOP file
  set stop_option = ndays
  set stop_n = 100
  set iop_file = CGILS_s6_p2k_iopfile_4scam.nc #IOP file name
# End Case specific stuff here

  # Location of IOP file
  set iop_path = atm/cam/scam/iop

  set presc_aero_path = atm/cam/chem/trop_mam/aero
  # Prescribed aerosol file path and name
  if ($e3sm_version != master) then
    set presc_aero_file = mam4_0.9x1.2_L72_2000clim_c170323.nc
  else
    set presc_aero_file = mam5_0.9x1.2_L80_F2010_c013024.nc
  endif

  set PROJECT=$projectname
  set E3SMROOT=${code_dir}/${code_tag}

  cd $E3SMROOT/cime/scripts

  if ($e3sm_version == v1) then
    set compset = F_SCAM5
    set atm_mod = cam
    set physset = cam5
  else
    # Since v1 the naming convention has changed
    set atm_mod = eam
    set physset = default
    set compset = FSCM
  endif

  if ($e3sm_version == master) then
    set nudge_flag = iop_nudge_tq
  else
    set nudge_flag = scm_relaxation
  endif

  if ($dycore == Eulerian) then
    set grid=T42_T42
  endif

# For the vast majority of cases, initializing from ne4 files is sufficient.
#  However, there are some scenarios where initializing from ne30_ne30 makes more
#  sense to ensure better surface type.  This will make the SCM about 3 time slower.
  if ($dycore == SE) then
    set grid=ne4_ne4
  endif

  set CASEID=$casename

  set CASEDIR=${casedirectory}/$CASEID

  set run_root_dir = $CASEDIR
  set temp_case_scripts_dir = $run_root_dir/case_scripts

  set case_scripts_dir = $run_root_dir/case_scripts
  set case_build_dir   = $run_root_dir/build
  set case_run_dir     = $run_root_dir/run

  set walltime = '00:10:00'

# COSP, set to false unless user really wants it
  setenv do_cosp  false

# Create new case
  ./create_newcase -case $casename --script-root $temp_case_scripts_dir -mach $machine -project $PROJECT -compset $compset -res $grid
  cd $temp_case_scripts_dir

# SCM must run in serial mode
  if ($dycore == Eulerian) then
    ./xmlchange --id MPILIB --val mpi-serial
  endif

  ./xmlchange JOB_WALLCLOCK_TIME=$walltime

# Define executable and run directories
  ./xmlchange --id EXEROOT --val "${case_build_dir}"
  ./xmlchange --id RUNDIR --val "${case_run_dir}"

# Set to debug, only on certain machines
  if ($machine =~ 'pm*') then
    ./xmlchange --id JOB_QUEUE --val 'debug'
  endif

  if ($machine == 'quartz' || $machine == 'syrah') then
    ./xmlchange --id JOB_QUEUE --val 'pdebug'
  endif

# Get local input data directory path
  set input_data_dir = `./xmlquery DIN_LOC_ROOT -value`

# need to use single thread
  set npes = 1
  foreach component ( ATM LND ICE OCN CPL GLC ROF WAV )
    ./xmlchange  NTASKS_$component=$npes,NTHRDS_$component=1
  end

# CAM configure options.  By default set up with settings the same as E3SMv1
  if ($e3sm_version != master) then
    set CAM_CONFIG_OPTS="-phys ${physset} -scam -nlev 72 -clubb_sgs"
  else
    set CAM_CONFIG_OPTS="-phys ${physset} -scam -nlev 80 -clubb_sgs -microphys p3"
  endif

  if ($dycore == Eulerian) then
    set CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS -nospmd -nosmp"
  endif

  if ( $do_cosp == true ) then
    set  CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS -cosp -verbose"
  endif

# This option ONLY to be used for the REPLAY mode
  if ($init_aero_type == none) then
    if ($e3sm_master != master) then
      set CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS -chem linoz_mam4_resus_mom_soag -rain_evap_to_coarse_aero -bc_dep_to_snow_updates"
    else
      set CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS -chem chemuci_linozv3_mam5_vbs -rain_evap_to_coarse_aero -vbs"
    endif
  endif

  if ($init_aero_type == cons_droplet || $init_aero_type == prescribed || $init_aero_type == observed) then
    set CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS -chem none"
  endif

  ./xmlchange CAM_CONFIG_OPTS="$CAM_CONFIG_OPTS"
  set clubb_micro_steps = 8
# If SE dycore is used then we need to change the timestep
# to be consistent with ne30 timestep.  Also change the
# cld_macmic_num_steps to be consistent
  if ($dycore == SE) then
    ./xmlchange ATM_NCPL='48'
    set clubb_micro_steps = 6
  endif

  if ($e3sm_version != v1) then
    ./xmlchange CAM_TARGET=theta-l
  endif

# Set timesteps, long term solution will be to modify compset. This will ensure
#  if a user initializes from a different resolution (i.e. ne30), the time steps
#  will still be consistent with what SCM expects.
if ($e3sm_version != v1) then
cat <<EOF >> user_nl_${atm_mod}
 se_tstep = 1800
 dt_remap_factor = 1
 dt_tracer_factor = 1
EOF
endif

# if we want to turn off SW radiation, then set appropriate namelist settings here
  if ($do_turnoff_swrad == true) then
    set iradsw_in = 0
  else
    set iradsw_in = 1
  endif

# if we want to turn off LW radiation, then set appropriate namelist settings here
  if ($do_turnoff_lwrad == true) then
    set iradlw_in = 0
  else
    set iradlw_in = 1
  endif

# User enter CAM namelist options
#  Add additional output here for example
cat <<EOF >> user_nl_${atm_mod}
 cld_macmic_num_steps = $clubb_micro_steps
 cosp_lite = .true.
 use_gw_front = .false.
 iopfile = '$input_data_dir/$iop_path/$iop_file'
 mfilt = 10000
 nhtfrq = 1
 scm_iop_srf_prop = $do_iop_srf_prop
 $nudge_flag = $do_scm_relaxation
 iradlw = $iradlw_in
 iradsw = $iradsw_in
 precip_off = $do_turnoff_precip
 scmlat = $lat
 scmlon = $lon
EOF

# Shared settings for all versions
cat <<EOF >> user_nl_${atm_mod}
 use_hetfrz_classnuc = .true.
 microp_aero_wsub_scheme = 1
 convproc_do_aer = .true.
 demott_ice_nuc = .true.
 liqcf_fix = .true.
 regen_fix = .true.
 resus_fix = .false.
 mam_amicphys_optaa = 1
 fix_g1_err_ndrop = .true.
 ssalt_tuning = .true.
 use_rad_dt_cosz = .true.
 do_tms = .false.
 n_so4_monolayers_pcage = 8.0D0
 se_ftype = 2
EOF

# Version-specific settings
if ($e3sm_version == v1) then
cat <<EOF >> user_nl_${atm_mod}
 cldfrc_dp1 = 0.045D0
 clubb_ice_deep = 16.e-6
 clubb_ice_sh = 50.e-6
 clubb_liq_deep = 8.e-6
 clubb_liq_sh = 10.e-6
 clubb_C2rt = 1.75D0
 zmconv_c0_lnd = 0.007
 zmconv_c0_ocn = 0.007
 zmconv_dmpdz = -0.7e-3
 zmconv_ke = 1.5E-6
 effgw_oro = 0.25
 seasalt_emis_scale = 0.85
 dust_emis_fact = 2.05D0
 clubb_gamma_coef = 0.32
 clubb_gamma_coefb = 0.32
 clubb_c1b = 1.335
 clubb_C8 = 4.3
 cldfrc2m_rhmaxi = 1.05D0
 clubb_c_K10 = 0.3
 effgw_beres = 0.4
 so4_sz_thresh_icenuc = 0.075e-6
 micro_mg_accre_enhan_fac = 1.5D0
 zmconv_tiedke_add = 0.8D0
 zmconv_cape_cin = 1
 zmconv_mx_bot_lyr_adj = 2
 taubgnd = 2.5D-3
 clubb_C1 = 1.335
 raytau0 = 5.0D0
 prc_coef1 = 30500.0D0
 prc_exp = 3.19D0
 prc_exp1 = -1.2D0
 clubb_C14 = 1.3D0
 rrtmg_temp_fix = .true.
 mg_prc_coeff_fix = .true.
 micro_mg_dcs_tdep = .true.
 ice_sed_ai = 500.0
 sscav_tuning = .true.
EOF

else
# v2 and master share many parameters
cat <<EOF >> user_nl_${atm_mod}
 zmconv_trigdcape_ull = .true.
 effgw_beres = 0.35
 effgw_oro = 0.375
 linoz_psc_T = 197.5
 clubb_c1 = 2.4
 clubb_c11 = 0.70
 clubb_c11b = 0.20
 clubb_c11c = 0.85
 clubb_c14 = 2.5D0
 clubb_c1b = 2.8
 clubb_c1c = 0.75
 clubb_c6rtb = 7.50
 clubb_c6rtc = 0.50
 clubb_c6thlb = 7.50
 clubb_c6thlc = 0.50
 clubb_c8 = 5.2
 clubb_c_k10 = 0.35
 clubb_c_k10h = 0.35
 clubb_gamma_coef = 0.12D0
 clubb_gamma_coefb = 0.28D0
 clubb_gamma_coefc = 1.2
 clubb_mu = 0.0005
 clubb_ice_deep = 14.e-6
 clubb_ice_sh = 50.e-6
 clubb_liq_deep = 8.e-6
 clubb_liq_sh = 10.e-6
 clubb_C2rt = 1.75D0
 clubb_wpxp_l_thresh = 100.0D0
 clubb_use_sgv = .true.
 zmconv_dmpdz = -0.7e-3
 zmconv_c0_lnd = 0.0020
 zmconv_c0_ocn = 0.0020
 zmconv_ke = 5.0E-6
 zmconv_alfa = 0.14D0
 zmconv_tp_fac = 2.0D0
 zmconv_tiedke_add = 0.8D0
 zmconv_cape_cin = 1
 zmconv_mx_bot_lyr_adj = 1
 microp_aero_wsubmin = 0.001D0
 so4_sz_thresh_icenuc = 0.080e-6
 cldfrc_dp1 = 0.018D0
 cldfrc2m_rhmaxi = 1.05D0
 taubgnd = 2.5D-3
 raytau0 = 5.0D0
EOF

if ($e3sm_version == v2) then
cat <<EOF >> user_nl_${atm_mod}
 cld_sed = 1.0D0
 prc_coef1 = 30500.0D0
 prc_exp = 3.19D0
 prc_exp1 = -1.40D0
 rrtmg_temp_fix = .true.
 micro_mg_accre_enhan_fac = 1.75D0
 mg_prc_coeff_fix = .true.
 micro_mg_berg_eff_factor = 0.7D0
 micro_mg_dcs_tdep = .true.
 ice_sed_ai = 500.0
 gw_convect_hcf = 12.5
 dust_emis_fact = 1.50D0
 clubb_tk1 = 253.15D0
 sscav_tuning = .true.
 seasalt_emis_scale = 0.6D0
EOF

else if ($e3sm_version == master) then
cat <<EOF >> user_nl_${atm_mod}
 zmconv_ke = 2.5E-6
 resus_fix = .true.
 gw_convect_hcf = 10.0
 dust_emis_fact = 13.8D0
 clubb_tk1 = 268.15D0
 sscav_tuning = .false.
 seasalt_emis_scale = 0.55D0
 sol_factb_interstitial = 0.1D0
 sol_facti_cloud_borne = 1.0D0
 sol_factic_interstitial = 0.4D0
EOF
endif

endif

# if constant droplet was selected then modify name list to reflect this
if ($init_aero_type == cons_droplet && $e3sm_version != master) then

cat <<EOF >> user_nl_${atm_mod}
  micro_do_nccons = .true.
  micro_do_nicons = .true.
  micro_nccons = $micro_nccons_val
  micro_nicons = $micro_nicons_val
EOF

endif

# if running v3 (p3) only constant droplet is supported (not ice)
if ($init_aero_type == cons_droplet && $e3sm_version == master) then

cat <<EOF >> user_nl_${atm_mod}
  micro_aerosolactivation = .false.
  micro_nccons = $micro_nccons_val
EOF

endif

# if prescribed or observed aerosols set then need to put in settings for prescribed aerosol model
if ($init_aero_type == cons_droplet || $init_aero_type == prescribed ||$init_aero_type == observed) then

cat <<EOF >> user_nl_${atm_mod}
  use_hetfrz_classnuc = .false.
  aerodep_flx_type = 'CYCLICAL'
  aerodep_flx_datapath = '$input_data_dir/$presc_aero_path'
  aerodep_flx_file = '$presc_aero_file'
  aerodep_flx_cycle_yr = 01
  prescribed_aero_type = 'CYCLICAL'
  prescribed_aero_datapath='$input_data_dir/$presc_aero_path'
  prescribed_aero_file='$presc_aero_file'
  prescribed_aero_cycle_yr = 01
EOF

endif

# if observed aerosols then set flag
if ($init_aero_type == observed) then

cat <<EOF >> user_nl_${atm_mod}
  scm_observed_aero = .true.
EOF

endif

# avoid the monthly cice file from writing as this
#   appears to be currently broken for SCM
cat <<EOF >> user_nl_cice
  histfreq='y','x','x','x','x'
EOF

# Set correct version of CLM or ELM (depending on version of code base)
if ($e3sm_version == v1) then
  set CLM_CONFIG_OPTS="-phys clm4_5"
  ./xmlchange CLM_CONFIG_OPTS="$CLM_CONFIG_OPTS"
else
  set ELM_CONFIG_OPTS="-phys elm"
  ./xmlchange ELM_CONFIG_OPTS="$ELM_CONFIG_OPTS"
endif

# Modify the run start and duration parameters for the desired case
  ./xmlchange RUN_STARTDATE="$startdate",START_TOD="$start_in_sec",STOP_OPTION="$stop_option",STOP_N="$stop_n"

# Modify the latitude and longitude for the particular case
  ./xmlchange PTS_MODE="TRUE",PTS_LAT="$lat",PTS_LON="$lon"
  ./xmlchange MASK_GRID="USGS"

  ./xmlchange SSTICE_DATA_FILENAME="$input_data_dir/ocn/docn7/SSTDATA/sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s6_p2k.nc"
  ./xmlchange SSTICE_YEAR_ALIGN=2003
  ./xmlchange SSTICE_YEAR_START=2003
  ./xmlchange SSTICE_YEAR_END=2004

  ./case.setup

# Don't want to write restarts as this appears to be broken for
#  CICE model in SCM.  For now set this to a high value to avoid
  ./xmlchange PIO_TYPENAME="netcdf"
  ./xmlchange REST_N=30000

# Modify some parameters for CICE to make it SCM compatible
  ./xmlchange CICE_AUTO_DECOMP="FALSE"
  ./xmlchange CICE_DECOMPTYPE="blkrobin"
  ./xmlchange --id CICE_BLCKX --val 1
  ./xmlchange --id CICE_BLCKY --val 1
  ./xmlchange --id CICE_MXBLCKS --val 1
  ./xmlchange CICE_CONFIG_OPTS="-nodecomp -maxblocks 1 -nx 1 -ny 1"

# Build the case
  ./case.build

  ./case.submit

  exit
