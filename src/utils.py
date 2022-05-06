from typing import List
import xarray as xr

def get_all_coords(ds: xr.Dataset) -> List[str]:
    coords = [icoord for icoord in ds.coords]
    return coords

def check_coords(ds: xr.Dataset, coords: List[str]) -> bool:
    verdict = all(elem in get_all_coords(ds) for elem in coords)
    return verdict


def reformat_time(ds, dt):
    
    ds = ds - ds[0]
    ds /= dt
    
    return ds