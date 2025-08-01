import xarray as xr
import numpy as np
import pandas as pd
import os
import csv

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/COMBLE_obs/maclwp_dat.csv"
output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/COMBLE.obs.maclwp.dpxx_format.nc"

# Ensure the directory for the output file exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

data = pd.read_csv(input_file)

maclwp_time = data['time'].values / 3600. + 2.  # unit: hr
maclwp = data['lwp_bu'].values

# Sort by time
sorted_indices = np.argsort(maclwp_time)
maclwp_time = maclwp_time[sorted_indices]
maclwp = maclwp[sorted_indices]

maclwp_time = maclwp_time/24.

print(np.shape(maclwp))

# Create a new dataset for the output
ds_out = xr.Dataset()

# Assign filtered time to output dataset
ds_out["time"] = xr.DataArray(maclwp_time, dims=["time"])

# This file will only have 1d data, make up vertical coordinates to satisfy diagnostics package requirements.

z_data = [10.0,20.0]
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# Define lists for variables
two_d_vars = [
    ("dummy", "LiqWaterPath_horiz_avg", 1.0),
]

# Process 2D variables

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    ds_out[var_out] = xr.DataArray(np.squeeze(maclwp), dims=["time"]) * factor

# Clip all variables in ds_out to ensure no values are below zero
for var_name in ds_out.data_vars:
    da = ds_out[var_name]
    if np.issubdtype(da.dtype, np.number):  # Only apply to numeric types
        ds_out[var_name] = da.clip(min=0)

# Add the units attribute
ds_out["LiqWaterPath_horiz_avg"].attrs["units"]="kg/m2"
ds_out["time"].attrs["units"] = "days since 2020-03-12 22:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

