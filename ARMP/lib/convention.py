''' preprocessing, formatting and standardizing input data'''
from dataclasses import dataclass, asdict, field, fields
from params.region_def import domain


@dataclass
class Case:
    case_name: str = field(default=None)
    tag_list: str = field(default=None)
    model: str = field(default=None)
    ARDT: str = field(default=None)
    region: str = field(default=None)
    season: str = field(default=None)
    season_month: list = field(default_factory=list)
    tag_var: str = field(default=None)
    tag_var_out: str = field(default=None)
    tag_freq: str = field(default=None)
    fn_var: str = field(default=None)
    fn_var_out: str = field(default=None)
    fn_freq: str = field(default=None)
    fn_list: str = field(default=None)

    def update(self, updates):
        for key, value in updates.items():
            if key in self.__annotations__:
                setattr(self, key, value)

    def __post_init__(self):
        self.fn_var = self.tag_var
        self.fn_var_out = self.tag_var_out
        self.fn_freq = self.tag_freq
        self.fn_list = self.tag_list

#    @property
#    def fn_var_out(self):
#        return self.tag_var_out

@dataclass
class Case_clim:
    case_name: str = field(default=None)
    clim_list: str = field(default=None)
    model: str = field(default=None)
    ARDT: str = field(default=None)
    region: str = field(default=None)
    season: str = field(default=None)
    season_month: list = field(default_factory=list)
    clim_var: str = field(default=None)
    clim_var_out: str = field(default=None)
    clim_freq: str = field(default=None)
    lev_dim: str = field(default=None)
    lev_coord: int = field(default=85000)
    fn_var: str = field(default=None)
    fn_var_out: str = field(default=None)
    fn_freq: str = field(default=None)
    fn_list: str = field(default=None)

    def update(self, updates):
        for key, value in updates.items():
            if key in self.__annotations__:
                setattr(self, key, value)

    def __post_init__(self):
        self.fn_var = self.clim_var
        self.fn_var_out = self.clim_var_out
        self.fn_freq = self.clim_freq
        self.fn_list = self.clim_list


@dataclass
class Setting:
    start_date: str = field(default=None)
    end_date: str = field(default=None)
    target_freq: str = field(default=None)
    mask_lndocn: str = field(default=None)
    dir_in: str = field(default='demo/data')
    dir_out: str = field(default='output')
    dir_fig: str = field(default='figures')
    debug: bool = field(default=False)
    make_plot: bool = field(default=False)
#    nc_out: bool = field(default=False)
    ar_freq_map: bool = field(default=False)
    ar_map_ts: bool = field(default=False)
    ar_count_ts: bool = field(default=False)
    out_map: bool = field(default=False)
    out_ts: bool = field(default=False)
    out_map_ts: bool = field(default=False)
    clim_4D: bool = field(default=False)
    parallel: bool = field(default=True)
    layout: list = field(default_factory=list)
    restart: bool = field(default=False)

    def update(self, updates):
        for key, value in updates.items():
            if key in self.__annotations__:
                setattr(self, key, value)

    

def time_swap(ds_tag):

    coord_list = list(ds_tag.coords.keys())

    if 'time' not in coord_list:
        print('time NOT in coords for model --> ')#, model_name)
        time_coords = [variable for variable in coord_list if 'time' in variable][0]
        ds_tag = ds_tag.rename({time_coords:'time'})

    return ds_tag


def lon_swap(ds_tag, region, **kwargs):

    lats,latn,lonw,lone = domain(region, **kwargs)

    coord_list = list(ds_tag.coords.keys())

    if 'lon' not in coord_list:
        print('lon NOT in coords for model --> ')#, model_name)
        lat_coords = [variable for variable in coord_list if 'lat' in variable][0]
        lon_coords = [variable for variable in coord_list if 'lon' in variable][0]

        ds_tag = ds_tag.rename({lat_coords: 'lat', lon_coords: 'lon'})

    if np.min(ds_tag.lon) < 0:
        print('swap lonw, lone to -180,180')
        print('lonw = ',lonw,' lone = ',lone)
        lonw = ( (lonw + 180) % 360) - 180
        lone = ( (lone + 180) % 360) - 180
        print('conformed lonw = ',lonw,' lone = ',lone)

    swap = False

    if lonw > lone:
        swap = True
        print('lonw > lone, then swap')

        if np.min(ds_tag.lon) < 0:
            ds_tag = xc.swap_lon_axis( ds_tag, (0, 360) ).compute()
            lonw = lonw % 360
            lone = lone % 360
            print('swapped lonw = ',lonw,' lone = ',lone)
        else:
            ds_tag = xc.swap_lon_axis( ds_tag, (-180, 180) ).compute()
            lonw = ( (lonw + 180) % 360) - 180
            lone = ( (lone + 180) % 360) - 180
            print('swapped lonw = ',lonw,' lone = ',lone)

        print("swapped longitude range ", np.min(ds_tag.lon), " - ", np.max(ds_tag.lon) )

    return lats, latn, lonw, lone, ds_tag


def lat_swap(ds_tag):

    if ds_tag.lat[0] > ds_tag.lat[-1]:
        swap = True
        ds_tag = ds_tag.isel(lat=slice(None, None, -1))

    return ds_tag


def coords_fmt(ds_tag, region, **kwargs):

    ds_tag = time_swap(ds_tag)
    lats,latn,lonw,lone,ds_tag = lon_swap(ds_tag, region, **kwargs)
    ds_tag = lat_swap(ds_tag)

    return lats,latn,lonw,lone,ds_tag



class SpecificError(Exception):
    pass
# raise SpecificError("This is a custom error")

class VariableNotExistError(Exception):
    pass

def check_variable(variable_name):
    if variable_name not in globals():
        raise VariableNotExistError(f"The variable '{variable_name}' does not exist.")

