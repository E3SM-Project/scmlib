import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/MAGIC_analysis/15A_Obs_diag_v2.nc"
output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/obs_data/MAGIC_snd_OBS.dpxx.nc"
time_offset = 1.25

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
time_data = ds_in["time_snd"].values
ds_out["time"] = xr.DataArray(time_data - time_offset, dims=["time"])

# This file will only have 1d data, make up vertical coordinates to satisfy diagnostics package requirements.

z_data = ds_in["z_snd"].values[::-1] # just a dummy variable
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# Define lists for variables
two_d_vars = [
    ("zi_pbl_snd", "pbl_height_horiz_avg", 1.0),
]

# Define lists for variables
three_d_vars = [
    ("rh_snd", "RelativeHumidity_horiz_avg", 1.0),
    ("q_snd", "qv_horiz_avg",1.0/1000.),
    ("t_snd", "T_mid_horiz_avg",1.0),
    ("p_snd", "P_mid_horiz_avg",1.0),
    ("theta_snd", "PotentialTemperature_horiz_avg",1.0),
]

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    if var_in in ds_in:
        ds_out[var_out] = xr.DataArray(np.squeeze(ds_in[var_in].values), dims=["time"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Process 3D variables
for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_val = np.squeeze(ds_in[var_in].values)[:,::-1]
        print(np.shape(data_val))
        ds_out[var_out] = xr.DataArray(data_val, dims=["time", "lev"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Add the units attribute
ds_out["time"].attrs["units"] = "days since 2013-07-21 05:27:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

