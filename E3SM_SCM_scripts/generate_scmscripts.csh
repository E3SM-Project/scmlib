#!/bin/csh -fe

#  GENERATE SCM scripts for each particular case
#  Uses a pre-defined template 

# Who to set these scripts up for?
#  - for general use select: general

#  - for specific user needs select: user
#    - if select user go to bottom of script and fill in deserired data paths etc. so that
#      that the user need not edit all scripts if they planning on running several.

setenv setupfor general

# helpful notes
# path to prescribed aerosol file = atm/cam/chem/presc_aero
# edison /project/projectdirs/e3sm/inputdata

################################
# RICO 
################################

set casename = RICO
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Precipitating trade-wind cumulus convection"/ $outfile
sed -i s/AEROTYPE/observed/ $outfile
sed -i s/CASElat/17.97/ $outfile
sed -i s/CASElon/298.54/ $outfile
sed -i s/CASEsrfprop/.false./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.true./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2004-12-16/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/1/ $outfile
sed -i s/OBSERVEDAERO/observed/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# ARM95 
################################

set casename = ARM95
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Deep convection over ARM SGP site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1995-07-18/ $outfile
sed -i s/CASEstartinsec/19800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/17/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# ARM97 
################################

set casename = ARM97
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Deep convection over ARM SGP site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1997-06-19/ $outfile
sed -i s/CASEstartinsec/84585/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# SGP Continuous (LONG CASE)
################################

set casename = SGP_continuous 
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Continuous forcing (2004-2015) over ARM SGP site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.61/ $outfile
sed -i s/CASElon/262.51/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASELONGstartdate/2004-01-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASELONGstopoption/nyears/ $outfile
sed -i s/CASELONGstopn/11/ $outfile
sed -i s/LENGTHNOTE2/"Possible range from Jan 2004 to Dec. 2015"/ $outfile
sed -i s/LENGTHNOTE/NOTE:/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# SGP broken cases
################################

set casename = SGP 
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASELONGNAME/SGP0003/ $outfile
sed -i s/THECASEDESCRIPTION/"Forcing fromARM SGP site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.61/ $outfile
sed -i s/CASElon/262.51/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASELONGstartdate/2000-03-01/ $outfile
sed -i s/CASELONGstartinsec/63003/ $outfile
sed -i s/CASELONGstopoption/ndays/ $outfile
sed -i s/CASELONGstopn/20/ $outfile
sed -i s/LENGTHNOTE2/"This script is set up to run with the SGP0003_iopfile_4scam.nc (March, 2000) forcingfile\n  # Other time periods exist (see E3SM SCM page) "/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i '/SGP_iopfile_4scam.nc/d' $outfile 
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DARWIN broken cases
################################

set casename = DARWIN 
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASELONGNAME/DARWIN_0405_p1/ $outfile
sed -i s/THECASEDESCRIPTION/"Forcing from Darwin site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/-12.425/ $outfile
sed -i s/CASElon/130.891/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASELONGstartdate/2004-11-03/ $outfile
sed -i s/CASELONGstartinsec/43200/ $outfile
sed -i s/CASELONGstopoption/ndays/ $outfile
sed -i s/CASELONGstopn/5/ $outfile
sed -i s/LENGTHNOTE2/"This script is set up to run with the DARWIN_0405_p1_iopfile_4scam.nc (April, 2005) forcingfile\n  # Other time periods exist (see E3SM SCM page) "/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i '/DARWIN_iopfile_4scam.nc/d' $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# GOAMAZON (LONG CASE)
################################

set casename = GOAMAZON
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"ARM's Green Ocean Amazon"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/-3.15/ $outfile
sed -i s/CASElon/300.01/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASELONGstartdate/2014-01-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASELONGstopoption/nmonths/ $outfile
sed -i s/CASELONGstopn/23/ $outfile
sed -i s/LENGTHNOTE2/"Possible range from Jan. 2014 to Nov. 2015"/ $outfile
sed -i s/LENGTHNOTE/NOTE:/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DYNAMO_northsounding
################################

set casename = DYNAMO_northsounding
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation North Sounding"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/3.0/ $outfile
sed -i s/CASElon/76.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DYNAMO_revelle
################################

set casename = DYNAMO_revelle
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation Revelle"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/3.0/ $outfile
sed -i s/CASElon/76.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DYNAMO_amie
################################

set casename = DYNAMO_amie
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Dynamics of the Madden Julian Oscillation AMIE"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/-0.63/ $outfile
sed -i s/CASElon/73.1/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2011-10-02/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/90/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# MC3E
################################

set casename = MC3E
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mid-latitude Continental Convective Clouds Experiment"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.61/ $outfile
sed -i s/CASElon/262.51/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2011-04-22/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/45/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# AEROSOLINDIRECT
################################

