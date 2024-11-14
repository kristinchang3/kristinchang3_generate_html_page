import numpy as np
import pandas as pd
import xarray as xr

# Define the spatial extent (latitude and longitude) for California
lat_min, lat_max = 32.5, 42.0
# lon_min, lon_max = -124.4, -114.1
lon_min, lon_max = -127.5, -110.5

# Define the 1-degree resolution
latitudes = np.arange(lat_min, lat_max + 1, 1)
longitudes = np.arange(lon_min, lon_max + 1, 1)

# Define the temporal range for the year 1997 with 6-hourly resolution
# FutureWarning: 'H' is deprecated and will be removed in a future version, please use 'h' instead
time_range = pd.date_range("1997-01-01", "1997-12-31", freq="6h")
# time_range = pd.date_range('1997-01-01', '1997-12-31', freq='1D')

# Generate random binary data (0 or 1) for the variable 'binary_tag'
# Shape: (time, lat, lon)

data = np.random.choice([0, 1], size=(len(time_range), len(latitudes), len(longitudes)))

# Create an xarray Dataset
dataset = xr.Dataset(
    {"binary_tag": (["time", "lat", "lon"], data)},
    coords={"time": time_range, "lat": latitudes, "lon": longitudes},
)

dataset.to_netcdf("AR_tag2_1997.nc")


# data = np.random.uniform(0, 20, size=(len(time_range), len(latitudes), len(longitudes)))
#
## Create an xarray Dataset with 'pr' as the variable name
# dataset = xr.Dataset(
#    {
#        'pr': (['time', 'lat', 'lon'], data)
#    },
#    coords={
#        'time': time_range,
#        'lat': latitudes,
#        'lon': longitudes
#    },
#    attrs={
#        'units': 'mm/day'  # Add units attribute for precipitation
#    }
# )
#
# dataset.to_netcdf("precip2_1997.nc")
