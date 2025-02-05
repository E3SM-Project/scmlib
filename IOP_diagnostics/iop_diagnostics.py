import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import tarfile
from jinja2 import Template
from scipy.interpolate import interp1d

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
        if ps_var:
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
            y_coord = ds['p_mid_obs'].isel(time=time_indices).mean(dim="time")
        elif 'p_mid_les' in ds.data_vars:
            y_coord = ds['p_mid_les'].isel(time=time_indices).mean(dim="time")
        else:
            print(f"Warning: 'PS' or 'ps' is missing. Using hybrid pressure coordinates.")
            y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
    else:
        raise ValueError(f"Invalid height_cord: {height_cord}. Must be 'z' or 'p'.")

    return y_coord

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
    usercmap="viridis_r"
):

    # Define some sizing parameters
    ticksize=14
    labelsize=14

    # START CODE

    # Make output directory for plots
    output_subdir = os.path.join(output_dir, general_id, "plots")
    os.makedirs(output_subdir, exist_ok=True)

    # Make output directory for diagnostics
    os.makedirs(output_dir, exist_ok=True)

    # Copy over logos for webpages
    os.system('cp logos/thread_logo.png '+output_subdir)
    os.system('cp logos/asr_logo_final.png '+output_subdir)
    os.system('cp logos/arm_logo.png '+output_subdir)
    os.system('cp logos/e3sm_logo.png '+output_subdir)

    # Collect datasets and simulation labels
    file_paths = [os.path.join(base_dir, case, "run", f"{case}{caseappend}") for case in casenames]
    datasets = []

    for fp, short_id in zip(file_paths, short_ids):
        ds = xr.open_dataset(fp, decode_times=False)
        datasets.append(ds)

    # Add LES file
    if les_file is not None:
       ds = xr.open_dataset(les_file, decode_times=False)
       datasets.append(ds)

    # Add Observation file
    if obs_file is not None:
       ds = xr.open_dataset(obs_file, decode_times=False)
       datasets.append(ds)

    # Verify the lengths of casenames and short_ids are the same
    if len(datasets) != len(short_ids):
        raise ValueError("The number of casenames must match the number of short_ids.")

    # Prepare lists to keep track of plot filenames for HTML pages
    profile_plots = []
    timeseries_plots = []
    time_height_plots = []

    # Collect all unique variables across datasets
    all_vars = set()
    for ds in datasets:
        all_vars.update(ds.data_vars.keys())

        # Check if both 'PRECC' and 'PRECL' are in the dataset
        if 'PRECC' in ds.data_vars and 'PRECL' in ds.data_vars:
            # Add 'PRECT' to all_vars if it's not already there
            all_vars.add('PRECT')

    #############################################################################################################
    # Plot profile variables with three dimensions (e.g., time, ncol, lev or ilev)
    for var_name in all_vars:
        # Determine if the variable qualifies as a profile variable
        if any(var_name in ds.data_vars and
            ds[var_name].ndim in [2, 3] and
            any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
            'time' in ds[var_name].dims for ds in datasets):

            # Loop over multiple averaging windows
            for window_idx, (start_time, end_time) in enumerate(zip(profile_time_s, profile_time_e)):
                plt.figure(figsize=(8, 6))
                valid_plot = False  # Track if any data was valid for this variable

                # Loop over each dataset, using short_ids for the legend
                for ds, short_id in zip(datasets, short_ids):
                    if var_name not in ds.data_vars:
                        print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                        continue  # Skip this case if variable is missing

                    valid_plot = True  # At least one dataset has the variable

                    # Convert `time` to a numeric array in days since the start
                    time_in_days = ds['time']

                    # Determine indices for the specified range
                    start_time = start_time if start_time != "end" else time_in_days[0]
                    end_time = end_time if end_time != "end" else time_in_days[-1]
                    time_indices = np.where((time_in_days >= start_time) & (time_in_days <= end_time))[0]

                    # Select data within the filtered time range and take the mean over time
                    time_filtered_data = ds[var_name].isel(time=time_indices).mean(dim="time")

                    # Compute vertical coordinate
                    y_coord = compute_y_coord(ds, time_indices, height_cord, var_name)

                    # Apply y-axis limits
                    if height_cord == "z":
                        y_min, y_max = (0, max_height_profile) if max_height_profile is not None else (y_coord.min(), y_coord.max())
                    elif height_cord == "p":
                        y_min, y_max = (max_height_profile, y_coord.max()) if max_height_profile is not None else (y_coord.min(), y_coord.max())

                    # Filter data to include only levels within the y-axis limits
                    valid_indices = np.where((y_coord >= y_min) & (y_coord <= y_max))[0]
                    filtered_y_coord = y_coord[valid_indices]
                    filtered_data = time_filtered_data.isel(lev=valid_indices) if "lev" in time_filtered_data.dims else time_filtered_data.isel(ilev=valid_indices)

                    # Plot profile
                    plt.plot(np.squeeze(filtered_data), filtered_y_coord, label=short_id, linewidth=linewidth)

                if valid_plot:
                    # Set y-axis limits
                    plt.ylim([y_min, y_max])

                    # Reverse the y-axis if plotting against pressure
                    if height_cord == "p":
                        plt.gca().invert_yaxis()

                    # Labeling and saving the plot
                    var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                    var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                    if (var_long_name == "MISSING"):
                        var_long_name = var_name

                    plt.xlabel(var_units, fontsize=labelsize)
                    ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
                    plt.ylabel(ylabel, fontsize=labelsize)
                    plt.title(f"{var_long_name} Profile (Day {start_time} to Day {end_time})", fontsize=16)
                    plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, alpha=0.5)

                    # Make things easier to see
                    plt.tick_params(labelsize=ticksize)

                    # Save plot
                    plot_filename = os.path.join(output_subdir, f"{var_name}_profile_window{window_idx+1}.jpg")
                    plt.savefig(plot_filename, format='jpg')
                    plt.close()
                    print(f"Saved profile plot for {var_name} (Window {window_idx+1}) as {plot_filename}")

                    # Add to profile plots list for HTML generation
                    profile_plots.append((plot_filename, window_idx+1))
                else:
                    print(f"Warning: Variable '{var_name}' was not found in any dataset. Skipping this variable.")

    #############################################################################################################
    # Plot time series for variables with two dimensions (e.g., time, ncol)
    prect_treatment=False # Initialize special treatment for PRECT to False
    for var_name in all_vars:
        # Determine if the variable qualifies as a time series variable
        if (
            any(
                var_name in ds.data_vars and
                ds[var_name].ndim in [1, 2] and
                'time' in ds[var_name].dims and
                not any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims)
                for ds in datasets
            )
            or (var_name == 'PRECT')
        ):

            plt.figure(figsize=(10, 5))
            valid_plot = False  # Track if any data was valid for this variable

            # Loop over each dataset, using short_ids for the legend
            for ds, short_id in zip(datasets, short_ids):
                if var_name not in ds.data_vars:
                    if var_name == 'PRECT':
                        if 'PRECC' and 'PRECL' in ds.data_vars:
                            print(f"Computing PRECT from PRECC and PRECL for case '{short_id}'.")
                            prect_treatment=True
                        else:
                            print(f"Variable is PRECT and PRECC and PRECL are not found for '{short_id}'.  Skipping")
                            continue
                    else:
                        print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                        continue  # Skip this case if variable is missing

                valid_plot = True  # At least one dataset has the variable

                # Convert `time` to a numeric array in days since the start
                time_in_days = ds['time']

                # Determine indices for the specified range
                start_time = time_series_time_s if time_series_time_s is not None else time_in_days[0]
                end_time = time_series_time_e if time_series_time_e is not None else time_in_days[-1]
                time_indices = np.where((time_in_days >= start_time) & (time_in_days <= end_time))[0]

                # check first to see if we are doing special treatment calculation for PRECT
                if prect_treatment:
                    variable_data = ds['PRECC'].isel(time=time_indices)[:,0]+\
                        ds['PRECL'].isel(time=time_indices)[:,0]
                    prect_treatment=False # reset
                elif ds[var_name].ndim == 2 and 'ncol' in ds[var_name].dims:
                        variable_data = ds[var_name].isel(time=time_indices)[:, 0]  # Select the single column (ncol = 1)
                elif ds[var_name].ndim == 1 and 'time' in ds[var_name].dims:
                    variable_data = ds[var_name].isel(time=time_indices)
                else:
                    print(f"Warning: Variable '{var_name}' has unexpected dimensions. Skipping for this case.")
                    continue

                # Plot time series with increased line width
                plt.plot(time_in_days[time_indices], variable_data, label=short_id, linewidth=linewidth)

            if valid_plot:
                # Labeling and saving the plot with larger font sizes
                plt.xlabel("Time (days)", fontsize=labelsize)

                # Do special treatment variables first
                if (var_name == 'PRECT'):
                    var_units='m/s'
                    var_long_name='Total Surface Precipitation Rate'
                else:
                    # Get attributes for the variable from the first dataset that contains it
                    var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                    var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                    if (var_long_name == "MISSING"):
                        var_long_name = var_name

                # Labeling and setting the plot title
                plt.ylabel(var_units, fontsize=labelsize)
                title = f"{var_long_name} Time Series"
                plt.title(title, fontsize=16)
                plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                plt.grid(color='#95a5a6',linestyle='--',linewidth=2,alpha=0.5)
                plt.grid('True')

                # Make things easier to see
                plt.tick_params(labelsize=ticksize)

                # Save plot in the general_id subdirectory
                plot_filename = os.path.join(output_subdir, f"{var_name}_timeseries.jpg")
                plt.savefig(plot_filename, format='jpg')
                plt.close()
                print(f"Saved time series plot for {var_name} as {plot_filename}")

                # Add to timeseries plots list for HTML generation
                timeseries_plots.append(plot_filename)
            else:
                print(f"Warning: Variable '{var_name}' was not found in any dataset. Skipping this variable.")

    #############################################################################################################
    # Plot time-height variables (two or three dimensions: time, ncol, lev or ilev)
    for var_name in all_vars:
        # Determine if the variable qualifies for a time-height plot
        if do_timeheight and any(var_name in ds.data_vars and
            ds[var_name].ndim in [2, 3] and
            any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
            'time' in ds[var_name].dims for ds in datasets):

            # Find global min and max values for consistent color scale across cases
            global_min, global_max = float('inf'), float('-inf')
            num_plots = 0
            for ds in datasets:
                if var_name in ds.data_vars:

                    # Convert `time` to a numeric array in days since the start
                    time_in_days = ds['time']

                    # Determine indices for the specified range
                    start_time = time_height_time_s if time_height_time_s is not None else time_in_days[0]
                    end_time = time_height_time_e if time_height_time_e is not None else time_in_days[-1]
                    time_indices = np.where((time_in_days >= start_time) & (time_in_days <= end_time))[0]

                    # Compute vertical coordinate
                    y_coord = compute_y_coord(ds, time_indices, height_cord, var_name)

                    # Filter y_coord and data to include only levels within the y-axis limits
                    if height_cord == "z":
                        y_min, y_max = (0, max_height_timeheight) if max_height_timeheight is not None else (y_coord.min(), y_coord.max())
                    elif height_cord == "p":
                        y_min, y_max = (max_height_timeheight, y_coord.max()) if max_height_timeheight is not None else (y_coord.min(), y_coord.max())

                    valid_indices = np.where((y_coord >= y_min) & (y_coord <= y_max))[0]

                    filtered_y_coord = y_coord[valid_indices]
                    filtered_data = ds[var_name].isel(lev=valid_indices) if "lev" in ds[var_name].dims else ds[var_name].isel(ilev=valid_indices)

                    # Handle cases where 'ncol' exists
                    if 'ncol' in filtered_data.dims:
                        filtered_data = filtered_data.mean(dim="ncol")

                    # Update global min and max
                    global_min = min(global_min, filtered_data.min().values)
                    global_max = max(global_max, filtered_data.max().values)
                    num_plots = num_plots+1

            # Handle case where global_min == global_max
            if global_min == global_max:
                print(f"Warning: Variable '{var_name}' has constant value {global_min}. Adjusting color scale.")
                global_min -= 0.01 * abs(global_min) if global_min != 0 else 0.01
                global_max += 0.01 * abs(global_max) if global_max != 0 else 0.01

            levels = np.linspace(global_min, global_max, 20)  # Define consistent levels

            # Determine the number of rows and columns for the layout
            n_cols = 2
            n_rows = -(-num_plots // n_cols)  # Ceiling division to determine rows needed

            # Create the subplots
            fig, axes = plt.subplots(
                n_rows, n_cols,
                figsize=(15, n_rows * 6),
                sharey=True,
                constrained_layout=True
            )

            # Ensure `axes` is always a 2D array
            axes = np.atleast_2d(axes)

            valid_plot = False  # Track if any data was valid for this variable
            contours = []  # Store contour objects for shared colorbar

            # Iterate over datasets and plot in each subplot
            for idx, (ax, (ds, short_id)) in enumerate(zip(axes.flat, zip(datasets, short_ids))):
                if var_name not in ds.data_vars:
                    print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                    ax.set_visible(False)  # Hide this subplot
                    continue  # Skip this case if variable is missing

                valid_plot = True  # At least one dataset has the variable

                # Convert `time` to a numeric array in days since the start
                time_in_days = ds['time']

                # Determine indices for the specified range
                start_time = time_height_time_s if time_height_time_s is not None else time_in_days[0]
                end_time = time_height_time_e if time_height_time_e is not None else time_in_days[-1]
                time_indices = np.where((time_in_days >= start_time) & (time_in_days <= end_time))[0]

                # Extract data within the filtered time range
                if 'ncol' in ds[var_name].dims:
                    data = ds[var_name].isel(time=time_indices).mean(dim="ncol")
                else:
                    data = ds[var_name].isel(time=time_indices)

                time_values = time_in_days[time_indices]

                # Compute vertical coordinate
                y_coord = compute_y_coord(ds, time_indices, height_cord, var_name)

                # Plot the contourf plot
                contour = ax.contourf(time_values, np.squeeze(y_coord), data.T, levels=levels, cmap=usercmap)
                contours.append(contour)

                ax.set_title(short_id, fontsize=16)
                ax.set_xlabel("Time (days)", fontsize=labelsize)
                if idx % n_cols == 0:  # Add ylabel only for the first column
                    ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
                    ax.set_ylabel(ylabel, fontsize=labelsize)

                # Set y-axis limit if specified
                if height_cord == "z":
                    if max_height_profile is not None:
                        ax.set_ylim([0, max_height_profile])
                elif height_cord == "p":
                    if max_height_profile is not None:
                        ax.set_ylim([max_height_profile, y_coord.max()])  # Adjust for pressure
                    else:
                        ax.set_ylim([0, y_coord.max()])

                # Reverse the y-axis if plotting against pressure
                if height_cord == "p":
                    ax.invert_yaxis()

                ax.tick_params(axis='x', labelsize=14)
                ax.tick_params(axis='y', labelsize=14)

            # Hide unused axes
            for ax in axes.flat[len(datasets):]:
                ax.set_visible(False)  # Hide any extra subplot

            if valid_plot:
                # Get attributes for the variable from the first dataset that contains it
                var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
                var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)
                if (var_long_name == "MISSING"):
                    var_long_name = var_name

                # Add a single colorbar for the entire figure
                cbar = fig.colorbar(contours[0], ax=axes, orientation='vertical', aspect=30, shrink=0.8, pad=0.02)
                cbar.set_label(var_units, fontsize=14)
                cbar.ax.tick_params(labelsize=12)  # Increase tick label size for colorbar

                # Make things easier to see
                plt.tick_params(labelsize=ticksize)

                # Save the plot
                plot_filename = os.path.join(output_subdir, f"{var_name}_time_height.jpg")
                plt.savefig(plot_filename, format='jpg')
                plt.close()
                print(f"Saved time-height plot for {var_name} as {plot_filename}")

                # Add to time-height plots list for HTML generation
                time_height_plots.append(plot_filename)
            else:
                print(f"Warning: Variable '{var_name}' was not found in any dataset. Skipping this variable.")

    # Close datasets
    for ds in datasets:
        ds.close()

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
            <li><a href="time_height_plots.html">Time-Height Plots</a></li>
        </ul>
    </body>
    </html>
    """).render(
        general_id=general_id,
        profile_windows=list(enumerate(zip(profile_time_s, profile_time_e)))
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
        tar.add(output_subdir, arcname="plots")

    print(f"Created archive {tar_filename} containing all plots and HTML files.")

