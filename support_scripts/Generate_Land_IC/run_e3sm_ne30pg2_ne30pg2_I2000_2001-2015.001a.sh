#!/bin/bash -fe

# E3SM Coupled Model Group run_e3sm script template.
#
# Bash coding style inspired by:
# http://kfirlavi.herokuapp.com/blog/2012/11/14/defensive-bash-programming

main() {

# For debugging, uncomment libe below
#set -x

# --- Configuration flags ----

# Machine and project
readonly MACHINE=pm-cpu
readonly PROJECT="mp193"

# Simulation
readonly COMPSET="IELM"
readonly RESOLUTION="ne30pg2_ne30pg2"
readonly CASE_NAME="Generate_land_IC_I2000.ne30pg2_ne30pg2.001a"
# If this is part of a simulation campaign, ask your group lead about using a case_group label
# otherwise, comment out
#readonly CASE_GROUP="v3.LR"

# Code and compilation
readonly CHECKOUT="E3SM_maint_3.0"
readonly BRANCH="v3.0.2"  # master as of 2024-03-04 399d4301138617088dd93214123d6c025e061302
readonly CHERRY=( )
readonly DEBUG_COMPILE=false

# Run options
readonly MODEL_START_TYPE="initial"  # 'initial', 'continue', 'branch', 'hybrid'
readonly START_DATE="2001-01-01"

# Set paths
readonly CODE_ROOT="/pscratch/sd/b/bogensch/dp_scream/codes/${CHECKOUT}"
readonly CASE_ROOT="/pscratch/sd/b/bogensch/E3SM_simulations/${CASE_NAME}"

# Sub-directories
readonly CASE_BUILD_DIR=${CASE_ROOT}/build
readonly CASE_ARCHIVE_DIR=${CASE_ROOT}/archive

# number of processors
readonly MY_NPES="256"

# Define type of run
#  short tests: 'XS_1x10_ndays', 'XS_2x5_ndays', 'S_1x10_ndays', 'M_1x10_ndays', 'L_1x10_ndays'
#  or 'production' for full simulation

#readonly run='L_1x10_ndays'  # build with this to ensure non-threading
#readonly run='S_1x10_ndays'
#readonly run='S_2x5_ndays'
#readonly run='M_1x10_ndays'

readonly run='production'

echo "setting up ${run}"
# Production simulation
readonly CASE_SCRIPTS_DIR=${CASE_ROOT}/case_scripts
readonly CASE_RUN_DIR=${CASE_ROOT}/run
readonly PELAYOUT="custom-perl"
readonly WALLTIME="24:00:00"
readonly STOP_OPTION="nyears"
readonly STOP_N="17"
readonly REST_OPTION="nmonths"
readonly REST_N="1"
readonly RESUBMIT="0"
readonly DO_SHORT_TERM_ARCHIVING=true

# Coupler history
readonly HIST_OPTION="nyears"
readonly HIST_N="1"

# Leave empty (unless you understand what it does)
readonly OLD_EXECUTABLE=""

# --- Toggle flags for what to do ----
do_fetch_code=false
do_create_newcase=true
do_case_setup=true
do_case_build=true
do_case_submit=true

# --- Now, do the work ---

# Make directories created by this script world-readable
umask 022

# Fetch code from Github
fetch_code

# Create case
create_newcase

# Custom PE layout
custom_pelayout

# Setup
case_setup

# Build
case_build

# Configure runtime options
runtime_options

# Copy script into case_script directory for provenance
copy_script

# Submit
case_submit

# All done
echo $'\n----- All done -----\n'

}

# =======================
# Custom user_nl settings
# =======================

