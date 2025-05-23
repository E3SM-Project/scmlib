#!/bin/csh -fe

#  GENERATE DP-SCREAM scripts for each particular case
#  Uses a pre-defined template 

# Who to set these scripts up for?
#  - for general use select: general

#  - for specific user needs select: user
#    - if select user go to bottom of script and fill in deserired data paths etc. so that
#      that the user need not edit all scripts if they planning on running several.

# Time step things to modify:
# se_nsplit, ATM_NCPL, CAM_NAMELIST_OPTS, ELM_NAMELIST_OPTS

# For runs, probably want to have more frequent averaged output for BL cases

setenv setupfor pm

# helpful notes
# path to prescribed aerosol file = atm/cam/chem/presc_aero
# edison /project/projectdirs/e3sm/inputdata

################################
# MAGIC
################################

set casename = MAGIC
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stratocumulus to Cumulus Transition"/ $outfile
sed -i s/CASElat/28/ $outfile
sed -i s/CASElon/225/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2013-07-21/ $outfile
sed -i s/CASEstartinsec/19620/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/78/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Xue Zheng"/ $outfile
sed -i s/CASESSTdata/"SCM_MAGIC_15A_sst_v0.3_2013-07-20-13UTC.nc"/ $outfile
sed -i s/CASESSTyearalign/2013/ $outfile
sed -i s/CASESSTyearstart/2013/ $outfile
sed -i s/CASESSTyearend/2014/ $outfile

################################
# COMBLE
################################

set casename = COMBLE
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Cold-Air Outbreaks in the Marine Boundary Layer Experiment"/ $outfile
sed -i s/CASElat/74.5/ $outfile
sed -i s/CASElon/9.9/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEangel/180.0/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2020-03-12/ $outfile
sed -i s/CASEstartinsec/79200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Xue Zheng and Meng Zheng"/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c101029_COMBLE.nc"/ $outfile
sed -i s/CASESSTyearalign/2020/ $outfile
sed -i s/CASESSTyearstart/2020/ $outfile
sed -i s/CASESSTyearend/2021/ $outfile

################################
# CASS
################################

set casename = CASS
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Continental Active Surface-forced Shallow-cumulus (CASS)"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2000-07-24/ $outfile
sed -i s/CASEstartinsec/43200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/14/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Yunyan Zhang"/ $outfile

################################
# LAFE
################################

set casename = LAFE
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"LAFE - Clear Convective Boundary Layer at SGP"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2017-08-23/ $outfile
sed -i s/CASEstartinsec/41400/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/15/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Yunyan Zhang"/ $outfile

################################
# GABLS
################################

set casename = GABLS
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stable boundary layer"/ $outfile
sed -i s/CASElat/73.0/ $outfile
sed -i s/CASElon/180.0/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1999-07-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/9/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# DYCOMSRF01
################################

set casename = DYCOMSrf01
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Non-precipitating marine stratocumulus"/ $outfile
sed -i s/CASElat/31.5/ $outfile
sed -i s/CASElon/238.500/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEangel/180.0/ $outfile
sed -i s/CASEstartdate/1999-07-10/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/6/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# DYCOMSRF02
################################

set casename = DYCOMSrf02
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Drizzling marine stratocumulus"/ $outfile
sed -i s/AEROTYPE/observed/ $outfile
sed -i s/CASElat/31.5/ $outfile
sed -i s/CASElon/238.500/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEstartdate/1999-07-11/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/6/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/true/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASEtqlow/650/ $outfile
sed -i s/CASEtqhigh/0/ $outfile
sed -i s/CASEtqtscale/3600/ $outfile

################################
# GATE Idealized
################################

set casename = GATEIDEAL
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Idealized version of GATE"/ $outfile
sed -i s/CASElat/9.00/ $outfile
sed -i s/CASElon/336.0/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/1974-08-30/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/1/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/01:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c101029_GATEIDEAL.nc"/ $outfile
sed -i s/CASESSTyearalign/1974/ $outfile
sed -i s/CASESSTyearstart/1974/ $outfile
sed -i s/CASESSTyearend/1975/ $outfile

