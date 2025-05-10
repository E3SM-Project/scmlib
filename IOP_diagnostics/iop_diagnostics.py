import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import tarfile
from jinja2 import Template
from scipy.interpolate import interp1d
from datetime import datetime, timedelta
import sys

def compute_y_coord(ds, time_indices, height_cord, var_name):
    """
    Compute the vertical coordinate (y_coord) for a dataset.

    Parameters:
        ds (xarray.Dataset): Dataset containing the variables.
        time_indices (numpy.ndarray): Indices of the time range to average over.
        height_cord (str): Vertical coordinate type ('z' or 'p').
        var_name (str): Variable name for which the vertical coordinate is required.

    Returns:
        numpy.ndarray: The computed y-coordinate.
    """
    if height_cord == "z":
        if height_cord == "z":
            if "z_mid" in ds.data_vars:
                height_var = "z_mid"
            elif "z_mid_horiz_avg" in ds.data_vars:
                height_var = "z_mid_horiz_avg"
            elif "Z3" in ds.data_vars:
                height_var = "Z3"
            else:
                raise ValueError("Cannot determine height coordinates ('z_mid', 'z_mid_horiz_avg', or 'Z3').")

            # Compute y_coord and subtract surface elevation
            y_coord = ds[height_var].isel(time=time_indices).mean(dim="time").squeeze()
            surface_elevation = ds[height_var].isel(lev=-1).mean(dim="time").squeeze() - 10.  # Surface elevation from highest index level
            y_coord -= surface_elevation

        # If variable has dimensions of ilev then we need to interpolate the height coordinate to the ilev grid
        if "ilev" in ds[var_name].dims:
            lev = ds['lev']
            ilev = ds['ilev']
            interp_func = interp1d(lev, np.squeeze(y_coord), fill_value="extrapolate")
            y_coord = interp_func(ilev)
            y_coord[-1] = 0.0  # Set surface boundary condition to 0

    elif height_cord == "p":
        ps_var = 'PS' if 'PS' in ds.data_vars else 'ps' if 'ps' in ds.data_vars else 'ps_horiz_avg' if 'ps_horiz_avg' in ds.data_vars else None
        model = 'hyam' in ds.data_vars and 'hybm' in ds.data_vars
        if ps_var and model:
            ps_avg = ds[ps_var].isel(time=time_indices).mean(dim="time") / 100.0  # Convert to hPa
            if "lev" in ds[var_name].dims and all(var in ds for var in ['hyam', 'hybm']):
                hyam = ds['hyam']
                hybm = ds['hybm']
                y_coord = 1000.0 * hyam + hybm * ps_avg
            elif "ilev" in ds[var_name].dims and all(var in ds for var in ['hyai', 'hybi']):
                hyai = ds['hyai']
                hybi = ds['hybi']
                y_coord = 1000.0 * hyai + hybi * ps_avg
            else:
                print(f"Warning: Hybrid coefficients or surface pressure data are missing. Using hybrid pressure coordinates.")
                y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
        elif 'p_mid_obs' in ds.data_vars:
            p_mid_obs_var = ds["p_mid_obs"]

            if "time" in p_mid_obs_var.dims:
                y_coord = p_mid_obs_var.isel(time=time_indices).mean(dim="time")
            else:
                y_coord = p_mid_obs_var
        elif 'p_mid_les' in ds.data_vars:
            y_coord = ds['p_mid_les'].isel(time=time_indices).mean(dim="time")
        else:
            print(f"Warning: 'PS' or 'ps' is missing. Using hybrid pressure coordinates.")
            y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
    else:
        raise ValueError(f"Invalid height_cord: {height_cord}. Must be 'z' or 'p'.")

    return y_coord

