json_structure = ['REF', 'RESULTS']
layout = ("model", "ARDT", "region", "season")

start_date = '1980-01-01'
end_date = '1981-12-31'

season_list = ['NDJFM','JJA']
season_month_list = [[11,12,1,2,3], [6,7,8]]


model_list = ['CanESM2', 'CCSM4'] # idm
ARDT_list = ['Mundhenk', 'TECA'] # idt
region_list = ['California', 'New_Zealand'] # idr


tag_var_list = ['binary_tag', 'binary_tag'] # idt
tag_freq_list = ['6h', '6h'] # idt, tag data frequency
tag_var_out = 'binary_tag'


include_clim = False # used to cross check at QA check

clim_var_list = ['pr', 'precip'] # idc
clim_freq_list = ['1D', '1ME'] # idc, climate data frequency
clim_var_out = 'pr'

clim_4D = False # if 4D select plev
lev_dim_list = ['plev','lev']
lev_dim = 'plev' # lev_dim_list[i]
lev_coord_list = [85000, 85000] 
lev_coord = 85000


#target_freq_list = ['1D', '1D'] # target frequency can not be higher than tag_freq or var_freq, this is the temporal resolution we want to use to perform statistics
target_freq = '1D'


mask_lndocn = None # 'ocean', 'land'


#unit_adjust = ('True', 'multiply', 86400)
#unit_src
#unit_target


dir_in = 'demo/data'
dir_out = 'output'
dir_fig = 'figures'


debug = False
make_plot = False

tag_out_ts = True
tag_out_map = True
tag_out_map_ts = True
clim_out_ts = True
clim_out_map = True
clim_out_map_ts = True


parallel = True
restart = False # run climate data metrics only, based on processed/existing/saved AR tags statistis



# ======== metrics =========
metric_freq = True
metric_peak_day = False
metric_character = False
metric_spatial_corr = False
metric_iou = False
metric_clim = False

vars_in_metric_freq = ('freq', 'count')
vars_in_metric_peak_day = ('peak_day', 'count_mean', 'count_std', 'count_ens')

# ======== diagnostics =========
diag_peak_day_histogram = False
diag_character_histogram = False