################################
# GATE
################################

set casename = GATEIII
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Maritime deep convection"/ $outfile
sed -i s/CASElat/9.00/ $outfile
sed -i s/CASElon/336.0/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/1974-08-30/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/04:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile

################################
# ARM95
################################

set casename = ARM95
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Deep convection over ARM SGP site"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1995-07-18/ $outfile
sed -i s/CASEstartinsec/19800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/17/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile

################################
# ARM97 
################################

set casename = ARM97
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Deep convection over ARM SGP site"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1997-06-19/ $outfile
sed -i s/CASEstartinsec/84585/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile

################################
# MC3E
################################

set casename = MC3E
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mid-latitude Continental Convective Clouds Experiment"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2011-04-22/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/45/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# AEROSOLINDIRECT
################################

set casename = AEROSOLINDIRECT
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Study of Aerosol Indirect Effects in China"/ $outfile
sed -i s/CASElat/32.55/ $outfile
sed -i s/CASElon/116.78/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2008-11-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/96/ $outfile
sed -i s/CASEnex/10/ $outfile
sed -i s/CASEney/10/ $outfile
sed -i s/CASElex/100000/ $outfile
sed -i s/CASEley/100000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# ISDAC
################################

set casename = ISDAC
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Indirect and semi-direct aerosol campaign"/ $outfile
sed -i s/CASElat/71.3/ $outfile
sed -i s/CASElon/156.4/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2008-04-01/ $outfile
sed -i s/CASEstartinsec/10800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/96/ $outfile
sed -i s/CASEnex/10/ $outfile
sed -i s/CASEney/10/ $outfile
sed -i s/CASElex/100000/ $outfile
sed -i s/CASEley/100000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# ISDAC
################################

set casename = RACORO
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Continental liquid boundary layer clouds at ARM SGP site"/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2009-05-01/ $outfile
sed -i s/CASEstartinsec/84585/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/96/ $outfile
sed -i s/CASEnex/10/ $outfile
sed -i s/CASEney/10/ $outfile
sed -i s/CASElex/100000/ $outfile
sed -i s/CASEley/100000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# SPARTICUS
################################

set casename = SPARTICUS
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Small particles in cirrus clouds"/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2010-04-01/ $outfile
sed -i s/CASEstartinsec/3599/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/96/ $outfile
sed -i s/CASEnex/10/ $outfile
sed -i s/CASEney/10/ $outfile
sed -i s/CASElex/100000/ $outfile
sed -i s/CASEley/100000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# SGP Continuous (LONG)
################################

set casename = SGP_continuous
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Continuous forcing (2004-2015) over ARM SGP site"/ $outfile
sed -i s/CASElat/36.61/ $outfile
sed -i s/CASElon/262.51/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASELONGstartdate/2004-01-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASELONGstopoption/nyears/ $outfile
sed -i s/CASELONGstopn/11/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/LENGTHNOTE2/"Possible range from Jan 2004 to Dec. 2015"/ $outfile
sed -i s/LENGTHNOTE/NOTE:/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# SGP broken cases (LONG)
################################

set casename = SGP
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASELONGNAME/SGP0003/ $outfile
sed -i s/THECASEDESCRIPTION/"Forcing from ARM SGP site"/ $outfile
sed -i s/CASElat/36.61/ $outfile
sed -i s/CASElon/262.51/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASELONGstartdate/2000-03-01/ $outfile
sed -i s/CASEstartinsec/63003/ $outfile
sed -i s/CASELONGstopoption/ndays/ $outfile
sed -i s/CASELONGstopn/20/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/LENGTHNOTE2/"This script is set up to run with the SGP0003_iopfile_4scam.nc (March, 2000) forcingfile\n  # Other time periods exist (see E3SM SCM page) "/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i '/SGP_iopfile_4scam.nc/d' $outfile

################################
# DARWIN broken cases
################################

