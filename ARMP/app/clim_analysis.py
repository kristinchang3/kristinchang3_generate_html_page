from lib.loader import dic, setting
from lib.convention import Case_clim
from itertools import product
from lib.control import make_case, iter_list
from stats.clim_count import Clim_count_mf
from stats.clim_stats import Clim_stats
from io.output import create_json_file, write_json_file


def Clim_analysis(dic, setting):

    layout_pool = iter_list(dic)

    for combi in product(*layout_pool):

        case = make_case(Case_clim, combi, dic)

        kwargs = {**asdict(case), **asdict(setting)}

        clim_reg_ts = Clim_count_mf(**kwargs)

        # clim stats
        if dic['metric_clim']:
            clim_mean = Clim_stats(clim_reg_ts)
            result = {case.fn_var_out: {'mean': clim_mean}}
            write_json_file(dic, 'metric_clim', case, result)
            
