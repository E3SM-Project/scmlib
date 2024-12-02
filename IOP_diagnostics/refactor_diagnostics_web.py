import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import tarfile
from jinja2 import Template

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?
output_dir = "dpxx_quickdiags"

# Where are simulations stored?
base_dir = "/pscratch/sd/b/bogensch/dp_scream3"

# User-specified general ID for this diagnostic set
general_id = "example_diagnostic_set"  # Change as needed

# User-specified list of casenames and corresponding short IDs
casenames = ["e3sm_scm_MAGIC.v2.001a"]  # Example casenames
short_ids = ["control"]  # Example short IDs for legend

caseappend = ".eam.h0.2013-07-21-19620.nc"

# Define start and end times for averaging as numerical values in days
time_s = 2.0   # Starting time for averaging
time_e = 3.0  # Ending time for averaging

# END: MANDATORY USER DEFINED SETTINGS
##########################################################
##########################################################
# Begin: User defined options - Set to defaults

# Can be height or pressure
height_cord = "p" # p = pressure; z = height

# Optional: Maximum y-axis height for profile plots (in meters or mb)
max_height = 400  # Set to desired height in meters or mb, or None for automatic scaling

# linewidth for curves
linewidth = 4

# End: User defined options
##########################################################
##########################################################

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

# Check if ncol is 1 for all files
for fp, short_id in zip(file_paths, short_ids):
    ds = xr.open_dataset(fp)
    if "ncol" in ds.dims and ds.dims["ncol"] != 1:
        print(f"Warning: File {fp} has ncol={ds.dims['ncol']}, which is not equal to 1. Skipping this file.")
        continue
    datasets.append(ds)

# Prepare lists to keep track of plot filenames for HTML pages
profile_plots = []
timeseries_plots = []

# Plot profile variables with three dimensions (e.g., time, ncol, lev)
for var_name, var_data in datasets[0].data_vars.items():
    if var_data.ndim == 3 and any(dim in ['lev'] for dim in var_data.dims) \
      and any(dim in ['time'] for dim in var_data.dims) and any(dim in ['ncol'] for dim in var_data.dims):

        plt.figure(figsize=(8, 6))

        # Loop over each dataset, using short_ids for the legend
        for ds, short_id in zip(datasets, short_ids):
            # Convert `time` to a numeric array in days since the start, to avoid datetime conflicts
            time_in_days = (ds['time'] - ds['time'][0]) / np.timedelta64(1, 'D')

            # Determine indices for the specified range
            time_indices = np.where((time_in_days >= time_s) & (time_in_days <= time_e))[0]

            # Select data within the filtered time range and take the mean over time
            time_filtered_data = ds[var_name].isel(time=time_indices).mean(dim="time")

            # Choose the y-coordinate based on height_cord
            if height_cord == "z":
                if "z_mid" in ds.data_vars:
                    y_coord = ds['z_mid'].isel(time=time_indices).mean(dim="time").squeeze()
                elif "Z3" in ds.data_vars:
                    # Adjust Z3 by subtracting surface elevation
                    lev0 = ds['Z3'].isel(lev=-1).mean(dim="time")  # Get Z3 at highest ilev index
                    surface_elevation = lev0 - 10.0  # Assume bottom layer of 10 meters
                    y_coord = ds['Z3'].isel(time=time_indices).mean(dim="time").squeeze() - surface_elevation
                else:
                    raise ValueError("Neither 'z_mid' nor 'Z3' is found for height_cord='z'.")
            elif height_cord == "p":
                # Check for surface pressure variable
                ps_var = None
                if 'PS' in ds.data_vars:
                    ps_var = 'PS'
                elif 'ps' in ds.data_vars:
                    ps_var = 'ps'

                if ps_var and all(var in ds for var in ['hyam', 'hybm']):
                    # Compute the pressure-based y-coordinate
                    hyam = ds['hyam']
                    hybm = ds['hybm']
                    ps_avg = ds[ps_var].isel(time=time_indices).mean(dim="time") / 100.0  # Convert to hPa
                    y_coord = 1000.0 * hyam + hybm * ps_avg
                else:
                    # Warn the user and fall back to hybrid pressure coordinates
                    print(f"Warning: 'PS' or 'ps' and/or 'hyam', 'hybm' are missing. Plotting against hybrid pressure coordinates ('lev').")
                    y_coord = ds['lev']  # Use hybrid pressure coordinate
            else:
                raise ValueError(f"Invalid height_cord: {height_cord}. Must be 'z' or 'p'.")

            # Plot profile with increased line width
            plt.plot(np.squeeze(time_filtered_data), y_coord, label=short_id, linewidth=linewidth)

        # Set y-axis limit if specified
        if max_height is not None:
            if height_cord == "z":
                plt.ylim([0, max_height])
            elif height_cord == "p":
                plt.ylim([max_height, y_coord.max()])  # Adjust for pressure

        # Reverse the y-axis if plotting against pressure
        if height_cord == "p":
            plt.gca().invert_yaxis()

        # Labeling and saving the plot with larger font sizes
        plt.xlabel(var_data.attrs.get('units', 'Value'), fontsize=14)
        ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
        plt.ylabel(ylabel, fontsize=14)
        title = f"{var_data.long_name} Profile" if 'long_name' in var_data.attrs else f"{var_name} Profile"
        plt.title(title, fontsize=16)
        plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
        plt.grid(True)

        # Save plot in the general_id subdirectory
        plot_filename = os.path.join(output_subdir, f"{var_name}_profile.jpg")
        plt.savefig(plot_filename, format='jpg')
        plt.close()
        print(f"Saved profile plot for {var_name} as {plot_filename}")

        # Add to profile plots list for HTML generation
        profile_plots.append(plot_filename)

