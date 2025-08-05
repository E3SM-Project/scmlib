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
        ("OMEGA", "omega_horiz_avg", 1.0),
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
        ("TS", "surf_radiative_T_horiz_avg", 1.0),
        ("TREFHT", "T_2m_horiz_avg", 1.0),
        ("QREFHT", "qv_2m_horiz_avg", 1.0),
        ("PRECT", "precip_total_surf_mass_flux_horiz_avg", 1.0),
        ("CLDHGH", "cldhgh_int_horiz_avg", 1.0),
        ("CLDMED", "cldmed_int_horiz_avg", 1.0),
        ("CLDLOW", "cldlow_int_horiz_avg", 1.0),
        ("CLDTOT", "cldtot_int_horiz_avg", 1.0),
        ("OMEGA500", "omega_at_500hPa_horiz_avg", 1.0),
        ("FLDS", "LW_flux_dn_at_model_bot_horiz_avg", 1.0),
        ("FSDS", "SW_flux_dn_at_model_bot_horiz_avg", 1.0),
        ("FSNS", "sfc_flux_sw_net_horiz_avg", 1.0),
        ("FLNS", "sfc_flux_lw_dn_horiz_avg", 1.0),
        ("FSNTOA", "model_top_flux_sw_net_horiz_avg", 1.0),
        ("FLNT", "model_top_flux_lw_net_horiz_avg", 1.0)
    ]

    for var_in, var_out, factor in three_d_vars:
        if var_in in ds_in:
            data_val = np.squeeze(ds_in[var_in].values)
            dims_in = ds_in[var_in].dims
            dims_out = ["time", "ilev"] if len(dims_in) >= 2 and dims_in[1] == 'ilev' else ["time", "lev"]
            if var_in == "Z3":
                surface_elev = data_val[:, -1][:, np.newaxis] - 10
                data_val = data_val - surface_elev
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

    if "PRECL" in ds_in and "PRECC" in ds_in:
        ds_out['precip_total_surf_mass_flux_horiz_avg'] = xr.DataArray(
            np.squeeze(ds_in['PRECL'].values + ds_in['PRECC'].values), dims=["time"]
        )
        ds_out['precip_large_surf_mass_flux_horiz_avg'] = xr.DataArray(
            np.squeeze(ds_in['PRECL'].values), dims=["time"]
        )
        ds_out['precip_conv_surf_mass_flux_horiz_avg'] = xr.DataArray(
            np.squeeze(ds_in['PRECC'].values), dims=["time"]
        )
        ds_out['precip_large_surf_mass_flux_horiz_avg'].attrs = ds_in['PRECL'].attrs
        ds_out['precip_conv_surf_mass_flux_horiz_avg'].attrs = ds_in['PRECC'].attrs

    ds_out.attrs = ds_in.attrs
    ds_out.to_netcdf(output_file)
    print(f"File saved to {output_file}\n")

# === MAIN BLOCK ===
use_batch_mode = True  # Set to False to run manually

if use_batch_mode:
    input_dir = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/pre_files/"
    output_dir = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/"
    os.makedirs(output_dir, exist_ok=True)

    input_files = sorted(glob.glob(os.path.join(input_dir, "*e3sm_format.nc")))
    for input_file in input_files:
        filename = os.path.basename(input_file).replace("e3sm_format", "dpxx_format")
        output_file = os.path.join(output_dir, filename)
        convert_file(input_file, output_file)
else:
    # Manual mode
    input_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/pre_files/ARM97.obs.e3sm_format.nc"
    output_file = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/ARM97.obs.dpxx_format.nc"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    convert_file(input_file, output_file)