user_nl() {

cat <<EOF >> user_nl_datm
streams = "datm.streams.txt.CLM_QIAN.Solar 2001 2001 2023",
          "datm.streams.txt.CLM_QIAN.Precip 2001 2001 2023",
          "datm.streams.txt.CLM_QIAN.TPQW 2001 2001 2023",
          "datm.streams.txt.presaero.clim_2000 1 1 1",
          "datm.streams.txt.topo.observed 1 1 1"
EOF

cat <<EOF >> user_datm.streams.txt.CLM_QIAN.Precip
<?xml version="1.0"?>
<file id="stream" version="1.0">
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon
  </filePath>
  <fileNames>
     domain.lnd.era5_721x1440_rdrlat_EC30to60E2r2.221115.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
     PRECTmms precn
   </variableNames>
   <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon/Precip
   </filePath>
   <fileNames>
clmforc.ERA5.Prec.2001-01.nc
clmforc.ERA5.Prec.2001-02.nc
clmforc.ERA5.Prec.2001-03.nc
clmforc.ERA5.Prec.2001-04.nc
clmforc.ERA5.Prec.2001-05.nc
clmforc.ERA5.Prec.2001-06.nc
clmforc.ERA5.Prec.2001-07.nc
clmforc.ERA5.Prec.2001-08.nc
clmforc.ERA5.Prec.2001-09.nc
clmforc.ERA5.Prec.2001-10.nc
clmforc.ERA5.Prec.2001-11.nc
clmforc.ERA5.Prec.2001-12.nc
clmforc.ERA5.Prec.2002-01.nc
clmforc.ERA5.Prec.2002-02.nc
clmforc.ERA5.Prec.2002-03.nc
clmforc.ERA5.Prec.2002-04.nc
clmforc.ERA5.Prec.2002-05.nc
clmforc.ERA5.Prec.2002-06.nc
clmforc.ERA5.Prec.2002-07.nc
clmforc.ERA5.Prec.2002-08.nc
clmforc.ERA5.Prec.2002-09.nc
clmforc.ERA5.Prec.2002-10.nc
clmforc.ERA5.Prec.2002-11.nc
clmforc.ERA5.Prec.2002-12.nc
clmforc.ERA5.Prec.2003-01.nc
clmforc.ERA5.Prec.2003-02.nc
clmforc.ERA5.Prec.2003-03.nc
clmforc.ERA5.Prec.2003-04.nc
clmforc.ERA5.Prec.2003-05.nc
clmforc.ERA5.Prec.2003-06.nc
clmforc.ERA5.Prec.2003-07.nc
clmforc.ERA5.Prec.2003-08.nc
clmforc.ERA5.Prec.2003-09.nc
clmforc.ERA5.Prec.2003-10.nc
clmforc.ERA5.Prec.2003-11.nc
clmforc.ERA5.Prec.2003-12.nc
clmforc.ERA5.Prec.2004-01.nc
clmforc.ERA5.Prec.2004-02.nc
clmforc.ERA5.Prec.2004-03.nc
clmforc.ERA5.Prec.2004-04.nc
clmforc.ERA5.Prec.2004-05.nc
clmforc.ERA5.Prec.2004-06.nc
clmforc.ERA5.Prec.2004-07.nc
clmforc.ERA5.Prec.2004-08.nc
clmforc.ERA5.Prec.2004-09.nc
clmforc.ERA5.Prec.2004-10.nc
clmforc.ERA5.Prec.2004-11.nc
clmforc.ERA5.Prec.2004-12.nc
clmforc.ERA5.Prec.2005-01.nc
clmforc.ERA5.Prec.2005-02.nc
clmforc.ERA5.Prec.2005-03.nc
clmforc.ERA5.Prec.2005-04.nc
clmforc.ERA5.Prec.2005-05.nc
clmforc.ERA5.Prec.2005-06.nc
clmforc.ERA5.Prec.2005-07.nc
clmforc.ERA5.Prec.2005-08.nc
clmforc.ERA5.Prec.2005-09.nc
clmforc.ERA5.Prec.2005-10.nc
clmforc.ERA5.Prec.2005-11.nc
clmforc.ERA5.Prec.2005-12.nc
clmforc.ERA5.Prec.2006-01.nc
clmforc.ERA5.Prec.2006-02.nc
clmforc.ERA5.Prec.2006-03.nc
clmforc.ERA5.Prec.2006-04.nc
clmforc.ERA5.Prec.2006-05.nc
clmforc.ERA5.Prec.2006-06.nc
clmforc.ERA5.Prec.2006-07.nc
clmforc.ERA5.Prec.2006-08.nc
clmforc.ERA5.Prec.2006-09.nc
clmforc.ERA5.Prec.2006-10.nc
clmforc.ERA5.Prec.2006-11.nc
clmforc.ERA5.Prec.2006-12.nc
clmforc.ERA5.Prec.2007-01.nc
clmforc.ERA5.Prec.2007-02.nc
clmforc.ERA5.Prec.2007-03.nc
clmforc.ERA5.Prec.2007-04.nc
clmforc.ERA5.Prec.2007-05.nc
clmforc.ERA5.Prec.2007-06.nc
clmforc.ERA5.Prec.2007-07.nc
clmforc.ERA5.Prec.2007-08.nc
clmforc.ERA5.Prec.2007-09.nc
clmforc.ERA5.Prec.2007-10.nc
clmforc.ERA5.Prec.2007-11.nc
clmforc.ERA5.Prec.2007-12.nc
clmforc.ERA5.Prec.2008-01.nc
clmforc.ERA5.Prec.2008-02.nc
clmforc.ERA5.Prec.2008-03.nc
clmforc.ERA5.Prec.2008-04.nc
clmforc.ERA5.Prec.2008-05.nc
clmforc.ERA5.Prec.2008-06.nc
clmforc.ERA5.Prec.2008-07.nc
clmforc.ERA5.Prec.2008-08.nc
clmforc.ERA5.Prec.2008-09.nc
clmforc.ERA5.Prec.2008-10.nc
clmforc.ERA5.Prec.2008-11.nc
clmforc.ERA5.Prec.2008-12.nc
clmforc.ERA5.Prec.2009-01.nc
clmforc.ERA5.Prec.2009-02.nc
clmforc.ERA5.Prec.2009-03.nc
clmforc.ERA5.Prec.2009-04.nc
clmforc.ERA5.Prec.2009-05.nc
clmforc.ERA5.Prec.2009-06.nc
clmforc.ERA5.Prec.2009-07.nc
clmforc.ERA5.Prec.2009-08.nc
clmforc.ERA5.Prec.2009-09.nc
clmforc.ERA5.Prec.2009-10.nc
clmforc.ERA5.Prec.2009-11.nc
clmforc.ERA5.Prec.2009-12.nc
clmforc.ERA5.Prec.2010-01.nc
clmforc.ERA5.Prec.2010-02.nc
clmforc.ERA5.Prec.2010-03.nc
clmforc.ERA5.Prec.2010-04.nc
clmforc.ERA5.Prec.2010-05.nc
clmforc.ERA5.Prec.2010-06.nc
clmforc.ERA5.Prec.2010-07.nc
clmforc.ERA5.Prec.2010-08.nc
clmforc.ERA5.Prec.2010-09.nc
clmforc.ERA5.Prec.2010-10.nc
clmforc.ERA5.Prec.2010-11.nc
clmforc.ERA5.Prec.2010-12.nc
clmforc.ERA5.Prec.2011-01.nc
clmforc.ERA5.Prec.2011-02.nc
clmforc.ERA5.Prec.2011-03.nc
clmforc.ERA5.Prec.2011-04.nc
clmforc.ERA5.Prec.2011-05.nc
clmforc.ERA5.Prec.2011-06.nc
clmforc.ERA5.Prec.2011-07.nc
clmforc.ERA5.Prec.2011-08.nc
clmforc.ERA5.Prec.2011-09.nc
clmforc.ERA5.Prec.2011-10.nc
clmforc.ERA5.Prec.2011-11.nc
clmforc.ERA5.Prec.2011-12.nc
clmforc.ERA5.Prec.2012-01.nc
clmforc.ERA5.Prec.2012-02.nc
clmforc.ERA5.Prec.2012-03.nc
clmforc.ERA5.Prec.2012-04.nc
clmforc.ERA5.Prec.2012-05.nc
clmforc.ERA5.Prec.2012-06.nc
clmforc.ERA5.Prec.2012-07.nc
clmforc.ERA5.Prec.2012-08.nc
clmforc.ERA5.Prec.2012-09.nc
clmforc.ERA5.Prec.2012-10.nc
clmforc.ERA5.Prec.2012-11.nc
clmforc.ERA5.Prec.2012-12.nc
clmforc.ERA5.Prec.2013-01.nc
clmforc.ERA5.Prec.2013-02.nc
clmforc.ERA5.Prec.2013-03.nc
clmforc.ERA5.Prec.2013-04.nc
clmforc.ERA5.Prec.2013-05.nc
clmforc.ERA5.Prec.2013-06.nc
clmforc.ERA5.Prec.2013-07.nc
clmforc.ERA5.Prec.2013-08.nc
clmforc.ERA5.Prec.2013-09.nc
clmforc.ERA5.Prec.2013-10.nc
clmforc.ERA5.Prec.2013-11.nc
clmforc.ERA5.Prec.2013-12.nc
clmforc.ERA5.Prec.2014-01.nc
clmforc.ERA5.Prec.2014-02.nc
clmforc.ERA5.Prec.2014-03.nc
clmforc.ERA5.Prec.2014-04.nc
clmforc.ERA5.Prec.2014-05.nc
clmforc.ERA5.Prec.2014-06.nc
clmforc.ERA5.Prec.2014-07.nc
clmforc.ERA5.Prec.2014-08.nc
clmforc.ERA5.Prec.2014-09.nc
clmforc.ERA5.Prec.2014-10.nc
clmforc.ERA5.Prec.2014-11.nc
clmforc.ERA5.Prec.2014-12.nc
clmforc.ERA5.Prec.2015-01.nc
clmforc.ERA5.Prec.2015-02.nc
clmforc.ERA5.Prec.2015-03.nc
clmforc.ERA5.Prec.2015-04.nc
clmforc.ERA5.Prec.2015-05.nc
clmforc.ERA5.Prec.2015-06.nc
clmforc.ERA5.Prec.2015-07.nc
clmforc.ERA5.Prec.2015-08.nc
clmforc.ERA5.Prec.2015-09.nc
clmforc.ERA5.Prec.2015-10.nc
clmforc.ERA5.Prec.2015-11.nc
clmforc.ERA5.Prec.2015-12.nc
clmforc.ERA5.Prec.2016-01.nc
clmforc.ERA5.Prec.2016-02.nc
clmforc.ERA5.Prec.2016-03.nc
clmforc.ERA5.Prec.2016-04.nc
clmforc.ERA5.Prec.2016-05.nc
clmforc.ERA5.Prec.2016-06.nc
clmforc.ERA5.Prec.2016-07.nc
clmforc.ERA5.Prec.2016-08.nc
clmforc.ERA5.Prec.2016-09.nc
clmforc.ERA5.Prec.2016-10.nc
clmforc.ERA5.Prec.2016-11.nc
clmforc.ERA5.Prec.2016-12.nc
clmforc.ERA5.Prec.2017-01.nc
clmforc.ERA5.Prec.2017-02.nc
clmforc.ERA5.Prec.2017-03.nc
clmforc.ERA5.Prec.2017-04.nc
clmforc.ERA5.Prec.2017-05.nc
clmforc.ERA5.Prec.2017-06.nc
clmforc.ERA5.Prec.2017-07.nc
clmforc.ERA5.Prec.2017-08.nc
clmforc.ERA5.Prec.2017-09.nc
clmforc.ERA5.Prec.2017-10.nc
clmforc.ERA5.Prec.2017-11.nc
clmforc.ERA5.Prec.2017-12.nc
clmforc.ERA5.Prec.2018-01.nc
clmforc.ERA5.Prec.2018-02.nc
clmforc.ERA5.Prec.2018-03.nc
clmforc.ERA5.Prec.2018-04.nc
clmforc.ERA5.Prec.2018-05.nc
clmforc.ERA5.Prec.2018-06.nc
clmforc.ERA5.Prec.2018-07.nc
clmforc.ERA5.Prec.2018-08.nc
clmforc.ERA5.Prec.2018-09.nc
clmforc.ERA5.Prec.2018-10.nc
clmforc.ERA5.Prec.2018-11.nc
clmforc.ERA5.Prec.2018-12.nc
clmforc.ERA5.Prec.2019-01.nc
clmforc.ERA5.Prec.2019-02.nc
clmforc.ERA5.Prec.2019-03.nc
clmforc.ERA5.Prec.2019-04.nc
clmforc.ERA5.Prec.2019-05.nc
clmforc.ERA5.Prec.2019-06.nc
clmforc.ERA5.Prec.2019-07.nc
clmforc.ERA5.Prec.2019-08.nc
clmforc.ERA5.Prec.2019-09.nc
clmforc.ERA5.Prec.2019-10.nc
clmforc.ERA5.Prec.2019-11.nc
clmforc.ERA5.Prec.2019-12.nc
clmforc.ERA5.Prec.2020-01.nc
clmforc.ERA5.Prec.2020-02.nc
clmforc.ERA5.Prec.2020-03.nc
clmforc.ERA5.Prec.2020-04.nc
clmforc.ERA5.Prec.2020-05.nc
clmforc.ERA5.Prec.2020-06.nc
clmforc.ERA5.Prec.2020-07.nc
clmforc.ERA5.Prec.2020-08.nc
clmforc.ERA5.Prec.2020-09.nc
clmforc.ERA5.Prec.2020-10.nc
clmforc.ERA5.Prec.2020-11.nc
clmforc.ERA5.Prec.2020-12.nc
clmforc.ERA5.Prec.2021-01.nc
clmforc.ERA5.Prec.2021-02.nc
clmforc.ERA5.Prec.2021-03.nc
clmforc.ERA5.Prec.2021-04.nc
clmforc.ERA5.Prec.2021-05.nc
clmforc.ERA5.Prec.2021-06.nc
clmforc.ERA5.Prec.2021-07.nc
clmforc.ERA5.Prec.2021-08.nc
clmforc.ERA5.Prec.2021-09.nc
clmforc.ERA5.Prec.2021-10.nc
clmforc.ERA5.Prec.2021-11.nc
clmforc.ERA5.Prec.2021-12.nc
clmforc.ERA5.Prec.2022-01.nc
clmforc.ERA5.Prec.2022-02.nc
clmforc.ERA5.Prec.2022-03.nc
clmforc.ERA5.Prec.2022-04.nc
clmforc.ERA5.Prec.2022-05.nc
clmforc.ERA5.Prec.2022-06.nc
clmforc.ERA5.Prec.2022-07.nc
clmforc.ERA5.Prec.2022-08.nc
clmforc.ERA5.Prec.2022-09.nc
clmforc.ERA5.Prec.2022-10.nc
clmforc.ERA5.Prec.2022-11.nc
clmforc.ERA5.Prec.2022-12.nc
clmforc.ERA5.Prec.2023-01.nc
clmforc.ERA5.Prec.2023-02.nc
clmforc.ERA5.Prec.2023-03.nc
clmforc.ERA5.Prec.2023-04.nc
clmforc.ERA5.Prec.2023-05.nc
clmforc.ERA5.Prec.2023-06.nc
clmforc.ERA5.Prec.2023-07.nc
clmforc.ERA5.Prec.2023-08.nc
clmforc.ERA5.Prec.2023-09.nc
clmforc.ERA5.Prec.2023-10.nc
clmforc.ERA5.Prec.2023-11.nc
clmforc.ERA5.Prec.2023-12.nc
   </fileNames>
   <offset>
      0
   </offset>
</fieldInfo>
</file>
EOF

cat <<EOF >> user_datm.streams.txt.CLM_QIAN.Solar
<?xml version="1.0"?>
<file id="stream" version="1.0">
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon
  </filePath>
  <fileNames>
     domain.lnd.era5_721x1440_rdrlat_EC30to60E2r2.221115.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
     FSDS swdn
   </variableNames>
   <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon/Solar
   </filePath>
   <fileNames>
clmforc.ERA5.Solr.2001-01.nc
clmforc.ERA5.Solr.2001-02.nc
clmforc.ERA5.Solr.2001-03.nc
clmforc.ERA5.Solr.2001-04.nc
clmforc.ERA5.Solr.2001-05.nc
clmforc.ERA5.Solr.2001-06.nc
clmforc.ERA5.Solr.2001-07.nc
clmforc.ERA5.Solr.2001-08.nc
clmforc.ERA5.Solr.2001-09.nc
clmforc.ERA5.Solr.2001-10.nc
clmforc.ERA5.Solr.2001-11.nc
clmforc.ERA5.Solr.2001-12.nc
clmforc.ERA5.Solr.2002-01.nc
clmforc.ERA5.Solr.2002-02.nc
clmforc.ERA5.Solr.2002-03.nc
clmforc.ERA5.Solr.2002-04.nc
clmforc.ERA5.Solr.2002-05.nc
clmforc.ERA5.Solr.2002-06.nc
clmforc.ERA5.Solr.2002-07.nc
clmforc.ERA5.Solr.2002-08.nc
clmforc.ERA5.Solr.2002-09.nc
clmforc.ERA5.Solr.2002-10.nc
clmforc.ERA5.Solr.2002-11.nc
clmforc.ERA5.Solr.2002-12.nc
clmforc.ERA5.Solr.2003-01.nc
clmforc.ERA5.Solr.2003-02.nc
clmforc.ERA5.Solr.2003-03.nc
clmforc.ERA5.Solr.2003-04.nc
clmforc.ERA5.Solr.2003-05.nc
clmforc.ERA5.Solr.2003-06.nc
clmforc.ERA5.Solr.2003-07.nc
clmforc.ERA5.Solr.2003-08.nc
clmforc.ERA5.Solr.2003-09.nc
clmforc.ERA5.Solr.2003-10.nc
clmforc.ERA5.Solr.2003-11.nc
clmforc.ERA5.Solr.2003-12.nc
clmforc.ERA5.Solr.2004-01.nc
clmforc.ERA5.Solr.2004-02.nc
clmforc.ERA5.Solr.2004-03.nc
clmforc.ERA5.Solr.2004-04.nc
clmforc.ERA5.Solr.2004-05.nc
clmforc.ERA5.Solr.2004-06.nc
clmforc.ERA5.Solr.2004-07.nc
clmforc.ERA5.Solr.2004-08.nc
clmforc.ERA5.Solr.2004-09.nc
clmforc.ERA5.Solr.2004-10.nc
clmforc.ERA5.Solr.2004-11.nc
clmforc.ERA5.Solr.2004-12.nc
clmforc.ERA5.Solr.2005-01.nc
clmforc.ERA5.Solr.2005-02.nc
clmforc.ERA5.Solr.2005-03.nc
clmforc.ERA5.Solr.2005-04.nc
clmforc.ERA5.Solr.2005-05.nc
clmforc.ERA5.Solr.2005-06.nc
clmforc.ERA5.Solr.2005-07.nc
clmforc.ERA5.Solr.2005-08.nc
clmforc.ERA5.Solr.2005-09.nc
clmforc.ERA5.Solr.2005-10.nc
clmforc.ERA5.Solr.2005-11.nc
clmforc.ERA5.Solr.2005-12.nc
clmforc.ERA5.Solr.2006-01.nc
clmforc.ERA5.Solr.2006-02.nc
clmforc.ERA5.Solr.2006-03.nc
clmforc.ERA5.Solr.2006-04.nc
clmforc.ERA5.Solr.2006-05.nc
clmforc.ERA5.Solr.2006-06.nc
clmforc.ERA5.Solr.2006-07.nc
clmforc.ERA5.Solr.2006-08.nc
clmforc.ERA5.Solr.2006-09.nc
clmforc.ERA5.Solr.2006-10.nc
clmforc.ERA5.Solr.2006-11.nc
clmforc.ERA5.Solr.2006-12.nc
clmforc.ERA5.Solr.2007-01.nc
clmforc.ERA5.Solr.2007-02.nc
clmforc.ERA5.Solr.2007-03.nc
clmforc.ERA5.Solr.2007-04.nc
clmforc.ERA5.Solr.2007-05.nc
clmforc.ERA5.Solr.2007-06.nc
clmforc.ERA5.Solr.2007-07.nc
clmforc.ERA5.Solr.2007-08.nc
clmforc.ERA5.Solr.2007-09.nc
clmforc.ERA5.Solr.2007-10.nc
clmforc.ERA5.Solr.2007-11.nc
clmforc.ERA5.Solr.2007-12.nc
clmforc.ERA5.Solr.2008-01.nc
clmforc.ERA5.Solr.2008-02.nc
clmforc.ERA5.Solr.2008-03.nc
clmforc.ERA5.Solr.2008-04.nc
clmforc.ERA5.Solr.2008-05.nc
clmforc.ERA5.Solr.2008-06.nc
clmforc.ERA5.Solr.2008-07.nc
clmforc.ERA5.Solr.2008-08.nc
clmforc.ERA5.Solr.2008-09.nc
clmforc.ERA5.Solr.2008-10.nc
clmforc.ERA5.Solr.2008-11.nc
clmforc.ERA5.Solr.2008-12.nc
clmforc.ERA5.Solr.2009-01.nc
clmforc.ERA5.Solr.2009-02.nc
clmforc.ERA5.Solr.2009-03.nc
clmforc.ERA5.Solr.2009-04.nc
clmforc.ERA5.Solr.2009-05.nc
clmforc.ERA5.Solr.2009-06.nc
clmforc.ERA5.Solr.2009-07.nc
clmforc.ERA5.Solr.2009-08.nc
clmforc.ERA5.Solr.2009-09.nc
clmforc.ERA5.Solr.2009-10.nc
clmforc.ERA5.Solr.2009-11.nc
clmforc.ERA5.Solr.2009-12.nc
clmforc.ERA5.Solr.2010-01.nc
clmforc.ERA5.Solr.2010-02.nc
clmforc.ERA5.Solr.2010-03.nc
clmforc.ERA5.Solr.2010-04.nc
clmforc.ERA5.Solr.2010-05.nc
clmforc.ERA5.Solr.2010-06.nc
clmforc.ERA5.Solr.2010-07.nc
clmforc.ERA5.Solr.2010-08.nc
clmforc.ERA5.Solr.2010-09.nc
clmforc.ERA5.Solr.2010-10.nc
clmforc.ERA5.Solr.2010-11.nc
clmforc.ERA5.Solr.2010-12.nc
clmforc.ERA5.Solr.2011-01.nc
clmforc.ERA5.Solr.2011-02.nc
clmforc.ERA5.Solr.2011-03.nc
clmforc.ERA5.Solr.2011-04.nc
clmforc.ERA5.Solr.2011-05.nc
clmforc.ERA5.Solr.2011-06.nc
clmforc.ERA5.Solr.2011-07.nc
clmforc.ERA5.Solr.2011-08.nc
clmforc.ERA5.Solr.2011-09.nc
clmforc.ERA5.Solr.2011-10.nc
clmforc.ERA5.Solr.2011-11.nc
clmforc.ERA5.Solr.2011-12.nc
clmforc.ERA5.Solr.2012-01.nc
clmforc.ERA5.Solr.2012-02.nc
clmforc.ERA5.Solr.2012-03.nc
clmforc.ERA5.Solr.2012-04.nc
clmforc.ERA5.Solr.2012-05.nc
clmforc.ERA5.Solr.2012-06.nc
clmforc.ERA5.Solr.2012-07.nc
clmforc.ERA5.Solr.2012-08.nc
clmforc.ERA5.Solr.2012-09.nc
clmforc.ERA5.Solr.2012-10.nc
clmforc.ERA5.Solr.2012-11.nc
clmforc.ERA5.Solr.2012-12.nc
clmforc.ERA5.Solr.2013-01.nc
clmforc.ERA5.Solr.2013-02.nc
clmforc.ERA5.Solr.2013-03.nc
clmforc.ERA5.Solr.2013-04.nc
clmforc.ERA5.Solr.2013-05.nc
clmforc.ERA5.Solr.2013-06.nc
clmforc.ERA5.Solr.2013-07.nc
clmforc.ERA5.Solr.2013-08.nc
clmforc.ERA5.Solr.2013-09.nc
clmforc.ERA5.Solr.2013-10.nc
clmforc.ERA5.Solr.2013-11.nc
clmforc.ERA5.Solr.2013-12.nc
clmforc.ERA5.Solr.2014-01.nc
clmforc.ERA5.Solr.2014-02.nc
clmforc.ERA5.Solr.2014-03.nc
clmforc.ERA5.Solr.2014-04.nc
clmforc.ERA5.Solr.2014-05.nc
clmforc.ERA5.Solr.2014-06.nc
clmforc.ERA5.Solr.2014-07.nc
clmforc.ERA5.Solr.2014-08.nc
clmforc.ERA5.Solr.2014-09.nc
clmforc.ERA5.Solr.2014-10.nc
clmforc.ERA5.Solr.2014-11.nc
clmforc.ERA5.Solr.2014-12.nc
clmforc.ERA5.Solr.2015-01.nc
clmforc.ERA5.Solr.2015-02.nc
clmforc.ERA5.Solr.2015-03.nc
clmforc.ERA5.Solr.2015-04.nc
clmforc.ERA5.Solr.2015-05.nc
clmforc.ERA5.Solr.2015-06.nc
clmforc.ERA5.Solr.2015-07.nc
clmforc.ERA5.Solr.2015-08.nc
clmforc.ERA5.Solr.2015-09.nc
clmforc.ERA5.Solr.2015-10.nc
clmforc.ERA5.Solr.2015-11.nc
clmforc.ERA5.Solr.2015-12.nc
clmforc.ERA5.Solr.2016-01.nc
clmforc.ERA5.Solr.2016-02.nc
clmforc.ERA5.Solr.2016-03.nc
clmforc.ERA5.Solr.2016-04.nc
clmforc.ERA5.Solr.2016-05.nc
clmforc.ERA5.Solr.2016-06.nc
clmforc.ERA5.Solr.2016-07.nc
clmforc.ERA5.Solr.2016-08.nc
clmforc.ERA5.Solr.2016-09.nc
clmforc.ERA5.Solr.2016-10.nc
clmforc.ERA5.Solr.2016-11.nc
clmforc.ERA5.Solr.2016-12.nc
clmforc.ERA5.Solr.2017-01.nc
clmforc.ERA5.Solr.2017-02.nc
clmforc.ERA5.Solr.2017-03.nc
clmforc.ERA5.Solr.2017-04.nc
clmforc.ERA5.Solr.2017-05.nc
clmforc.ERA5.Solr.2017-06.nc
clmforc.ERA5.Solr.2017-07.nc
clmforc.ERA5.Solr.2017-08.nc
clmforc.ERA5.Solr.2017-09.nc
clmforc.ERA5.Solr.2017-10.nc
clmforc.ERA5.Solr.2017-11.nc
clmforc.ERA5.Solr.2017-12.nc
clmforc.ERA5.Solr.2018-01.nc
clmforc.ERA5.Solr.2018-02.nc
clmforc.ERA5.Solr.2018-03.nc
clmforc.ERA5.Solr.2018-04.nc
clmforc.ERA5.Solr.2018-05.nc
clmforc.ERA5.Solr.2018-06.nc
clmforc.ERA5.Solr.2018-07.nc
clmforc.ERA5.Solr.2018-08.nc
clmforc.ERA5.Solr.2018-09.nc
clmforc.ERA5.Solr.2018-10.nc
clmforc.ERA5.Solr.2018-11.nc
clmforc.ERA5.Solr.2018-12.nc
clmforc.ERA5.Solr.2019-01.nc
clmforc.ERA5.Solr.2019-02.nc
clmforc.ERA5.Solr.2019-03.nc
clmforc.ERA5.Solr.2019-04.nc
clmforc.ERA5.Solr.2019-05.nc
clmforc.ERA5.Solr.2019-06.nc
clmforc.ERA5.Solr.2019-07.nc
clmforc.ERA5.Solr.2019-08.nc
clmforc.ERA5.Solr.2019-09.nc
clmforc.ERA5.Solr.2019-10.nc
clmforc.ERA5.Solr.2019-11.nc
clmforc.ERA5.Solr.2019-12.nc
clmforc.ERA5.Solr.2020-01.nc
clmforc.ERA5.Solr.2020-02.nc
clmforc.ERA5.Solr.2020-03.nc
clmforc.ERA5.Solr.2020-04.nc
clmforc.ERA5.Solr.2020-05.nc
clmforc.ERA5.Solr.2020-06.nc
clmforc.ERA5.Solr.2020-07.nc
clmforc.ERA5.Solr.2020-08.nc
clmforc.ERA5.Solr.2020-09.nc
clmforc.ERA5.Solr.2020-10.nc
clmforc.ERA5.Solr.2020-11.nc
clmforc.ERA5.Solr.2020-12.nc
clmforc.ERA5.Solr.2021-01.nc
clmforc.ERA5.Solr.2021-02.nc
clmforc.ERA5.Solr.2021-03.nc
clmforc.ERA5.Solr.2021-04.nc
clmforc.ERA5.Solr.2021-05.nc
clmforc.ERA5.Solr.2021-06.nc
clmforc.ERA5.Solr.2021-07.nc
clmforc.ERA5.Solr.2021-08.nc
clmforc.ERA5.Solr.2021-09.nc
clmforc.ERA5.Solr.2021-10.nc
clmforc.ERA5.Solr.2021-11.nc
clmforc.ERA5.Solr.2021-12.nc
clmforc.ERA5.Solr.2022-01.nc
clmforc.ERA5.Solr.2022-02.nc
clmforc.ERA5.Solr.2022-03.nc
clmforc.ERA5.Solr.2022-04.nc
clmforc.ERA5.Solr.2022-05.nc
clmforc.ERA5.Solr.2022-06.nc
clmforc.ERA5.Solr.2022-07.nc
clmforc.ERA5.Solr.2022-08.nc
clmforc.ERA5.Solr.2022-09.nc
clmforc.ERA5.Solr.2022-10.nc
clmforc.ERA5.Solr.2022-11.nc
clmforc.ERA5.Solr.2022-12.nc
clmforc.ERA5.Solr.2023-01.nc
clmforc.ERA5.Solr.2023-02.nc
clmforc.ERA5.Solr.2023-03.nc
clmforc.ERA5.Solr.2023-04.nc
clmforc.ERA5.Solr.2023-05.nc
clmforc.ERA5.Solr.2023-06.nc
clmforc.ERA5.Solr.2023-07.nc
clmforc.ERA5.Solr.2023-08.nc
clmforc.ERA5.Solr.2023-09.nc
clmforc.ERA5.Solr.2023-10.nc
clmforc.ERA5.Solr.2023-11.nc
clmforc.ERA5.Solr.2023-12.nc
   </fileNames>
   <offset>
      0
   </offset>
</fieldInfo>
</file>
EOF

cat <<EOF >> user_datm.streams.txt.CLM_QIAN.TPQW
<?xml version="1.0"?>
<file id="stream" version="1.0">
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon
  </filePath>
  <fileNames>
     domain.lnd.era5_721x1440_rdrlat_EC30to60E2r2.221115.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
     TBOT     tbot
     WIND     wind
     TDEW     tdew
     PSRF     pbot
   </variableNames>
   <filePath>
     /global/cfs/projectdirs/mp193/DATM/atm_forcing.datm7.ERA5.0.25d.mon/TPHWL
   </filePath>
   <fileNames>
clmforc.ERA5.TPQWL.2001-01.nc
clmforc.ERA5.TPQWL.2001-02.nc
clmforc.ERA5.TPQWL.2001-03.nc
clmforc.ERA5.TPQWL.2001-04.nc
clmforc.ERA5.TPQWL.2001-05.nc
clmforc.ERA5.TPQWL.2001-06.nc
clmforc.ERA5.TPQWL.2001-07.nc
clmforc.ERA5.TPQWL.2001-08.nc
clmforc.ERA5.TPQWL.2001-09.nc
clmforc.ERA5.TPQWL.2001-10.nc
clmforc.ERA5.TPQWL.2001-11.nc
clmforc.ERA5.TPQWL.2001-12.nc
clmforc.ERA5.TPQWL.2002-01.nc
clmforc.ERA5.TPQWL.2002-02.nc
clmforc.ERA5.TPQWL.2002-03.nc
clmforc.ERA5.TPQWL.2002-04.nc
clmforc.ERA5.TPQWL.2002-05.nc
clmforc.ERA5.TPQWL.2002-06.nc
clmforc.ERA5.TPQWL.2002-07.nc
clmforc.ERA5.TPQWL.2002-08.nc
clmforc.ERA5.TPQWL.2002-09.nc
clmforc.ERA5.TPQWL.2002-10.nc
clmforc.ERA5.TPQWL.2002-11.nc
clmforc.ERA5.TPQWL.2002-12.nc
clmforc.ERA5.TPQWL.2003-01.nc
clmforc.ERA5.TPQWL.2003-02.nc
clmforc.ERA5.TPQWL.2003-03.nc
clmforc.ERA5.TPQWL.2003-04.nc
clmforc.ERA5.TPQWL.2003-05.nc
clmforc.ERA5.TPQWL.2003-06.nc
clmforc.ERA5.TPQWL.2003-07.nc
clmforc.ERA5.TPQWL.2003-08.nc
clmforc.ERA5.TPQWL.2003-09.nc
clmforc.ERA5.TPQWL.2003-10.nc
clmforc.ERA5.TPQWL.2003-11.nc
clmforc.ERA5.TPQWL.2003-12.nc
clmforc.ERA5.TPQWL.2004-01.nc
clmforc.ERA5.TPQWL.2004-02.nc
clmforc.ERA5.TPQWL.2004-03.nc
clmforc.ERA5.TPQWL.2004-04.nc
clmforc.ERA5.TPQWL.2004-05.nc
clmforc.ERA5.TPQWL.2004-06.nc
clmforc.ERA5.TPQWL.2004-07.nc
clmforc.ERA5.TPQWL.2004-08.nc
clmforc.ERA5.TPQWL.2004-09.nc
clmforc.ERA5.TPQWL.2004-10.nc
clmforc.ERA5.TPQWL.2004-11.nc
clmforc.ERA5.TPQWL.2004-12.nc
clmforc.ERA5.TPQWL.2005-01.nc
clmforc.ERA5.TPQWL.2005-02.nc
clmforc.ERA5.TPQWL.2005-03.nc
clmforc.ERA5.TPQWL.2005-04.nc
clmforc.ERA5.TPQWL.2005-05.nc
clmforc.ERA5.TPQWL.2005-06.nc
clmforc.ERA5.TPQWL.2005-07.nc
clmforc.ERA5.TPQWL.2005-08.nc
clmforc.ERA5.TPQWL.2005-09.nc
clmforc.ERA5.TPQWL.2005-10.nc
clmforc.ERA5.TPQWL.2005-11.nc
clmforc.ERA5.TPQWL.2005-12.nc
clmforc.ERA5.TPQWL.2006-01.nc
clmforc.ERA5.TPQWL.2006-02.nc
clmforc.ERA5.TPQWL.2006-03.nc
clmforc.ERA5.TPQWL.2006-04.nc
clmforc.ERA5.TPQWL.2006-05.nc
clmforc.ERA5.TPQWL.2006-06.nc
clmforc.ERA5.TPQWL.2006-07.nc
clmforc.ERA5.TPQWL.2006-08.nc
clmforc.ERA5.TPQWL.2006-09.nc
clmforc.ERA5.TPQWL.2006-10.nc
clmforc.ERA5.TPQWL.2006-11.nc
clmforc.ERA5.TPQWL.2006-12.nc
clmforc.ERA5.TPQWL.2007-01.nc
clmforc.ERA5.TPQWL.2007-02.nc
clmforc.ERA5.TPQWL.2007-03.nc
clmforc.ERA5.TPQWL.2007-04.nc
clmforc.ERA5.TPQWL.2007-05.nc
clmforc.ERA5.TPQWL.2007-06.nc
clmforc.ERA5.TPQWL.2007-07.nc
clmforc.ERA5.TPQWL.2007-08.nc
clmforc.ERA5.TPQWL.2007-09.nc
clmforc.ERA5.TPQWL.2007-10.nc
clmforc.ERA5.TPQWL.2007-11.nc
clmforc.ERA5.TPQWL.2007-12.nc
clmforc.ERA5.TPQWL.2008-01.nc
clmforc.ERA5.TPQWL.2008-02.nc
clmforc.ERA5.TPQWL.2008-03.nc
clmforc.ERA5.TPQWL.2008-04.nc
clmforc.ERA5.TPQWL.2008-05.nc
clmforc.ERA5.TPQWL.2008-06.nc
clmforc.ERA5.TPQWL.2008-07.nc
clmforc.ERA5.TPQWL.2008-08.nc
clmforc.ERA5.TPQWL.2008-09.nc
clmforc.ERA5.TPQWL.2008-10.nc
clmforc.ERA5.TPQWL.2008-11.nc
clmforc.ERA5.TPQWL.2008-12.nc
clmforc.ERA5.TPQWL.2009-01.nc
clmforc.ERA5.TPQWL.2009-02.nc
clmforc.ERA5.TPQWL.2009-03.nc
clmforc.ERA5.TPQWL.2009-04.nc
clmforc.ERA5.TPQWL.2009-05.nc
clmforc.ERA5.TPQWL.2009-06.nc
clmforc.ERA5.TPQWL.2009-07.nc
clmforc.ERA5.TPQWL.2009-08.nc
clmforc.ERA5.TPQWL.2009-09.nc
clmforc.ERA5.TPQWL.2009-10.nc
clmforc.ERA5.TPQWL.2009-11.nc
clmforc.ERA5.TPQWL.2009-12.nc
clmforc.ERA5.TPQWL.2010-01.nc
clmforc.ERA5.TPQWL.2010-02.nc
clmforc.ERA5.TPQWL.2010-03.nc
clmforc.ERA5.TPQWL.2010-04.nc
clmforc.ERA5.TPQWL.2010-05.nc
clmforc.ERA5.TPQWL.2010-06.nc
clmforc.ERA5.TPQWL.2010-07.nc
clmforc.ERA5.TPQWL.2010-08.nc
clmforc.ERA5.TPQWL.2010-09.nc
clmforc.ERA5.TPQWL.2010-10.nc
clmforc.ERA5.TPQWL.2010-11.nc
clmforc.ERA5.TPQWL.2010-12.nc
clmforc.ERA5.TPQWL.2011-01.nc
clmforc.ERA5.TPQWL.2011-02.nc
clmforc.ERA5.TPQWL.2011-03.nc
clmforc.ERA5.TPQWL.2011-04.nc
clmforc.ERA5.TPQWL.2011-05.nc
clmforc.ERA5.TPQWL.2011-06.nc
clmforc.ERA5.TPQWL.2011-07.nc
clmforc.ERA5.TPQWL.2011-08.nc
clmforc.ERA5.TPQWL.2011-09.nc
clmforc.ERA5.TPQWL.2011-10.nc
clmforc.ERA5.TPQWL.2011-11.nc
clmforc.ERA5.TPQWL.2011-12.nc
clmforc.ERA5.TPQWL.2012-01.nc
clmforc.ERA5.TPQWL.2012-02.nc
clmforc.ERA5.TPQWL.2012-03.nc
clmforc.ERA5.TPQWL.2012-04.nc
clmforc.ERA5.TPQWL.2012-05.nc
clmforc.ERA5.TPQWL.2012-06.nc
clmforc.ERA5.TPQWL.2012-07.nc
clmforc.ERA5.TPQWL.2012-08.nc
clmforc.ERA5.TPQWL.2012-09.nc
clmforc.ERA5.TPQWL.2012-10.nc
clmforc.ERA5.TPQWL.2012-11.nc
clmforc.ERA5.TPQWL.2012-12.nc
clmforc.ERA5.TPQWL.2013-01.nc
clmforc.ERA5.TPQWL.2013-02.nc
clmforc.ERA5.TPQWL.2013-03.nc
clmforc.ERA5.TPQWL.2013-04.nc
clmforc.ERA5.TPQWL.2013-05.nc
clmforc.ERA5.TPQWL.2013-06.nc
clmforc.ERA5.TPQWL.2013-07.nc
clmforc.ERA5.TPQWL.2013-08.nc
clmforc.ERA5.TPQWL.2013-09.nc
clmforc.ERA5.TPQWL.2013-10.nc
clmforc.ERA5.TPQWL.2013-11.nc
clmforc.ERA5.TPQWL.2013-12.nc
clmforc.ERA5.TPQWL.2014-01.nc
clmforc.ERA5.TPQWL.2014-02.nc
clmforc.ERA5.TPQWL.2014-03.nc
clmforc.ERA5.TPQWL.2014-04.nc
clmforc.ERA5.TPQWL.2014-05.nc
clmforc.ERA5.TPQWL.2014-06.nc
clmforc.ERA5.TPQWL.2014-07.nc
clmforc.ERA5.TPQWL.2014-08.nc
clmforc.ERA5.TPQWL.2014-09.nc
clmforc.ERA5.TPQWL.2014-10.nc
clmforc.ERA5.TPQWL.2014-11.nc
clmforc.ERA5.TPQWL.2014-12.nc
clmforc.ERA5.TPQWL.2015-01.nc
clmforc.ERA5.TPQWL.2015-02.nc
clmforc.ERA5.TPQWL.2015-03.nc
clmforc.ERA5.TPQWL.2015-04.nc
clmforc.ERA5.TPQWL.2015-05.nc
clmforc.ERA5.TPQWL.2015-06.nc
clmforc.ERA5.TPQWL.2015-07.nc
clmforc.ERA5.TPQWL.2015-08.nc
clmforc.ERA5.TPQWL.2015-09.nc
clmforc.ERA5.TPQWL.2015-10.nc
clmforc.ERA5.TPQWL.2015-11.nc
clmforc.ERA5.TPQWL.2015-12.nc
clmforc.ERA5.TPQWL.2016-01.nc
clmforc.ERA5.TPQWL.2016-02.nc
clmforc.ERA5.TPQWL.2016-03.nc
clmforc.ERA5.TPQWL.2016-04.nc
clmforc.ERA5.TPQWL.2016-05.nc
clmforc.ERA5.TPQWL.2016-06.nc
clmforc.ERA5.TPQWL.2016-07.nc
clmforc.ERA5.TPQWL.2016-08.nc
clmforc.ERA5.TPQWL.2016-09.nc
clmforc.ERA5.TPQWL.2016-10.nc
clmforc.ERA5.TPQWL.2016-11.nc
clmforc.ERA5.TPQWL.2016-12.nc
clmforc.ERA5.TPQWL.2017-01.nc
clmforc.ERA5.TPQWL.2017-02.nc
clmforc.ERA5.TPQWL.2017-03.nc
clmforc.ERA5.TPQWL.2017-04.nc
clmforc.ERA5.TPQWL.2017-05.nc
clmforc.ERA5.TPQWL.2017-06.nc
clmforc.ERA5.TPQWL.2017-07.nc
clmforc.ERA5.TPQWL.2017-08.nc
clmforc.ERA5.TPQWL.2017-09.nc
clmforc.ERA5.TPQWL.2017-10.nc
clmforc.ERA5.TPQWL.2017-11.nc
clmforc.ERA5.TPQWL.2017-12.nc
clmforc.ERA5.TPQWL.2018-01.nc
clmforc.ERA5.TPQWL.2018-02.nc
clmforc.ERA5.TPQWL.2018-03.nc
clmforc.ERA5.TPQWL.2018-04.nc
clmforc.ERA5.TPQWL.2018-05.nc
clmforc.ERA5.TPQWL.2018-06.nc
clmforc.ERA5.TPQWL.2018-07.nc
clmforc.ERA5.TPQWL.2018-08.nc
clmforc.ERA5.TPQWL.2018-09.nc
clmforc.ERA5.TPQWL.2018-10.nc
clmforc.ERA5.TPQWL.2018-11.nc
clmforc.ERA5.TPQWL.2018-12.nc
clmforc.ERA5.TPQWL.2019-01.nc
clmforc.ERA5.TPQWL.2019-02.nc
clmforc.ERA5.TPQWL.2019-03.nc
clmforc.ERA5.TPQWL.2019-04.nc
clmforc.ERA5.TPQWL.2019-05.nc
clmforc.ERA5.TPQWL.2019-06.nc
clmforc.ERA5.TPQWL.2019-07.nc
clmforc.ERA5.TPQWL.2019-08.nc
clmforc.ERA5.TPQWL.2019-09.nc
clmforc.ERA5.TPQWL.2019-10.nc
clmforc.ERA5.TPQWL.2019-11.nc
clmforc.ERA5.TPQWL.2019-12.nc
clmforc.ERA5.TPQWL.2020-01.nc
clmforc.ERA5.TPQWL.2020-02.nc
clmforc.ERA5.TPQWL.2020-03.nc
clmforc.ERA5.TPQWL.2020-04.nc
clmforc.ERA5.TPQWL.2020-05.nc
clmforc.ERA5.TPQWL.2020-06.nc
clmforc.ERA5.TPQWL.2020-07.nc
clmforc.ERA5.TPQWL.2020-08.nc
clmforc.ERA5.TPQWL.2020-09.nc
clmforc.ERA5.TPQWL.2020-10.nc
clmforc.ERA5.TPQWL.2020-11.nc
clmforc.ERA5.TPQWL.2020-12.nc
clmforc.ERA5.TPQWL.2021-01.nc
clmforc.ERA5.TPQWL.2021-02.nc
clmforc.ERA5.TPQWL.2021-03.nc
clmforc.ERA5.TPQWL.2021-04.nc
clmforc.ERA5.TPQWL.2021-05.nc
clmforc.ERA5.TPQWL.2021-06.nc
clmforc.ERA5.TPQWL.2021-07.nc
clmforc.ERA5.TPQWL.2021-08.nc
clmforc.ERA5.TPQWL.2021-09.nc
clmforc.ERA5.TPQWL.2021-10.nc
clmforc.ERA5.TPQWL.2021-11.nc
clmforc.ERA5.TPQWL.2021-12.nc
clmforc.ERA5.TPQWL.2022-01.nc
clmforc.ERA5.TPQWL.2022-02.nc
clmforc.ERA5.TPQWL.2022-03.nc
clmforc.ERA5.TPQWL.2022-04.nc
clmforc.ERA5.TPQWL.2022-05.nc
clmforc.ERA5.TPQWL.2022-06.nc
clmforc.ERA5.TPQWL.2022-07.nc
clmforc.ERA5.TPQWL.2022-08.nc
clmforc.ERA5.TPQWL.2022-09.nc
clmforc.ERA5.TPQWL.2022-10.nc
clmforc.ERA5.TPQWL.2022-11.nc
clmforc.ERA5.TPQWL.2022-12.nc
clmforc.ERA5.TPQWL.2023-01.nc
clmforc.ERA5.TPQWL.2023-02.nc
clmforc.ERA5.TPQWL.2023-03.nc
clmforc.ERA5.TPQWL.2023-04.nc
clmforc.ERA5.TPQWL.2023-05.nc
clmforc.ERA5.TPQWL.2023-06.nc
clmforc.ERA5.TPQWL.2023-07.nc
clmforc.ERA5.TPQWL.2023-08.nc
clmforc.ERA5.TPQWL.2023-09.nc
clmforc.ERA5.TPQWL.2023-10.nc
clmforc.ERA5.TPQWL.2023-11.nc
clmforc.ERA5.TPQWL.2023-12.nc
   </fileNames>
   <offset>
      0
   </offset>
</fieldInfo>
</file>

EOF

}