def plot_time_height_panel_grid(
    var_name,
    datasets,
    short_ids,
    time_offset,
    height_cord,
    output_subdir,
    labelsize,
    ticksize,
    usercmap,
    start_time,
    end_time,
    max_height,
    is_diurnal=False,
    time_labels=None,
    title_suffix=""
):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    global_min, global_max = float('inf'), float('-inf')
    valid_datasets = []

    for idx, ds in enumerate(datasets):
        if var_name not in ds:
            continue

        if is_diurnal:
            composite, hour_labels, success, ndim, stime, etime = compute_diurnal_composite(
                ds, var_name, idx, time_offset, start_time, end_time)
            if not success or ndim != 2:
                continue
            time_vals = hour_labels
            time_indices = np.where((time_vals >= 0) & (time_vals <= 24))[0]
            data = composite
            # height levels should come from lev or ilev (assumes consistent across time)
            if 'lev' in ds[var_name].dims:
                lev_dim = 'lev'
            elif 'ilev' in ds[var_name].dims:
                lev_dim = 'ilev'
            else:
                continue

            timecords = np.where((time_vals >= stime) & (time_vals <= etime))[0]
            y_coord = compute_y_coord(ds, timecords, height_cord, var_name)

            if height_cord == "z":
                y_min, y_max = (0, max_height) if max_height is not None else (y_coord.min(), y_coord.max())
            elif height_cord == "p":
                y_min, y_max = (max_height, y_coord.max()) if max_height is not None else (y_coord.min(), y_coord.max())

            valid_lev_idx = np.where((y_coord >= y_min) & (y_coord <= y_max))[0]

            if max_height is not None:
                if height_cord == "z":
                    valid_idx = np.where(y_coord <= max_height)[0]
                else:
                    valid_idx = np.where(y_coord >= max_height)[0]
                data = data[:, valid_lev_idx]

            global_min = min(global_min, float(data.min()))
            global_max = max(global_max, float(data.max()))
            valid_datasets.append((idx, time_vals, data, y_coord[valid_lev_idx]))

        else:
            time_vals = ds['time'].values - time_offset[idx]

            stime = start_time if start_time is not None else time_vals[0]
            etime = end_time if end_time is not None else time_vals[-1]

            time_indices = np.where((time_vals >= stime) & (time_vals <= etime))[0]
            time_vals = time_vals[time_indices]
            if len(time_indices) == 0:
                continue
            y_coord = compute_y_coord(ds, time_indices, height_cord, var_name)

            if height_cord == "z":
                y_min, y_max = (0, max_height) if max_height is not None else (y_coord.min(), y_coord.max())
            elif height_cord == "p":
                y_min, y_max = (max_height, y_coord.max()) if max_height is not None else (y_coord.min(), y_coord.max())

            valid_lev_idx = np.where((y_coord >= y_min) & (y_coord <= y_max))[0]

            data = ds[var_name].isel(time=time_indices)
            if "lev" in ds[var_name].dims:
                data = data.isel(lev=valid_lev_idx)
            elif "ilev" in ds[var_name].dims:
                data = data.isel(ilev=valid_lev_idx)
            if 'ncol' in data.dims:
                data = data.mean(dim="ncol")

            global_min = min(global_min, float(data.min().values))
            global_max = max(global_max, float(data.max().values))
            valid_datasets.append((idx, time_vals, data, y_coord[valid_lev_idx]))

    if not valid_datasets:
        print(f"Warning: No valid data found for {var_name}. Skipping.")
        return None

    if global_min == global_max:
        global_min -= 0.01 * abs(global_min) if global_min != 0 else 0.01
        global_max += 0.01 * abs(global_max) if global_max != 0 else 0.01

    levels = np.linspace(global_min, global_max, 20)
    n_cols = 2
    n_rows = -(-len(valid_datasets) // n_cols)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 6), sharey=True, constrained_layout=True)
    axes = np.atleast_2d(axes)

    contours = []
    for ax, (idx, time_vals, data, y_coord) in zip(axes.flat, valid_datasets):

        y_coord = np.squeeze(y_coord)
        contour = ax.contourf(time_vals, y_coord, data.T, levels=levels, cmap=usercmap)
        contours.append(contour)

        ax.set_title(short_ids[idx], fontsize=16)
        ax.set_xlabel("Hour" if is_diurnal else "Time (days)", fontsize=labelsize)
        ax.set_ylabel("Height (m)" if height_cord == "z" else "Pressure (hPa)", fontsize=labelsize)

        # Set y-axis limit if specified
        if height_cord == "z":
            if max_height is not None:
                ax.set_ylim([0, max_height])
        elif height_cord == "p":
            if max_height is not None:
                ax.set_ylim([max_height, y_coord.max()])  # Adjust for pressure
            else:
                ax.set_ylim([0, y_coord.max()])

        if height_cord == "p":
            ax.invert_yaxis()
        ax.tick_params(axis='both', labelsize=ticksize)

    for ax in axes.flat[len(valid_datasets):]:
        ax.set_visible(False)

    cbar = fig.colorbar(contours[0], ax=axes, orientation='vertical', aspect=30, shrink=0.8, pad=0.02)
    cbar.set_label(next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds), 'Value'), fontsize=14)
    cbar.ax.tick_params(labelsize=12)

    long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds), var_name)
    if long_name == "MISSING":
        long_name = var_name
    plt.suptitle(f"{long_name} {'Diurnal Composite' if is_diurnal else 'Time-Height'} {title_suffix}", fontsize=18)

    outname = f"{var_name}_{'diurnal2d' if is_diurnal else 'time_height'}.jpg"
    outfile = os.path.join(output_subdir, outname)
    plt.savefig(outfile, format='jpg')
    plt.close()
    return outfile

