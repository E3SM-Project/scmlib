import xarray as xr
import numpy as np
import os

# Output path
outpath = "/pscratch/sd/b/bogensch/E3SM_simulations/iopdiags_OBS_and_LES_files/DP_EAMxx/"

# Define all cases in a list of dictionaries
cases = [
    {
        "input_file": "/global/homes/b/bogensch/mk_iop_forcing/make_lafe/lafe_0823/thick_512x512x156_50m_50m_1s.nc",
        "output_file": outpath + "LAFE.les.SAM.dpxx_format.nc",
        "time_offset": 235.4807,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/CASS_LES/thick_512x512x156_50m_50m_1s.nc",
        "output_file": outpath + "CASS.les.SAM.dpxx_format.nc",
        "time_offset": 205.5017,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/SAM_LES/GATE_IDEAL_S_2048x2048x256_100m_2s.nc",
        "output_file": outpath + "GATEIDEAL.les.SAM.dpxx_format.nc",
        "time_offset": 0.0,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/SAM_LES/MAG3D.15A.20130720.1729_105h_128x128x460_LES.nc",
        "output_file": outpath + "MAGIC.les.SAM.dpxx_format.nc",
        "time_offset": 201.25,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/LESfiles/GOAMAZON_goamazon_278_test1.nc",
        "output_file": outpath + "GOAMAZON_singlepulse.les.SAM.dpxx_format.nc",
        "time_offset": 278.5042,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/GOAMAZON_analysis/LESfiles/GOAMAZON_goamazon_603_test3.nc",
        "output_file": outpath + "GOAMAZON_doublepulse.les.SAM.dpxx_format.nc",
        "time_offset": 603.5021,
    },
    {
        "input_file": "/global/homes/b/bogensch/THREAD/SAM_LES/COMBLE_MIP_V2.4_with_ice_vm.nc",
        "output_file": outpath + "COMBLE.les.SAM.dpxx_format.nc",
        "time_offset": 71.92007,
    },
]

# Define variable mappings
three_d_vars = [
    ("CLD", "cldfrac_tot_for_analysis_horiz_avg", 1.0),
    ("QCL", "qc_horiz_avg", 0.001),
    ("QPL", "qr_horiz_avg", 0.001),
    ("THETAL", "LiqPotentialTemperature_horiz_avg", 1.0),
    ("THETA", "PotentialTemperature_horiz_avg", 1.0),
    ("RELH", "RelativeHumidity_horiz_avg", 1.0 / 100.0),
    ("TABS", "T_mid_horiz_avg", 1.0),
    ("U", "U_horiz_avg", 1.0),
    ("V", "V_horiz_avg", 1.0),
    ("QV", "qv_horiz_avg", 1.0 / 1000.0),
    ("QCI", "qi_horiz_avg", 1.0 / 1000.0),
    ("TKES", "tke_horiz_avg", 1.0),
    ("TK", "eddy_diff_mom_horiz_avg", 1.0),
    ("QPEVP", "micro_vap_liq_exchange_horiz_avg", 1.0 / 86400.0 / 1000.0),
]

two_d_vars = [
    ("SHF", "surf_sens_flux_horiz_avg", 1.0),
    ("LHF", "surf_evap_horiz_avg", 4e-7),
    ("LHF", "surface_upward_latent_heat_flux_horiz_avg", 1.0),
    ("CWP", "LiqWaterPath_horiz_avg", 1.0 / 1000.0),
    ("IWP", "IceWaterPath_horiz_avg", 1.0 / 1000.0),
    ("PW", "VapWaterPath_horiz_avg", 1.0 / 1.0),
    ("RWP", "RainWaterPath_horiz_avg", 1.0 / 1000.0),
    ("PREC", "precip_total_surf_mass_flux_horiz_avg", 1.15741e-8),
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
    time_data = ds_in["time"].values
    ds_out["time"] = xr.DataArray(time_data - time_offset, dims=["time"])

    # Process z and p
    z_data_flipped = ds_in["z"].values[::-1]
    z_mid_les = np.tile(z_data_flipped, (len(ds_out["time"]), 1))
    ds_out["z_mid_horiz_avg"] = xr.DataArray(z_mid_les, dims=["time", "lev"])

    p_data_flipped = ds_in["p"].values[::-1]
    p_mid_les = np.tile(p_data_flipped, (len(ds_out["time"]), 1))
    ds_out["p_mid_les"] = xr.DataArray(p_mid_les, dims=["time", "lev"])

    # Process 3D variables
    for var_in, var_out, factor in three_d_vars:
        if var_in in ds_in:
            data_flipped = ds_in[var_in].values[:, ::-1]
            ds_out[var_out] = xr.DataArray(data_flipped, dims=["time", "lev"]) * factor
        else:
            print(f"Warning: Variable '{var_in}' not found in {input_file}. Skipping.")

    # Process 2D variables
    for var_in, var_out, factor in two_d_vars:
        if var_in in ds_in:
            ds_out[var_out] = xr.DataArray(ds_in[var_in].values, dims=["time"]) * factor
        else:
            print(f"Warning: Variable '{var_in}' not found in {input_file}. Skipping.")

    # Copy attributes and save
    ds_out.attrs = ds_in.attrs
    ds_out.to_netcdf(output_file)
    print(f"Output file created at: {output_file}")
