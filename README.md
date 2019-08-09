# SedimentTransport_modelling
Sediment_modelling
Author:		J.M. Wilms
email:		fine.wilms@deltares.nl
date:			09/08/2019

--clean_waterlevel.py clean waterlevel time series files in the SPM/Rawdata folder and plots the results for each individual station in
	the 'images_daily' folder. Each figure contains three graphs:  1) The original timeseries 2) The timeseries with values larger than
	998 cm/s removed. Consecutive values that are less than 200 seconds apart and change less than 1 cm are also removed. The 
	third graph contains a data set that has been resampled from its original frequency or frequencies to a daily frequency. This
	is done by taking the mean of all the available mesurements during that day.
	This scripts saves each preporcessed clean time series for each station to a .csv file with the extension _orig_postproc_daily.
	In addition, it creates one csv file that contains all the stations' time series on a daily frequency.

--water_level_sparse_data_removal.py filters all stations' timeseries with more than 1000 missing values. It then determines the 
	lat/lon coordinates of the remaining stations by converting the X/Y positions in the original time series file from EPSG 25831 to EPSG 4326.
	The locations of the stations are then plotted on a map along with the locations of the locations of sites that contain sediment
	information.
	

