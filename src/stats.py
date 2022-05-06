from typing import List, Optional
import numpy as np
import xarray as xr
import xrft
import matplotlib.pyplot as plt
from .utils import get_all_coords
from dask.diagnostics import ProgressBar

def rmse_coords(
    ds_truth: xr.DataArray, 
    ds_preds: xr.DataArray, 
    coords: Optional[List[str]]=None, 
    normalized: bool=True
) -> xr.DataArray:
    
    # calculate difference
    sq_diff = (ds_preds - ds_truth)**2
    
    # mean
    sq_diff = sq_diff.mean(dim=coords)
    
    # squared difference
    rmse_t = np.sqrt(sq_diff)
    
    if normalized:
        sq_true = ds_truth**2
        sq_true = sq_true.mean(dim=coords)
        
        rmse_t = 1.0 - rmse_t /np.sqrt(sq_true)
        
        # rename coordinate
        rmse_t = rmse_t.rename("nrmse")
        
    else:
        
    
        # rename coordinate
        rmse_t = rmse_t.rename("rmse")
    
    return rmse_t

def compute_psd(
    ds_truth,
    ds_preds,
    coords,
):
    Nx, Ny, Nz = coords[0], coords[1], coords[2]
    
    with ProgressBar():
        # compute error = SSH recon - SSH gt
        diff = ds_preds - ds_truth
        
        # rechunk differences
        diff = diff.chunk({Nx:1, Ny: diff[Ny].size, Nz: diff[Nz].size})
        
        # rechunk SSH truth
        signal = ds_truth.chunk({Nx:1, Ny: ds_truth[Ny].size, Nz: ds_truth[Nz].size})
        
        # Compute PSD_err and PSD_signal
        psd_diff = xrft.power_spectrum(diff, dim=[Ny, Nz], detrend='constant', window=True).compute()
        psd_signal = xrft.power_spectrum(signal, dim=[Ny, Nz], detrend='constant', window=True).compute()
        
        # average over Nx coord
        psd_diff = psd_diff.mean(dim=Nx).where((psd_diff[f"freq_{Ny}"] > 0.) & (psd_diff[f"freq_{Nz}"] > 0), drop=True)
        psd_signal = psd_signal.mean(dim=Nx).where((psd_signal[f"freq_{Ny}"] > 0.) & (psd_signal[f"freq_{Nz}"] > 0), drop=True)
        
        # save psd
        psd = xr.Dataset({
            "psd_diff": psd_diff,
            "psd_signal": psd_signal
        })
        
        # compute normalized psd score
        psd["psd_score"] = 1.0 - (psd_diff/psd_signal)
        
        return psd

def shortest_resolved_scale(ds, level: float=0.5):
    
    level = [level]
    
    coords = get_all_coords(ds)


    pts = plt.contour(
        1./ds[coords[0]].values,
        1./ds[coords[1]].values,
        1./ds.psd_score.transpose(*coords).values.T,
        level
    )
    x05, y05 = pts.collections[0].get_paths()[0].vertices.T

    plt.close()

    return {coords[0]: np.min(x05), coords[1]: np.min(y05)}