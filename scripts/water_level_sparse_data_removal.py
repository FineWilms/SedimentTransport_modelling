import datetime
import matplotlib
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from mpl_toolkits.basemap import Basemap

import warnings
# warnings.filterwarnings("ignore")

def get_coordinates(x, y):
	inProj  = Proj("+init=EPSG:25831", preserve_units=True)
	outProj = Proj("+init=EPSG:4326")

	long, lat= transform(inProj,outProj,x,y)
	return long, lat

fp_to_postproc = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','postprocessed_waterlevel','all_postproc_daily.csv'))
fp_to_locs = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','rawdata','waterlevel'))



df = pd.read_csv(fp_to_postproc, index_col=0)
df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

drop_criteria = df.isnull().sum(axis = 0)
for key in drop_criteria.keys():
	if drop_criteria[key]>1000:
		df.drop([key], axis=1, inplace=True)


files_to_process = list(df)
fnames = ['%s.csv' %fname for fname in files_to_process]
DF = {}
for fname in fnames:
	fp = os.path.join(fp_to_locs,fname)
	df_tmp = pd.read_csv(fp)
	X = df_tmp['X'][0]
	Y = df_tmp['Y'][0]
	lon,lat = get_coordinates(X,Y)
	coordsys = df_tmp['Coordinatenstelsel'][0]
	DF[fname[:-4]] = [lat,lon,coordsys]
	print(DF[fname[:-4]])

lats_wl = []
lons_wl = []
station_names = []
for key in DF.keys():
	lats_wl.append(DF[key][0])
	lons_wl.append(DF[key][1])
	station_names.append(key)

labels_wl = [n[:-8] for n in station_names]
"""******************************************************************************************************************"""
"""sediment locations and labels"""
fp_to_locs_sediment = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','rawdata','spm.csv'))

df_sed = pd.read_csv(fp_to_locs_sediment, index_col=0)
df_loc_only = df_sed[["Naam",'geometry']]

df_loc_only.drop_duplicates(subset="Naam", keep='first', inplace=True)

labels_sed = df_loc_only['Naam'].tolist()
locs = df_loc_only['geometry'].tolist()
lons_sed = []
lats_sed = []
for itm in locs:
	lons_sed.append(np.float(itm.strip().split('POINT')[-1].strip().strip('()').split(' ')[0]))
	lats_sed.append(np.float(itm.strip().split('POINT')[-1].strip().strip('()').split(' ')[1]))

"""******************************************************************************************************************"""

lonmin = np.nanmin(lons_sed) - 5
lonmax = np.nanmax(lons_sed) + 5
latmin = np.nanmin(lats_sed) - 5
latmax = np.nanmax(lats_sed) + 5


fig = plt.figure(figsize=(10, 6))
fig.set_tight_layout(False)

ax0 = fig.add_subplot(111)
colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

m = Basemap(resolution='l',
	llcrnrlon=lonmin,
	llcrnrlat=latmin,
	urcrnrlon=lonmax,
	urcrnrlat=latmax,ax=ax0)

m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(latmin, latmax, 0.5), labels=[1, 0, 0, 0], fontsize=6,linewidth=0.3, fmt='%3.1f')
meridians = m.drawmeridians(np.arange(lonmin, lonmax, 0.5), labels=[0, 0, 0, 1], fontsize=6,linewidth=0.3,fmt='%3.1f')
m.shadedrelief(ax=ax0)

x, y = m(lons_sed, lats_sed)

for i in range(0,len(x)):
	sc = m.plot(x[i], y[i],'bo',markersize=5, label=labels_sed[i],alpha=0.5)
#
# for label, x, y in zip(labels_sed, x, y):
# 	plt.annotate(
# 		label,
# 		xy=(x, y), xytext=(-30, 30),
# 		textcoords='offset points', ha='right', va='bottom',
# 		bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
# 		arrowprops=dict(facecolor='yellow', shrink=0.5, width=0.5))

x, y = m(lons_wl, lats_wl)

for i in range(0,len(x)):
	sc = m.plot(x[i], y[i],'ro',markersize=5, label=labels_wl[i], alpha=0.5)

for label, x, y in zip(labels_wl, x, y):
	plt.annotate(
		label,
		xy=(x, y), xytext=(-30, 30),
		textcoords='offset points', ha='right', va='bottom',
		bbox=dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
		arrowprops=dict(facecolor='red', shrink=0.1, width=0.5))




plt.show()






plt.show()
# plt.legend()
plt.savefig('station_locations.png')



