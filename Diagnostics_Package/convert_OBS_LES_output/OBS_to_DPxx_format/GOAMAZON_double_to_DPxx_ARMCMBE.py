import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/ARM_obs/maoarmbecldradM1.c1.20150101.003000.nc"
output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/GOAMAZON_doublepulse.obs.ARMCMBE.dpxx_format.nc"
time_offset = 168.5

# Ensure the directory for the output file exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

# Open the input file
ds_in = xr.open_dataset(input_file,decode_times=False)

# Create a new dataset for the output
ds_out = xr.Dataset()

# 1. Transfer and adjust the "time" variable
time_data = ds_in["time"].values
# convert time from seconds to days
#ds_out["time"] = xr.DataArray(time_data/86400. - time_offset, dims=["time"])

# Convert time from seconds to days
time_days = time_data / 86400.0 - time_offset

# Filter for time values between day 0 and 0.5
time_filtered = (time_days >= 0.0) & (time_days <= 0.5)

# Apply filtering to input dataset
ds_in = ds_in.isel(time=time_filtered)

# Assign filtered time to output dataset
ds_out["time"] = xr.DataArray(time_days[time_filtered], dims=["time"])


# This file will only have 1d data, make up vertical coordinates to satisfy diagnostics package requirements.

z_data = ds_in["height"].values[::-1] # just a dummy variable
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# Define lists for variables
three_d_vars = [
    ("cld_frac", "cldfrac_tot_for_analysis_horiz_avg", 1.0/100.0),
]

# Process 3D variables

for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_val = np.squeeze(ds_in[var_in].values)[:,::-1]
        print(np.shape(data_val))
        ds_out[var_out] = xr.DataArray(data_val, dims=["time", "lev"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Clip all variables in ds_out to ensure no values are below zero
for var_name in ds_out.data_vars:
    da = ds_out[var_name]
    if np.issubdtype(da.dtype, np.number):  # Only apply to numeric types
        ds_out[var_name] = da.clip(min=0)

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Add the units attribute
ds_out["time"].attrs["units"] = "days since 2015-08-26 12:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

