# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'
# Path to API ids file
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'

import os
import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
from pylife.useful import unwrap
import matplotlib.pyplot as plt
from report.excel import excel_report
import numpy as np
import pandas as pd

# %%

# Folder where results will be saved
results_folder = os.getcwd()

end_user   	= '3g5Vbz' #3g5Vbz, 3JLqh6
from_time   = "2022-10-25 19:30:00"
to_time     = "2022-10-25 20:15:00"
time_zone   = 'CEST'

entity          = 'test'     # Medbase: 5qfYth, Skinup: 5YXjZB, Rowan: 4CDHyt
device          = ''
project         = ''

params = {'path_ids': path_ids, 'api_version': 2,
          'end_user': end_user, 
          'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
          'device_model': 'tshirt',
          'flag_acc': True, 'flag_breath': True, 
          'flag_ecg': True, 'flag_temp': True, 'flag_temp_valid': False,
          'flag_imp': False,  'activity_types': '',
          }

al = Apilife(params)
print('Getting...')
al.get()
print('Parsing...')
al.parse()

# plt.close('all')
# al.show()

print(al.fw_versions_)

# %%
print('filtering...')
al.filt()
# print('cleaning...')
# al.clean()
# print('analysing...')
# al.analyze()

# %% Generate xls report 
# path_save = 'C:/Users/MichelClet/Desktop/mcl/python/api'
report = excel_report(al, verbose=1,
                        flag_clean=al.flag_clean_,
                        flag_analyze=al.flag_analyze_,
                        path_save=None)

# Init Dataframe
df = pd.DataFrame(columns=['seg_id', 'user_id', 'start_at', 'stop_at'])

# Figure parameters
path_save_image = 'image/'
path_save_data  = 'data/'
alpha = 0.1
facecolor = 'blue'
fontsize = 16

# Signals
fs      = al.ecg.fs_
length  = 500*fs # sec
ecgfs   = al.ecg.sig_filt_
times   = al.ecg.sig_

window          = 15*fs
overlap         = 10*fs
window_center   = 5*fs
cnt             = 1

for i, ecgf in enumerate(ecgfs):
    times   = al.ecg.times_[i]
    ecg     = al.ecg.sig_[i]
    
    for iw in range(0, len(ecgf[:length]), window-overlap):  
        
        # Main window
        imin        = iw 
        imax        = imin + window 
        print(imin/fs, imax/fs)
        if imax >= len(ecgf[:length]):
            imax = len(ecgf[:length])-1
        ecgf_seg    = ecgf[imin:imax]
        ecg_seg     = ecg[imin:imax]
        tseg        = times[imin:imax]
        
        # Centered window
        imin_center     = int((imax-imin)/3) 
        imiax_center    = imin_center + window_center
        if imiax_center >= len(tseg):
            imiax_center = len(tseg)-1
            
        # Complete Dataframe
        df.loc[cnt, 'seg_id']      = cnt
        df.loc[cnt, 'start_at']    = tseg[imin_center]
        df.loc[cnt, 'stop_at']     = tseg[imiax_center]
        df.loc[cnt, 'user_id']     = end_user
        
        # Figure
        plt.figure(figsize=(15,5))
        plt.subplot(211)
        plt.plot(tseg, ecg_seg, label='Raw')
        plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
        plt.xticks([])
        plt.legend(fontsize=fontsize)
        plt.subplot(212)
        plt.plot(tseg, ecgf_seg, label='Filtered')
        plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
        plt.xticks([])
        plt.legend(fontsize=fontsize)
        plt.savefig(path_save_image + str(cnt)+'.jpg')
        plt.close('all')
        cnt+=1


# %%
df.to_excel(path_save_data + 'data.xls', index=False)