# =====================================
# Customize MPAS stream files if needed
# =====================================

patch_mpas_streams() {

echo

}

# =====================================================
# Custom PE layout: custom-N where N is number of nodes
# =====================================================

custom_pelayout(){

if [[ ${PELAYOUT} == custom-* ]];
then
    echo $'\n CUSTOMIZE PROCESSOR CONFIGURATION:'

    # Number of cores per node (machine specific)
    if [ "${MACHINE}" == "pm-cpu" ]; then
        ncore=256
        hthrd=1  # hyper-threading
    else
        echo 'ERROR: MACHINE = '${MACHINE}' is not supported for current custom PE layout setting.'
        exit 400
    fi

    # Extract number of nodes
    tmp=($(echo ${PELAYOUT} | tr "-" " "))
    nnodes=${tmp[1]}

    # Applicable to all custom layouts
    pushd ${CASE_SCRIPTS_DIR}
    ./xmlchange NTASKS=1
    ./xmlchange NTHRDS=1
    ./xmlchange ROOTPE=0
    ./xmlchange MAX_MPITASKS_PER_NODE=$ncore
    ./xmlchange MAX_TASKS_PER_NODE=$(( $ncore * $hthrd))

    ###################################################
    # For ICASE runs

    ./xmlchange MAX_MPITASKS_PER_NODE="64"
    ./xmlchange MAX_TASKS_PER_NODE="256"

    ./xmlchange CPL_NTASKS=${MY_NPES}
    ./xmlchange ATM_NTASKS=${MY_NPES}
    ./xmlchange OCN_NTASKS=${MY_NPES}
    ./xmlchange OCN_ROOTPE=0

    ./xmlchange LND_NTASKS=${MY_NPES}
    ./xmlchange ROF_NTASKS=${MY_NPES}
    ./xmlchange ICE_NTASKS=${MY_NPES}
    ./xmlchange LND_ROOTPE=0
    ./xmlchange ROF_ROOTPE=0

    ./xmlchange NTHRDS_ATM="2"
    ./xmlchange NTHRDS_LND="2"
    ./xmlchange NTHRDS_ICE="2"
    ./xmlchange NTHRDS_OCN="2"
    ./xmlchange NTHRDS_CPL="2"
    ./xmlchange NTHRDS_GLC="1"
    ./xmlchange NTHRDS_ROF="2"
    ./xmlchange NTHRDS_WAV="1"

    popd

fi

}
######################################################
### Most users won't need to change anything below ###
######################################################

