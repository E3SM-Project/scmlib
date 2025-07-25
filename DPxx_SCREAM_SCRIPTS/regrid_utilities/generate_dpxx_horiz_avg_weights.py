# -*- coding: utf-8 -*-
"""

NOTE: This script is now obsolete as there is a much EASIER way to get horizontally averaged
output in DPxx.  That is to append any variable name in your YAML file with "_horiz_avg".
Will retain this script for legacy purposes and because there could be some edge use cases
where this script is still handy.

Will generate a mapping file to produce horizontally averaged output
during runtime for DPxx simulations. NOTE that these simple mapping files
will ONLY work for online DPxx remapping and not offline. The eamxx online
horizontal mapping only needs S (sparse matrix for weights), col, row, which is
what the script does. The map file used for offline mapping (.e.g., nco) requires
other "nominal" variables (frac_a/b, area_a/b, yc_a/b, xc_a/b, yv_a/b, xv_a/b,
src_grid_dims, dst_grid_dims). These nominal variables require other procedures
to generate (e.g., by a complex art of ESMF-NCL), but some field values are meaningless
in DPxx cases and are indeed not required by online mapping.

User only needs to supply basic geometry data for their DPxx simulation.  This
needs to be exactly the same as you've specified in your run script for
num_ne_x, num_ne_y, domain_size_x, domain_size_y.

Once you have generated your mapping file simply point to it in your YAML file like so:
horiz_remap_file: /path/to/your/file/mapping_dpxx_x200000m_y200000m_nex20_ney20_to_1x1.20241024.nc

Script authors: Peter Bogenschutz (bogenschutz1@llnl.gov)
                Jishi Zhang (zhang73@llnl.gov)
"""

import netCDF4 as nc4
import numpy as np
import os
from datetime import datetime

#######################################################################
###### Start user input

# These geometry parameters should match what you plan to use in your simulation
num_ne_x=166
num_ne_y=12
domain_size_x=6000000
domain_size_y=432000

# Supply path where mapping file will be placed
outputpath="/global/homes/b/bogensch/dp_scream_scripts_xx/remap_files/"

###### End user input
#######################################################################

# Figure out number of physics columns
phys_col=num_ne_x*num_ne_y*4

# Compute the physics resolution
dx=float(domain_size_x)/(num_ne_x*2.0)
dy=float(domain_size_y)/(num_ne_y*2.0)

# Compute the area of each column
area_col=dx*dy
area_dom=float(domain_size_x)*float(domain_size_y)

S_in=np.float64(area_col/area_dom)
col_in=np.arange(phys_col)+1
row_in=np.ones(phys_col)

### Now make the output file

# what is the current date?
current_date = datetime.now()
formatted_date = current_date.strftime("%Y%m%d")

# Make output string
filename="mapping_dpxx_x"+str(domain_size_x)+"m_y"+str(domain_size_y)+\
         "m_nex"+str(num_ne_x)+"_ney"+str(num_ne_y)+"_to_1x1."+formatted_date+".nc"

fullfile=outputpath+filename

# check to see if outputfile already exists, if so overwrite
ishere=os.path.isfile(fullfile)
if ishere:
   os.system('rm '+fullfile)

f=nc4.Dataset(fullfile,'w',format='NETCDF4')
f.createDimension('n_s',phys_col)
f.createDimension('n_a',phys_col)
f.createDimension('n_b',1)

S=f.createVariable('S','f8','n_s')
col=f.createVariable('col','i4','n_s')
row=f.createVariable('row','i4','n_s')

S[:]=np.full(phys_col, S_in, dtype='float64')
col[:]=col_in
row[:]=row_in

f.close()

print("Generated file: ",fullfile)
