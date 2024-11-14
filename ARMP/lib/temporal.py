import numpy as np


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


def adjust_time_for_season(time, months):
    """prepare for the adjusted time index for seasonal average."""

    adjustment_months = get_adjustment_months(months)

    # Check if adjustment_months is empty
    if not adjustment_months:
        return time  # Return the original time if no adjustments are needed

    # Create a copy of the original years
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

    return adjusted_time


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