#-----------------------------------------------------
fetch_code() {

    if [ "${do_fetch_code,,}" != "true" ]; then
        echo $'\n----- Skipping fetch_code -----\n'
        return
    fi

    echo $'\n----- Starting fetch_code -----\n'
    local path=${CODE_ROOT}
    local repo=E3SM

    echo "Cloning $repo repository branch $BRANCH under $path"
    if [ -d "${path}" ]; then
        echo "ERROR: Directory already exists. Not overwriting"
        exit 20
    fi
    mkdir -p ${path}
    pushd ${path}

    # This will put repository, with all code
    git clone git@github.com:E3SM-Project/${repo}.git .

    # Check out desired branch
    git checkout ${BRANCH}

    # Custom addition
    if [ "${CHERRY}" != "" ]; then
        echo ----- WARNING: adding git cherry-pick -----
        for commit in "${CHERRY[@]}"
        do
            echo ${commit}
            git cherry-pick ${commit}
        done
        echo -------------------------------------------
    fi

    # Bring in all submodule components
    git submodule update --init --recursive

    popd
}

#-----------------------------------------------------
create_newcase() {

    if [ "${do_create_newcase,,}" != "true" ]; then
        echo $'\n----- Skipping create_newcase -----\n'
        return
    fi

    echo $'\n----- Starting create_newcase -----\n'

    if [[ ${PELAYOUT} == custom-* ]];
    then
        layout="M" # temporary placeholder for create_newcase
    else
        layout=${PELAYOUT}

    fi

    # Base arguments
    args=" --case ${CASE_NAME} \
        --output-root ${CASE_ROOT} \
        --script-root ${CASE_SCRIPTS_DIR} \
        --handle-preexisting-dirs u \
        --compset ${COMPSET} \
        --walltime ${WALLTIME} \
        --res ${RESOLUTION} \
        --machine ${MACHINE} \
        --pecount ${PELAYOUT}"

    # Oprional arguments
    if [ ! -z "${PROJECT}" ]; then
      args="${args} --project ${PROJECT}"
    fi
    if [ ! -z "${CASE_GROUP}" ]; then
      args="${args} --case-group ${CASE_GROUP}"
    fi
    if [ ! -z "${QUEUE}" ]; then
      args="${args} --queue ${QUEUE}"
    fi

    # For Dane, force it
    args="${args} --queue pdebug"
    
    echo "HERE" ${args}

    ${CODE_ROOT}/cime/scripts/create_newcase ${args}

    if [ $? != 0 ]; then
      echo $'\nNote: if create_newcase failed because sub-directory already exists:'
      echo $'  * delete old case_script sub-directory'
      echo $'  * or set do_newcase=false\n'
      exit 35
    fi

}

