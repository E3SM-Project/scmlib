import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import tarfile
from jinja2 import Template
from scipy.interpolate import interp1d

##########################################################
# Quick diagnostics package for E3SM Single Column Model (SCM)
#  or doubly-periodic EAMxx (DP-EAMxx).
# NOTE that for DP-EAMxx this program only works on output
#  streams that contain horizontally averaged output.

# Will produce time averaged profile plots, time series plots,
#  and time height plots.
# Finally, will produce .tar file with plots and html viewer.

# This is a work in progress that will be routinely updated.
# Upcoming features: ability to plot against ARM observations
#  and LES!

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?  Provide path.
output_dir = "dpxx_quickdiags"

# User-specified general ID for this diagnostic set
general_id = "magic_conv"  # Change as needed

# Where are simulation case directories stored?
#   This program assumes that all output is in the run directory for each case.
base_dir = "/pscratch/sd/b/bogensch/dp_screamxx_conv/"

# User-specified list of casenames and corresponding short IDs
casenames = ["scream_dpxx_MAGIC.cntl.001a",
             "scream_dpxx_MAGIC.conv.001a",
             "scream_dpxx_MAGIC.conv.002a"]  # Example casenames
# short IDs used in legend
short_ids = ["CNTL","MICRO","MICRO+SHOC"]

# All cases should end with this appendix for the output stream to be considered
caseappend = ".horiz_avg.AVERAGE.nmins_x5.2013-07-21-19620.nc"

# Define start and end times for averaging for profiles as numerical values in days
profile_time_s = [0.2, 1.0, 2.0]  # Starting times for averaging
profile_time_e = [1.0, 2.0, 3.0]  # Ending times for averaging (put "end" to average to end of simulation)

# END: MANDATORY USER DEFINED SETTINGS
##########################################################
##########################################################
# BEGIN: OPTIONAL user defined settings

# Do time-height plots? These can take a bit longer to make
do_timeheight=False

# Choose vertical plotting coordinate; can be pressure or height.
#  -If height then the variable Z3 (E3SM) or z_mid (EAMxx) needs to be in your output file.
#  -If pressure then PS (E3SM) or ps (EAMxx) should be in your output file.  If it is not then
#    the package will use hybrid levels to plot, which may not be accurate compared to observations.
height_cord = "z"  # p = pressure; z = height

# Optional: Maximum y-axis height for profile plots (in meters or mb; depending on vertical coordinate)
max_height_profile = 2000  # Set to desired height in meters or mb, or None for automatic scaling

# Optional: Maximum y-axis height for time-height (in meters or mb; depending on vertical coordinate)
max_height_timeheight = 4000  # Set to desired height in meters or mb, or None for automatic scaling

# linewidth for curves
linewidth = 4

# Optional: Time range for time series plots in days
time_series_time_s = None  # Starting time for time series, None for default (entire range)
time_series_time_e = None  # Ending time for time series, None for default (entire range)

# Optional: Time range for time-height plots in days
time_height_time_s = None  # Starting time for time-height plots, None for default (entire range)
time_height_time_e = None  # Ending time for time-height plots, None for default (entire range)

# END: OPTIONAL user defined settings
##########################################################
##########################################################

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
        if "z_mid" in ds.data_vars:
            y_coord = ds['z_mid'].isel(time=time_indices).mean(dim="time").squeeze()
        elif "z_mid_horiz_avg" in ds.data_vars:
            y_coord = ds['z_mid_horiz_avg'].isel(time=time_indices).mean(dim="time").squeeze()
        elif "Z3" in ds.data_vars:
            # Adjust Z3 by subtracting surface elevation
            lev0 = ds['Z3'].isel(lev=-1).mean(dim="time")  # Get Z3 at highest ilev index
            surface_elevation = lev0 - 10.0  # Assume bottom layer of 10 meters
            y_coord = ds['Z3'].isel(time=time_indices).mean(dim="time").squeeze() - surface_elevation
        else:
            raise ValueError("Cannot determine height coordinates ('z_mid', or 'Z3').")

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
        else:
            print(f"Warning: 'PS' or 'ps' is missing. Using hybrid pressure coordinates.")
            y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
    else:
        raise ValueError(f"Invalid height_cord: {height_cord}. Must be 'z' or 'p'.")

    return y_coord