def compute_diurnal_composite(ds, var_name, idx, time_offset, diurnal_start_day, diurnal_end_day):
    """
    Compute the diurnal composite for a given variable in a dataset.
    Returns:
        composite (np.ndarray), hour_labels (np.ndarray), success (bool), ndim (int)
    """
    try:
        times = ds['time'].values
        time_vals = times - time_offset[idx]
        time_res = float(time_vals[1] - time_vals[0])
        steps_per_day = int(round(1.0 / time_res))

        total_days = len(time_vals) / steps_per_day
        if steps_per_day < 4:
            print(f"Skipping {var_name}: fewer than 4 time steps/day.")
            return None, None, False, None
        if total_days < 3:
            print(f"Skipping {var_name}: fewer than 3 days in dataset.")
            return None, None, False, None

        stime = diurnal_start_day if diurnal_start_day is not None else time_vals[0]
        etime = diurnal_end_day if diurnal_end_day is not None else time_vals[-1]

        valid_idx = np.where((time_vals >= stime) & (time_vals <= etime))[0]
        if len(valid_idx) == 0:
            return None, None, False, None

        data = ds[var_name].isel(time=valid_idx)
        if 'ncol' in data.dims:
            data = data.mean(dim='ncol')

        hour_bins = np.linspace(0, 24, steps_per_day + 1)
        hour_labels = (hour_bins[:-1] + hour_bins[1:]) / 2

        daily_data = []
        for i in range(0, len(data), steps_per_day):
            if i + steps_per_day > len(data):
                break
            daily_data.append(data[i:i + steps_per_day])

        composite = np.mean(daily_data, axis=0)

        return composite, hour_labels, True, data.ndim, stime, etime
    except Exception as e:
        print(f"Error computing diurnal composite for {var_name}: {e}")
        return None, None, False, None

#############################

import netCDF4
from datetime import datetime

def extract_time_info(ds):
    try:
        # Get time units
        time_units = ds['time'].attrs['units']
    except (KeyError, AttributeError):
        print("Warning: 'time' variable or its 'units' attribute is not available.")
        return -999, -999

    try:
        # Extract the portion after "since"
        _, ref_str = time_units.split("since", 1)
        ref_str = ref_str.strip()

        # Allow for extra descriptors like "UTC"
        tokens = ref_str.split()
        if len(tokens) < 2:
            raise ValueError("Not enough components after 'since' to extract date and time.")
        date_str, time_str = tokens[0], tokens[1]
    except ValueError:
        print("Warning: The 'time:units' attribute is not in the expected format 'days since YYYY-MM-DD HH:MM:SS'.")
        return -999, -999

    # Format the date to "yyyymmdd"
    formatted_date = date_str.replace("-", "")

    try:
        from datetime import datetime
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        time_in_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    except ValueError:
        print("Warning: The time portion in 'time:units' is not in the expected format (HH:MM:SS).")
        return -999, -999

    return formatted_date, time_in_seconds


#############################

