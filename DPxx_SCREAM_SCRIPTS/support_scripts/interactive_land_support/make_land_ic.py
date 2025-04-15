import xarray as xr
import numpy as np

# Define the input and output file paths
input_file = '/pscratch/sd/b/bogensch/E3SM_simulations/IELM.ne30pg2_ne30pg2.ERA5_GoAmazon.002a/run/IELM.ne30pg2_ne30pg2.ERA5_GoAmazon.002a.elm.r.2014-10-01-00000.nc'
output_file = '/pscratch/sd/b/bogensch/dp_screamxx/land_ic/land_ic_test.nc'

# Define new sizes for only specific dimensions
new_dims = {
    'gridcell': 100,
    'topounit': 100,
    'landunit': 500,
    'column': 1700,
    'pft': 3300,
    'levurb': 5,
    'max_chars': 256,
    'month': 12,
    'string_length': 64,
}

# Define the target latitude and longitude
target_lat = -3.2
target_lon = 299.4

# Open the input NetCDF file
with xr.open_dataset(input_file) as ds_in:
    # Find the closest index for gridcell
    def find_closest_index(lat_var, lon_var, target_lat, target_lon):
        latitudes = ds_in[lat_var].values
        longitudes = ds_in[lon_var].values
        distances = np.sqrt((latitudes - target_lat)**2 + (longitudes - target_lon)**2)
        return np.argmin(distances)

    gridcell_index = find_closest_index('grid1d_lat', 'grid1d_lon', target_lat, target_lon)

    # Find matching indices for landunit, column, and pft based on gridcell_index
    landunit_matching_indices = np.where(ds_in['land1d_gridcell_index'].values == gridcell_index)[0]
    column_matching_indices = np.where(ds_in['cols1d_gridcell_index'].values == gridcell_index)[0]
    pft_matching_indices = np.where(ds_in['pfts1d_gridcell_index'].values == gridcell_index)[0]

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

    # Loop over each variable in the dataset
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
            values_at_matching_indices = var_data.isel(landunit=landunit_matching_indices).values
            repeated_values = np.tile(values_at_matching_indices, int(np.ceil(new_dims['landunit'] / len(values_at_matching_indices))))[:new_dims['landunit']]
            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)
            data_vars[var_name] = (var_dims, repeated_values.reshape(new_shape))
            print(f"{var_name}: Filled with cyclic values from {len(landunit_matching_indices)} matching landunit indices.")

        elif 'column' in var_dims:
            values_at_matching_indices = var_data.isel(column=column_matching_indices).values
            original_shape = values_at_matching_indices.shape  # e.g., (n_col, second_dim, ...)

            # Number of matching columns and number of repeats needed
            n_matching = original_shape[0]
            n_target = new_dims['column']
            n_repeat = int(np.ceil(n_target / n_matching))

            # Repeat only along the first axis (column), preserve the rest
            tiled_values = np.tile(values_at_matching_indices, (n_repeat,) + (1,) * (values_at_matching_indices.ndim - 1))

            # Trim to desired number of columns
            final_values = tiled_values[:n_target, ...]

            # Define new shape, replacing only the column dimension with new_dims value
            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)

            # Confirm shape match and assign
            assert final_values.shape == new_shape, f"Shape mismatch: expected {new_shape}, got {final_values.shape}"
            data_vars[var_name] = (var_dims, final_values)
            print(f"{var_name}: Filled with cyclic values from {len(column_matching_indices)} matching column indices.")


#        elif 'column' in var_dims:
#            values_at_matching_indices = var_data.isel(column=column_matching_indices).values
#            repeated_values = np.tile(values_at_matching_indices, int(np.ceil(new_dims['column'] / len(values_at_matching_indices))))[:new_dims['column']]
#            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)
#            data_vars[var_name] = (var_dims, repeated_values.reshape(new_shape))
#            print(f"{var_name}: Filled with cyclic values from {len(column_matching_indices)} matching column indices.")

        elif 'pft' in var_dims:
            values_at_matching_indices = var_data.isel(pft=pft_matching_indices).values
            repeated_values = np.tile(values_at_matching_indices, int(np.ceil(new_dims['pft'] / len(values_at_matching_indices))))[:new_dims['pft']]
            new_shape = tuple(new_dims.get(dim, ds_in.dims[dim]) for dim in var_dims)
            data_vars[var_name] = (var_dims, repeated_values.reshape(new_shape))

            print(f"{var_name}: Filled with cyclic values from {len(pft_matching_indices)} matching pft indices.")

        else:
            # Copy other variables without changing dimensions
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


    # Replace all missing values explicitly with their _FillValue
#    for var_name, data_array in data_vars_with_metadata.items():
#        fill_value = data_array.encoding.get('_FillValue', None)
#        fill_value = 0

#        if fill_value is not None:
#            if np.issubdtype(data_array.dtype, np.floating):
#                data_array.values = np.where(np.isnan(data_array.values), fill_value, data_array.values)
#            elif np.issubdtype(data_array.dtype, np.integer):
#                missing_value = ds_in[var_name].attrs.get('missing_value', None)
#                if missing_value is not None:
#                    data_array.values = np.where(data_array.values == missing_value, fill_value, data_array.values)
#            print(f"Replaced missing values in {var_name} with _FillValue: {fill_value}")


    # Save the dataset to a new NetCDF file
    ds_out.to_netcdf(output_file)

print("New dataset created successfully.")
