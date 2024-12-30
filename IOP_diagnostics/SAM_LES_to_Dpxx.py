import xarray as xr
import numpy as np

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/SAM_LES/MAG3D.15A.20130720.1729_105h_128x128x460_LES.nc"
output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_MAGIC.les.001a/run/SAM_MAGIC.les.001a.horiz_avg.AVERAGE.nmins_x5.2013-07-21-19620.nc"
time_offset = 201.25

# Open the input file
ds_in = xr.open_dataset(input_file)

# Create a new dataset for the output
ds_out = xr.Dataset()

# 1. Transfer and adjust the "time" variable
time_data = ds_in["time"].values
ds_out["time"] = xr.DataArray(time_data - time_offset, dims=["time"])

# 2. Transfer and rename "z" to "z_mid_les"
# Repeat the z profile for each time index
z_data = ds_in["z"].values
z_data_flipped = z_data[::-1]  # Flip the "z" array
z_mid_les = np.tile(z_data_flipped, (len(ds_out["time"]), 1))
ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid_les, dims=["time", "lev"])

p_data = ds_in["p"].values
p_data_flipped = p_data[::-1]  # Flip the "p" array
p_mid_les = np.tile(p_data_flipped, (len(ds_out["time"]), 1))
ds_out["p_mid_les"] = xr.DataArray(p_mid_les, dims=["time", "lev"])

# 3. Define lists for 3D and 2D variables
three_d_vars = [
    ("CLD", "cldfrac_tot_for_analysis_horiz_avg", 1.0),
    ("QCL", "qc_horiz_avg", 0.001),
    ("QPL", "qr_horiz_avg", 0.001),
]

two_d_vars = [
    ("SHF", "surf_sens_flux_horiz_avg", 1.0),
    ("LHF", "surf_evap_horiz_avg", 4e-7),
]

# Process 3D variables
for var_in, var_out, factor in three_d_vars:
    data_flipped = ds_in[var_in].values[:, ::-1]
    ds_out[var_out] = xr.DataArray(data_flipped, dims=["time", "lev"]) * factor

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    ds_out[var_out] = xr.DataArray(ds_in[var_in].values, dims=["time"]) * factor

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

