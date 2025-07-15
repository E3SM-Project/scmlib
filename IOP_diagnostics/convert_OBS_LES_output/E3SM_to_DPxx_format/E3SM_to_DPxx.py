import xarray as xr
import numpy as np
import os

# Define input and output file paths
input_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/e3sm_scm_GOAMAZON.cntl.2014-01-01.002a/run/e3sm_scm_GOAMAZON.cntl.2014-01-01.002a.horiz_avg.AVERAGE.nhours_x1.2014-01-01-00000.nc"
output_file = "/pscratch/sd/b/bogensch/dp_screamxx_conv/e3sm_scm_GOAMAZON.cntl.2014-01-01.002a/run/e3sm_scm_dpxxformat_GOAMAZON.cntl.2014-01-01.002a.horiz_avg.AVERAGE.nhours_x1.2014-01-01-00000.nc"
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
time_data = ds_in["time"].values
ds_out["time"] = xr.DataArray(time_data - time_offset, dims=["time"])

ds_out["lev"] = ds_in["lev"].values
ds_out["ilev"] = ds_in["ilev"].values

ds_out["hyam"] = xr.DataArray(ds_in["hyam"].values, dims=["lev"])
ds_out["hybm"] = xr.DataArray(ds_in["hybm"].values, dims=["lev"])
ds_out["hyai"] = xr.DataArray(ds_in["hyai"].values, dims=["ilev"])
ds_out["hybi"] = xr.DataArray(ds_in["hybi"].values, dims=["ilev"])

for var in ["hyam", "hybm", "hyai", "hybi", "time"]:
    ds_out[var].attrs = ds_in[var].attrs

# 3. Define lists for 3D and 2D variables
three_d_vars = [
    ("Q", "qv_horiz_avg", 1.0),
    ("U", "U_horiz_avg", 1.0),
    ("V", "V_horiz_avg", 1.0),
    ("T", "T_mid_horiz_avg", 1.0),
    ("RELHUM", "RelativeHumidity_horiz_avg", 1.0/100.),
    ("Z3", "z_mid_horiz_avg", 1.0),
    ("CLDLIQ", "qc_horiz_avg", 1.0),
    ("CLDICE", "qi_horiz_avg", 1.0),
    ("RAINQM", "qr_horiz_avg", 1.0),
    ("CLOUD", "cldfrac_tot_for_analysis_horiz_avg", 1.0),
    ("WPTHLP_CLUBB", "wthl_sec_horiz_avg", 1./1004./1.2),
    ("WPRTP_CLUBB", "wqw_sec_horiz_avg", 1./(2.5*10**6)/1.2),
    ("WP2_CLUBB", "w_variance_horiz_avg", 1.0),
    ("WP3_CLUBB", "w3_horiz_avg", 1.0),
    ("WPTHVP_CLUBB", "sgs_buoy_flux_horiz_avg", 1./1004./1.2),
    ("THLP2_CLUBB", "thl_sec_horiz_avg", 1.0),
    ("RTP2_CLUBB", "qw_sec_horiz_avg", 1.0/1000./1000.)
]

two_d_vars = [
    ("SHFLX", "surf_sens_flux_horiz_avg", 1.0),
    ("LHFLX", "surface_upward_latent_heat_flux_horiz_avg",1.0),
    ("PS", "ps_horiz_avg",1.0),
    ("TMQ", "VapWaterPath_horiz_avg", 1.0),
    ("TGCLDLWP", "LiqWaterPath_horiz_avg", 1.0),
    ("TGCLDIWP", "IceWaterPath_horiz_avg", 1.0),
    ("SWCF", "ShortwaveCloudForcing_horiz_avg", 1.0),
    ("LWCF", "LongwaveCloudForcing_horiz_avg", 1.0),
    ("TREFHT", "T_2m_horiz_avg", 1.0),
    ("PS", "ps_horiz_avg", 1.0)
]

# ("", "", ),

# Process 3D variables

for var_in, var_out, factor in three_d_vars:
    if var_in in ds_in:
        data_val = np.squeeze(ds_in[var_in].values)
        # Get dimension names of the variable
        dims_in = ds_in[var_in].dims

        # Determine if second dimension is 'lev' or 'ilev'
        if len(dims_in) >= 2 and dims_in[1] == 'ilev':
            dims_out = ["time", "ilev"]
        else:
            dims_out = ["time", "lev"]

        ds_out[var_out] = xr.DataArray(data_val, dims=dims_out) * factor
        ds_out[var_out].attrs = ds_in[var_in].attrs
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Process 2D variables
for var_in, var_out, factor in two_d_vars:
    if var_in in ds_in:
        ds_out[var_out] = xr.DataArray(np.squeeze(ds_in[var_in].values), dims=["time"]) * factor
        ds_out[var_out].attrs = ds_in[var_in].attrs
    else:
        print(f"Warning: Variable '{var_in}' not found in input dataset. Skipping.")

# Handle Precipitation Specially
ds_out['precip_total_surf_mass_flux_horiz_avg']=xr.DataArray(np.squeeze(ds_in['PRECL'].values)+np.squeeze(ds_in['PRECC'].values), dims=["time"])

ds_out['precip_large_surf_mass_flux_horiz_avg']=xr.DataArray(np.squeeze(ds_in['PRECL'].values), dims=["time"])
ds_out['precip_conv_surf_mass_flux_horiz_avg']=xr.DataArray(np.squeeze(ds_in['PRECC'].values), dims=["time"])

# Copy attributes from the input dataset to the output dataset
ds_out.attrs = ds_in.attrs

# Add the units attribute
#ds_out["time"].attrs["units"] = "days since 2003-07-15 00:00:00"

# Save the new dataset to a NetCDF file
ds_out.to_netcdf(output_file)

print(f"Output file created at: {output_file}")

