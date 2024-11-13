import xarray as xr
from typing import Union


def check_ds_attrs(ds):

    if not ds.coords['lat'].attrs:
        ds.coords['lat'].attrs = \
                {'bounds': 'lat_bnds', 'units': 'degrees_north', 'axis': 'Y', 'long_name': 'latitude', 'standard_name': 'latitude'}

    if not ds.coords['lon'].attrs:
        ds.coords['lon'].attrs = \
                {'bounds': 'lon_bnds', 'units': 'degrees_east', 'axis': 'X', 'long_name': 'longitude', 'standard_name': 'longitude'}

    return ds



def da_to_ds(d: Union[xr.Dataset, xr.DataArray], var: str = "variable") -> xr.Dataset:

    if isinstance(d, xr.Dataset):
        return d.copy()
    elif isinstance(d, xr.DataArray):
        ds = d.to_dataset(name=var)
        ds = check_ds_attrs(ds)
        return ds.bounds.add_missing_bounds().copy()
    else:
        raise TypeError(
            "Input must be an instance of either xarrary.DataArray or xarrary.Dataset"
        )



def regrid(da_in, da_grid, data_var="var"):

    ds_in = da_to_ds(da_in, data_var)
    ds_grid = da_to_ds(da_grid, data_var)

    if 'units' not in ds_in.coords['lat'].attrs:
        ds_in.coords['lat'].attrs['units'] = 'degrees_north'
        print("Added 'units' attribute to 'lat' coordinate.")

    if 'units' not in ds_grid.coords['lat'].attrs:
        ds_grid.coords['lat'].attrs['units'] = 'degrees_north'
        ds_grid.coords['lat'].attrs['axis'] = "Y"
        ds_grid.coords['lon'].attrs['axis'] = "X"
        print("Added 'units' attribute to 'lat' coordinate.")

    lat_units = ds_in.coords['lat'].attrs.get('units', None)
    if lat_units != 'degrees_north':
        ds_in.coords['lat'].attrs['units'] == 'degrees_north'
        print("Added lat unit to 'lat' coordinate attrs.")

    lat_units = ds_grid.coords['lat'].attrs.get('units', None)
    if lat_units != 'degrees_north':
        ds_grid.coords['lat'].attrs['units'] == 'degrees_north'
        print("Added lat unit to 'lat' coordinate attrs.")

    try: 
        ds_out = ds_in.regridder.horizontal(data_var, ds_grid, tool="regrid2")
        da_out = ds_out[data_var]
    except ValueError:
    # in case time dim size of ds_in and ds_grid are not the same, drop dime dimension for ds_grid
    # ValueError: cannot reindex or align along dimension 'time' because of conflicting dimension sizes
        ds_grid = ds_grid.isel(time=0)
        ds_grid = ds_grid.drop_vars(["time"])
        ds_out = ds_in.regridder.horizontal(data_var, ds_grid, tool="regrid2")
        da_out = ds_out[data_var]

    return da_out



def regrid_coords_precision(data_array, mask_array, precision=2):

    lat_data, lon_data = data_array.lat.values, data_array.lon.values
    lat_mask, lon_mask = mask_array.lat.values, mask_array.lon.values

    lat_match = np.array_equal(lat_data, lat_mask)
    lon_match = np.array_equal(lon_data, lon_mask)

    if lat_match and lon_match:

        return data_array

    data_array_aligned = regrid(data_array, mask_array)

    return data_array_aligned

