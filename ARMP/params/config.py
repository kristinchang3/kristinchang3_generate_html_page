# from pathlib import Path
from ARMP.io.input import set_dir

json_structure = ["REF", "RESULTS"]
layout = ("model", "ARDT", "region", "season")

start_date = "1997-01-01"
end_date = "1999-12-31"

#season_list = ["NDJFM"]
season_list = ["annual"]
season_month_list = [[11, 12, 1, 2, 3]]


model_list = ["ERA5", "CanESM2"]  # idm
ARDT_list = ["Mundhenk"]  # idt
region_list = ["California"]  # idr


tag_var_list = ["binary_tag", "binary_tag"]  # idt
tag_freq_list = ["6h", "6h"]  # idt, tag data frequency
tag_var_out = "binary_tag"
tag_var_fn = tag_var_out


include_clim = False  # used to cross check at QA check

clim_var_list = ["pr", "pr"]  # idc
clim_freq_list = ["1D", "1D"]  # idc, climate data frequency
clim_var_out = "pr"
clim_var_fn = clim_var_out

clim_4D = False  # if 4D select plev
lev_dim_list = ["plev", "lev"]
lev_dim = "plev"  # lev_dim_list[i]
lev_coord_list = [85000, 85000]
lev_coord = 85000


# target_freq_list = ['1D', '1D'] # target frequency can not be higher than tag_freq or var_freq, this is the temporal resolution we want to use to perform statistics
target_freq = "1D"


mask_lndocn = None  # 'ocean', 'land'


# unit_adjust = ('True', 'multiply', 86400)
# unit_src
# unit_target


# dir_in = Path(__file__).parent.parent/'data'
# dir_out = Path(__file__).parent.parent/'output'
# dir_fig = Path(__file__).parent.parent/'figure'
# dir_in.mkdir(parents=True, exist_ok=True)
# dir_out.mkdir(parents=True, exist_ok=True)
# dir_fig.mkdir(parents=True, exist_ok=True)

dir_in = set_dir("data")
dir_out = set_dir("output")
dir_fig = set_dir("figure")

debug = False
make_plot = True

tag_out_ts = True
tag_out_map = True
tag_out_map_ts = True
clim_out_ts = True
clim_out_map = True
clim_out_map_ts = True


parallel = True
restart = False  # run climate data metrics only, based on processed/existing/saved AR tags statistis


# ======== metrics =========
metric_freq = True
metric_peak_day = True
metric_character = False
metric_spatial_corr = True
metric_iou = True
metric_clim = True

vars_in_metric_freq = ("freq", "count")
vars_in_metric_peak_day = ("peak_day", "count_mean", "count_std", "count_ens")

# ======== diagnostics =========
diag_peak_day_histogram = True
diag_character_histogram = False
diag_freq_map = False