set casename = DARWIN
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASELONGNAME/DARWIN_0405_p1/ $outfile
sed -i s/THECASEDESCRIPTION/"Forcing from Darwin site"/ $outfile
sed -i s/CASElat/-12.425/ $outfile
sed -i s/CASElon/130.891/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASELONGstartdate/2004-11-03/ $outfile
sed -i s/CASEstartinsec/43200/ $outfile
sed -i s/CASELONGstopoption/ndays/ $outfile
sed -i s/CASELONGstopn/5/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/LENGTHNOTE2/"This script is set up to run with the DARWIN_0405_p1_iopfile_4scam.nc (April, 2005) forcingfile\n  # Other time periods exist (see E3SM SCM page) "/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i '/DARWIN_iopfile_4scam.nc/d' $outfile

################################
# GOAMAZON (LONG)
################################

set casename = GOAMAZON
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"ARM's Green Ocean Amazon"/ $outfile
sed -i s/CASElat/-3.15/ $outfile
sed -i s/CASElon/300.01/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASELONGstartdate/2014-01-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASELONGstopoption/nmonths/ $outfile
sed -i s/CASELONGstopn/23/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/LENGTHNOTE2/"Possible range from Jan. 2014 to Nov. 2015"/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/LENGTHNOTE/NOTE:/ $outfile

################################
# GOAMAZON (single pulse)
################################

set casename = GOAMAZON_singlepulse
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Transition from shallow cumulus to deep cumulus (single pulse)"/ $outfile
sed -i s/CASElat/-3.2/ $outfile
sed -i s/CASElon/299.4/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2014-10-05/ $outfile
sed -i s/CASEstartinsec/43200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Yang Tian (Tian and Zhang 2025)"/ $outfile

################################
# GOAMAZON (double pulse)
################################

set casename = GOAMAZON_doublepulse
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Transition from shallow cumulus to deep cumulus (double pulse)"/ $outfile
sed -i s/CASElat/-3.2/ $outfile
sed -i s/CASElon/299.4/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2015-08-26/ $outfile
sed -i s/CASEstartinsec/43200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Yang Tian (Tian and Zhang 2025)"/ $outfile

################################
# DYNAMO_northsounding
################################

set casename = DYNAMO_northsounding
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation North Sounding"/ $outfile
sed -i s/CASElat/3.0/ $outfile
sed -i s/CASElon/76.5/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# DYNAMO_revelle
################################

set casename = DYNAMO_revelle
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation Revelle"/ $outfile
sed -i s/CASElat/3.0/ $outfile
sed -i s/CASElon/76.5/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# DYNAMO_amie
################################

set casename = DYNAMO_amie
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation AMIE"/ $outfile
sed -i s/CASElat/-0.63/ $outfile
sed -i s/CASElon/73.1/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# ARM Shallow convection
################################

set casename = ARM_shallow
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"ARM GCSS shallow convection"/ $outfile
sed -i s/CASElat/36.605/ $outfile
sed -i s/CASElon/262.515/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1997-06-21/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/14/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# BOMEX
################################

set casename = BOMEX
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Non-precipitating trade-wind cumulus convection"/ $outfile
sed -i s/CASElat/15.0/ $outfile
sed -i s/CASElon/300.0/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1969-06-25/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/6/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# ATEX
################################

set casename = ATEX
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Cumulus under stratocumulus"/ $outfile
sed -i s/CASElat/15.0/ $outfile
sed -i s/CASElon/325.0/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1969-02-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/8/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# RICO
################################

set casename = RICO
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Precipitating trade-wind cumulus convection"/ $outfile
sed -i s/CASElat/17.97/ $outfile
sed -i s/CASElon/298.54/ $outfile
sed -i s/CASEswoff/true/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2004-12-16/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c101029_RICO.nc"/ $outfile
sed -i s/CASESSTyearalign/2004/ $outfile
sed -i s/CASESSTyearstart/2004/ $outfile
sed -i s/CASESSTyearend/2005/ $outfile

################################
# LBA
################################

