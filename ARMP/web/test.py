import os
import sys
import json
import requests
from itertools import product
import numpy as np
from ARMP.io.printting import str_fn
from ARMP.io.input import extract_dict, read_json_file, flatten_layout
from ARMP.io.output import create_json_file, write_json_file
from ARMP.lib.control import iter_list, make_case
from ARMP.lib.convention import Case
from ARMP.lib.loader import init_dataclass

def make_case2(dataclass, combi, dic):
    layout = dic["layout"]

    layout_dic = {key: None for key in layout}
    layout_dic.update(zip(layout_dic.keys(), combi))

    case = init_dataclass(dataclass, dic)
    case.update(layout_dic)

    return case


json_structure = ["REF", "RESULTS"]
layout = ("model", "ARDT", "region", "season")

model_list = ['BCC-CSM2-MR', 'CanESM2', 'CCSM4', 'CSIRO-Mk3-6-0', 'NorESM1-M', 'MRI-ESM2-0', 'IPSL-CM51-LR', 'IPSL-CM5B-LR', 'IPSLCM61-LR']
region_list = ['N Pacific', 'S Pacific', 'N Atlantic', 'S Atlantic', 'Indian Ocean']
season_list = ['annual']
ARDT_list = ['TE']

dic = {"json_structure": json_structure, "layout": layout, "model_list": model_list, "region_list": region_list, "season_list": season_list, "ARDT_list":ARDT_list, "dir_out": "data/", "metric_spatial_corr":True}

ml = [str_fn(x) for x in region_list]

#print(ml)

# fig_freq_m_r_land.png
# map_freq_CanESM2_California_Mundhenk_annual.png in figure/
# output_spatial_corr.txt
#metric_json_corr.json

data = np.loadtxt("data/output_spatial_corr.txt")

#for i, model in enumerate(model_list):
#    for j, region in enumerate(region_list):
#
#        original_filename = "data/fig_freq_"+str(i)+"_"+str(j)+"_land.png"
#        #new_filename = original_filename.replace(str(i), model).replace(str(j), region)
#        new_filename = "data/map_freq_"+model+"_"+str_fn(region)+"_TE_annual.png"
#
#        os.rename(original_filename, new_filename)


angle = data.reshape(9,-1)


#create_json_file(dic)
#
#layout_pool = iter_list(dic)
#
#for combi in product(*layout_pool):
#    case = make_case2(Case, combi, dic)
#
#    model = case.model
#    ARDT = case.ARDT
#    region = case.region
#    season = case.season
#
#
#    model_ind = model_list.index(model)
#    region_ind = region_list.index(region)
#
#    result = {"corr":angle[model_ind, region_ind]}
#
#    write_json_file(dic, "metric_spatial_corr", case, result)



if __name__ == "__main__":

    dir_web = 'data'
    metric_layout = flatten_layout([model_list, ARDT_list, region_list, season_list])
    metric_var = "corr"
    # metric_sig = 'pvalue'
    metric = "metric_spatial_corr"

    #dict_in = read_json_file(dic, metric)
    metric_fn = os.path.join(dir_web, "{}.json".format(metric))
    with open(metric_fn, 'r') as json_file:
        dict_in = json.load(json_file)

    metric_value = extract_dict(dict_in["RESULTS"], metric_layout, metric_var)


    #img_path = 'https://raw.githubusercontent.com/PCMDI/ARMP/main/ARMP/web/data'
    #img_path = 'https://raw.githubusercontent.com/PCMDI/ARMP/main/ARMP/metrics/'
    img_path = 'https://raw.githubusercontent.com/PCMDI/ARMP/main'

    response = requests.get(img_path)
    
    if response.status_code == 200:
        print(response.text)  # Prints the content of the file
    else:
        print(f"Error: {response.status_code}")