# Plot time series for variables with two dimensions (e.g., time, ncol)
for var_name, var_data in datasets[0].data_vars.items():
    if var_data.ndim == 2 and any(dim in ['time'] for dim in var_data.dims) \
       and any(dim in ['ncol'] for dim in var_data.dims):  # Generalized to check for 2D variables

        plt.figure(figsize=(10, 5))

        # Loop over each dataset, using short_ids for the legend
        for ds, short_id in zip(datasets, short_ids):
            # Convert `time` to a numeric array in days since the start
            time_in_days = (ds['time'] - ds['time'][0]) / np.timedelta64(1, 'D')
            variable_data = ds[var_name][:, 0]  # Select the single column (ncol = 1)

            # Plot time series with increased line width
            plt.plot(time_in_days, variable_data, label=short_id, linewidth=linewidth)

        # Labeling and saving the plot with larger font sizes
        plt.xlabel("Time (days)", fontsize=14)
        plt.ylabel(var_data.attrs.get('units', 'Value'), fontsize=14)
        title = f"{var_data.long_name} Time Series" if 'long_name' in var_data.attrs else f"{var_name} Time Series"
        plt.title(title, fontsize=16)
        plt.legend(title="Simulations", fontsize=12, title_fontsize=14)
        plt.grid(True)

        # Save plot in the general_id subdirectory
        plot_filename = os.path.join(output_subdir, f"{var_name}_timeseries.jpg")
        plt.savefig(plot_filename, format='jpg')
        plt.close()
        print(f"Saved time series plot for {var_name} as {plot_filename}")

        # Add to timeseries plots list for HTML generation
        timeseries_plots.append(plot_filename)

# Close datasets
for ds in datasets:
    ds.close()

# HTML Templates for profile and timeseries pages with grid layout
html_template = """
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
            width: 90%;  /* Increased width */
            max-width: 600px;  /* Increased max width */
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

# Generate profile and timeseries HTML files
profile_html_content = Template(html_template).render(title="Profile Plots", images=[os.path.basename(p) for p in profile_plots])
timeseries_html_content = Template(html_template).render(title="Time Series Plots", images=[os.path.basename(t) for t in timeseries_plots])

# Write profile and timeseries HTML files to disk
with open(os.path.join(output_dir, general_id, "profile_plots.html"), "w") as f:
    f.write(profile_html_content)
with open(os.path.join(output_dir, general_id, "timeseries_plots.html"), "w") as f:
    f.write(timeseries_html_content)

# Main HTML page with links to profile and timeseries pages
main_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ general_id }} Diagnostics</title>
</head>
<body>
    <h1>{{ general_id }} Diagnostics</h1>
    <ul>
        <li><a href="profile_plots.html">Profile Plots</a></li>
        <li><a href="timeseries_plots.html">Time Series Plots</a></li>
    </ul>
</body>
</html>
"""

main_html = Template(main_html_content).render(general_id=general_id)
with open(os.path.join(output_dir, general_id, "index.html"), "w") as f:
    f.write(main_html)

# Tar all the plots and HTML files
tar_filename = os.path.join(output_dir, f"{general_id}_diagnostics.tar")
with tarfile.open(tar_filename, "w") as tar:
    tar.add(os.path.join(output_dir, general_id, "index.html"), arcname="index.html")
    tar.add(os.path.join(output_dir, general_id, "profile_plots.html"), arcname="profile_plots.html")
    tar.add(os.path.join(output_dir, general_id, "timeseries_plots.html"), arcname="timeseries_plots.html")
    tar.add(output_subdir, arcname="plots")

print(f"Created archive {tar_filename} containing all plots and HTML files.")