set casename = LBA
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"LBA Transition from shallow cumulus to deep convection"/ $outfile
sed -i s/CASElat/3.0/ $outfile
sed -i s/CASElon/300.0/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1999-02-23/ $outfile
sed -i s/CASEstartinsec/41400/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/6/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/192/ $outfile
sed -i s/CASEnex/15/ $outfile
sed -i s/CASEney/15/ $outfile
sed -i s/CASElex/150000/ $outfile
sed -i s/CASEley/150000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile

################################
# TOGA
################################

set casename = TOGAII
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"TOGA-COARE deep convection"/ $outfile
sed -i s/CASElat/-2.10/ $outfile
sed -i s/CASElon/154.69/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/1992-12-18/ $outfile
sed -i s/CASEstartinsec/64800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile

################################
# TWP06
################################

set casename = TWP06
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"TWP-ICE deep convection in the warm pool"/ $outfile
sed -i s/CASElat/-12.43/ $outfile
sed -i s/CASElon/130.89/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2006-01-17/ $outfile
sed -i s/CASEstartinsec/10800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/true/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile

################################
# MPACEB
################################

set casename = MPACEB
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mixed phase Arctic clouds subset"/ $outfile
sed -i s/CASElat/71.75/ $outfile
sed -i s/CASElon/209.0/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2004-10-09/ $outfile
sed -i s/CASEstartinsec/61200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# MPACE full
################################

set casename = MPACE
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mixed phase Arctic clouds Full IOP"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/70.5/ $outfile
sed -i s/CASElon/206.0/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASErelax/false/ $outfile
sed -i s/CASEnccons/50.0D6/ $outfile
sed -i s/CASEnicons/0.00016D6/ $outfile
sed -i s/CASEstartdate/2004-10-05/ $outfile
sed -i s/CASEstartinsec/7200/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/384/ $outfile
sed -i s/CASEstopn/17/ $outfile
sed -i s/CASEnex/20/ $outfile
sed -i s/CASEney/20/ $outfile
sed -i s/CASElex/200000/ $outfile
sed -i s/CASEley/200000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-24/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile

################################
# RCE
################################

set casename = RCE
set outfile = run_dpxx_scream_$casename.csh 
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/{$casename}"_300K"/ $outfile
sed -i s/THECASEDESCRIPTION/"Radiative Convective Equilibrium (RCEMIP1 configuration; Wing et al. 2018)"/ $outfile
sed -i s/RCEMSG/"Can run with SSTs set to 295, 300 (default), or 305 K."/ $outfile
sed -i s/SSTMSG/"To change, modify the IOP file name and sst_val accordingly (in case specific settings)."/ $outfile
sed -i s/SST2MSG/"It is possible to run with other SST values, but will take longer for simulation to equilibrate."/ $outfile
sed -i s/CASElat/0.0/ $outfile
sed -i s/CASElon/0.0/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2000-01-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/512/ $outfile
sed -i s/CASEnex/50/ $outfile
sed -i s/CASEney/50/ $outfile
sed -i s/CASElex/500000/ $outfile
sed -i s/CASEley/500000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/false/ $outfile
sed -i s/CASEdosub/false/ $outfile
sed -i s/CASEwalltime/16:00:00/ $outfile
sed -i s/FIOP-SCREAMv1-DP/FRCE-SCREAMv1-DP/ $outfile
sed -i s/CASEsstaqua/"sst_val"/ $outfile
sed -i s/CASEsstval/300/ $outfile
sed -i '/ELM_CONFIG_OPTS/d' $outfile
sed -i '/ELM_NAMELIST_OPTS/d' $outfile
sed -i '/CICE_CONFIG_OPTS/d' $outfile
sed -i '/CALENDAR/d' $outfile
sed -i '/constant_zenith_deg/d' $outfile

################################
# CGILS S12 (stratus) CNTL
################################

set casename = CGILS_s12_cntl
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stratus location - control"/ $outfile
sed -i s/CASElat/35.0/ $outfile
sed -i s/CASElon/235.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s12_cntl.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# CGILS S12 (stratus) P2K
################################

