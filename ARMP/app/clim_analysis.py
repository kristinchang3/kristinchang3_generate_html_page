from dataclasses import asdict
from itertools import product

from ARMP.io.output import write_json_file
from ARMP.io.printting import print_case
from ARMP.lib.control import iter_list, make_case
from ARMP.lib.convention import Case_clim
from ARMP.stats.clim_count import Clim_count_mf
from ARMP.stats.clim_stats import Clim_stats


def Clim_analysis(dic, setting):
    layout_pool = iter_list(dic)

    for combi in product(*layout_pool):
        case = make_case(Case_clim, combi, dic)

        print_case(case, var=case.fn_var_out)

        kwargs = {**asdict(case), **asdict(setting)}

        clim_reg_ts = Clim_count_mf(**kwargs)

        # clim stats
        if dic["metric_clim"]:
            clim_mean = Clim_stats(clim_reg_ts).values.tolist()
            result = {case.fn_var_out: {"mean": clim_mean}}
            # print(result)
            write_json_file(dic, "metric_clim", case, result)