#-----------------------------------------------------
case_setup() {

    if [ "${do_case_setup,,}" != "true" ]; then
        echo $'\n----- Skipping case_setup -----\n'
        return
    fi

    echo $'\n----- Starting case_setup -----\n'
    pushd ${CASE_SCRIPTS_DIR}

    ./xmlchange EPS_AGRID=1e-9
    ./xmlchange CALENDAR="GREGORIAN"

    # Setup some CIME directories
    ./xmlchange EXEROOT=${CASE_BUILD_DIR}
    ./xmlchange RUNDIR=${CASE_RUN_DIR}

    # Short term archiving
    ./xmlchange DOUT_S=${DO_SHORT_TERM_ARCHIVING^^}
    ./xmlchange DOUT_S_ROOT=${CASE_ARCHIVE_DIR}

    # Extracts input_data_dir in case it is needed for user edits to the namelist later
    local input_data_dir=`./xmlquery DIN_LOC_ROOT --value`

    # Custom user_nl
    user_nl

    # Finally, run CIME case.setup
    ./case.setup --reset

    popd
}

#-----------------------------------------------------
case_build() {

    pushd ${CASE_SCRIPTS_DIR}

    # do_case_build = false
    if [ "${do_case_build,,}" != "true" ]; then

        echo $'\n----- case_build -----\n'

        if [ "${OLD_EXECUTABLE}" == "" ]; then
            # Ues previously built executable, make sure it exists
            if [ -x ${CASE_BUILD_DIR}/e3sm.exe ]; then
                echo 'Skipping build because $do_case_build = '${do_case_build}
            else
                echo 'ERROR: $do_case_build = '${do_case_build}' but no executable exists for this case.'
                exit 297
            fi
        else
            # If absolute pathname exists and is executable, reuse pre-exiting executable
            if [ -x ${OLD_EXECUTABLE} ]; then
                echo 'Using $OLD_EXECUTABLE = '${OLD_EXECUTABLE}
                cp -fp ${OLD_EXECUTABLE} ${CASE_BUILD_DIR}/
            else
                echo 'ERROR: $OLD_EXECUTABLE = '$OLD_EXECUTABLE' does not exist or is not an executable file.'
                exit 297
            fi
        fi
        echo 'WARNING: Setting BUILD_COMPLETE = TRUE.  This is a little risky, but trusting the user.'
        ./xmlchange BUILD_COMPLETE=TRUE

    # do_case_build = true
    else

        echo $'\n----- Starting case_build -----\n'

        # Turn on debug compilation option if requested
        if [ "${DEBUG_COMPILE^^}" == "TRUE" ]; then
            ./xmlchange DEBUG=${DEBUG_COMPILE^^}
        fi

        # Run CIME case.build
        ./case.build

    fi

    # Some user_nl settings won't be updated to *_in files under the run directory
    # Call preview_namelists to make sure *_in and user_nl files are consistent.
    echo $'\n----- Preview namelists -----\n'
    ./preview_namelists

    popd
}

