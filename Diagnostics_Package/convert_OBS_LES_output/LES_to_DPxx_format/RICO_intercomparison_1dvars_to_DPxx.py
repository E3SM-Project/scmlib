import xarray as xr
import numpy as np
import os

# Output path
outpath = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/"

# Define all cases
cases = [
    {
        "input_file": "/global/homes/b/bogensch/dp_scream_paper/first_submission_scripts/rico_data/RICO_les_MF.nc",
        "output_file": outpath + "RICO.les.intercomparison_ensavg.1dvars.dpxx_format.nc",
        "time_offset": 86400.0,
    },
]

# Define 2D variable mappings
two_d_vars = [
    ("lwp", "LiqWaterPath_horiz_avg", 1.0 / 1000.0),
    ("rwp", "RainWaterPath_horiz_avg", 1.0 / 1000.0),
    ("prec_srf", "precip_total_surf_mass_flux_horiz_avg", 1.15741e-8),
]

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
    time_data = ds_in["time_series"].values
    ds_out["time"] = xr.DataArray(time_data / time_offset, dims=["time"])

    # Process z
    z_data_flipped = ds_in["height"].values[::-1]
    z_mid_les = np.tile(z_data_flipped, (len(time_data), 1))
    ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid_les, dims=["time", "lev"])

    # Process 2D variables: take nanmean over les
    for var_in, var_out, factor in two_d_vars:
        if var_in in ds_in:
            var_data = ds_in[var_in].mean(dim="les", skipna=True).values * factor
            ds_out[var_out] = xr.DataArray(var_data, dims=["time"])
            print(f"{var_out}: shape={var_data.shape}, valid={np.sum(np.isfinite(var_data))}")
        else:
            print(f"Warning: Variable '{var_in}' not found in {input_file}. Skipping.")

    # Copy global attributes
    ds_out.attrs = ds_in.attrs

    # Write output
    ds_out.to_netcdf(output_file)
    print(f"Output file created at: {output_file}")
