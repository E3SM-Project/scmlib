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

# Will produce .tar file with plots and html viewer.

# Work in progress.

##########################################################
##########################################################
# BEGIN: MANDATORY USER DEFINED SETTINGS

# Where do you want output diagnostics to be placed?  Provide path.
output_dir = "dpxx_quickdiags"

# User-specified general ID for this diagnostic set
general_id = "rce_comp"  # Change as needed

# Where are simulation case directories stored?
#   This program assumes that all output is in the run directory for each case.
base_dir = "/pscratch/sd/b/bogensch/dp_screamxx"

# User-specified list of casenames and corresponding short IDs
casenames = ["scream_dpxx_RCEMIP_300K.001a","scream_dpxx_RCE_200m.300K.001a"]  # Example casenames
# short IDs used in legend
short_ids = ["3 km","200 m"]

# All cases should end with this appendix for the output stream to be considered
caseappend = ".scream.hourly.horiz_avg.AVERAGE.nhours_x1.2000-01-01-00000.nc"

# Define start and end times for averaging for profiles as numerical values in days
time_s = 3.0  # Starting time for averaging
time_e = 5.0  # Ending time for averaging

# END: MANDATORY USER DEFINED SETTINGS
##########################################################
##########################################################
# BEGIN: OPTIONAL user defined settings

# Choose vertical plotting coordinate; can be pressure or height.
#  -If height then the variable Z3 (E3SM) or z_mid (EAMxx) needs to be in your output file.
#  -If pressure then PS (E3SM) or ps (EAMxx) should be in your output file.  If it is not then
#    the package will use hybrid levels to plot, which may not be accurate compared to observations.
height_cord = "p"  # p = pressure; z = height

# Optional: Maximum y-axis height for profile plots (in meters or mb; depending on vertical coordinate)
max_height = 400  # Set to desired height in meters or mb, or None for automatic scaling

# linewidth for curves
linewidth = 4

# Optional: Time range for time series plots in days
time_series_time_s = None  # Starting time for time series, None for default (entire range)
time_series_time_e = None  # Ending time for time series, None for default (entire range)

# END: OPTIONAL user defined settings
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

# Collect all unique variables across datasets
all_vars = set()
for ds in datasets:
    all_vars.update(ds.data_vars.keys())

#############################################################################################################
# Plot profile variables with three dimensions (e.g., time, ncol, lev or ilev)
for var_name in all_vars:
    # Determine if the variable qualifies as a profile variable
    if any(var_name in ds.data_vars and ds[var_name].ndim == 3 and
           any(dim in ['lev', 'ilev'] for dim in ds[var_name].dims) and
           any(dim in ['time'] for dim in ds[var_name].dims) and
           any(dim in ['ncol'] for dim in ds[var_name].dims) for ds in datasets):

        plt.figure(figsize=(8, 6))
        valid_plot = False  # Track if any data was valid for this variable

        # Loop over each dataset, using short_ids for the legend
        for ds, short_id in zip(datasets, short_ids):
            if var_name not in ds.data_vars:
                print(f"Warning: Variable '{var_name}' not found in case '{short_id}'. Skipping for this case.")
                continue  # Skip this case if variable is missing

            valid_plot = True  # At least one dataset has the variable

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
                    raise ValueError("Cannot determine height coordinates ('z_mid', or 'Z3').")

                # If variable has dimensions of ilev then we need to interpolate the height coordinate to the ilev grid
                if "ilev" in ds[var_name].dims:
                    # Interpolate from lev to ilev
                    lev = ds['lev']
                    ilev = ds['ilev']
                    interp_func = interp1d(lev, np.squeeze(y_coord), fill_value="extrapolate")
                    y_coord = interp_func(ilev)
                    y_coord[-1] = 0.0  # Set surface boundary condition to 0

            elif height_cord == "p":
                # Check for surface pressure variable
                ps_var = None
                if 'PS' in ds.data_vars:
                    ps_var = 'PS'
                elif 'ps' in ds.data_vars:
                    ps_var = 'ps'

                if ps_var:
                    ps_avg = ds[ps_var].isel(time=time_indices).mean(dim="time") / 100.0  # Convert to hPa

                    # Use hyam/hybm for lev and hyai/hybi for ilev
                    if "lev" in ds[var_name].dims and all(var in ds for var in ['hyam', 'hybm']):
                        hyam = ds['hyam']
                        hybm = ds['hybm']
                        y_coord = 1000.0 * hyam + hybm * ps_avg
                    elif "ilev" in ds[var_name].dims and all(var in ds for var in ['hyai', 'hybi']):
                        hyai = ds['hyai']
                        hybi = ds['hybi']
                        y_coord = 1000.0 * hyai + hybi * ps_avg
                    else:
                        print(f"Warning: Hybrid coefficients or surface pressure data are missing for case '{short_id}'. Using hybrid pressure coordinates ('lev' or 'ilev').")
                        y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
                else:
                    print(f"Warning: 'PS' or 'ps' is missing for case '{short_id}'. Using hybrid pressure coordinates ('lev' or 'ilev').")
                    y_coord = ds['lev'] if "lev" in ds[var_name].dims else ds['ilev']
            else:
                raise ValueError(f"Invalid height_cord: {height_cord}. Must be 'z' or 'p'.")

            # Plot profile with increased line width
            plt.plot(np.squeeze(time_filtered_data), y_coord, label=short_id, linewidth=linewidth)

        if valid_plot:
            # Set y-axis limit if specified
            if height_cord == "z":
                if max_height is not None:
                    plt.ylim([0, max_height])
            elif height_cord == "p":
                if max_height is not None:
                    plt.ylim([max_height, y_coord.max()])  # Adjust for pressure
                else:
                    plt.ylim([0, y_coord.max()])

            # Reverse the y-axis if plotting against pressure
            if height_cord == "p":
                plt.gca().invert_yaxis()

            # Labeling and saving the plot with larger font sizes
            # Get attributes for the variable from the first dataset that contains it
            var_units = next((ds[var_name].attrs.get('units', 'Value') for ds in datasets if var_name in ds.data_vars), 'Value')
            var_long_name = next((ds[var_name].attrs.get('long_name', var_name) for ds in datasets if var_name in ds.data_vars), var_name)

            # Labeling and saving the plot
            plt.xlabel(var_units, fontsize=14)
            title = f"{var_long_name} Profile"

            ylabel = 'Height (m)' if height_cord == "z" else 'Pressure (hPa)'
            plt.ylabel(ylabel, fontsize=14)
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

        else:
            print(f"Warning: Variable '{var_name}' was not found in any dataset. Skipping this variable.")

#############################################################################################################
# Plot time series for variables with two dimensions (e.g., time, ncol)
for var_name in all_vars:
    # Determine if the variable qualifies as a time series variable
    if any(var_name in ds.data_vars and ds[var_name].ndim == 2 and
           any(dim in ['time'] for dim in ds[var_name].dims) and
           any(dim in ['ncol'] for dim in ds[var_name].dims) for ds in datasets):

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
            variable_data = ds[var_name].isel(time=time_indices)[:, 0]  # Select the single column (ncol = 1)

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
            plt.grid(True)

            # Save plot in the general_id subdirectory
            plot_filename = os.path.join(output_subdir, f"{var_name}_timeseries.jpg")
            plt.savefig(plot_filename, format='jpg')
            plt.close()
            print(f"Saved time series plot for {var_name} as {plot_filename}")

            # Add to timeseries plots list for HTML generation
            timeseries_plots.append(plot_filename)
        else:
            print(f"Warning: Variable '{var_name}' was not found in any dataset. Skipping this variable.")


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
