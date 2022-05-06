from typing import List, Union
import numpy as np

def get_streaming_lines(
    data: np.ndarray, rate: int=10, width: int=4, axis: str="x"
) -> Union[np.ndarray, List[np.ndarray]]:
    """
    Parameters
    ----------
    data : np.ndarray, (Nt, Nx, Ny)
        a 2D Spatio-Temporal array
    rate : int, default=10
        the speed of the tracks wrt to time.
        (best values are between 1-10)
    width : int, default=4
        the width of the track, SWOT=30, Nadir=2-4
    axis : str, default="x"
        (note, I dont think this does anything)
    
    Returns
    -------
    obs : np.ndarray, (Nt, Nx, Ny)
        an array where the values outside the track are masked out
    inds : List[np.ndarray]
        the indices that are masked per time step.
    """
    
    
    nt, nx, ny = data.shape
    
    data = data.reshape((nt, nx * ny))
    
    y_obs = np.empty_like(data)
    y_obs[:] = np.nan
    
    index_obs = []
        
    if axis == "x":
        loop_axis = nx
        n_points = ny
    elif axis == "y":
        loop_axis = ny
        n_points = nx
    else:
        raise ValueError(f"Unrecognized loop axis")
    
    
    for i in range(nt):
        
        index = []
        
        for j in range(loop_axis):
            start = n_points * (j - 1) + rate + j + (rate * np.mod(i, n_points))
            index.extend(np.arange(start, start+width))
            
            start = n_points * (j - 1) + rate - j - (rate * np.mod(i, n_points))
            index.extend(np.arange(start - width, start))
            
        index = np.array(index)
        
        idx = np.unique(np.where( (index < (nx * ny)) & (index >= 0) )[0])
        
        index = index[idx]
        
        index_obs.append(index)
        y_obs[i, index] = data[i, index]
        
    
    y_obs = y_obs.reshape((nt, nx, ny))
    
    return y_obs, index_obs