set casename = CGILS_s12_p2k
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stratus location - Plus 2 K SST"/ $outfile
sed -i s/CASElat/35.0/ $outfile
sed -i s/CASElon/235.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s12_p2k.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# CGILS S11 (stratocumulus) CNTL
################################

set casename = CGILS_s11_cntl
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stratocumulus location - control"/ $outfile
sed -i s/CASElat/32.0/ $outfile
sed -i s/CASElon/231.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s11_cntl.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# CGILS S11 (stratocumulus) P2K
################################

set casename = CGILS_s11_p2k
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Stratocumulus location - Plus 2 K SST"/ $outfile
sed -i s/CASElat/32.0/ $outfile
sed -i s/CASElon/231.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s11_p2k.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# CGILS S6 (cumulus) CNTL
################################

set casename = CGILS_s6_cntl
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Cumulus location - control"/ $outfile
sed -i s/CASElat/17.0/ $outfile
sed -i s/CASElon/211.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s6_cntl.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# CGILS S6 (cumulus) P2K
################################

set casename = CGILS_s6_p2k
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Cumulus location - Plus 2 K SST"/ $outfile
sed -i s/CASElat/17.0/ $outfile
sed -i s/CASElon/211.0/ $outfile
sed -i s/CASEswoff/false/ $outfile
sed -i s/CASEsrfprop/false/ $outfile
sed -i s/CASEstartdate/2003-07-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEdebug/false/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEstopn/10/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/05:00:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/CASESSTdata/"sst_HadOIBl_bc_1x1_clim_c011425_CGILS_s6_p2k.nc"/ $outfile
sed -i s/CASESSTyearalign/2003/ $outfile
sed -i s/CASESSTyearstart/2003/ $outfile
sed -i s/CASESSTyearend/2004/ $outfile
sed -i s/FORCINGPROVIDER/"Yi Qin"/ $outfile

################################
# EPCAPE 2023-04-26
################################

set casename = EPCAPE_2023-04-26
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"EPCAPE 2023-04-06"/ $outfile
sed -i s/CASElat/32.68/ $outfile
sed -i s/CASElon/242.13/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2023-04-26/ $outfile
sed -i s/CASEstartinsec/00000/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/66/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Haipeng Zhang"/ $outfile

################################
# EPCAPE 2023-05-15
################################

set casename = EPCAPE_2023-05-15
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"EPCAPE 2023-05-15"/ $outfile
sed -i s/CASElat/32.68/ $outfile
sed -i s/CASElon/242.13/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2023-05-15/ $outfile
sed -i s/CASEstartinsec/00000/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/66/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Haipeng Zhang"/ $outfile

################################
# EPCAPE 2023-07-02
################################

set casename = EPCAPE_2023-07-02
set outfile = run_dpxx_scream_$casename.csh
cp -r run_dpxx_scream_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"EPCAPE 2023-07-02"/ $outfile
sed -i s/CASElat/32.68/ $outfile
sed -i s/CASElon/242.13/ $outfile
sed -i s/CASEsrfprop/true/ $outfile
sed -i s/CASEstartdate/2023-07-02/ $outfile
sed -i s/CASEstartinsec/00000/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/66/ $outfile
sed -i s/CASEdebug/true/ $outfile
sed -i s/CASEnumprocs/24/ $outfile
sed -i s/CASEnex/5/ $outfile
sed -i s/CASEney/5/ $outfile
sed -i s/CASElex/50000/ $outfile
sed -i s/CASEley/50000/ $outfile
sed -i s/CASEtqnudge/false/ $outfile
sed -i s/CASEuvnudge/false/ $outfile
sed -i s/CASEcoriolis/true/ $outfile
sed -i s/CASEdosub/true/ $outfile
sed -i s/CASEwalltime/00:30:00/ $outfile
sed -i s/CASEnhtfrq/-1/ $outfile
sed -i s/FORCINGPROVIDER/"Haipeng Zhang"/ $outfile

