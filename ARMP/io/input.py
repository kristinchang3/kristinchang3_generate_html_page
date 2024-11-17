import json
import os
from itertools import product
from pathlib import Path

import numpy as np
import xarray as xr


def set_dir(folder):
    """
    set absolute directory path for a specific folder in ARMP
    """
    # Define the path for the 'data' directory as structured in ARMP
    data_dir = Path(__file__).parent.parent / folder
    # Create the directory with parents and without raising an error if it exists
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def current_dir():
    """ get absolute path for current script dir """
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir


def unpack_fn_list(fn_list):
    """
    fn_list is a .txt file contains filenames
    unpack it as a list of filenames
    """
    with open(fn_list, "r") as f:
        file_list = [line.strip() for line in f]

    fn_dir = os.path.dirname(fn_list)
    absolute_file_list = [os.path.join(fn_dir, file_name) for file_name in file_list]

    return absolute_file_list


def flatten_layout(metric_layout):
    metric_layout_flatten = [item if isinstance(item, list) else [item] for item in metric_layout]
    return metric_layout_flatten


# def create_variables_dict(model, ARDT, region, season, **kwargs):
#    # Use locals() to get all local variables, and filter out kwargs
#    variables_dict = {k: v for k, v in locals().items() if k != 'kwargs'}
#
#    # Update with kwargs directly`
#    variables_dict.update(kwargs)
#
#    return variables_dict


def remove_last_underscore(string):
    # Find the last occurrence of the underscore
    idx = string.rfind("_")

    # If there's no underscore, return the original string
    if idx == -1:
        return string

    # Return the substring up to (but not including) the last underscore
    return string[:idx]


def case_combi(case_name, var1, var2):
    new_case_name = case_name.replace(var1, var2)
    return new_case_name


def nc_in(var_name, suffix, case_name, dir_out):
    fn_out = "_".join([case_name, var_name, suffix])
    ds = xr.open_dataset(os.path.join(dir_out, fn_out))
    da = ds[var_name]

    return da


def read_json_file(dic, metric):
    """
    access to metric results from saved json file
    """
    json_filename = "{}.json".format(metric)
    json_filepath = os.path.join(dic["dir_out"], json_filename)

    with open(json_filepath, "r") as json_file:
        dict_in = json.load(json_file)

    return dict_in


def extract_dict(nested_dict, key_layers, target_key):
    """
    Extracts data from the specified layers and target key in a nested dictionary
    and returns the extracted data as a numpy array, with dimensions depending on
    the layers in the key_layers argument.

    Parameters:
        nested_dict (dict): The nested dictionary to extract data from.
        key_layers (list of lists): A list of lists of keys representing the layers.
        target_key (str): The target key whose values need to be extracted from the leaf dictionaries.

    Returns:
        np.ndarray: A numpy array containing the extracted values with dimensions corresponding
                    to the structure of key_layers.
    """

    def get_nested_value(nested_dict, key_path):
        """Helper function to access a value given a list of keys (path)."""
        for key in key_path:
            nested_dict = nested_dict.get(key, {})
        return nested_dict

    layer_combinations = list(product(*key_layers))

    # List to collect the values for the specified target_key
    result = []

    # For each combination of layers, extract the value for the target key
    for combination in layer_combinations:
        # Get the data at this combination of layers
        data_at_layer = get_nested_value(
            nested_dict, combination[:-1]
        )  # All but the last key

        # Extract the data corresponding to the target key from the last layer
        final_key = combination[
            -1
        ]  # The final layer key (e.g., 'California' or 'Mundhenk')
        final_layer_data = data_at_layer.get(final_key, {})

        # Append the value for the target key (or None if not found)
        if target_key:
            result.append(final_layer_data.get(target_key, None))
        else:
            result.append(final_layer_data)

    # Convert the result to a numpy array and return it
    result_array = np.array(result).reshape([len(layer) for layer in key_layers])

    return result_array.squeeze()
