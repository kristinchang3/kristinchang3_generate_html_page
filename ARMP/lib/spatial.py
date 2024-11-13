from utils.landsea_mask import create_land_sea_mask 
import numpy as np

def land_sea_mask(ds_reg, mask_lndocn, **kwargs):
    ''' create land sea mask with same spatial dims of ds_reg'''

    mask_land = create_land_sea_mask(ds_reg)

    if mask_lndocn = 'land':
        return mask_land

    if mask_lndocn = 'ocean':
        mask_ocean = (~mask_land.astype(bool))#.astype(int)
        return mask_ocean

    return None


def apply_mask(ds_reg, mask_lndocn, **kwargs):
    '''apply land sea mask to data'''

    if mask_lndocn is not None:
        #mask_reg = land_sea_mask(ds_reg, mask=mask)
        mask_reg = land_sea_mask(ds_reg, mask_lndocn, **kwargs)
        tag_lf = xr.apply_ufunc(np.logical_and, ds_reg, mask_reg)
        return tag_lf

    else:
        return ds_reg



def region_select(ds_tag, region, **kwargs):

    lats, latn, lonw, lone, ds_tag = coords_fmt(ds_tag, region, **kwargs)

    ds_tag_reg = ds_tag.sel(lat=slice(lats,latn),lon=slice(lonw,lone))

    return ds_tag_reg



def dim_select(ds, fn_var, **kwargs):
    ''' drop dims other than time,lat,lon'''

    if len(ds[fn_var].dims) in <= 3:
        return ds[fn_var]

	# for data with level coords
    else:
        dims_to_keep = ['time','lat', 'lon']
        dims_to_drop = [dim for dim in ds.dims if dim not in dims_to_keep]

        if clim_4D:
            coord_list = list(ds[fn_var].coords.keys())
            dim_4D = [dim for dim in coord_list if 'lev' in variable]

            # for standard level coords name e.g. plev, lev
            if dim_4D:
                lev_dim = dim_4D[0]

            # for non-standard level coords name
            else:
                lev_dim = kwargs.get('lev_dim')

			lev_coord = kwargs.get('lev_coord')

            if len(ds[fn_var].dims) == 4:
                da = ds[fn_var]
                    .sel({lev_dim:lev_coord})
                    .drop_vars(dims_to_drop)
			
			# if da has more dimensions other than lev
            else:
                other_dims_to_drop = list(filter(lambda dim: dim!=lev_dim, dims_to_drop))
                da = ds[fn_var]
                    .sel({lev_dim:lev_coord})
                    .isel({dim: 0 for dim in other_dims_to_drop})
                    .drop_vars(dims_to_drop)

			return da

        # if not clim_4D: drop all other dims
        else:
            da = ds[fn_var]
                .isel({dim: 0 for dim in dims_to_drop})
                .drop_vars(dims_to_drop)

			return da


def domain_average_series(da):

    weights = np.cos(np.deg2rad(da.lat))
    da_weighted = da.weighted(weights)
    da_weighted_mean_series = da_weighted.mean(("lon", "lat")).compute() 

    return da_weighted_mean_series



def match_coords_dtype(da1, da2):
    """
    da1 -> model, da2-> ref data
    """
    dtype_da1 = da1.coords['lat'].dtype
    dtype_da2 = da2.coords['lat'].dtype

    if dtype_da1 != dtype_da2:
        da1.coords['lat'] = da1.coords['lat'].astype(dtype_da2)
        da1.coords['lon'] = da1.coords['lon'].astype(dtype_da2)
        
    return da1


def match_coords_precision(data_array, mask_array, precision=2):

    data_array = match_coords_dtype(data_array, mask_array)

    lat_data, lon_data = data_array.lat.values, data_array.lon.values
    lat_mask, lon_mask = mask_array.lat.values, mask_array.lon.values

    lat_match = np.array_equal(lat_data, lat_mask)
    lon_match = np.array_equal(lon_data, lon_mask)

    if lat_match and lon_match:
        return data_array

    if not lat_match and not lon_match:
        data_array_aligned = data_array.interp(lat=lat_mask, lon=lon_mask)

    elif not lat_match:
        data_array_aligned = data_array.interp(lat=lat_mask)

    elif not lon_match:
        data_array_aligned = data_array.interp(lon=lon_mask)

    return data_array_aligned


