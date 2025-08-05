import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file = "/pscratch/sd/b/bogensch/E3SM_simulations/ARMdata/sgpinterpolatedsondeC1.c1.20170823_24.000030.nc"
output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/LAFE.obs.sounding.dpxx_format.nc"

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
ds_out["time"] = xr.DataArray((time_data - 41400.)/86400., dims=["time"])

z_data = ds_in["height"].values[::-1] # just a dummy variable
z_mid = np.tile(z_data, (len(ds_out["time"]), 1))
print(np.shape(z_mid))
print(z_mid[:,-1])
z_mid = z_mid - z_mid[:,-1][:, None]
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid, dims=["time", "lev"]) * 1000. # convert to m

# Define lists for variables
three_d_vars = [
    ("temp", "T_mid_horiz_avg", 1.0),
    ("vap_pres", "qv_horiz_avg", 1.0),
    ("temp", "PotentialTemperature_horiz_avg", 1.0)
]

# Process 3D variables

# Constants for theta calculation
Rd = 287.05  # J/kg/K
Cp = 1004.6  # J/kg/K

for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_val = np.squeeze(ds_in[var_in].values)[:, ::-1]  # reverse vertical

        if var_out == "T_mid_horiz_avg":
            temp_K = data_val + 273.15
            ds_out[var_out] = xr.DataArray(temp_K, dims=["time", "lev"])

        elif var_out == "qv_horiz_avg":
            # Read vap_pres and pressure (reverse vertical to match)
            vap_pres = np.squeeze(ds_in["vap_pres"].values)[:, ::-1] * 10.0  # hPa to Pa
            pressure = np.squeeze(ds_in["bar_pres"].values)[:, ::-1] * 10.0  # hPa to Pa
            qv = 621.97 * (vap_pres / (pressure - vap_pres))
            ds_out[var_out] = xr.DataArray(qv, dims=["time", "lev"])/1000.

        elif var_out == "PotentialTemperature_horiz_avg":
            # Reuse temp_K and pressure from earlier
            temp_K = np.squeeze(ds_in["temp"].values)[:, ::-1] + 273.15
            pressure = np.squeeze(ds_in["bar_pres"].values)[:, ::-1] * 10.0  # hPa to Pa
            theta = temp_K * (1000.0 / pressure) ** (Rd / Cp)
            ds_out[var_out] = xr.DataArray(theta, dims=["time", "lev"])

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
ds_out["time"].attrs["units"] = "days since 2017-08-23 11:30:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

