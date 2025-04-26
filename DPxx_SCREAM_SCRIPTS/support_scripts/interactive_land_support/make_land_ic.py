import xarray as xr
import numpy as np
import re
import sys

#######################################################################
###### Start user input

# Define the target latitude and longitude.  this is the lat/lon that you want to extract from the
#  ELM restart file.  It should also be the lat/lon you plan to use in your DPxx simulation.

# Enter location to extract.  "GOAMAZON" and "SGP" are currently supported.  Custom locations
#   can easily be added.
site='GOAMAZON'

# Enter Date Timestamp to be extracted (yyyy-dd-mm-ttttt)
date='2015-08-26-43200'

# These geometry parameters should match what you plan to use in your DPxx simulation
num_ne_x=267
num_ne_y=267

# Define the file where your ELM restart file resides that you want to extract from
input_file = '/pscratch/sd/b/bogensch/E3SM_simulations/land_initial_conditions_dpxx/SGP_GOAMAZON_2013-2015'
# Case name of run used to spin up ELM files
input_case = 'IELM.ne30pg2_ne30pg2.ERA5_GoAmazon.003a'

# Provide the path for your output file
output_path = '/pscratch/sd/b/bogensch/dp_screamxx/land_ic/'

###### End user input
#######################################################################

if (site == 'GOAMAZON'):
    target_lat = -3.2
    target_lon = 299.4
elif (site == 'SGP'):
    target_lat = 36.6
    target_lon = 262.51
elif (site == 'CUSTOM'):
    target_lat = 0
    target_lon = 0
else:
    print("Site location no defined or supported.  Aborting.")
    sys.exit()

# make input file string
input_file = input_file+'/'+input_case+'.elm.r.'+date+'.nc'

# Attempt to extract date from input ELM file for the sake of the output file
match = re.search(r'\d{4}-\d{2}-\d{2}-\d{5}', input_file)

# Form the name of the outputfile
output_file = output_path+site+'_elm_dpxx_init_nex'+str(num_ne_x)+'_ney'+str(num_ne_y)+'_'+date+'.nc'

# start to extract

phys_col=num_ne_x*num_ne_y*4

