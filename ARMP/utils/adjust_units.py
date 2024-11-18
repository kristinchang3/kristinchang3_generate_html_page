import xarray as xr

def adjust_units(da: xr.DataArray, adjust_tuple: tuple) -> xr.DataArray:
    """
    Convert unit following information in the given tuple.
    This is a PMP utils function

    Parameters
    ----------
    da : xr.DataArray
        Input data array
    adjust_tuple : tuple
        A tuple with at least 3 elements (4th element is optional for units).
        Example format:
        - (True, 'multiply', 86400., 'mm d-1'): converts units, e.g., from kg m-2 s-1 to mm d-1.
        - (False, 0, 0, 0): no unit conversion.

    Returns
    -------
    xr.DataArray
        Data array with converted values and updated attributes.

    Examples
    --------
    Convert units from kg m-2 s-1 to mm d-1:

    >>> import xarray as xr
    >>> da = xr.DataArray([0.1, 0.2, 0.3], dims="time", attrs={"units": "kg m-2 s-1"})
    >>> adjust_units(da, (True, 'multiply', 86400., 'mm d-1'))
    """
    action_dict = {"multiply": "*", "divide": "/", "add": "+", "subtract": "-"}
    if adjust_tuple[0]:
        print("Converting units by ", adjust_tuple[1], adjust_tuple[2])
        cmd = " ".join(["da", str(action_dict[adjust_tuple[1]]), str(adjust_tuple[2])])
        da = eval(cmd)
        if len(adjust_tuple) > 3:
            da.assign_attrs(units=adjust_tuple[3])
    return da
