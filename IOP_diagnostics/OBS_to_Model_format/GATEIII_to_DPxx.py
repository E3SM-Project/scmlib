import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file = "/global/cfs/cdirs/e3sm/inputdata/atm/cam/scam/iop/GATEIII_iopfile_4scam.nc"
output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/obs_data/OBS_GATEIII.dpxx.nc"
time_offset = 0.0

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
time_data = ds_in["tsec"].values
time_data = (time_data-time_data[0])/86400.
ds_out["time"] = xr.DataArray(time_data - time_offset, dims=["time"])

p_data = ds_in["lev"].values/100.
p_mid_obs = np.tile(p_data, (len(ds_out["time"]), 1))
ds_out["p_mid_obs"] = xr.DataArray(p_mid_obs, dims=["time", "lev"])

# 3. Define lists for 3D and 2D variables
three_d_vars = [
    ("q", "qv_horiz_avg", 1.0),
    ("u", "U_horiz_avg", 1.0),
    ("v", "V_horiz_avg", 1.0),
    ("T", "T_mid_horiz_avg", 1.0),
    ("relhum", "RelativeHumidity_horiz_avg", 1.0/100.0)
]

two_d_vars = [
    ("Prec", "precip_total_surf_mass_flux_horiz_avg", 1.0)
]

# ("", "", ),

# Process 3D variables

for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_val = np.squeeze(ds_in[var_in].values)
        print(np.shape(data_val))
        ds_out[var_out] = xr.DataArray(data_val, dims=["time", "lev"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    if var_in in ds_in:
        ds_out[var_out] = xr.DataArray(np.squeeze(ds_in[var_in].values), dims=["time"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Add the units attribute
ds_out["time"].attrs["units"] = "days since 1974-08-30 00:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

