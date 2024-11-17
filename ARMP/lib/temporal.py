import numpy as np
import pandas as pd
import xarray as xr
import cftime


def time_select(ds_tag_reg, start_date, end_date, **kwargs):
    ds_tag_reg_tm = ds_tag_reg.sel(time=slice(start_date, end_date))

    return ds_tag_reg_tm


def season_select(ds, season, **kwargs):
    if season == "annual":
        return ds
    elif season in ["DJF", "MAM", "JJA", "SON"]:
        ds = ds.sel(time=ds.time.dt.season == season)
        return ds
    elif season == "NDJFM":
        ds.sel(time=ds["time.month"].isin([11, 12, 1, 2, 3]))
        return ds
    elif season == "MJJAS":
        ds.sel(time=ds["time.month"].isin([5, 6, 7, 8, 9]))
        return ds
    else:
        season_month = kwargs.get("season_month")
        ds.sel(time=ds["time.month"].isin(season_month))
        return ds


def get_adjustment_months(months):
    if len(months) == 1:
        return []

    if months[0] < months[-1]:
        return []

    result = []
    for num in months:
        if num > 1 and num > months[-1]:
            result.append(num)
    return result


def adjust_season(da, months):
    """prepare for the adjusted time index for seasonal average."""

    adjustment_months = get_adjustment_months(months)

    if not adjustment_months:
        return da 

    if isinstance(da.coords['time'].values[0], cftime.datetime):

        #calendar = da.coords['time'].attrs.get("calendar", "standard")
        #if calendar == "360_day":
        #    da = da.convert_calendar('standard', align_on="year")
        
        time = da.coords['time']
        
        years = np.array([t.year for t in time.values])
        months = np.array([t.month for t in time.values])
        days = np.array([t.day for t in time.values])
        hours = np.array([t.hour for t in time.values])
        minutes = np.array([t.minute for t in time.values])
        seconds = np.array([t.second for t in time.values])

        adjusted_years = np.copy(years)
        adjusted_years[np.isin(months, adjustment_months)] += 1

        # adjusted_time = pd.to_datetime(
        #     [f"{year}-{month:02d}-{day:02d}" for year, month, day in zip(adjusted_years, months, days)],
        #     errors='coerce'  # Automatically handle invalid dates by returning NaT
        # )

        adjusted_time = pd.to_datetime(
            [f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}" for year, month, day, hour, minute, second in zip(adjusted_years, months, days, hours, minutes, seconds)],
            errors='coerce'  # Automatically handle invalid dates by returning NaT
        )

        adjusted_time = np.array(adjusted_time)
        
    else:

        time = da.coords['time']
        adjusted_years = time.dt.year.copy()

        # Adjust the year for specified months to the next year
        adjusted_years = xr.where(
            time.dt.month.isin(adjustment_months),
            adjusted_years + 1,  # Move to the next year
            adjusted_years,
        )

        # Construct a new time array with the adjusted years
        adjusted_time = pd.to_datetime(
            [
                pd.Timestamp(year, month, day)
                for year, month, day in zip(
                    adjusted_years.values, time.dt.month.values, time.dt.day.values
                )
            ]
        )

    
    da.coords['time'] = ('time', adjusted_time)

    return da


def season_group(da, months, group='year'):
    """
    seasonal average
    with treatment for season spanning two years e.g. DJF
    """
    da = adjust_season(da, months)
    da_grp = da.groupby(f"time.{group}")
    da_grp_mean = da_grp.mean(dim='time')

    return da_grp_mean


def dim_year_to_time(da_grp_mean):
    """
    convert 'year' dim and coords to 'time'
    """
    time_index = pd.to_datetime(da_grp_mean['year'], format='%Y')
    time_index = pd.DatetimeIndex([str(year) + '-01-01' for year in da_grp_mean['year'].values])
    da_grp_mean = da_grp_mean.swap_dims({'year': 'time'})
    da_grp_mean['time'] = time_index

    return da_grp_mean


def extract_time_components(time_array):
    """extract hours and minutes of time array"""

    if isinstance(time_array, xr.DataArray):
        time_values = time_array.values
    else:
        time_values = time_array

    # Convert to pandas datetime for easier manipulation
    if np.issubdtype(time_values.dtype, np.datetime64):
        return pd.Series(time_values).dt.strftime("%H:%M")
    else:
        return pd.Series([t.strftime("%H:%M") for t in time_values])


def check_time_align(da1, da2):
    """check if timestamps align in terms of hours and minutes"""
    # Extract hours and minutes
    times_1 = extract_time_components(da1["time"])
    times_2 = extract_time_components(da2["time"])

    # Check for common hours and minutes
    common_times = np.intersect1d(times_1, times_2)

    if len(common_times) == 0:
        # print("The timestamps do NOT align in terms of hours and minutes.")
        return False
    else:
        # print("The timestamps align with common hours and minutes:", common_times)
        return True
