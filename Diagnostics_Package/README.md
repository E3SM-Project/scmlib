## ARM/ASR Diagnostics Package for E3SM SCM and DP-EAMxx

This is a diagnostics package for the E3SM SCM and Doubly-Periodic Configuration of EAMxx (DP-EAMxx).

This diagnostics package is used by selecting the example script:

`diagnostics_user_driver.py`

Make a copy of this, which will be ignored by git.  This script then needs to be edited to add
the relevant data sets, case specifics, observation files, and plotting styles to fit the user's needs.
The new user script can then be executed after loading the suitable environment (see Setup Notes).

Development of this diagnostics package was primarily supported by the Atmospheric System Research program, Tying in High Resolution E3SM with ARM Data (THREAD) project (SCW1800) and partially supported by the Atmospheric Radiation Measurement (ARM) program, funded by the U.S. Department of Energy (DOE), Office of Science, Office of Biological and Environmental Research.

--------------------------------------------------------------------------------

### TABLE OF CONTENTS
  - [Package Overview](#package-overview)
  - [Setup Notes](#setup-notes)
  - [Valid E3SM SCM Input Data](#valid-e3sm-scm-input-data)
  - [Valid DP-EAMxx Input Data](#valid-dp-eamxx-input-data)
  - [Adding Datasets](#adding-datasets)
  - [User Specifications](#user-specifications)
  - [Observation and LES Datasets](#observation-and-les-datasets)
  - [Development Plans](#development-plans)

--------------------------------------------------------------------------------

### Package Overview

This diagnostics package is designed to provide users with a simple, user-friendly interface for quickly evaluating process-level simulations using the E3SM SCM and DP-EAMxx configurations. It also facilitates straightforward comparisons with ARM observations and large eddy simulation (LES) results, where available. The package is not intended for generating publication quality figures or performing advanced analysis. Rather, it offers a basic suite of plots to help users assess the fidelity of their simulations and identify areas for more detailed investigation. 

--------------------------------------------------------------------------------

### Setup Notes

It is recommended to use the E3SM unified environment to run this package.

On Perlmutter:

`source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh`

On Chrysalis:

`source /lcrc/soft/climate/e3sm-unified/load_latest_e3sm_unified_chrysalis.sh`

Alternatively a user can create their own environment, if they wish.  The following packages would be needed in such an environment:
  ```
  conda create --name e3sm_asr_diag python=3.10 -c conda-forge xarray numpy matplotlib jinja2 netCDF4 scipy 
  ```
After creating the environment it can be activated via:

  `source activate e3sm_asr_diag`

--------------------------------------------------------------------------------

### Valid E3SM SCM Input Data

--------------------------------------------------------------------------------

### Valid DP-EAMxx Input Data

--------------------------------------------------------------------------------

### Adding Datasets

--------------------------------------------------------------------------------

### User Specifications

--------------------------------------------------------------------------------

### Observation and LES Files

--------------------------------------------------------------------------------

### Development Plans


