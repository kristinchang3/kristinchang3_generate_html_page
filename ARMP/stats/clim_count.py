from io.output import nc_out 
from io.input import case_combi
from lib.proc import init_ds
from lib.preprocessing import data_QAQC, data_QAQC_mf, data_QAQC_mf_xc, freq_convert
from lib.loader import setting
from lib.sampling import match_calendar
from utils.regridder import regrid_coords_precision
from lib.spatial import match_coords_precision
from lib.spatial import domain_average_series


def Clim_count(fn_list, fn_var, region, season, start_date, end_date, mask_lndocn, **kwargs):
    # to be developed
    pass


def Clim_count_mf(fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs):

    globals().update(**kwargs)

    #clim_reg_lf = data_QAQC_mf(fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs)
    clim_reg_lf = data_QAQC_mf_xc(fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs)

    clim_reg_lf = freq_convert(clim_reg_lf, fn_freq, target_freq, **kwargs)

    # read in AR tag data
    case_name_tag = case_combi(case_name)+'_tag'
    tag_reg_mpts = nc_in('binary_tag', 'mpts.nc', case_name_tag, dir_out, **kwargs)

    tag_reg_mpts, clim_reg_mpts = match_calendar(tag_reg_mpts, clim_reg_mpts)

    clim_reg_mpts= clim_reg_lf.sel(time=tag_reg_mpts.time, method='nearest')

    try:
        clim_reg_mpts = regrid_coords_precision(clim_reg_mpts, tag_reg_mpts)
    except RuntimeError as e:
        clim_reg_mpts = match_coords_precision(clim_reg_mpts, tag_reg_mpts)

    #clim_reg_mpts = clim_reg_mpts.where(~np.isnan(tag_reg_mpts)).compute()
    clim_reg_mpts = clim_reg_mpts.where(tag_reg_mpts).compute()

    clim_reg_ts = domain_average_series(clim_reg_mpts)

    if clim_out_ts:
        nc_out(clim_reg_ts, kwargs['fn_var_out'], 'ts.nc', case_name, dir_out)

    if clim_out_map_ts:
        nc_out(clim_reg_mpts, kwargs['fn_var_out'], 'mpts.nc', case_name, dir_out)

    return clim_reg_ts