def compute_date_time_difference(date1, time1_seconds, date2, time2_seconds):
    """
    Compute the difference in days (as a floating-point value) between two dates and times.

    Parameters:
        date1 (str): First date in 'yyyymmdd' format.
        time1_seconds (int): Time of the first date in seconds (0 to 86400).
        date2 (str): Second date in 'yyyymmdd' format.
        time2_seconds (int): Time of the second date in seconds (0 to 86400).

    Returns:
        float: Difference in days, including the fractional day component.
    """
    try:
        # Convert date strings to datetime objects
        date_obj1 = datetime.strptime(date1, "%Y%m%d")
        date_obj2 = datetime.strptime(date2, "%Y%m%d")

        # Validate time in seconds (must be between 0 and 86400)
        if not (0 <= time1_seconds <= 86400 and 0 <= time2_seconds <= 86400):
            print("Error: Time in seconds must be between 0 and 86400.")
            return -999.0  # Error flag

        # Add time offset to the datetime objects
        datetime1 = date_obj1 + timedelta(seconds=time1_seconds)
        datetime2 = date_obj2 + timedelta(seconds=time2_seconds)

        # Compute the difference in days as a float
        day_difference = abs((datetime2 - datetime1).total_seconds()) / 86400.0

        return round(day_difference, 6)  # Rounded for better precision

    except ValueError:
        print("Error: One or both dates are not in the correct 'yyyymmdd' format.")
        return -999.0  # Error flag

#################################
###### Main program

