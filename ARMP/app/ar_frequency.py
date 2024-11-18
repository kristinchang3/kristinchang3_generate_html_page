from dataclasses import asdict
from itertools import product

from stats.ar_count import LFAR_count, LFAR_count_mf

from ARMP.io.output import create_json_file, write_json_file
from ARMP.io.printting import print_case
from ARMP.lib.control import iter_list, make_case
from ARMP.lib.convention import Case
from ARMP.stats.peak_day import peak_day_stats


def AR_frequency(dic, setting):
    layout_pool = iter_list(dic)

    create_json_file(dic)

    for combi in product(*layout_pool):
        case = make_case(Case, combi, dic)

        print_case(case)

        kwargs = {**asdict(case), **asdict(setting)}

        if kwargs["parallel"]:
            da_occur_ts, freq_reg_mp, tag_reg_mpts = LFAR_count_mf(**kwargs)
        else:
            da_occur_ts, freq_reg_mp, tag_reg_mpts = LFAR_count(**kwargs)

        # AR frequency stats
        if dic["metric_freq"]:
            count = da_occur_ts.sum(
                dim="time"
            ).values.tolist()  # DataArray->np->list for json output
            freq = count / da_occur_ts.time_size
            result = {"freq": freq, "count": count}
            write_json_file(dic, "metric_freq", case, result)

        # AR peak day stats
        if dic["metric_peak_day"]:
            if not dic["diag_peak_day_histogram"]:
                peak = peak_day_stats(da_occur_ts, dic)
                result = {"peak_day": peak}
                write_json_file(dic, "metric_peak_day", case, result)

            else:
                peak, clim_mean, clim_std, clim = peak_day_stats(da_occur_ts, dic)

                #                print("type peak = ", type(peak))
                #                print("clim = ", clim)
                #                print("clim_mean = ", clim_mean.values.tolist())
                #                print("clim_std = ", clim_std.values)
                result = {
                    "peak_day": peak,
                    "count_mean": clim_mean.values.tolist(),
                    "count_std": clim_std.values.tolist(),
                    "count_ens": [arr.tolist() for arr in clim],
                }

                write_json_file(dic, "metric_peak_day", case, result)

        # if dic['include_clim']:
        #    return tag_reg_mpts

        # else:
        #    return None

        # if metric_spatial_corr:
