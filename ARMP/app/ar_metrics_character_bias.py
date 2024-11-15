from itertools import product

import numpy as np

from ARMP.io.input import read_json_file
from ARMP.io.output import update_json_file, update_json_ref
from ARMP.lib.control import iter_list_ref, make_case
from ARMP.lib.convention import Case
from ARMP.lib.loader import dic


def AR_character_bias(dic, metric):
    """
    add AR characteristics bias result to metrics json file
    """
    field_list = ["lat", "lon", "area", "width", "length"]

    update_json_ref(dic, metric)

    # load updated json file and calculate bias and z-score
    layout_pool, model_ref = iter_list_ref(dic)

    for combi in product(*layout_pool):
        case = make_case(Case, combi, dic)

        model = case.model
        ARDT = case.ARDT
        region = case.region
        season = case.season

        dict_in = read_json_file(dic, metric)

        for character in field_list:
            results = dict_in["RESULTS"][model][ARDT][region][season][character]
            results_ref = dict_in["REF"][model_ref][ARDT][region][season][character]

            bias = results["mean"] - results_ref["mean"]

            n = results["count"]
            n_ref = results_ref["count"]
            std = results["std"]
            std_ref = results_ref["std"]

            bias_norm = bias / std

            zscore = bias / np.sqrt(std**2 / n + std_ref**2 / n_ref)

            bias_dict = {"bias": bias, "bias_norm": bias_norm, "zscore": zscore}

            dict_in["RESULTS"][model][ARDT][region][season][character].update(bias_dict)

        update_json_file(dic, metric, dict_in)


if __name__ == "__main__":
    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={"float_kind": float_formatter})

    metric = "metric_character"

    AR_character_bias(dic, metric)