def run_diagnostics(
    output_dir,
    general_id,
    base_dir,
    casenames,
    les_file,
    obs_file,
    short_ids,
    caseappend,
    profile_time_s,
    profile_time_e,
    do_timeheight,
    height_cord,
    max_height_profile,
    max_height_timeheight,
    linewidth,
    time_series_time_s,
    time_series_time_e,
    time_height_time_s,
    time_height_time_e,
    do_diurnal_composites=False,
    diurnal_start_day=0,
    diurnal_end_day=9999,
    usercmap="viridis_r",
    line_colors=None,
    line_styles=None,
    ticksize=14,
    labelsize=14
):

    output_subdir = os.path.join(output_dir, general_id, "plots")
    os.makedirs(output_subdir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    os.system('cp logos/thread_logo.png ' + output_subdir)
    os.system('cp logos/asr_logo_final.png ' + output_subdir)
    os.system('cp logos/arm_logo.png ' + output_subdir)
    os.system('cp logos/e3sm_logo.png ' + output_subdir)

    file_paths = [os.path.join(base_dir, case, "run", f"{case}{caseappend}") for case in casenames]
    datasets = []

    for fp in file_paths:
        ds = xr.open_dataset(fp, decode_times=False)

        # Treatement of PRECT for E3SM
        if 'PRECC' in ds.data_vars and 'PRECL' in ds.data_vars:
            ds['PRECT'] = ds['PRECC'] + ds['PRECL']
            # Add metadata
            ds['PRECT'].attrs['long_name'] = 'Total Surface Precipitation Rate'
            ds['PRECT'].attrs['units'] = ds['PRECC'].attrs.get('units', 'm/s')

        datasets.append(ds)

    if les_file is not None:
        ds = xr.open_dataset(les_file, decode_times=False)
        datasets.append(ds)

    if obs_file is not None:
        ds = xr.open_dataset(obs_file, decode_times=False)
        datasets.append(ds)

    if len(datasets) != len(short_ids):
        raise ValueError("The number of casenames must match the number of short_ids.")
    if line_colors and len(line_colors) != len(datasets):
        raise ValueError("Length of 'line_colors' must match the number of casenames.")
    if line_styles and len(line_styles) != len(datasets):
        raise ValueError("Length of 'line_styles' must match the number of casenames.")

    profile_plots = []
    timeseries_plots = []
    time_height_plots = []
    diurnal1d_plots = []
    diurnal2d_plots = []
    
    # Initialize some variables
    diurnal_start_day_web=0
    diurnal_end_day_web=0

    all_vars = set()
    for ds in datasets:
        all_vars.update(ds.data_vars.keys())

    print("Starting IOP Diagnostics Package")

    start_date_base, start_seconds_base = extract_time_info(datasets[0])

    time_offset = []
    for ds in datasets:
        test_date, test_seconds = extract_time_info(ds)
        offset = compute_date_time_difference(start_date_base, start_seconds_base, test_date, test_seconds) if test_date != -999 else 0.0
        time_offset.append(offset)

    print("Datasets that will be considered:")
    for ds in datasets:
        print(" -", ds.encoding.get('source', 'Unknown source'))

    print("Generating Profile Plots")

    for var_name in all_vars:
        if any(var_name in ds.data_vars and
               ds[var_name].ndim in [2, 3] and
               any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
               'time' in ds[var_name].dims for ds in datasets):

            for window_idx, (start_time, end_time) in enumerate(zip(profile_time_s, profile_time_e)):
                plt.figure(figsize=(8, 6))
                valid_plot = False

                for idx, (ds, short_id) in enumerate(zip(datasets, short_ids)):
                    if var_name not in ds.data_vars:
                        continue

                    valid_plot = True
                    time_in_days = ds['time'] - time_offset[idx]
                    stime = start_time if start_time != "end" else time_in_days[0]
                    etime = end_time if end_time != "end" else time_in_days[-1]
                    time_indices = np.where((time_in_days >= stime) & (time_in_days <= etime))[0]

                    time_filtered_data = ds[var_name].isel(time=time_indices).mean(dim="time")
                    y_coord = compute_y_coord(ds, time_indices, height_cord, var_name)

                    if height_cord == "z":
                        y_min, y_max = (0, max_height_profile) if max_height_profile else (y_coord.min(), y_coord.max())
                    else:
                        y_min, y_max = (max_height_profile, y_coord.max()) if max_height_profile else (y_coord.min(), y_coord.max())

                    valid_indices = np.where((y_coord >= y_min) & (y_coord <= y_max))[0]
                    filtered_y_coord = y_coord[valid_indices]
                    filtered_data = time_filtered_data.isel(lev=valid_indices) if "lev" in time_filtered_data.dims else time_filtered_data.isel(ilev=valid_indices)

                    plot_kwargs = {'label': short_id, 'linewidth': linewidth}
                    if line_colors: plot_kwargs['color'] = line_colors[idx]
                    if line_styles: plot_kwargs['linestyle'] = line_styles[idx]

                    plt.plot(np.squeeze(filtered_data), filtered_y_coord, **plot_kwargs)

                if valid_plot:
                    plt.ylim([y_min, y_max])
                    if height_cord == "p":
                        plt.gca().invert_yaxis()

                    var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                    var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                    if var_long_name == "MISSING": var_long_name = var_name

                    plt.xlabel(var_units, fontsize=labelsize)
                    ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
                    plt.ylabel(ylabel, fontsize=labelsize)
                    plt.title(f"{var_long_name} Profile (Day {start_time} to Day {end_time})", fontsize=16)
                    plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, alpha=0.5)
                    plt.tick_params(labelsize=ticksize)

                    plot_filename = os.path.join(output_subdir, f"{var_name}_profile_window{window_idx+1}.jpg")
                    plt.savefig(plot_filename, format='jpg')
                    plt.close()
                    profile_plots.append((plot_filename, window_idx+1))
                else:
                    print(f"Warning: Variable '{var_name}' is not a valid plotting variable. Skipping this variable.")

    # =================================================================
    # Plot time series
    # =================================================================

    print("Generating Time Series Plots")
    for var_name in all_vars:
        if any(
            var_name in ds.data_vars and
            ds[var_name].ndim in [1, 2] and
            'time' in ds[var_name].dims and
            not any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims)
            for ds in datasets
        ):
            plt.figure(figsize=(10, 5))
            valid_plot = False

            for idx, (ds, short_id) in enumerate(zip(datasets, short_ids)):
                if var_name not in ds.data_vars:
                    continue

                time_in_days = ds['time'] - time_offset[idx]
                stime = time_series_time_s if time_series_time_s is not None else time_in_days[0]
                etime = time_series_time_e if time_series_time_e is not None else time_in_days[-1]
                time_indices = np.where((time_in_days >= stime) & (time_in_days <= etime))[0]

                if ds[var_name].ndim == 2 and 'ncol' in ds[var_name].dims:
                    variable_data = ds[var_name].isel(time=time_indices)[:, 0]
                elif ds[var_name].ndim == 1 and 'time' in ds[var_name].dims:
                    variable_data = ds[var_name].isel(time=time_indices)
                else:
                    continue

                plot_kwargs = {'label': short_id, 'linewidth': linewidth}
                if line_colors: plot_kwargs['color'] = line_colors[idx]
                if line_styles: plot_kwargs['linestyle'] = line_styles[idx]

                plt.plot(time_in_days[time_indices], variable_data, **plot_kwargs)
                valid_plot = True

            if valid_plot:
                var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                if var_long_name == "MISSING":
                    var_long_name = var_name

                plt.xlabel("Time (days)", fontsize=labelsize)
                plt.ylabel(var_units, fontsize=labelsize)
                plt.title(f"{var_long_name} Time Series", fontsize=16)
                plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                plt.grid(color='#95a5a6', linestyle='--', linewidth=2, alpha=0.5)
                plt.tick_params(labelsize=ticksize)

                plot_filename = os.path.join(output_subdir, f"{var_name}_timeseries.jpg")
                plt.savefig(plot_filename, format='jpg')
                plt.close()
                timeseries_plots.append(plot_filename)
            else:
                print(f"Warning: Variable '{var_name}' is not a valid plotting variable. Skipping this variable.")


    #############################################################################################################
    # Plot time-height variables (two or three dimensions: time, ncol, lev or ilev)
    if do_timeheight:
        print("Generating Time Time-Height Plots")
        for var_name in all_vars:
            if any(
                var_name in ds.data_vars and
                ds[var_name].ndim in [2, 3] and
                any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
                'time' in ds[var_name].dims
                for ds in datasets
            ):
                outfile = plot_time_height_panel_grid(
                    var_name,
                    datasets,
                    short_ids,
                    time_offset,
                    height_cord,
                    output_subdir,
                    labelsize,
                    ticksize,
                    usercmap,
                    time_height_time_s,
                    time_height_time_e,
                    max_height_timeheight,
                    is_diurnal=False
                )
                if outfile:
                    time_height_plots.append(outfile)

    #############################################################################################################
    # Diurnal Composite diagnostics 1-D

    if do_diurnal_composites:
        print("Generating 1D Diurnal Composite Plots")
        diurnal1d_plots = []
        for var_name in all_vars:
            # Initialize figure
            plt.figure(figsize=(10, 5))
            valid_plot = False
            prect_treatment = False

            for idx, (ds, short_id) in enumerate(zip(datasets, short_ids)):
                if var_name not in ds:
                    continue

                allowed_dims = {'time', 'ncol', 'lev', 'ilev'}
                var_dims = set(ds[var_name].dims)

                # Must include 'time', and all dims must be in the allowed list
                if 'time' not in var_dims or not var_dims.issubset(allowed_dims):
                    continue

                if ds[var_name].dtype.kind in {'S', 'U'}:
                    continue

                composite, hour_labels, success, ndim, stime, etime = compute_diurnal_composite(
                    ds, var_name, idx, time_offset, diurnal_start_day, diurnal_end_day)
                if not success or ndim !=1:
                    continue

                if success:
                    diurnal_start_day_web = stime
                    diurnal_end_day_web = etime

                plot_kwargs = {'label': short_id, 'linewidth': linewidth}
                if line_colors: plot_kwargs['color'] = line_colors[idx]
                if line_styles: plot_kwargs['linestyle'] = line_styles[idx]
                plt.plot(hour_labels, composite, **plot_kwargs)
                valid_plot = True

            if valid_plot:
                plt.xlabel("Time (hour - UTC)", fontsize=labelsize)
                var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                if var_long_name == "MISSING": var_long_name = var_name

                plt.ylabel(var_units, fontsize=labelsize)
                plt.title(f"{var_long_name} Diurnal Composite", fontsize=16)
                plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                plt.grid(color='#95a5a6', linestyle='--', linewidth=2, alpha=0.5)
                plt.tick_params(labelsize=ticksize)

                plot_filename = os.path.join(output_subdir, f"{var_name}_diurnal1d.jpg")
                plt.savefig(plot_filename, format='jpg')
                plt.close()
                diurnal1d_plots.append(plot_filename)

            plt.close()

    #############################################################################################################
    # 2D diurnal composite plots (two or three dimensions: time, ncol, lev or ilev)
    if do_diurnal_composites:
        print("Generating 2D Diurnal Composite Plots")
        for var_name in all_vars:
            if any(
                var_name in ds.data_vars and
                ds[var_name].ndim in [2, 3] and
                any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
                'time' in ds[var_name].dims
                for ds in datasets
            ):
                outfile = plot_time_height_panel_grid(
                    var_name,
                    datasets,
                    short_ids,
                    time_offset,
                    height_cord,
                    output_subdir,
                    labelsize,
                    ticksize,
                    usercmap,
                    diurnal_start_day,
                    diurnal_end_day,
                    max_height_timeheight,
                    is_diurnal=True
                )
                if outfile:
                    diurnal2d_plots.append(outfile)

    # Close datasets
    for ds in datasets:
        ds.close()

    #############################################################################################################
    # End of diagnostics generation, rest of program makes web interface

    # HTML Templates with different width and max-width settings
    profile_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                padding: 10px;
            }
            .grid-item {
                text-align: center;
            }
            img {
                width: 100%;  /* Profile plot width */
                max-width: 500px;  /* Profile plot max width */
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <div class="grid-container">
        {% for img in images %}
            <div class="grid-item">
                <h3>{{ img }}</h3>
                <img src="plots/{{ img }}" alt="{{ img }}">
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
    """

    timeseries_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                padding: 10px;
            }
            .grid-item {
                text-align: center;
            }
            img {
                width: 100%;  /* Time series plot width */
                max-width: 800px;  /* Time series plot max width */
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <div class="grid-container">
        {% for img in images %}
            <div class="grid-item">
                <h3>{{ img }}</h3>
                <img src="plots/{{ img }}" alt="{{ img }}">
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
    """

    time_height_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 10px;
            }
            .grid-item {
                text-align: center;
            }
            img {
                width: 100%;  /* Time-height plot width */
                max-width: 900px;  /* Time-height plot max width */
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <div class="grid-container">
        {% for img in images %}
            <div class="grid-item">
                <h3>{{ img }}</h3>
                <img src="plots/{{ img }}" alt="{{ img }}">
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
    """

    diurnal1d_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                padding: 10px;
            }
            .grid-item {
                text-align: center;
            }
            img {
                width: 100%;  /* Diurnal Composite plot width */
                max-width: 800px;  /* Diurnal Composite plot max width */
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <div class="grid-container">
        {% for img in images %}
            <div class="grid-item">
                <h3>{{ img }}</h3>
                <img src="plots/{{ img }}" alt="{{ img }}">
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
    """

    diurnal2d_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 10px;
            }
            .grid-item {
                text-align: center;
            }
            img {
                width: 100%;  /* Time-height plot width */
                max-width: 900px;  /* Time-height plot max width */
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <div class="grid-container">
        {% for img in images %}
            <div class="grid-item">
                <h3>{{ img }}</h3>
                <img src="plots/{{ img }}" alt="{{ img }}">
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
    """

    # Generate profile HTML files for each averaging window
    for window_idx, (start_time, end_time) in enumerate(zip(profile_time_s, profile_time_e)):
        sorted_images = sorted([os.path.basename(p[0]) for p in profile_plots if p[1] == window_idx+1],key=str.lower)
        profile_html_content = Template(profile_html_template).render(
            title=f"Profile Plots (Averaging Window: Day {start_time} to Day {end_time})",
            images=sorted_images
        )
        html_filename = os.path.join(output_dir, general_id, f"profile_plots_window{window_idx+1}.html")
        with open(html_filename, "w") as f:
            f.write(profile_html_content)

    # Generate timeseries HTML file
    sorted_timeseries_images = sorted([os.path.basename(t) for t in timeseries_plots],key=str.lower)
    timeseries_html_content = Template(timeseries_html_template).render(
        title="Time Series Plots",
        images=sorted_timeseries_images
    )
    with open(os.path.join(output_dir, general_id, "timeseries_plots.html"), "w") as f:
        f.write(timeseries_html_content)

    # Generate time-height HTML file
    sorted_time_height_images = sorted([os.path.basename(p) for p in time_height_plots],key=str.lower)
    time_height_html_content = Template(time_height_html_template).render(
        title="Time-Height Plots",
        images=sorted_time_height_images
    )
    with open(os.path.join(output_dir, general_id, "time_height_plots.html"), "w") as f:
        f.write(time_height_html_content)

    # Generate diurnal composite HTML file
    sorted_diurnal1d_images = sorted([os.path.basename(t) for t in diurnal1d_plots],key=str.lower)
    diurnal1d_html_content = Template(diurnal1d_html_template).render(
        title=f"Diurnal Cycle 1D Composite Plots: Day {diurnal_start_day_web} to {diurnal_end_day_web}",
        images=sorted_diurnal1d_images
    )
    with open(os.path.join(output_dir, general_id, "diurnal1d_plots.html"), "w") as f:
        f.write(diurnal1d_html_content)

    # Generate diurnal composite HTML file
    sorted_diurnal2d_images = sorted([os.path.basename(t) for t in diurnal2d_plots],key=str.lower)
    diurnal2d_html_content = Template(diurnal2d_html_template).render(
        title=f"Diurnal Cycle 2D Composite Plots: Day {diurnal_start_day_web} to {diurnal_end_day_web}",
        images=sorted_diurnal2d_images
    )
    with open(os.path.join(output_dir, general_id, "diurnal2d_plots.html"), "w") as f:
        f.write(diurnal2d_html_content)

    # Main HTML page with links to profile, timeseries, and time-height pages
    main_html_content = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ general_id }} Diagnostics</title>
        <style>
            .logo-container {
                display: flex;
                align-items: center;
                gap: 20px; /* Adjust spacing between logos */
            }
            .logo-container img {
                width: 150px; /* Adjust logo size */
                height: auto;
            }
            header h1 {
                margin: 10px 0; /* Add space around the title */
            }
            header h2 {
                margin: 5px 0; /* Add space around the subtitle */
                font-size: 1.2em; /* Slightly smaller font size for the subtitle */
                color: gray; /* Optional: Add color to distinguish the subtitle */
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo-container">
                <img src="plots/thread_logo.png" alt="Thread Logo">
                <img src="plots/asr_logo_final.png" alt="Logo 1">
                <img src="plots/arm_logo.png" alt="Logo 2">
                <img src="plots/e3sm_logo.png" alt="Logo 3">
            </div>
            <h1>ARM/ASR Diagnostics Package for E3SM SCM and DP-SCREAM</h1>
            <h2>Case: {{ general_id }}</h2>
        </header>
        <ul>
            {% for idx, (start_time, end_time) in profile_windows %}
            <li>
                <a href="profile_plots_window{{ idx+1 }}.html">
                    Profile Plots (Averaging Window: Day {{ "%.1f" | format(start_time) }} to Day {{ "%.1f" | format(end_time) }})
                </a>
            </li>
            {% endfor %}
            <li><a href="timeseries_plots.html">Time Series Plots</a></li>
	    {% if do_timeheight %}
            <li><a href="time_height_plots.html">Time-Height Plots</a></li>
	    {% endif %}
	    {% if do_diurnal_composites %}
            <li><a href="diurnal1d_plots.html">Diurnal Cycle 1D Composite Plots (Day {{ "%.1f" | format(diurnal_start_day_web) }} to Day {{ "%.1f" | format(diurnal_end_day_web) }})</a></li>
	    {% endif %}
	    {% if do_diurnal_composites %}
            <li><a href="diurnal2d_plots.html">Diurnal Cycle 2D Composite Plots (Day {{ "%.1f" | format(diurnal_start_day_web) }} to Day {{ "%.1f" | format(diurnal_end_day_web) }})</a></li>
	    {% endif %}
        </ul>
    </body>
    </html>
    """).render(
        general_id=general_id,
        profile_windows=list(enumerate(zip(profile_time_s, profile_time_e))),
        diurnal_start_day_web=diurnal_start_day_web,
        diurnal_end_day_web=diurnal_end_day_web,
        do_timeheight=bool(do_timeheight),
	do_diurnal_composites=bool(do_diurnal_composites)
    )

    with open(os.path.join(output_dir, general_id, "index.html"), "w") as f:
        f.write(main_html_content)

    # Tar all the plots and HTML files
    tar_filename = os.path.join(output_dir, f"{general_id}_diagnostics.tar")
    with tarfile.open(tar_filename, "w") as tar:
        tar.add(os.path.join(output_dir, general_id, "index.html"), arcname="index.html")
        for window_idx in range(len(profile_time_s)):
            tar.add(os.path.join(output_dir, general_id, f"profile_plots_window{window_idx+1}.html"), arcname=f"profile_plots_window{window_idx+1}.html")
        tar.add(os.path.join(output_dir, general_id, "timeseries_plots.html"), arcname="timeseries_plots.html")
        tar.add(os.path.join(output_dir, general_id, "time_height_plots.html"), arcname="time_height_plots.html")
        tar.add(os.path.join(output_dir, general_id, "diurnal1d_plots.html"), arcname="diurnal1d_plots.html")
        tar.add(os.path.join(output_dir, general_id, "diurnal2d_plots.html"), arcname="diurnal2d_plots.html")
        tar.add(output_subdir, arcname="plots")

    print(f"Created archive {tar_filename} containing all plots and HTML files.")
    print("Ending IOP Diagnostics Package")

