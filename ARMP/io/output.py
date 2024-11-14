import copy
import json
import os
from itertools import product

from ARMP.lib.control import iter_list

# import sys


def nc_out(da, var_name, suffix, case_name, dir_out, **kwargs):
    da.name = var_name
    # fn_out =  "_".join([case_name, da.name, suffix])
    fn_out = "_".join([case_name, var_name, suffix])
    da.load().to_netcdf(os.path.join(dir_out, fn_out))


def json_create(metric_structure):
    """
    create dictionary tree structure for metric results
    """
    tree_dict = {}
    current_level = tree_dict

    for key in metric_structure:
        current_level[key] = {}
        current_level = current_level[key]

    return tree_dict


def replace_key_name(d, target_key, replace_key):
    """
    generate dictionary tree branches according to
    the number of models, ARDTs, regions, seasons
    in the statistics
    """
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == target_key:
                d[replace_key] = d.pop(key)  # Replace key with 'smart'
            else:
                replace_key_name(d[key], target_key, replace_key)
    return d


def merge_dicts(d1, d2):
    """
    concatenate dictionary branches into one metrics dictionary tree
    """
    # If d1 is None or empty, just return d2
    if not d1:
        return d2

    # If d2 is None or empty, just return d1
    if not d2:
        return d1

    for key, value in d2.items():
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(value, dict):
                merge_dicts(d1[key], value)  # Recursively merge dictionaries
            else:
                d1[key] = value  # Replace if not a dict
        else:
            d1[key] = value  # Add new key

        return d1


def create_json_dict(dic):
    """
    create json dictionary for metrics output
    """
    json_structure = dic["json_structure"]
    layout_pool = iter_list(dic)

    json_dict = {key: {} for key in json_structure}
    tree_dict = json_create(dic["layout"])

    result_dict = {}

    for combi in product(*layout_pool):
        metric_dict = copy.deepcopy(tree_dict)

        for var_name, var in zip(dic["layout"], combi):
            replace_key_name(metric_dict, var_name, var)

        result_dict = merge_dicts(result_dict, metric_dict)

    json_dict["RESULTS"].update(result_dict)

    return json_dict


def create_json_file(dic):
    """
    create json file for metrics output
    """
    metrics = [key for key in dic.keys() if key.startswith("metric_")]

    for metric in metrics:
        if dic[metric]:
            json_dict = create_json_dict(dic)
            json_filename = "{}.json".format(metric)
            json_filepath = os.path.join(dic["dir_out"], json_filename)
            # print("json_filepath = ", json_filepath)

            with open(json_filepath, "w") as json_file:
                json.dump(json_dict, json_file, indent=4)


def write_json_file(dic, metric, case, result):
    """
    write metric results to json file
    """
    json_filename = "{}.json".format(metric)
    json_filepath = os.path.join(dic["dir_out"], json_filename)

    with open(json_filepath, "r") as json_file:
        dict_in = json.load(json_file)

    dict_in["RESULTS"][case.model][case.ARDT][case.region][case.season].update(result)

    with open(json_filepath, "w") as json_file:
        json.dump(dict_in, json_file, indent=4)


def update_dict_ref(dic, dict_in):
    """
    move ref stats in RESULTS section to REF section
    """
    ref_data = dic["model_list"][0]

    ref_dict = dict_in["RESULTS"].pop(ref_data, None)
    dict_in["REF"][ref_data] = ref_dict

    return dict_in


def update_json_ref(dic, metric):
    """
        move ref stats in RESULTS section to REF section
    and update json file
    """
    json_filename = "{}.json".format(metric)
    json_filepath = os.path.join(dic["dir_out"], json_filename)

    with open(json_filepath, "r") as json_file:
        dict_in = json.load(json_file)

    dict_in = update_dict_ref(dic, dict_in)

    with open(json_filepath, "w") as json_file:
        json.dump(dict_in, json_file, indent=4)


def update_json_file(dic, metric, result_dict):
    """
    update  RESULTS section if the json file
    """
    json_filename = "{}.json".format(metric)
    json_filepath = os.path.join(dic["dir_out"], json_filename)

    with open(json_filepath, "w") as json_file:
        json.dump(result_dict, json_file, indent=4)
