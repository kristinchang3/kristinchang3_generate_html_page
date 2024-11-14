import numpy as np
import xarray as xr
import xcdat as xc
from ARMP.lib.spatial import dim_select, region_select, apply_mask
from ARMP.lib.convention import Case, Case_clim, Setting


def freq_convert(da, fn_freq, target_freq, **kwargs):

    #if freq_match(fn_freq, target_freq, **kwargs):
    if fn_freq == target_freq:
        return da
    
    else:
        if 'tag_var' in kwargs:
        #if isinstance(case, Case):
        #if hasattr(case, 'tag_var'):
            da_rsp = da.resample(time=target_freq).max(dim='time')
            #da_rsp = season_select(da_rsp, season, **kwargs)
            #time_size = da_rsp.time.size

        else:
            da_rsp = da.resample(time=target_freq).meam(dim='time')
            #da_rsp = season_select(da_rsp, season, **kwargs)
            #time_size = da_rsp.time.size

        da_rsp = da_rsp.dropna(dim='time', how='all')
        time_size = da_rsp.time.size
        da_rsp.attrs['time_size'] = time_size

    return da_rsp



def data_QAQC(fn, mask_reg, region, season, fn_var, 
              start_date, end_date, **kwargs):

    ds_tag = xr.open_dataset(fn)

    ds_tag_reg = region_select(ds_tag, region, **kwargs)

    ds_tag_reg_tm = time_select(ds_tag_reg, start_date, end_date, **kwargs)

    if len(ds_tag_reg_tm.time) == 0:
        return None

    ds_tag_reg_tm_sn = season_select(ds_tag_reg_tm, season, **kwargs)

    da = dim_select(ds_tag_reg_tm_sn, fn_var, **kwargs)

    #da = dim_select(ds_tag_reg_tm, fn_var=fn_var, **kwargs)
    #da = season_select(da, season)

    #da_lf = apply_mask(da, mask=mask_lndocn)
    #if tag_var:
    if 'tag_var' in kwargs:
    #if isinstance(case, Case):
    #if hasattr(case, 'tag_var'):
        da_lf = xr.apply_ufunc(np.logical_and, da, mask_reg)


    return da_lf
        


def data_QAQC_mf(fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs):

    ds_tag = xr.open_mfdataset(fn_list, concat_dim="time", combine="by_coords", chunks={'time': 100})

    ds_tag_reg = region_select(ds_tag, region, **kwargs)

    ds_tag_reg_tm = time_select(ds_tag_reg, start_date, end_date, **kwargs)

    ds_tag_reg_tm_sn = season_select(ds_tag_reg_tm, season, **kwargs)

    da = dim_select(ds_tag_reg_tm_sn, fn_var, **kwargs)

    da = da.persist()

    #if tag_var:
    if 'tag_var' in kwargs:
    #if isinstance(case, Case):
    #if hasattr(case, 'tag_var'):
        da_lf = apply_mask(da, mask_lndocn, **kwargs)


    return da_lf
        


def data_QAQC_mf_xc(fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs):

    ds_tag = xc.open_mfdataset(fn_list, concat_dim="time", combine="by_coords", chunks={'time': 100})
    ds_tag_reg = region_select(ds_tag, region, **kwargs)
    ds_tag_reg_tm = time_select(ds_tag_reg, start_date, end_date, **kwargs)
    ds_tag_reg_tm_sn = season_select(ds_tag_reg_tm, season, **kwargs)
    da = dim_select(ds_tag_reg_tm_sn, fn_var, **kwargs)
    da = da.persist()
    if 'tag_var' in kwargs:
        da_lf = apply_mask(da, mask_lndocn, **kwargs)

    return da_lf




