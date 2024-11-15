import datetime

import cftime
import numpy as np


def detect_calendar(da):
    """Detects the calendar type from an xarray DataArray."""
    time_var = da["time"]

    # Check if time is encoded using cftime (for custom calendars like NoLeap)
    if isinstance(time_var.values[0], cftime.datetime):
        # Return calendar type (e.g., 'noleap', '365_day', etc.)
        return time_var.encoding.get("calendar", "standard")
    elif isinstance(time_var.values[0], np.datetime64):
        # For standard datetime64, return 'datetime64'
        return "datetime64"
    else:
        raise ValueError("Unknown calendar format")


def convert_to_target_calendar(da, target_calendar):
    """Convert the time of an xarray DataArray to the target calendar."""
    source_calendar = detect_calendar(da)

    if source_calendar == "datetime64" and target_calendar != "datetime64":
        # Convert datetime64 to the target custom calendar (e.g., NoLeap)
        time_values = da["time"].values
        # Use cftime's num2date for conversion
        converted_times = [
            cftime.datetime(
                year=int(t.astype("M8[Y]").astype(int) + 1970),
                month=int(t.astype("M8[M]").astype(int) % 12 + 1),
                day=int(t.astype("M8[D]").astype(int) % 31 + 1),
                calendar=target_calendar,
            )
            for t in time_values
        ]
        da["time"] = converted_times

    elif source_calendar != "datetime64" and target_calendar == "datetime64":
        # Convert custom calendar (e.g., NoLeap) to datetime64
        time_values = da["time"].values
        #        converted_times = np.array(
        #            [np.datetime64(cftime.num2date(t, units="days since 1850-01-01", calendar=source_calendar).to_pydatetime())
        #            for t in time_values]
        #        )

        # print('source_calendar = ', source_calendar) # proleptic gregorian
        # print('time_values = ', time_values[0:10])

        #        converted_times = np.array(
        #            [np.datetime64(datetime.datetime(
        #                cftime.num2date(t, units="days since 1850-01-01", calendar=source_calendar).year,
        #                cftime.num2date(t, units="days since 1850-01-01", calendar=source_calendar).month,
        #                cftime.num2date(t, units="days since 1850-01-01", calendar=source_calendar).day
        #            )) for t in time_values]
        #        )

        #        converted_times = np.array([np.datetime64(dt.to_pydatetime()) for dt in time_values])

        converted_times = np.array(
            [
                np.datetime64(
                    datetime.datetime(
                        dt.year,
                        dt.month,
                        dt.day,
                        dt.hour,
                        dt.minute,
                        dt.second,
                        # dt.microsecond,
                        # dt.nanosecond,
                    )
                )
                for dt in time_values
            ]
        )

        da["time"] = converted_times

    return da


def match_calendar(da1, da2):
    """Match calendars between da1 and da2."""
    # Detect the calendars
    calendar1 = detect_calendar(da1)
    calendar2 = detect_calendar(da2)
    # print(calendar1)
    # print(calendar2)

    # Convert da2 to match da1's calendar, if needed
    if calendar1 != calendar2:
        if calendar1 == "datetime64":
            # Convert da2 to datetime64
            da2 = convert_to_target_calendar(da2, "datetime64")
        elif calendar2 == "datetime64":
            # Convert da1 to datetime64
            da1 = convert_to_target_calendar(da1, "datetime64")
        else:
            # Convert to 360_day calendar
            if calendar1 == "360_day":
                da2 = da2.convert_calendar(calendar1, align_on="year")
            elif calendar2 == "360_day":
                da1 = da1.convert_calendar(calendar2, align_on="year")
            elif calendar1 in ["365_day", "no_leap"]:
                da2 = da2.convert_calendar(calendar1)
            elif calendar2 in ["365_day", "no_leap"]:
                da1 = da1.convert_calendar(calendar2)
            else:
                da1 = da1.convert_calendar(calendar2)

    return da1, da2


def time_index_interp(da1, da2):
    da2 = da2.reindex(time=da1.time, method="nearest")

    return da1, da2


def find_common_times(da1, da2):
    """find common timestamps between da1 and da2."""

    da1, da2 = match_calendar(da1, da2)

    # Now both datasets are on the same calendar, find the common timestamps
    common_times = np.intersect1d(da1["time"].values, da2["time"].values)

    if len(common_times) == 0:
        da1, da2 = time_index_interp(da1, da2)
        return da1, da2

    else:
        # Select the data with common timestamps
        da1_common = da1.sel(time=common_times)
        da2_common = da2.sel(time=common_times)

    return da1_common, da2_common
