import datetime
import matplotlib
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pyproj import Proj, transform

import warnings
warnings.filterwarnings("ignore")


fp = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','rawdata','waterlevel'))
fns = os.listdir(fp)


fp_to_fig_daily = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','images_daily'))

if not os.path.exists(fp_to_fig_daily):
	os.makedirs(fp_to_fig_daily)


fp_to_postproc = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','postprocessed_waterlevel'))
if not os.path.exists(fp_to_postproc):
	os.makedirs(fp_to_postproc)
DF = {}
failed_files = []
for f in fns:
	try:
		print(f)
		fig_orig = '%s_orig.png' %f[:-4]
		fn = os.path.join(fp,f)
		df = pd.read_csv(fn)#,index_col=0)

		cols2keep = ['t','Meetwaarde.Waarde_Numeriek','X','Y','Coordinatenstelsel']
		cols2drop = [col for col in list(df) if not col in cols2keep]
		df.drop(cols2drop, axis=1, inplace=True)
		df = df[df['Meetwaarde.Waarde_Numeriek']  < 900]
		if not df.empty:
			df.reset_index(inplace=True, drop=True)
			df['t'] = pd.to_datetime(df['t'], format='%Y-%m-%d %H:%M:%S')
			df_plot = df.copy()

			df_plot.set_index('t', inplace=True)
			df_plot = df_plot[['Meetwaarde.Waarde_Numeriek']]

			fig, axes = plt.subplots(3, 1, figsize=(16, 8))

			df_plot.plot(marker='.',ax = axes[0], style='-')

			plt.ylabel('daily water level [cm]')


			df_wl = df[['Meetwaarde.Waarde_Numeriek','t']]


			for i in range(5):
				print('iteration %i' %i)
				df_wl['delta_t'] = pd.to_timedelta(df_wl['t']).diff(-1).dt.total_seconds()

				df_wl['delta'] = np.abs(df_wl[['Meetwaarde.Waarde_Numeriek']] - df_wl[['Meetwaarde.Waarde_Numeriek']].shift(-1))
				df_wl['delta_t'] = df_wl['delta_t']
				label_delta0 = df_wl.loc[df_wl['delta'] < 1.0].index
				label_delta_time_too_small = df_wl.loc[df_wl['delta_t'] > -201].index
				label_delta0 = [lbl for lbl in label_delta0 if lbl not in label_delta_time_too_small]

				df_wl = df_wl.drop(df_wl.index[label_delta0])

				df_wl.reset_index(inplace=True, drop=True)

				df_wl['delta'] = np.abs(df_wl[['Meetwaarde.Waarde_Numeriek']] - df_wl[['Meetwaarde.Waarde_Numeriek']].shift(-1))
				df_wl['delta_t'] = pd.to_timedelta(df_wl['t']).diff(-1).dt.total_seconds()

				# df_wl.drop_duplicates(subset='t',
				# 					 keep='first', inplace=True)

				label_delta2large_10min = df_wl.loc[df_wl['delta'] > 20].index
				label_delta_time_too_large = df_wl.loc[df_wl['delta_t']<-600].index
				label_delta2large = [lbl for lbl in label_delta2large_10min if lbl not in label_delta_time_too_large]

				df_wl.drop(df_wl.index[label_delta2large], inplace=True)
				df_wl.reset_index(inplace=True, drop=True)

				label_delta2large_60min = df_wl.loc[df_wl['delta'] > 100].index
				label_delta_time_too_large = df_wl.loc[df_wl['delta_t'] < -7200].index
				label_delta2large = [lbl for lbl in label_delta2large_60min if lbl not in label_delta_time_too_large]

				df_wl.drop(df_wl.index[label_delta2large], inplace=True)
				df_wl.reset_index(inplace=True, drop=True)




			df_wl.set_index('t', inplace=True)
			df_wl.drop('delta_t', axis=1, inplace=True)
			df_wl.drop('delta', axis=1, inplace=True)
			fig_orig_cleaned = '%s_cleaned.png' % f[:-4]
			df_wl.plot(marker='.', ax=axes[1], style='-')
			plt.ylabel('cleaned water level [cm]')



			df_wl = df_wl.interpolate('linear', limit=5)
			df_wl = df_wl.resample('D').mean()
			dates = df_wl.index
			start_date = pd.Timestamp(dates.min())
			end_date = pd.Timestamp(dates.max())
			daily = pd.date_range(start_date, end_date, freq='D')


			df_wl = df_wl.reindex(daily, fill_value=np.nan)
			df_wl = df_wl.interpolate('linear',limit=2)

			fig_orig_cleaned_daily = '%s_cleaned_daily.png' % f[:-4]
			df_wl.plot(marker='.', ax=axes[2], style='-')
			plt.ylabel('mean daily water level [cm]')

			plt.savefig(os.path.join(fp_to_fig_daily, fig_orig_cleaned_daily))
			df_wl.rename(columns={'Meetwaarde.Waarde_Numeriek': '%s' %f[:-4]}, inplace=True)

			fn_postproc = os.path.join(fp_to_postproc,'%s_orig_postproc_daily.csv' %f[:-4])
			df_wl.to_csv(fn_postproc)
			keyName =  f[:-4]
			DF[keyName] = df_wl

			plt.close('all')
	except AttributeError as error:
		print('error encountered for %s' %f)
		failed_files.append(f)
		continue

df_all = pd.concat(DF.values(), sort=True, axis=1)
fn_postproc_all = os.path.join(fp_to_postproc,'all_postproc_daily.csv')
df_all.to_csv(fn_postproc_all)

fig_cleaned_daily_all = 'ALL_STATIONS_cleaned_daily.png'
plt.figure(figsize=(20, 8))
df_all.plot(marker='.', ax=plt.gca(), style='-')
plt.ylabel('mean daily water level [cm]')
plt.title(f)
plt.savefig(os.path.join(fp_to_fig_daily, fig_cleaned_daily_all))


err_file=open('err.txt','w')
err_file.writelines(failed_files)
err_file.close()
