## ARM/ASR Diagnostics Package for E3SM SCM and DP-EAMxx

This is a diagnostics package for the E3SM SCM and Doubly-Periodic Configuration of EAMxx (DP-EAMxx).

This diagnostics package is used by selecting the example script:

`diagnostics_user_driver.py`

Make a copy of this, which will be ignored by git.  This script then needs to be edited to add
the relevant data sets, case specifics, observation files, and plotting styles to fit the user's needs.
The new user script can then be executed after loading the suitable environment (see Setup Notes).
