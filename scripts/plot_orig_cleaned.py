import pandas as pd
import os
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

fp_to_fig = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','images_compare'))

if not os.path.exists(fp_to_fig):
	os.makedirs(fp_to_fig)

fdir_postproc = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','postprocessed_waterlevel'))
fdir_raw = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','rawdata','waterlevel'))

file_list_raw = os.listdir(fdir_raw)
for fn in file_list_raw[8::]:
	try:
		fp_raw = os.path.join(fdir_raw,fn)
		fn_clean = fn[:-4]+'_postproc_daily.csv'
		fn_fig = fn[:-4]+'_compare.png'
		fp_clean = os.path.join(fdir_postproc, fn_clean)
		df_raw = pd.read_csv(fp_raw)
		cols2keep = ['t', 'Meetwaarde.Waarde_Numeriek']
		cols2drop = [col for col in list(df_raw) if not col in cols2keep]
		df_raw.drop(cols2drop, axis=1, inplace=True)


		df_clean = pd.read_csv(fp_clean)
		df_clean = df_clean.rename(columns={'Unnamed: 0': 't'})

		if not df_clean.empty:
			df_raw.reset_index(inplace=True, drop=True)
			df_raw['t'] = pd.to_datetime(df_raw['t'], format='%Y-%m-%d %H:%M:%S')
			df_raw.set_index('t', inplace=True)

			df_clean.reset_index(inplace=True, drop=True)
			df_clean['t'] = pd.to_datetime(df_clean['t'], format='%Y-%m-%d')
			df_clean.set_index('t', inplace=True)

			fig, axes = plt.subplots(2,1,figsize=(16,8))
			df_raw.plot(marker='.', ax=axes[0], style='-')

			plt.ylabel('water level [cm]')

			df_clean.plot(marker='.', ax=axes[1], style='-')

			plt.ylabel('mean daily water level [cm]')
			plt.savefig(os.path.join(fp_to_fig, fn_fig))
			print('saved org figure')
	except IOError:
		print('No such file')
		continue