import os
from dataclasses import fields

from ARMP.lib.convention import Case, Case_clim
from ARMP.lib.loader import init_dataclass


def modify_list_keys(dictionary):
    modified_keys = []
    for key, value in dictionary.items():
        if key.endswith("_list"):
            modified_key = key[:-5]  # Remove the last 5 characters "_list"
            modified_keys.append(modified_key)
    return modified_keys


def case_across_list(item, list1, list2):
    """find the corresponding item in list2 for a given item in list1"""
    if item in list1:
        index = list1.index(item)
        if index < len(list2):
            return list2[index]
    return None


def iter_list(dic, ext="_list"):
    layout_pool = []
    # for field in layout:
    for field in dic["layout"]:
        # lst = globals().get(field + ext, None)
        lst = dic.get(field + ext)  # .copy()
        layout_pool.append(lst)
    return layout_pool


def iter_list_ref(dic, ext="_list"):
    layout_pool = []
    for field in dic["layout"]:
        lst = dic.get(field + ext)  # .copy()
        if field == "model":
            #    model_ref = lst.pop(0)
            # layout_pool.append(lst)
            model_ref = lst[0]
            layout_pool.append(lst[1:])
        else:
            layout_pool.append(lst)
    return layout_pool, model_ref


def iter_list_ref_ARDT(dic, ext="_list"):
    layout_pool = []
    for field in dic["layout"]:
        lst = dic.get(field + ext)  # .copy()
        if field == "ARDT":
            #    ARDT_ref = lst.pop(0)
            # layout_pool.append(lst)
            ARDT_ref = lst[0]
            layout_pool.append(lst[1:])
        else:
            layout_pool.append(lst)
    return layout_pool, ARDT_ref


def make_case(dataclass, combi, dic):
    layout = dic["layout"]

    layout_dic = {key: None for key in layout}
    layout_dic.update(zip(layout_dic.keys(), combi))
    season_month = case_across_list(
        layout_dic["season"], dic["season_list"], dic["season_month_list"]
    )
    layout_dic.update({"season_month": season_month})

    # keys = list(case.__dataclass_fields__.keys())
    # keys = [item for item in keys if item not in list(layout_dic.keys()) ] # remove layout keys
    # list_keys = [key + "_list" for key in keys] # get params end with _list except layout *_list

    case_keys = [
        field.name for field in fields(dataclass)
    ]  # get defined keys in dataclass

    dic_list_keys = modify_list_keys(dic)  # return keys endwith _list, removing _list
    dic_list_keys = [
        item for item in dic_list_keys if item not in list(layout_dic.keys())
    ]

    list_keys = list(set(case_keys).intersection(set(dic_list_keys)))

    # QA make sure list_keys are in dic
    # if not, remove the corresponding item in both
    # keys and list keys
    # list_keys = list(filter(lambda item: item in list(dic.keys()), list_keys))
    # this following two lines need to be modified
    # if len(list_keys) != len(keys):
    #    raise KeyError("{dataclass} key value list not specified in config")

    case = init_dataclass(dataclass, dic)
    case.update(layout_dic)

    if isinstance(case, Case):
        value_list = []
        value = case_across_list(case.ARDT, dic["ARDT_list"], dic["tag_var_list"])
        value_list.append(value)
        case.fn_var = value
        value = case_across_list(case.model, dic["model_list"], dic["tag_freq_list"])
        value_list.append(value)
        case.fn_freq = value
        # case_name = "_".join(combi)
        case_name = "{}_tag".format("_".join(combi))
        # fn_in = "{}_tag_list.txt".format('_'.join(combi[0:2]))
        fn_in = "{}_tag_list.in".format(
            "_".join((layout_dic["model"], layout_dic["ARDT"]))
        )
        fn_list = os.path.join(dic["dir_in"], fn_in)

        case.tag_list = fn_list
        case.fn_var_out = dic["tag_var_out"]

    elif isinstance(case, Case_clim):
        value_list = []
        for key in list_keys:
            value = case_across_list(case.model, dic["model_list"], dic[key + "_list"])
            value_list.append(value)
            if key == "clim_var":
                case.fn_var = value
            if key == "clim_freq":
                case.fn_freq = value

        case_name = "{}_{}".format("_".join(combi), dic["clim_var_out"])
        # fn_in = "{}_{}_clim_list.txt".format(combi[0], dic['clim_var_out'])
        fn_in = "{}_{}_clim_list.in".format(layout_dic["model"], dic["clim_var_out"])
        fn_list = os.path.join(dic["dir_in"], fn_in)

        case.clim_list = fn_list
        case.fn_var_out = dic["clim_var_out"]

    value_dic = dict(zip(list_keys, value_list))
    case.update(value_dic)

    case.case_name = case_name.replace(" ", "_")
    case.fn_list = fn_list

    return case