# START CODE

# Make output directory for plots
output_subdir = os.path.join(output_dir, general_id, "plots")
os.makedirs(output_subdir, exist_ok=True)

# Make output directory for diagnostics
os.makedirs(output_dir, exist_ok=True)

# Verify the lengths of casenames and short_ids are the same
if len(casenames) != len(short_ids):
    raise ValueError("The number of casenames must match the number of short_ids.")

# Collect datasets and simulation labels
file_paths = [os.path.join(base_dir, case, "run", f"{case}{caseappend}") for case in casenames]
datasets = []

for fp, short_id in zip(file_paths, short_ids):
    ds = xr.open_dataset(fp)
#    if "ncol" in ds.dims and ds.dims["ncol"] != 1:
#        print(f"Warning: File {fp} has ncol={ds.dims['ncol']}, which is not equal to 1. Skipping this file.")
#        continue
    datasets.append(ds)

# Prepare lists to keep track of plot filenames for HTML pages
profile_plots = []
timeseries_plots = []
time_height_plots = []

# Collect all unique variables across datasets
all_vars = set()
for ds in datasets:
    all_vars.update(ds.data_vars.keys())

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
                time_in_days = (ds['time'] - ds['time'][0]) / np.timedelta64(1, 'D')

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

                plt.xlabel(var_units, fontsize=14)
                ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
                plt.ylabel(ylabel, fontsize=14)
                plt.title(f"{var_long_name} Profile (Window {window_idx+1})", fontsize=16)
                plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
                plt.grid(color='#95a5a6', linestyle='--', linewidth=2, alpha=0.5)

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
for var_name in all_vars:
    # Determine if the variable qualifies as a time series variable
    if any(var_name in ds.data_vars and
        ds[var_name].ndim in [1, 2] and
        'time' in ds[var_name].dims and
        not any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) for ds in datasets):

        plt.figure(figsize=(10, 5))
        valid_plot = False  # Track if any data was valid for this variable

        # Loop over each dataset, using short_ids for the legend
        for ds, short_id in zip(datasets, short_ids):
            if var_name not in ds.data_vars:
                print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                continue  # Skip this case if variable is missing

            valid_plot = True  # At least one dataset has the variable

            # Convert `time` to a numeric array in days since the start
            time_in_days = (ds['time'] - ds['time'][0]) / np.timedelta64(1, 'D')

            # Determine indices for the specified range
            start_time = time_series_time_s if time_series_time_s is not None else time_in_days[0]
            end_time = time_series_time_e if time_series_time_e is not None else time_in_days[-1]
            time_indices = np.where((time_in_days >= start_time) & (time_in_days <= end_time))[0]

            # Select data within the filtered time range
            if ds[var_name].ndim == 2 and 'ncol' in ds[var_name].dims:
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
            plt.xlabel("Time (days)", fontsize=14)

            # Get attributes for the variable from the first dataset that contains it
            var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
            var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)

            # Labeling and setting the plot title
            plt.ylabel(var_units, fontsize=14)
            title = f"{var_long_name} Time Series"  
            plt.title(title, fontsize=16)
            plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
            plt.grid(color='#95a5a6',linestyle='--',linewidth=2,alpha=0.5)
            plt.grid('True')

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
        for ds in datasets:
            if var_name in ds.data_vars:
                if 'ncol' in ds[var_name].dims:
                    data = ds[var_name].mean(dim="ncol")
                else:
                    data = ds[var_name]
                global_min = min(global_min, data.min().values)
                global_max = max(global_max, data.max().values)

        # Handle case where global_min == global_max
        if global_min == global_max:
            print(f"Warning: Variable '{var_name}' has constant value {global_min}. Adjusting color scale.")
            global_min -= 0.01 * abs(global_min) if global_min != 0 else 0.01
            global_max += 0.01 * abs(global_max) if global_max != 0 else 0.01

        levels = np.linspace(global_min, global_max, 20)  # Define consistent levels

        # Loop over each dataset, creating a multi-panel plot for each case
        fig, axes = plt.subplots(1, len(datasets), figsize=(15, 6), sharey=True, constrained_layout=True)
        if len(datasets) == 1:
            axes = [axes]  # Ensure axes is always a list

        valid_plot = False  # Track if any data was valid for this variable
        contours = []  # Store contour objects for shared colorbar

        for ax, (ds, short_id) in zip(axes, zip(datasets, short_ids)):
            if var_name not in ds.data_vars:
                print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                ax.set_visible(False)
                continue  # Skip this case if variable is missing

            valid_plot = True  # At least one dataset has the variable

            # Convert `time` to a numeric array in days since the start
            time_in_days = (ds['time'] - ds['time'][0]) / np.timedelta64(1, 'D')

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
            contour = ax.contourf(time_values, np.squeeze(y_coord), data.T, levels=levels, cmap="viridis")
            contours.append(contour)

            ax.set_title(short_id, fontsize=14)
            ax.set_xlabel("Time (days)", fontsize=12)
            if ax is axes[0]:
                ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
                ax.set_ylabel(ylabel, fontsize=12)

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

        if valid_plot:
            # Add a single colorbar for the entire figure
            cbar = fig.colorbar(contours[0], ax=axes, orientation='vertical', aspect=30, shrink=0.8, pad=0.02)
            cbar.set_label(ds[var_name].attrs.get('units', 'Value'), fontsize=14)
            cbar.ax.tick_params(labelsize=12)  # Increase tick label size for colorbar

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
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 10px;
        }
        .grid-item {
            text-align: center;
        }
        img {
            width: 100%;  /* Time-height plot width */
            max-width: 800px;  /* Time-height plot max width */
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
for window_idx in range(len(profile_time_s)):
    profile_html_content = Template(profile_html_template).render(
        title=f"Profile Plots (Window {window_idx+1})",
        images=[os.path.basename(p[0]) for p in profile_plots if p[1] == window_idx+1]
    )
    html_filename = os.path.join(output_dir, general_id, f"profile_plots_window{window_idx+1}.html")
    with open(html_filename, "w") as f:
        f.write(profile_html_content)

# Generate timeseries and time-height HTML files
timeseries_html_content = Template(timeseries_html_template).render(
    title="Time Series Plots", 
    images=[os.path.basename(t) for t in timeseries_plots]
)
time_height_html_content = Template(time_height_html_template).render(
    title="Time-Height Plots", 
    images=[os.path.basename(p) for p in time_height_plots]
)

with open(os.path.join(output_dir, general_id, "timeseries_plots.html"), "w") as f:
    f.write(timeseries_html_content)
with open(os.path.join(output_dir, general_id, "time_height_plots.html"), "w") as f:
    f.write(time_height_html_content)

# Main HTML page with links to profile, timeseries, and time-height pages
main_html_content = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ general_id }} Diagnostics</title>
</head>
<body>
    <h1>{{ general_id }} Diagnostics</h1>
    <ul>
        {% for window_idx in range(num_windows) %}
        <li><a href="profile_plots_window{{ window_idx+1 }}.html">Profile Plots (Window {{ window_idx+1 }})</a></li>
        {% endfor %}
        <li><a href="timeseries_plots.html">Time Series Plots</a></li>
        <li><a href="time_height_plots.html">Time-Height Plots</a></li>
    </ul>
</body>
</html>
""").render(general_id=general_id, num_windows=len(profile_time_s))

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
