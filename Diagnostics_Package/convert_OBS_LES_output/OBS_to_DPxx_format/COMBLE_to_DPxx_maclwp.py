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

# ----------------------------------------------------------------------
# Load and prepare input data
# ----------------------------------------------------------------------
data = pd.read_csv(input_file)

maclwp_time = data['time'].values / 3600.0 + 2.0  # hours
maclwp = data['lwp_bu'].values

# Sort by time
sorted_indices = np.argsort(maclwp_time)
maclwp_time = maclwp_time[sorted_indices]
maclwp = maclwp[sorted_indices]

# Convert hours -> days
maclwp_time = maclwp_time / 24.0

print(np.shape(maclwp))

# ----------------------------------------------------------------------
# Build output dataset
# ----------------------------------------------------------------------
ds_out = xr.Dataset()

# 1) Prepend a new time=0 without overwriting existing first value
#    (shift all original times to the next index)
time_with_leading_zero = np.concatenate(([0.0], maclwp_time.astype(float)))
ds_out["time"] = xr.DataArray(time_with_leading_zero, dims=["time"])
ds_out["time"].attrs["units"] = "days since 2020-03-12 22:00:00"

# 2) Minimal vertical info to satisfy diagnostics (kept numeric)
z_data = [10.0, 20.0]
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# 3) Define and populate 1-D time series variables
two_d_vars = [
    ("dummy", "LiqWaterPath_horiz_avg", 1.0),
]

for var_in, var_out, factor in two_d_vars:
    # Allocate with the NEW time length, set first value NaN, then copy original data
    arr = np.empty(len(ds_out["time"]), dtype=float)
    arr[:] = np.nan  # initialize to NaN
    arr[1:] = np.squeeze(maclwp) * factor  # shift original data by one index
    ds_out[var_out] = xr.DataArray(arr, dims=["time"])

# 4) Clip numeric variables to be >= 0 (NaNs are preserved)
for var_name in ds_out.data_vars:
    da = ds_out[var_name]
    if np.issubdtype(da.dtype, np.number):
        ds_out[var_name] = da.clip(min=0)

# 5) Units/attrs
ds_out["LiqWaterPath_horiz_avg"].attrs["units"] = "kg/m2"

# 6) (Safety) Ensure all 1-D time series variables have NaN at the first (new) time
#    This covers any future additions like more *_horiz_avg time series.
for var_name, da in ds_out.data_vars.items():
    if ("time",) == da.dims:  # only 1-D time series
        ds_out[var_name][0] = np.nan

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")
