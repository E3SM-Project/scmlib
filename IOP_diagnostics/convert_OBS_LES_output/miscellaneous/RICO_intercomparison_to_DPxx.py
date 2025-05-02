import xarray as xr
import numpy as np
import os

# Output path
outpath = "/pscratch/sd/b/bogensch/dp_screamxx_conv/les_data/"

# Define all cases in a list of dictionaries
cases = [
    {
        "input_file": "/global/homes/b/bogensch/dp_scream_paper/first_submission_scripts/rico_data/RICO_les_MF_ensavg.nc",
        "output_file": outpath + "RICO.les.dpxx.nc",
        "time_offset": 86400.0,
    },
]

# Define variable mappings
three_d_vars = [
    ("cld_frac", "cldfrac_tot_for_analysis_horiz_avg", 1.0),
    ("ql", "qc_horiz_avg", 0.001),
    ("qr", "qr_horiz_avg", 0.001),
    ("thetal", "LiqPotentialTemperature_horiz_avg", 1.0),
    ("qt", "qv_horiz_avg", 1.0 / 1000.0),
]

#two_d_vars = [
#    ("lwp", "LiqWaterPath_horiz_avg", 1.0 / 1000.0),
#    ("rwp", "RainWaterPath_horiz_avg", 1.0 / 1000.0),
#    ("prec_srf", "precip_total_surf_mass_flux_horiz_avg", 1.15741e-8),
#]

# Process each case
for case in cases:
    input_file = case["input_file"]
    output_file = case["output_file"]
    time_offset = case["time_offset"]

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    # Open the input file
    ds_in = xr.open_dataset(input_file)
    ds_out = xr.Dataset()

    # Process time
    time_data = ds_in["time"].values
    ds_out["time"] = xr.DataArray(time_data/time_offset, dims=["time"])

    # Process z and p
    z_data_flipped = ds_in["height"].values[::-1]
    z_mid_les = np.tile(z_data_flipped, (len(ds_out["time"]), 1))
    ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid_les, dims=["time", "lev"])

    # Process 3D variables
    for var_in, var_out, factor in three_d_vars:
        if var_in in ds_in:
            if var_in == 'qt':
                data_flipped1 = ds_in['qt'].values[:, ::-1]
                data_flipped2 = ds_in['ql'].values[:, ::-1]
                ds_out[var_out] = (xr.DataArray(data_flipped1, dims=["time", "lev"]) -
		                  xr.DataArray(data_flipped2, dims=["time", "lev"])) * factor	        
            else:
                data_flipped = ds_in[var_in].values[:, ::-1]
                ds_out[var_out] = xr.DataArray(data_flipped, dims=["time", "lev"]) * factor
        else:
            print(f"Warning: Variable '{var_in}' not found in {input_file}. Skipping.")

#    # Process 2D variables
#    for var_in, var_out, factor in two_d_vars:
#        if var_in in ds_in:
#            ds_out[var_out] = xr.DataArray(ds_in[var_in].values, dims=["time"]) * factor
#        else:
#            print(f"Warning: Variable '{var_in}' not found in {input_file}. Skipping.")

    # Copy attributes and save
    ds_out.attrs = ds_in.attrs
    ds_out.to_netcdf(output_file)
    print(f"Output file created at: {output_file}")
