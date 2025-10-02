import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file1 = "/global/homes/b/bogensch/THREAD/CASS_obs/cass_obs_lwp_m2.nc"
input_file2 = "/global/homes/b/bogensch/THREAD/CASS_obs/cass_obs_shortwave_down.nc"
input_file3 = "/global/homes/b/bogensch/THREAD/CASS_obs/cass_obs_longwave_down.nc"
output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/CASS.obs.1dvars.dpxx_format.nc"
time_offset = 0.0

# Ensure the directory for the output file exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

# Open the input file
ds_in1 = xr.open_dataset(input_file1,decode_times=False)
ds_in2 = xr.open_dataset(input_file2,decode_times=False)
ds_in3 = xr.open_dataset(input_file3,decode_times=False)

# Create a new dataset for the output
ds_out = xr.Dataset()

# 1. Transfer and adjust the "time" variable
time_data = ds_in1["hour"].values - 6.0
ds_out["time"] = xr.DataArray((time_data - 0.5)/24.0, dims=["time"])

# This file will only have 1d data, make up vertical coordinates to satisfy diagnostics package requirements.

z_data = [10.0,20.0]
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"])

# Define lists for variables
two_d_vars = [
    ("lwp_m3", "LiqWaterPath_horiz_avg", 1.0/1000.0),
    ("swdn_m0", "SW_flux_dn_at_model_bot_horiz_avg", 1.0),
    ("lwdn_m0", "LW_flux_dn_at_model_bot_horiz_avg", 1.0),
]

# Process 2D variables
for var_in, var_out, factor in two_d_vars:

    if var_in == "lwp_m3":
        data_in = np.squeeze(ds_in1["lwp_m3"].values)

    if var_in == "swdn_m0":
        data_in = np.squeeze(ds_in2["swdn_m0"].values)

    if var_in == "lwdn_m0":
        data_in = np.squeeze(ds_in3["lwdn_m0"].values)    
    
    ds_out[var_out] = xr.DataArray(np.squeeze(data_in), dims=["time"]) * factor

# Clip all variables in ds_out to ensure no values are below zero
for var_name in ds_out.data_vars:
    da = ds_out[var_name]
    if np.issubdtype(da.dtype, np.number):  # Only apply to numeric types
        ds_out[var_name] = da.clip(min=0)

ds_out["LiqWaterPath_horiz_avg"].attrs["units"]="kg/m2"
ds_out["SW_flux_dn_at_model_bot_horiz_avg"].attrs["units"]="W/m2"
ds_out["LW_flux_dn_at_model_bot_horiz_avg"].attrs["units"]="W/m2"

# Add the units attribute
ds_out["time"].attrs["units"] = "days since 2000-07-24 12:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