# Open the input NetCDF file
with xr.open_dataset(input_file) as ds_in:
    # Code to deal with pft, landunit, and column related variables
    def expand_dimension(var_data, dim_name, matching_indices, new_size, all_dims, ds_in_dims):
        """Expand a variable along the given dimension by tiling and trimming."""
        values_at_matching_indices = var_data.isel({dim_name: matching_indices}).values
        original_shape = values_at_matching_indices.shape  # (n_matching, other_dims...)

        n_matching = original_shape[0]
        n_target = new_size
        n_repeat = int(np.ceil(n_target / n_matching))

        tiled_values = np.tile(values_at_matching_indices, (n_repeat,) + (1,) * (values_at_matching_indices.ndim - 1))
        final_values = tiled_values[:n_target, ...]

        new_shape = tuple(all_dims.get(d, ds_in_dims[d]) for d in var_data.dims)
        assert final_values.shape == new_shape, f"Shape mismatch for {dim_name}: expected {new_shape}, got {final_values.shape}"

        return (var_data.dims, final_values)


    # Find the closest index for gridcell
    def find_closest_index(lat_var, lon_var, target_lat, target_lon):
        latitudes = ds_in[lat_var].values
        longitudes = ds_in[lon_var].values
        distances = np.abs(latitudes-target_lat)+np.abs(longitudes - target_lon)
        return np.argmin(distances)

    gridcell_index = find_closest_index('grid1d_lat', 'grid1d_lon', target_lat, target_lon)

    # Find matching indices for landunit, column, and pft based on gridcell_index
    landunit_matching_indices = np.where(ds_in['land1d_gridcell_index'].values == gridcell_index+1)[0]
    column_matching_indices = np.where(ds_in['cols1d_gridcell_index'].values == gridcell_index+1)[0]
    pft_matching_indices = np.where(ds_in['pfts1d_gridcell_index'].values == gridcell_index+1)[0]

    num_landunits = len(landunit_matching_indices)
    num_cols = len(column_matching_indices)
    num_pfts = len(pft_matching_indices)

    # Define new sizes for only specific dimensions
    new_dims = {
        'gridcell': phys_col,
        'topounit': phys_col,
        'landunit': phys_col*num_landunits,
        'column': phys_col*num_cols,
        'pft': phys_col*num_pfts,
        'levurb': 5,
        'max_chars': 256,
        'month': 12,
        'string_length': 64,
    }

    # Create dictionaries to hold data and metadata for the new file
    data_vars = {}
    coords = {}

    coords['levurb'] = ('levurb', np.arange(new_dims['levurb']))
    coords['month'] = ('month', np.arange(new_dims['month']))
    coords['max_chars'] = ('max_chars', np.arange(new_dims['max_chars']))
    coords['string_length'] = ('string_length', np.arange(new_dims['string_length']))

    # Copy coordinates and adjust only specific dimensions
    for dim_name, dim_size in ds_in.dims.items():
        if dim_name in new_dims:
            coords[dim_name] = (dim_name, np.arange(new_dims[dim_name]))
        else:
            coords[dim_name] = (dim_name, np.arange(dim_size))

    for var_name, var_data in ds_in.data_vars.items():
        var_dims = var_data.dims

        if 'gridcell' in var_dims:
            value_at_closest = var_data.isel(gridcell=gridcell_index).values
            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)
            data_vars[var_name] = (var_dims, np.full(new_shape, value_at_closest))
            print(f"{var_name}: Set to value at closest gridcell index {gridcell_index}")

        elif 'topounit' in var_dims:
            value_at_closest = var_data.isel(topounit=gridcell_index).values
            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)
            data_vars[var_name] = (var_dims, np.full(new_shape, value_at_closest))
            print(f"{var_name}: Set to value at closest topounit index {gridcell_index}")

        elif 'landunit' in var_dims:
            data_vars[var_name] = expand_dimension(var_data, 'landunit', landunit_matching_indices, new_dims['landunit'], new_dims, ds_in.dims)
            print(f"{var_name}: Filled with cyclic values from {len(landunit_matching_indices)} matching landunit indices.")

        elif 'column' in var_dims:
            data_vars[var_name] = expand_dimension(var_data, 'column', column_matching_indices, new_dims['column'], new_dims, ds_in.dims)
            print(f"{var_name}: Filled with cyclic values from {len(column_matching_indices)} matching column indices.")

        elif 'pft' in var_dims:
            data_vars[var_name] = expand_dimension(var_data, 'pft', pft_matching_indices, new_dims['pft'], new_dims, ds_in.dims)
            print(f"{var_name}: Filled with cyclic values from {len(pft_matching_indices)} matching pft indices.")

        else:
            data_vars[var_name] = (var_dims, var_data.values)
            print(f"{var_name}: Copied as-is")



    # Copy metadata to new DataArray objects with _FillValue set correctly
    data_vars_with_metadata = {}
    for var_name, (dims, values) in data_vars.items():
        # Retrieve the FillValue and missing_value from the input file's variable encoding
        fill_value = ds_in[var_name].encoding.get('_FillValue', None)
        missing_value = ds_in[var_name].encoding.get('missing_value', None)

        # If both attributes are present and conflict, resolve the conflict
        if fill_value is not None and missing_value is not None and fill_value != missing_value:
            print(f"Variable {var_name} has conflicting _FillValue ({fill_value}) and missing_value ({missing_value}). Resolving conflict.")
            # Use the _FillValue and discard the missing_value
            missing_value = fill_value

        # Add the variable to the dataset with metadata and the correct _FillValue
        data_vars_with_metadata[var_name] = xr.DataArray(
            values,
            dims=dims,
            attrs=ds_in[var_name].attrs
        )

        # Explicitly set the _FillValue if it exists
        if fill_value is not None:
            data_vars_with_metadata[var_name].encoding['_FillValue'] = fill_value

        # Optionally add missing_value (only if it does not conflict)
        if missing_value is not None and missing_value == fill_value:
            data_vars_with_metadata[var_name].encoding['missing_value'] = missing_value

    # Create the new dataset with updated dimensions, variables, and metadata
    ds_out = xr.Dataset(data_vars_with_metadata, coords=coords)

    # Add global attribute
    ds_out.attrs['title'] = "ELM Restart information"

    # Save the dataset to a new NetCDF file
    ds_out.to_netcdf(output_file)

print("New dataset created successfully:", output_file)
