
#%% librairies

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import sys
path_root='C:/Users/blandrieu/OneDrive - Passage innovation/Documents/GitHub/'
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
from pylife.useful import unwrap


path_root='C:/Users/blandrieu/OneDrive - Passage innovation/Documents/Labellisation/labelife/'
sys.path.append(path_root)
from constant import PATH_DATA, PATH_IMAGE
from data import patients_continuity, patients_BPMH, patients_BPML

os.chdir(path_root)
print(os.getcwd())

# %% Request data
path_api_ids        = 'C:/Users/blandrieu/OneDrive - Passage innovation/Documents/GitCode/api' #'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'


testeurs = patients_BPML
print([t['name_user'] for t in testeurs])

i=0
name            = testeurs[i]['name_user']
name_user       = testeurs[i]['name_user']
end_user        = testeurs[i]['end_user'] 
from_time       = testeurs[i]['from_time']
to_time         = testeurs[i]['to_time']
time_zone       = testeurs[i]['time_zone'] #
print(name)


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
#count           = 1

#load previous excel and get count of last recorded point
df_old = pd.read_excel(PATH_DATA + 'data.xls')
count = df_old.loc[df_old.shape[0]-1,'seg_id'] +1


for i, ecgf in enumerate(ecgfs):
    times   = al.ecg.times_[i]
    ecg     = al.ecg.sig_[i]
    
    for iw in range(0, len(ecgf[:length]), window-overlap):  
        
        # Main window
        imin        = iw 
        imax        = imin + window 
        # print(imin/fs, imax/fs)
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
        date_savefriendly = str(tseg[imin_center])[:13]+'_'+str(tseg[imin_center])[14:16]+'_'+str(tseg[imin_center])[17:19]
        plt.savefig(PATH_IMAGE +str(count)+'_'+end_user+'_'+ date_savefriendly+'.jpg')
        plt.show()
        plt.close('all')
        count+=1

# Dataset
#concat
dfnew = pd.concat([df_old, df])

dfnew.to_excel(PATH_DATA + 'data.xls', index=False)