foreach file (*.csh)
  if ($file != run_dpxx_scream_TEMPLATE.csh && $file != generate_dpscripts.csh) then
    sed -i '/OBSERVEDAERO/d' $file
    sed -i '/LENGTHNOTE/d' $file
    sed -i '/CASEstartdate/d' $file
    sed -i '/CASEstopoption/d' $file
    sed -i '/CASEstopn/d' $file  
    sed -i '/CASEstartinsec/d' $file 
    sed -i '/CASELONGstartdate/d' $file
    sed -i '/CASELONGstopoption/d' $file
    sed -i '/CASELONGstopn/d' $file 
    sed -i '/CASElwoff/d' $file
    sed -i '/CASElat/d' $file
    sed -i '/CASElon/d' $file
    sed -i '/CASELONGlat/d' $file
    sed -i '/CASELONGlon/d' $file    
    sed -i '/CASELONGstartinsec/d' $file 
    sed -i '/FORCINGPROVIDER/d' $file 
    sed -i '/THECASELONGNAME/d' $file
    sed -i '/CASEcaltype/d' $file  
    sed -i '/CASEconfigappend/d' $file
    sed -i '/CASEsstaqua/d' $file
    sed -i '/CASEsstval/d' $file
    sed -i '/CASEncdata/d' $file
    sed -i '/CASESSTdata/d' $file
    sed -i '/CASESSTyearalign/d' $file
    sed -i '/CASESSTyearstart/d' $file
    sed -i '/CASESSTyearend/d' $file
    sed -i '/CASEcoriolis/d' $file
    sed -i '/CASEhydrostatic/d' $file
    sed -i '/CASEtstep/d' $file
    sed -i '/RCEMSG/d' $file
    sed -i '/SSTMSG/d' $file
    sed -i '/SST2MSG/d' $file
    sed -i '/CASEtqlow/d' $file
    sed -i '/CASEtqhigh/d' $file
    sed -i '/CASEtqtscale/d' $file
    sed -i s/CASEangel/180/ $file
    sed -i s/CASEswoff/false/ $file
  endif
end

# Fill in each script with specific user info so you don't have to do it for every script,
#   use example below for how one Peter Bogenschutz sets his scripts for Cori.  Note that 
#   the following may not be exhaustive to get up and running on your machine.
if ($setupfor == LC) then

  foreach file (*.csh)
    if ($file != run_dpxx_scream_TEMPLATE.csh && $file != generate_dpscripts.csh) then

      # Path to output
      sed -i s+'$CSCRATCH/SCM_runs'+/p/lustre2/bogensch/ACME_simulations+ $file
      
      # Path to code base
      sed -i s+'$HOME/SCREAM_code'+/g/g19/bogensch/code+ $file

      # Name of code base
      sed -i s+'SCREAM_codetag'+SCREAM_DP+ $file

      # Name of machine used
      sed -i s+'mach_name'+quartz+ $file

      # Name of project to be charged
      sed -i s+'proj_name'+cbronze+ $file
    endif
  end

endif

if ($setupfor == pm) then

  foreach file (*.csh)
    if ($file != run_dpxx_scream_TEMPLATE.csh && $file != generate_dpscripts.csh) then

      # Path to output
      sed -i s+'$CSCRATCH/SCM_runs'+/pscratch/sd/b/bogensch/dp_scream+ $file
      
      # Path to code base
      sed -i s+'$HOME/SCREAM_code'+/global/homes/b/bogensch/ACME_development+ $file

      # Name of code base
      sed -i s+'SCREAM_codetag'+SCREAM_DP+ $file

      # Name of machine used
      sed -i s+'mach_name'+pm-cpu+ $file

      # Name of project to be charged
      sed -i s+'proj_name'+e3sm+ $file
    endif
  end

endif

# Move CGILS scripts to their own folder
mv run_dpxx_scream_CGILS*.csh CGILS
mv run_dpxx_scream_EPCAPE*.csh EPCAPE
