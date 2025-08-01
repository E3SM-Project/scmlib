import xarray as xr
import numpy as np
import os
import glob

def convert_file(input_file, output_file):
    print(f"Processing file: {input_file}")
    ds_in = xr.open_dataset(input_file, decode_times=False)
    ds_out = xr.Dataset()

    # Transfer and adjust the "time" variable
    time_data = ds_in["time"].values
    ds_out["time"] = xr.DataArray(time_data, dims=["time"])
    if "units" in ds_in["time"].attrs:
        ds_out["time"].attrs["units"] = ds_in["time"].attrs["units"]
    ds_out["lev"] = ds_in["lev"].values
    ds_out["lev"].attrs = ds_in["lev"].attrs

    if "ilev" in ds_in:
        ds_out["ilev"] = ds_in["ilev"].values
        ds_out["ilev"].attrs = ds_in["ilev"].attrs

    if "hyam" in ds_in:
        for name in ["hyam", "hybm", "hyai", "hybi"]:
            ds_out[name] = ds_in[name].values
            ds_out[name].attrs = ds_in[name].attrs

    if "p_mid_obs" in ds_in:
        ds_out["p_mid_obs"] = ds_in["p_mid_obs"]
        ds_out["p_mid_obs"].attrs = ds_in["p_mid_obs"].attrs

    three_d_vars = [
        ("qv_horiz_avg", "Q", 1.0),
        ("U_horiz_avg", "U", 1.0),
        ("V_horiz_avg", "V", 1.0),
        ("T_mid_horiz_avg", "T", 1.0),
        ("RelativeHumidity_horiz_avg", "RELHUM", 100.),
        ("z_mid_horiz_avg", "Z3", 1.0),
        ("qc_horiz_avg", "CLDLIQ", 1.0),
        ("qi_horiz_avg", "CLDICE", 1.0),
        ("qr_horiz_avg", "RAINQM", 1.0),
        ("cldfrac_tot_for_analysis_horiz_avg", "CLOUD", 1.0),
        ("omega_horiz_avg", "OMEGA", 1.0),
        ("wthl_sec_horiz_avg", "WPTHLP_CLUBB", 1004.*1.2),
        ("wqw_sec_horiz_avg", "WPRTP_CLUBB", (2.5*10**6)*1.2),
        ("w_variance_horiz_avg", "WP2_CLUBB", 1.0),
        ("w3_horiz_avg", "WP3_CLUBB", 1.0),
        ("sgs_buoy_flux_horiz_avg", "WPTHVP_CLUBB", 1004.*1.2),
        ("thl_sec_horiz_avg", "THLP2_CLUBB", 1.0),
        ("qw_sec_horiz_avg", "RTP2_CLUBB", 1000.*1000.)
    ]

    two_d_vars = [
        ("surf_sens_flux_horiz_avg", "SHFLX", 1.0),
        ("surface_upward_latent_heat_flux_horiz_avg", "LHFLX", 1.0),
        ("ps_horiz_avg", "PS", 1.0),
        ("VapWaterPath_horiz_avg", "TMQ", 1.0),
        ("LiqWaterPath_horiz_avg", "TGCLDLWP", 1.0),
        ("IceWaterPath_horiz_avg", "TGCLDIWP", 1.0),
        ("ShortwaveCloudForcing_horiz_avg", "SWCF", 1.0),
        ("LongwaveCloudForcing_horiz_avg", "LWCF", 1.0),
        ("surf_radiative_T_horiz_avg", "TS", 1.0),
        ("T_2m_horiz_avg", "TREFHT", 1.0),
        ("qv_2m_horiz_avg", "QREFHT", 1.0),
        ("precip_total_surf_mass_flux_horiz_avg", "PRECT", 1.0),
        ("cldhgh_int_horiz_avg", "CLDHGH", 1.0),
        ("cldmed_int_horiz_avg", "CLDMED", 1.0),
        ("cldlow_int_horiz_avg", "CLDLOW", 1.0),
        ("cldtot_int_horiz_avg", "CLDTOT", 1.0),
        ("omega_at_500hPa_horiz_avg", "OMEGA500", 1.0),
        ("LW_flux_dn_at_model_bot_horiz_avg", "FLDS", 1.0),
        ("SW_flux_dn_at_model_bot_horiz_avg", "FSDS", 1.0),
        ("sfc_flux_sw_net_horiz_avg", "FSNS", 1.0),
        ("sfc_flux_lw_dn_horiz_avg", "FLNS", 1.0),
        ("model_top_flux_sw_net_horiz_avg", "FSNTOA", 1.0),
        ("model_top_flux_lw_net_horiz_avg", "FLNT", 1.0)
    ]

    for var_in, var_out, factor in three_d_vars:
        if var_in in ds_in:
            data_val = np.squeeze(ds_in[var_in].values)
            dims_in = ds_in[var_in].dims
            dims_out = ["time", "ilev"] if len(dims_in) >= 2 and dims_in[1] == 'ilev' else ["time", "lev"]

            ds_out[var_out] = xr.DataArray(data_val, dims=dims_out) * factor
            ds_out[var_out].attrs = ds_in[var_in].attrs
        else:
            print(f"Warning: Variable '{var_in}' not found.")

    for var_in, var_out, factor in two_d_vars:
        if var_in in ds_in:
            ds_out[var_out] = xr.DataArray(np.squeeze(ds_in[var_in].values), dims=["time"]) * factor
            ds_out[var_out].attrs = ds_in[var_in].attrs
        else:
            print(f"Warning: Variable '{var_in}' not found.")

    ds_out.attrs = ds_in.attrs
    ds_out.to_netcdf(output_file)
    print(f"File saved to {output_file}\n")

# === MAIN BLOCK ===
use_batch_mode = True  # Set to False to run manually

if use_batch_mode:
    input_dir = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/"
    output_dir = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/E3SM_SCM/"
    os.makedirs(output_dir, exist_ok=True)

    input_files = sorted(glob.glob(os.path.join(input_dir, "*dpxx_format.nc")))
    for input_file in input_files:
        filename = os.path.basename(input_file).replace("dpxx_format", "e3sm_format")
        output_file = os.path.join(output_dir, filename)
        convert_file(input_file, output_file)
else:
    # Manual mode
    input_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/ARM97.obs.dpxx_format.nc"
    output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/E3SM_SCM/ARM97.obs.e3sm_format.nc"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    convert_file(input_file, output_file)