set casename = AEROSOLINDIRECT
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Study of Aerosol Indirect Effects in China"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/32.55/ $outfile
sed -i s/CASElon/116.78/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2008-11-01/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# ARM Shallow convection 
################################

set casename = ARM_shallow
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"ARM GCSS shallow convection"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.true./ $outfile
sed -i s/CASEnccons/50.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1997-06-21/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/14/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# ATEX 
################################

set casename = ATEX
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Cumulus under stratocumulus"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/15.0/ $outfile
sed -i s/CASElon/325.0/ $outfile
sed -i s/CASEsrfprop/.false./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.true./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1969-02-15/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/2/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# BOMEX
################################

set casename = BOMEX
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Non-precipitating trade-wind cumulus convection"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/15.0/ $outfile
sed -i s/CASElon/300.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.true./ $outfile
sed -i s/CASEprecipoff/.true./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1969-06-25/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/1/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DYCOMSRF01
################################

set casename = DYCOMSrf01
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Non-precipitating marine stratocumulus"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/31.5/ $outfile
sed -i s/CASElon/239.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.true./ $outfile
sed -i s/CASEnccons/55.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1999-07-10/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# DYCOMSRF02
################################

set casename = DYCOMSrf02
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Drizzling marine stratocumulus"/ $outfile
sed -i s/AEROTYPE/observed/ $outfile
sed -i s/CASElat/31.5/ $outfile
sed -i s/CASElon/239.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.true./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/55.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1999-07-11/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/OBSERVEDAERO/observed/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# GATE
################################

set casename = GATEIII
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Maritime deep convection"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/9.00/ $outfile
sed -i s/CASElon/336.0/ $outfile
sed -i s/CASEsrfprop/.false./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1974-08-30/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# GATEIDEAL
################################

set casename = GATEIDEAL
set outfile = run_e3sm_scm_$casename.csh
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Idealized version of GATE"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/9.00/ $outfile
sed -i s/CASElon/336.0/ $outfile
sed -i s/CASEsrfprop/.false./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.true./ $outfile
sed -i s/CASElwoff/.true./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1974-08-30/ $outfile
sed -i s/CASEstartinsec/0/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/1/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# LBA
################################

set casename = LBA
set outfile = run_e3sm_scm_$casename.csh
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"LBA Transition from shallow cumulus to deep convection"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/3.00/ $outfile
sed -i s/CASElon/300.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1999-02-23/ $outfile
sed -i s/CASEstartinsec/41400/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/6/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# MPACEB
################################

set casename = MPACEB
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mixed phase Arctic clouds Intercomparison Period"/ $outfile
sed -i s/AEROTYPE/observed/ $outfile
sed -i s/CASElat/71.75/ $outfile
sed -i s/CASElon/209.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/50.0D6/ $outfile
sed -i s/CASEnicons/0.00016D6/ $outfile
sed -i s/CASEstartdate/2004-10-09/ $outfile
sed -i s/CASEstartinsec/61200/ $outfile
sed -i s/CASEstopoption/nhours/ $outfile
sed -i s/CASEstopn/12/ $outfile
sed -i s/OBSERVEDAERO/observed/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# MPACE full
################################

set casename = MPACE
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Mixed phase Arctic clouds Full IOP"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/70.5/ $outfile
sed -i s/CASElon/206.0/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/50.0D6/ $outfile
sed -i s/CASEnicons/0.00016D6/ $outfile
sed -i s/CASEstartdate/2004-10-05/ $outfile
sed -i s/CASEstartinsec/7200/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/17/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# ISDAC
################################

set casename = ISDAC
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Indirect and semi-direct aerosol campaign"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/71.3/ $outfile
sed -i s/CASElon/156.4/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/50.0D6/ $outfile
sed -i s/CASEnicons/0.00016D6/ $outfile
sed -i s/CASEstartdate/2008-04-01/ $outfile
sed -i s/CASEstartinsec/10800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# RACORO
################################

set casename = RACORO
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Continental liquid boundary layer clouds at ARM SGP site"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/100.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2009-05-01/ $outfile
sed -i s/CASEstartinsec/84585/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# SPARTICUS
################################

set casename = SPARTICUS
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"Small particles in cirrus clouds"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/36.6/ $outfile
sed -i s/CASElon/262.5/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2010-04-01/ $outfile
sed -i s/CASEstartinsec/3599/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/29/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# TOGA
################################

set casename = TOGAII
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"TOGA-COARE deep convection"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/-2.10/ $outfile
sed -i s/CASElon/154.69/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/1992-12-18/ $outfile
sed -i s/CASEstartinsec/64800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/20/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# TWP06
################################

