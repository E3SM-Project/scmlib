import xarray as xr
import numpy as np
import os
import csv

def csv_read_in(filename):

    file=open(filename)
    csvreader=csv.reader(file)

    data=[]
    for row in csvreader:
        data.append(row)

    floatdata=np.float_(data)
    return floatdata

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/603_obs/GOAMAZON_day603.csv"
output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/GOAMAZON_doublepulse.obs.radar_precip.dpxx_format.nc"
time_offset = 168.5

# Ensure the directory for the output file exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

# Read in dataset
prect_in=csv_read_in(input_file)

# time stored in prect_in[:,0]
# precip values stored in prect_in[:,1]

prect_in[:,0]=(prect_in[:,0]-8.0)/24.

# Create a new dataset for the output
ds_out = xr.Dataset()

# Assign filtered time to output dataset
ds_out["time"] = xr.DataArray(prect_in[:,0], dims=["time"])


# This file will only have 1d data, make up vertical coordinates to satisfy diagnostics package requirements.

z_data = [10,20]
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# Define lists for variables
two_d_vars = [
    ("cld_frac", "precip_total_surf_mass_flux_horiz_avg", 0.001/3600.0),
]

# Process 2D variables

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    ds_out[var_out] = xr.DataArray(np.squeeze(prect_in[:,1]), dims=["time"]) * factor

# Clip all variables in ds_out to ensure no values are below zero
for var_name in ds_out.data_vars:
    da = ds_out[var_name]
    if np.issubdtype(da.dtype, np.number):  # Only apply to numeric types
        ds_out[var_name] = da.clip(min=0)

# Add the units attribute
ds_out["precip_total_surf_mass_flux_horiz_avg"].attrs["units"]="m/s"
ds_out["time"].attrs["units"] = "days since 2015-08-26 12:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

