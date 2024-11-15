import numpy as np
import pandas as pd
import xarray as xr

from ARMP.lib.convention import coords_fmt
from ARMP.lib.spatial import land_sea_mask


def init_ds(fn_list, region, mask_lndocn, fn_var, **kwargs):  # , lev=85000):
    with open(fn_list, "r") as f_tag:
        first_line = f_tag.readline().strip()
        ds_tag = xr.open_dataset(first_line)

        lats, latn, lonw, lone, ds_tag = coords_fmt(ds_tag, region, **kwargs)

        ds_tag_reg = ds_tag.sel(lat=slice(lats, latn), lon=slice(lonw, lone))

        # !!!!! creat utils def land_sea_mask(ds_tag, mask=None): !!!!!
        mask_reg = land_sea_mask(ds_tag_reg, mask_lndocn, **kwargs)

        # create 1D empty time series dataarray
        empty_time = pd.date_range(
            "1850-01-01", periods=0, freq="H"
        )  # No initial time points
        da_occur_ts = xr.DataArray(
            np.empty((0,)), dims=["time"], coords={"time": empty_time}, name=fn_var
        )

        # create empty 2D dataarray
        # tag_reg_2d = ds_tag_reg[fn_var].isel(time=0)
        # count_reg_mp = xr.DataArray(np.empty(tag_reg_2d.shape), dims=tag_reg_2d.dims, coords=tag_reg_2d.coords)

        nlat = ds_tag_reg.lat.size
        nlon = ds_tag_reg.lon.size

        # consider to change it to da_reg_2d
        count_reg_mp = xr.DataArray(
            np.empty((nlat, nlon)),
            dims=["lat", "lon"],
            coords={"lat": ds_tag_reg.coords["lat"], "lon": ds_tag_reg.coords["lon"]},
            name=fn_var,
        )

        # create empty 3D dataarray
        # consider to change it to da_reg_3d
        tag_reg_mpts = xr.DataArray(
            data=np.empty((0, ds_tag_reg.lat.size, ds_tag_reg.lon.size)),
            dims=["time", "lat", "lon"],
            coords={
                "time": pd.date_range("1850-01-01", periods=0, freq="H"),
                "lat": ds_tag_reg.coords["lat"],
                "lon": ds_tag_reg.coords["lon"],
            },
            name=fn_var,
        )

    #        dims_to_keep = ['time','lat', 'lon']
    #        dims_to_drop = [dim for dim in ds_tag.dims if dim not in dims_to_keep]
    #
    #        #if fn_var in clim_var_list and clim_4D:
    #        if clim_4D:
    #            if len(ds_tag_reg[fn_var].dims) == 4:
    #                tag_reg = ds_tag_reg[fn_var]
    #                    .sel({lev_dim:lev_coord})
    #                    .sel(lat=slice(lats,latn),lon=slice(lonw,lone))
    #                    .sel(time=slice(start_date, end_date))
    #                    .drop_vars(dims_to_drop)
    #            else:
    #                other_dims_to_drop = list(filter(lambda dim: dim!=lev_dim, dims_to_drop))
    #                tag_reg = ds_tag_reg[fn_var]
    #                    .sel({lev_dim:lev_coord})
    #                    .sel(lat=slice(lats,latn),lon=slice(lonw,lone))
    #                    .sel(time=slice(start_date, end_date))
    #                    .isel({dim: 0 for dim in other_dims_to_drop})
    #                    .drop_vars(dims_to_drop)
    #
    #
    #        tag_reg_3d = ds_tag_reg[fn_var].isel({dim: 0 for dim in dims_to_drop})
    #        tag_reg_3d = tag_reg_3d.drop_vars(dims_to_drop)
    #
    #        tag_reg_mpts = xr.DataArray(
    #            data=np.empty((0, tag_reg_3d.lat.size, tag_reg_3d.lon.size)),
    #            dims=["time", "lat", "lon"],
    #            coords={
    #                'time': pd.date_range('1850-01-01', periods=0, freq='H'),
    #                "lat": tag_reg_3d.coords['lat'],
    #                "lon": tag_reg_3d.coords['lon']
    #            },
    #        name=fn_var
    #        )

    # 		if ar_freq_map and ar_map_ts:
    # 		if ar_freq_ts:
    #
    #
    # 			empty_time = pd.date_range('2023-01-01', periods=0, freq='H')  # No initial time points
    #    		da_occur_ts = xr.DataArray(np.empty((0,)), dims=['time'], coords={'time': empty_time})
    #
    # 			return count_reg_mp, mask_reg

    return mask_reg, da_occur_ts, count_reg_mp, tag_reg_mpts


# def prep_ds_loop(region, fn_list, fn_var='binary_tag')#, lev=85000):
