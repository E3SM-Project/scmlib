import calendar
import os
import xarray as xr
import numpy as np
import re
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#######################################################################
###### Start user input

site = 'GOAMAZON'
start_date = '2014-01-01-00000'  # format: yyyy-mm-dd-sssss
num_months = 12  # <== number of days to loop over

num_ne_x = 20
num_ne_y = 20

input_file_root = '/pscratch/sd/b/bogensch/E3SM_simulations/IELM.ne30pg2_ne30pg2.ERA5_GoAmazon.004a/run'
input_case = 'IELM.ne30pg2_ne30pg2.ERA5_GoAmazon.004a'

output_path = '/pscratch/sd/b/bogensch/dp_screamxx/land_ic/goamazon_hindcasts_monthly/'

###### End user input
#######################################################################

if site == 'GOAMAZON':
    target_lat = -3.2
    target_lon = 299.4
elif site == 'SGP':
    target_lat = 36.6
    target_lon = 262.51
elif site == 'CUSTOM':
    target_lat = 0
    target_lon = 0
else:
    print("Site location not defined or supported. Aborting.")
    sys.exit()


def process_day(date):
    input_file = f"{input_file_root}/{input_case}.elm.r.{date}.nc"
    output_file = output_path + f"{site}_elm_dpxx_init_nex{num_ne_x}_ney{num_ne_y}_{date}.nc"
    phys_col = num_ne_x * num_ne_y * 4

    try:
        with xr.open_dataset(input_file) as ds_in:
            def expand_dimension(var_data, dim_name, matching_indices, new_size, all_dims, ds_in_dims):
                values_at_matching_indices = var_data.isel({dim_name: matching_indices}).values
                n_matching = values_at_matching_indices.shape[0]
                n_repeat = int(np.ceil(new_size / n_matching))
                tiled_values = np.tile(values_at_matching_indices, (n_repeat,) + (1,) * (values_at_matching_indices.ndim - 1))
                final_values = tiled_values[:new_size, ...]
                new_shape = tuple(all_dims.get(d, ds_in_dims[d]) for d in var_data.dims)
                assert final_values.shape == new_shape, f"Shape mismatch: {final_values.shape} vs {new_shape}"
                return (var_data.dims, final_values)

            def find_closest_index(lat_var, lon_var, target_lat, target_lon):
                latitudes = ds_in[lat_var].values
                longitudes = ds_in[lon_var].values
                distances = np.abs(latitudes - target_lat) + np.abs(longitudes - target_lon)
                return np.argmin(distances)

            gridcell_index = find_closest_index('grid1d_lat', 'grid1d_lon', target_lat, target_lon)
            landunit_matching_indices = np.where(ds_in['land1d_gridcell_index'].values == gridcell_index + 1)[0]
            column_matching_indices = np.where(ds_in['cols1d_gridcell_index'].values == gridcell_index + 1)[0]
            pft_matching_indices = np.where(ds_in['pfts1d_gridcell_index'].values == gridcell_index + 1)[0]

            new_dims = {
                'gridcell': phys_col,
                'topounit': phys_col,
                'landunit': phys_col * len(landunit_matching_indices),
                'column': phys_col * len(column_matching_indices),
                'pft': phys_col * len(pft_matching_indices),
                'levurb': 5,
                'max_chars': 256,
                'month': 12,
                'string_length': 64,
            }

            data_vars, coords = {}, {}
            coords['levurb'] = ('levurb', np.arange(new_dims['levurb']))
            coords['month'] = ('month', np.arange(new_dims['month']))
            coords['max_chars'] = ('max_chars', np.arange(new_dims['max_chars']))
            coords['string_length'] = ('string_length', np.arange(new_dims['string_length']))

            for dim_name, dim_size in ds_in.dims.items():
                coords[dim_name] = (dim_name, np.arange(new_dims.get(dim_name, dim_size)))

            for var_name, var_data in ds_in.data_vars.items():
                var_dims = var_data.dims
                if 'gridcell' in var_dims:
                    v = var_data.isel(gridcell=gridcell_index).values
                    s = tuple(new_dims.get(d, ds_in.dims[d]) for d in var_dims)
                    data_vars[var_name] = (var_dims, np.full(s, v))
                elif 'topounit' in var_dims:
                    v = var_data.isel(topounit=gridcell_index).values
                    s = tuple(new_dims.get(d, ds_in.dims[d]) for d in var_dims)
                    data_vars[var_name] = (var_dims, np.full(s, v))
                elif 'landunit' in var_dims:
                    data_vars[var_name] = expand_dimension(var_data, 'landunit', landunit_matching_indices, new_dims['landunit'], new_dims, ds_in.dims)
                elif 'column' in var_dims:
                    data_vars[var_name] = expand_dimension(var_data, 'column', column_matching_indices, new_dims['column'], new_dims, ds_in.dims)
                elif 'pft' in var_dims:
                    data_vars[var_name] = expand_dimension(var_data, 'pft', pft_matching_indices, new_dims['pft'], new_dims, ds_in.dims)
                else:
                    data_vars[var_name] = (var_dims, var_data.values)

            data_vars_with_metadata = {}
            for var_name, (dims, values) in data_vars.items():
                fill_value = ds_in[var_name].encoding.get('_FillValue', None)
                missing_value = ds_in[var_name].encoding.get('missing_value', None)
                if fill_value is not None and missing_value is not None and fill_value != missing_value:
                    missing_value = fill_value
                da = xr.DataArray(values, dims=dims, attrs=ds_in[var_name].attrs)
                if fill_value is not None:
                    da.encoding['_FillValue'] = fill_value
                if missing_value is not None and missing_value == fill_value:
                    da.encoding['missing_value'] = missing_value
                data_vars_with_metadata[var_name] = da

            ds_out = xr.Dataset(data_vars_with_metadata, coords=coords)
            ds_out.attrs['title'] = "ELM Restart information"
            ds_out.to_netcdf(output_file)
            print("Created:", output_file)

    except FileNotFoundError:
        print(f"Input file not found for date {date}. Skipping.")


# Loop over all months
base_date = datetime.strptime(start_date[:7], "%Y-%m")
for i in range(num_months):
    date_obj = base_date + relativedelta(months=i)
    formatted_date = date_obj.strftime("%Y-%m")+"-01-00000"
    process_day(formatted_date)
    
# Loop over each day of the year and link to first-of-month file
link_base_date = datetime.strptime(start_date[:10], "%Y-%m-%d")
for i in range(365 + calendar.isleap(link_base_date.year)):  # Handle leap years
    date_obj = link_base_date + timedelta(days=i)
    full_date_str = date_obj.strftime("%Y-%m-%d-00000")
    month_anchor_str = date_obj.strftime("%Y-%m-01-00000")

    src_file = os.path.join(output_path, f"{site}_elm_dpxx_init_nex{num_ne_x}_ney{num_ne_y}_{month_anchor_str}.nc")
    dst_file = os.path.join(output_path, f"{site}_elm_dpxx_init_nex{num_ne_x}_ney{num_ne_y}_{full_date_str}.nc")

    try:
        if not os.path.exists(dst_file):
            os.symlink(src_file, dst_file)
            print(f"Linked {dst_file} to {src_file}")
    except FileNotFoundError:
        print(f"Source file not found: {src_file}")
