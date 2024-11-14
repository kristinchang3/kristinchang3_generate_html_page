from ARMP.lib.loader import dic, setting
from ARMP.io.input import read_json_file
from ARMP.io.output import update_dict_ref, update_json_file, update_json_ref, write_json_file 
from ARMP.lib.control import iter_list, iter_list_ref
from itertools import product
import os
import copy


def load_blobstats(fn_in):

    data = np.loadtxt(fn_in)
    data[:,5] /= 1e6 # m2->km2
    columns = data[:, 3:8]

    return columns


def AR_character_stats(fn_in, field_list):
    """
    do statistics on blobstats output
    return a dictionary
    """
    field_dict = {key: {} for key in field_list}

    columns = load_blobstats(fn_in)
    #data = np.loadtxt(fn_in)
    #data[:,5] /= 1e6 # m2->km2
    #columns = data[:, 3:8]

    for i in range(columns.shape[1]):
        character = field_list[i]
        array = columns[:,i]

        count = array.shape[0]

        if i in [3, 4]:
            array = [x for x in array if "nan" not in str(x)]
            count = len(array)

        mean = np.nanmean(array)
        std = np.nanstd(array)

        field_dict[character]['count'] = count
        field_dict[character]['mean'] = mean
        field_dict[character]['std'] = std

    return field_dict


def AR_character_stats_json(dic, metric):
    '''
    add AR characteristics stats to json file
    '''
    field_list = ['lat','lon','area','width','length']

    layout_pool = iter_list(dic)

    for combi in product(*layout_pool):
        case = make_case(Case, combi, dic)

        case_name = case.case_name
        fn_in = os.path.join(dic['dir_out'], case_name, "_blobstats.txt")
        result = AR_character_stats(fn_in, field_list)

        write_json_file(dic, metric, case, result)



if __name__ == "__main__":

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind':float_formatter})

    metric = 'metric_character'

    AR_character_stats_json(dic, metric)

