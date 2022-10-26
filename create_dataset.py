import os
import sys
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
from pylife.useful import unwrap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %% Request data
path_api_ids        = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'
path_save_image     = 'image/'
path_save_data      = 'data/'

end_user   	= '3JLqh6'
from_time   = "2022-10-21 11:00:00"
to_time     = "2022-10-21 11:05:00"
time_zone   = 'CEST'

params = {'path_ids': path_api_ids, 'api_version': 2,
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
print('filtering...')
al.filt()

# %% Create dataset
# Init Dataframe
df = pd.DataFrame(columns=['seg_id', 'user_id', 'start_at', 'stop_at'])

# Figure parameters
alpha       = 0.1
facecolor   = 'blue'
fontsize    = 16

# Signals
fs      = al.ecg.fs_
length  = 500*fs # sec
ecgfs   = al.ecg.sig_filt_
times   = al.ecg.sig_

window          = 15*fs # sec
overlap         = 10*fs # sec
window_center   = 5*fs # sec
count           = 1

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
        df.loc[count, 'seg_id']      = count
        df.loc[count, 'start_at']    = tseg[imin_center]
        df.loc[count, 'stop_at']     = tseg[imiax_center]
        df.loc[count, 'user_id']     = end_user
        
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
        plt.savefig(path_save_image + str(count)+'.jpg')
        plt.close('all')
        count+=1

# Dataset
df.to_excel(path_save_data + 'data.xls', index=False)