set casename = TWP06
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"TWP-ICE deep convection in the warm pool"/ $outfile
sed -i s/AEROTYPE/prescribed/ $outfile
sed -i s/CASElat/-12.43/ $outfile
sed -i s/CASElon/130.89/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i s/CASEstartdate/2006-01-17/ $outfile
sed -i s/CASEstartinsec/10800/ $outfile
sed -i s/CASEstopoption/ndays/ $outfile
sed -i s/CASEstopn/26/ $outfile
sed -i s/FORCINGPROVIDER/"Shuaiqi Tang and Shaocheng Xie"/ $outfile
sed -i s/CASEcaltype/GREGORIAN/ $outfile

################################
# REPLAY
################################

set casename = REPLAY
set outfile = run_e3sm_scm_$casename.csh 
cp -r run_e3sm_scm_TEMPLATE.csh $outfile
sed -i s/THECASENAME/$casename/ $outfile
sed -i s/THECASEDESCRIPTION/"REPLAY an E3SM column"/ $outfile
sed -i s/ne4_ne4/ne30_ne30/ $outfile
sed -i s/AEROTYPE/"none # keep this as none for REPLAY option"/ $outfile
sed -i s/THECASELONGNAME_iopfile_4scam.nc/"# supply the name of your forcing file"/ $outfile
sed -i s/CASELONGstartdate/"# set desired start date"/ $outfile
sed -i s/CASELONGstartinsec/"# set start time in seconds"/ $outfile
sed -i s/CASELONGstopoption/"# set desired stop option"/ $outfile
sed -i s/CASELONGstopn/"# set desired stop n"/ $outfile
sed -i s/CASELONGlat/"# set desired latitude"/ $outfile
sed -i s/CASELONGlon/"# set desired longitude"/ $outfile
sed -i s/"dycore Eulerian"/"dycore SE # do NOT change for REPLAY mode"/ $outfile
sed -i s/CASEsrfprop/.true./ $outfile
sed -i s/CASErelax/.false./ $outfile
sed -i s/CASEswoff/.false./ $outfile
sed -i s/CASElwoff/.false./ $outfile
sed -i s/CASEprecipoff/.false./ $outfile
sed -i s/CASEnccons/70.0D6/ $outfile
sed -i s/CASEnicons/0.0001D6/ $outfile
sed -i '/REPLAY_iopfile_4scam/d' $outfile
sed -i s/CASEcaltype/NO_LEAP/ $outfile
sed -i s/REPLAYDYCOREMSG1/"REPLAY MUST use preqx dycore"/ $outfile
sed -i s/REPLAYDYCORESETTING/"preqx"/ $outfile

foreach file (*.csh)
  if ($file != run_e3sm_scm_TEMPLATE.csh && $file != generate_scmscripts.csh) then
    sed -i '/OBSERVEDAERO/d' $file
    sed -i '/LENGTHNOTE/d' $file
    sed -i '/CASEstartdate/d' $file
    sed -i '/CASEstopoption/d' $file
    sed -i '/CASEstopn/d' $file  
    sed -i '/CASEstartinsec/d' $file 
    sed -i '/CASELONGstartdate/d' $file
    sed -i '/CASELONGstopoption/d' $file
    sed -i '/CASELONGstopn/d' $file 
    sed -i '/CASElat/d' $file
    sed -i '/CASElon/d' $file
    sed -i '/CASELONGlat/d' $file
    sed -i '/CASELONGlon/d' $file    
    sed -i '/CASELONGstartinsec/d' $file 
    sed -i '/FORCINGPROVIDER/d' $file 
    sed -i '/THECASELONGNAME/d' $file
    sed -i '/CASEcaltype/d' $file
    sed -i '/REPLAYDYCOREMSG1/d' $file
    sed -i '/REPLAYDYCORESETTING/d' $file
  endif
end

# Fill in each script with specific user info so you don't have to do it for every script,
#   use example below for how one Peter Bogenschutz sets his scripts for Cori.  Note that 
#   the following may not be exhaustive to get up and running on your machine.
if ($setupfor == user) then

  foreach file (*.csh)
    if ($file != run_e3sm_scm_TEMPLATE.csh && $file != generate_scmscripts.csh) then

      # Path to output
      sed -i s+'$CSCRATCH/SCM_runs'+/global/cscratch1/sd/bogensch/SCM_sims+ $file
      
      # Path to code base
      sed -i s+'$HOME/e3sm_code'+/global/homes/b/bogensch/ACME_development+ $file

      # Name of code base
      sed -i s+e3sm_codetag+E3SM_master+ $file

      # Name of machine used
      sed -i s+mach_name+cori-knl+ $file

      # Name of project to be charged
      sed -i s+proj_name+e3sm+ $file
    endif
  end

endif
