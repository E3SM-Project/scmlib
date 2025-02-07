import xarray as xr
import numpy as np
import os

outpath="/pscratch/sd/b/bogensch/dp_screamxx_conv/les_data/"

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/CASS_LES/thick_512x512x156_50m_50m_1s.nc"
output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_CASS.les.001a/run/SAM_CASS.les.001a.horiz_avg.AVERAGE.nmins_x5.2000-07-24-43200.nc"
time_offset = 205.5017

# Define input and output file paths
#input_file = "/global/homes/b/bogensch/THREAD/SAM_LES/GATE_IDEAL_S_2048x2048x256_100m_2s.nc"
#output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_GATEIDEAL.les.001a/run/SAM_GATEIDEAL.les.001a.horiz_avg.AVERAGE.nmins_x5.1974-08-30-00000.nc"
#time_offset = 0.0

# Define input and output file paths
#input_file = "/global/homes/b/bogensch/THREAD/SAM_LES/GATE_IDEAL_S_2048x2048x256_100m_2s.nc"
#output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_GATEIDEAL.les.001a/run/SAM_GATEIDEAL.les.001a.horiz_avg.AVERAGE.nmins_x5.1974-08-30-00000.nc"
#time_offset = 0.0

# Define input and output file paths
input_file = "/global/homes/b/bogensch/THREAD/SAM_LES/MAG3D.15A.20130720.1729_105h_128x128x460_LES.nc"
output_file = outpath+"SAM_MAGIC.les.e3sm.nc"
time_offset = 201.25

#input_file = "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/LESfiles/GOAMAZON_goamazon_278_test1.nc"
#output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_GOAMAZON.single.les.001a/run/SAM_GOAMAZON.single.les.001a.horiz_avg.AVERAGE.nmins_x5.2014-10-05-43200.nc"
#time_offset = 278.5042

#input_file = "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/LESfiles/GOAMAZON_goamazon_603_test3.nc"
#output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_GOAMAZON.double.les.001a/run/SAM_GOAMAZON.double.les.001a.horiz_avg.AVERAGE.nmins_x5.2015-08-26-43200.nc"
#time_offset = 603.5021

# Define input and output file paths
#input_file = "/global/homes/b/bogensch/THREAD/SAM_LES/COMBLE_MIP_V2.4_with_ice_vm.nc"
#output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/SAM_COMBLE.les.001a/run/SAM_COMBLE.les.001a.horiz_avg.AVERAGE.nmins_x5.2020-03-12-79200.nc"
#time_offset = 71.92007

# Ensure the directory for the output file exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")
else:
    print(f"Directory '{output_dir}' already exists.")

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
    ("CLD", "CLOUD", 1.0),
]

two_d_vars = [
    ("SHF", "SHFLX", 1.0),
]

# ("", "", ),

# Process 3D variables
for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_flipped = ds_in[var_in].values[:, ::-1]
        ds_out[var_out] = xr.DataArray(data_flipped, dims=["time", "lev"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    if var_in in ds_in:
        ds_out[var_out] = xr.DataArray(ds_in[var_in].values, dims=["time"]) * factor
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

