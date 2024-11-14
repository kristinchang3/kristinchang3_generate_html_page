from typing import Union

import regionmask
import xarray as xr
import xcdat as xc


def create_land_sea_mask(
    obj: Union[xr.Dataset, xr.DataArray],
    lon_key: str = None,
    lat_key: str = None,
    as_boolean: bool = False,
) -> xr.DataArray:
    """Generate a land-sea mask (1 for land, 0 for sea) for a given xarray Dataset or DataArray.
    stemed from pcmdi_metrics.utils.land_sea_mask

    Parameters
    ----------
    obj : Union[xr.Dataset, xr.DataArray]
        The Dataset or DataArray object.
    lon_key : str, optional
        Name of DataArray for longitude, by default None
    lat_key : str, optional
        Name of DataArray for latitude, by default None
    as_boolean : bool, optional
        Set mask value to True (land) or False (ocean), by default False, thus 1 (land) and 0 (ocean).

    Returns
    -------
    xr.DataArray
        A DataArray of land-sea mask (1 or 0 for land or sea, or True or False for land or sea).

    Examples
    --------
    >>> mask = create_land_sea_mask(ds)  #  Generate land-sea mask (land: 1, sea: 0)
    >>> mask = create_land_sea_mask(ds, as_boolean=True)  # Generate land-sea mask (land: True, sea: False)
    """

    # Use regionmask
    land_mask = regionmask.defined_regions.natural_earth_v5_0_0.land_110

    # Get the longitude and latitude from the xarray dataset
    if lon_key is None:
        lon_key = xc.axis.get_dim_keys(obj, axis="X")
    if lat_key is None:
        lat_key = xc.axis.get_dim_keys(obj, axis="Y")

    lon = obj[lon_key]
    lat = obj[lat_key]

    # Mask the land-sea mask to match the dataset's coordinates
    land_sea_mask = land_mask.mask(lon, lat=lat)

    if as_boolean:
        # Convert the 0 (land) & nan (ocean) land-sea mask to a boolean mask
        land_sea_mask = xr.where(land_sea_mask, False, True)
    else:
        # Convert the boolean land-sea mask to a 1/0 mask
        land_sea_mask = xr.where(land_sea_mask, 0, 1)

    return land_sea_mask
