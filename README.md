# Quasi-Geostropic Mapping Data Challenge 2022b

This repository contains codes and samples notebooks for generating and processing the QG mapping data challenge.



Steam Function       |  Potential Vorticity
:-------------------------:|:-------------------------:
 ![animation](assets/p_movie.gif)  |  ![animation](assets/q_movie.gif) 
 ![animation](assets/obs_p_movie.gif)  |  ![animation](assets/obs_q_movie.gif) 

## Motivation

## Data

You can download the file needed for the data challenge here:

```bash
wget -P data/ https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/dc2022b_q/qg_sim.nc
```


Check [here](https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/catalog/meomopendap/extract/dc2022b_q/catalog.html) for the available files.


## Evaluation (TODO)

You will also find an example of evaluation notebook using the baseline method. The reconstuctions shall be stored in a NetCDF file compliant with the format used in this Notebook.


### Leaderboard

| Method     |   µ(RMSE) |   σ(RMSE) |   λx (dx=1) |   λt (dt=1) | Notes                     | Reference        |
|:-----------|------------------------:|---------------------:|-------------------------:|-----------------------:|:--------------------------|:-----------------|
| baseline  :trophy: |                    **???** |                 **???** |            **???** |        **???** | Simplest | eval/.ipynb |
| | | | | | | |


**µ(RMSE)**: average RMSE score.  
**σ(RMSE)**: standard deviation of the RMSE score.  
**λx**: minimum spatial scale resolved.  
**λt**: minimum time scale resolved. 


### Special Thanks

#### QG Model

The original QG model was taken from Hugo. It can be found [here](https://github.com/hrkz/torchqg). I have forked a branch which has a refactored version which has the notebook to generate the data. This can be found [here](https://github.com/jejjohnson/torchqg/tree/package).