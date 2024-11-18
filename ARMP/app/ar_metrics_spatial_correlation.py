from dataclasses import asdict
from itertools import product

from ARMP.io.input import nc_in
from ARMP.io.output import update_json_ref, write_json_file
from ARMP.lib.control import iter_list_ref, make_case
from ARMP.lib.convention import Case
from ARMP.lib.loader import dic
from ARMP.metrics.spatial_corr import spatial_corr


def AR_spatial_correlation(dic, metric, ne=False):
    """
    add AR frequency spatial correlation result to metrics json file
    """
    print("\ncalculating AR spatial correlation metrics")

    update_json_ref(dic, metric)

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

        ### correlation and pvalue
        # two-tailed p-value of the cumulative distribution function (CDF) of the t-statistics, with effective sample size ne

        #        freq_reg_mp = match_coords_precision(freq_reg_mp, freq_reg_mp_ref)
        #        freq_reg_mp_1d = freq_reg_mp.to_numpy().flatten()
        #        freq_reg_mp_ref_1d = freq_reg_mp_ref.to_numpy().flatten()
        #        corr, pvalue = pearsonr(freq_reg_mp_1d, freq_reg_mp_ref_1d)

        if not ne:
            corr, pvalue = spatial_corr(freq_reg_mp, freq_reg_mp_ref)

        else:
            corr, pvalue = spatial_corr(
                freq_reg_mp, freq_reg_mp_ref, ne=ne, **{**asdict(case), **dic}
            )

        result = {"corr": corr, "pvalue": pvalue}
        write_json_file(dic, metric, case, result)


if __name__ == "__main__":
    metric = "metric_spatial_corr"
    AR_spatial_correlation(dic, "metric_spatial_corr", ne=True)