#-----------------------------------------------------
runtime_options() {

    echo $'\n----- Starting runtime_options -----\n'
    pushd ${CASE_SCRIPTS_DIR}

    ./xmlchange JOB_WALLCLOCK_TIME=${WALLTIME}

    # Set simulation start date
    ./xmlchange RUN_STARTDATE=${START_DATE}

    # Segment length
    ./xmlchange STOP_OPTION=${STOP_OPTION,,},STOP_N=${STOP_N}

    # Restart frequency
    ./xmlchange REST_OPTION=${REST_OPTION,,},REST_N=${REST_N}

    # Coupler history
    ./xmlchange HIST_OPTION=${HIST_OPTION,,},HIST_N=${HIST_N}

    # Coupler budgets (always on)
    ./xmlchange BUDGETS=TRUE

    # Set resubmissions
    if (( RESUBMIT > 0 )); then
        ./xmlchange RESUBMIT=${RESUBMIT}
    fi

    # Run type
    # Start from default of user-specified initial conditions
    if [ "${MODEL_START_TYPE,,}" == "initial" ]; then
        ./xmlchange RUN_TYPE="startup"
        ./xmlchange CONTINUE_RUN="FALSE"

    # Continue existing run
    elif [ "${MODEL_START_TYPE,,}" == "continue" ]; then
        ./xmlchange CONTINUE_RUN="TRUE"
	echo "Prepare the restart files - copy restart-point files over to ../run for the relocated case"

    elif [ "${MODEL_START_TYPE,,}" == "branch" ] || [ "${MODEL_START_TYPE,,}" == "hybrid" ]; then
        ./xmlchange RUN_TYPE=${MODEL_START_TYPE,,}
        ./xmlchange GET_REFCASE=${GET_REFCASE}
        ./xmlchange RUN_REFDIR=${RUN_REFDIR}
        ./xmlchange RUN_REFCASE=${RUN_REFCASE}
        ./xmlchange RUN_REFDATE=${RUN_REFDATE}
        echo 'Warning: $MODEL_START_TYPE = '${MODEL_START_TYPE} 
        echo '$RUN_REFDIR = '${RUN_REFDIR}
        echo '$RUN_REFCASE = '${RUN_REFCASE}
        echo '$RUN_REFDATE = '${START_DATE}
    else
        echo 'ERROR: $MODEL_START_TYPE = '${MODEL_START_TYPE}' is unrecognized. Exiting.'
        exit 380
    fi

    # Patch mpas streams files
    patch_mpas_streams

    popd
}

#-----------------------------------------------------
case_submit() {

    if [ "${do_case_submit,,}" != "true" ]; then
        echo $'\n----- Skipping case_submit -----\n'
        return
    fi

    echo $'\n----- Starting case_submit -----\n'
    pushd ${CASE_SCRIPTS_DIR}
    
    # Run CIME case.submit
    ./case.submit

    popd
}

#-----------------------------------------------------
copy_script() {

    echo $'\n----- Saving run script for provenance -----\n'

    local script_provenance_dir=${CASE_SCRIPTS_DIR}/run_script_provenance
    mkdir -p ${script_provenance_dir}
    local this_script_name=`basename $0`
    local script_provenance_name=${this_script_name}.`date +%Y%m%d-%H%M%S`
    cp -vp ${this_script_name} ${script_provenance_dir}/${script_provenance_name}

}

#-----------------------------------------------------
# Silent versions of popd and pushd
pushd() {
    command pushd "$@" > /dev/null
}
popd() {
    command popd "$@" > /dev/null
}

# Now, actually run the script
#-----------------------------------------------------
main
