from itertools import product

from scipy.stats import pearsonr

from ARMP.io.input import nc_in
from ARMP.io.output import update_json_file, write_json_file
from ARMP.lib.control import iter_list_ref, make_case
from ARMP.lib.convention import Case
from ARMP.lib.spatial import match_coords_precision

# metric = 'metric_spatial_corr'


def AR_spatial_correlation(dic, metric):
    """
    add AR frequency spatial correlation result to metrics json file
    """

    update_json_file(dic, metric)

    layout_pool, model_ref = iter_list_ref(dic)

    dir_out = dic["dir_out"]

    for combi in product(*layout_pool):
        case = make_case(Case, combi, dic)

        # model = case.model
        ARDT = case.ARDT
        region = case.region
        season = case.season

        case_name = case.case_name
        case_name_ref = "{}_tag".format("_".join([model_ref, ARDT, region, season]))

        freq_reg_mp = nc_in("freq", "mp.nc", case_name, dir_out)
        freq_reg_mp_ref = nc_in("freq", "mp.nc", case_name_ref, dir_out)

        # regrid ------------
        freq_reg_mp = match_coords_precision(freq_reg_mp, freq_reg_mp_ref)

        freq_reg_mp_1d = freq_reg_mp.to_numpy().flatten()
        freq_reg_mp_ref_1d = freq_reg_mp_ref.to_numpy().flatten()

        corr, pvalue = pearsonr(freq_reg_mp_1d, freq_reg_mp_ref_1d)

        # pvalue ------------
        # tag_reg_mpts = nc_in('tag', 'mpts.nc', case_name, dir_out)
        # tag_reg_mpts_ref = nc_in('tag', 'mpts.nc', case_name_ref, dir_out)
        # metrics/ne.py
        # pvalue done -------

        result = {"corr": corr, "pvalue": pvalue}
        write_json_file(dic, metric, case, result)


#        spatial_count_ds = spatial_count.to_dataset()
#        spatial_count_m_ds = spatial_count_m.to_dataset()
#
#        spatial_count_ds.lat.attrs["axis"] = "Y"
#        spatial_count_ds.lon.attrs["axis"] = "X"
#        spatial_count_ds.time.attrs["axis"] = "T"
#
#        spatial_count_ds = spatial_count_ds.bounds.add_missing_bounds()
#        spatial_count_m_ds = spatial_count_m_ds.bounds.add_missing_bounds()
#
#
#        spatial_count_CMIP_res_ds = spatial_count_ds.regridder.horizontal("binary_tag", spatial_count_m_ds, tool='regrid2').compute()
