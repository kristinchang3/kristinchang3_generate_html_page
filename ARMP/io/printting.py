import os

from ARMP.params.config import project_name


def str_print(input_string):
    return input_string.replace("_", " ")


def str_fn(input_string):
    return input_string.replace(" ", "_")


def print_case(case, var="AR"):
    model = case.model
    ARDT = case.ARDT
    region = case.region
    season = case.season
    print(f"processing {var} ---> {model}, {ARDT}, {region}, {season}")


def get_version_from_pkg_info(pkg_info_filename="PKG-INFO"):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    pkg_info_path = os.path.join(current_dir, "..", "..", pkg_info_filename)

    if not os.path.isfile(pkg_info_path):
        print(f"Error: {pkg_info_filename} not found in: {pkg_info_path}")
        return "Unknown"

    version = "Unknown"
    try:
        with open(pkg_info_path, "r") as file:
            for line in file:
                if line.startswith("Version:"):
                    version = line.strip().split("Version:")[1].strip()
                    break
    except Exception as e:
        print(f"Error reading version: {e}")
    return version


def print_armp():
    version = get_version_from_pkg_info()

    #    message = r"""
    #    ################################################################################
    #        _    ____  __  __ ____
    #       / \  |  _ \|  \/  |  _ \
    #      / _ \ | |_) | |\/| | |_) |
    #     / ___ \|  _ <| |  | |  __/
    #    /_/   \_\_| \_\_|  |_|_|
    #
    #    Welcome to Atmospheric River Metrics Package!  (Version: {version})
    #
    #    Job starts for {project_name}
    #    ################################################################################
    #    """
    message = f"""
################################################################################
    _    ____  __  __ ____
   / \\  |  _ \\|  \\/  |  _ \\
  / _ \\ | |_) | |\\/| | |_) |
 / ___ \\|  _ <| |  | |  __/
/_/   \\_\\_| \\_\\_|  |_|_|

Welcome to Atmospheric River Metrics Package!  (Version: {version})

Job starts for {project_name}
################################################################################
    """
    print(message)
