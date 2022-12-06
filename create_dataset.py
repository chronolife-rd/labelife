
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
from data import patients_continuity, patients_BPMH, patients_BPML, patients_BPMM

os.chdir(path_root)
print(os.getcwd())


# %% Request data
path_api_ids        = 'C:/Users/blandrieu/OneDrive - Passage innovation/Documents/GitCode/api' #'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'


testeurs = patients_BPMH #patients_BPMM #patients_BPML #patients_continuity
print([t['name_user'] for t in testeurs])

for i in [0,1, 2]:
    name            = testeurs[i]['name_user']
    name_user       = testeurs[i]['name_user']
    end_user        = testeurs[i]['end_user'] 
    from_time       = testeurs[i]['from_time']
    to_time         = testeurs[i]['to_time']
    time_zone       = testeurs[i]['time_zone'] #
    print(name,end_user )
    
    
    params = {'path_ids': path_api_ids, 'api_version': 2,
              'end_user': end_user, 
              'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
              'device_model': 'tshirt',
              'flag_acc': False, 'flag_breath': False, 
              'flag_ecg': True, 'flag_temp': False, 'flag_temp_valid': False,
              'flag_imp': True,  'activity_types': '',
              }
    
    al = Apilife(params)
    print('Getting...')
    al.get()
    print('Parsing...')
    al.parse()
    print('filtering...')
    al.filt()
    
    # % Create dataset
    # Init Dataframe
    df = pd.DataFrame(columns=['seg_id', 'user_id', 'start_at', 'stop_at'])
    
    # Figure parameters
    alpha       = 0.1
    facecolor   = 'blue'
    fontsize    = 16
    
    # Signals
    fs        = al.ecg.fs_
    length    = 500*fs # sec
    ecgfs     = al.ecg.sig_filt_
    times     = al.ecg.sig_
    imp_times = pd.DataFrame({'imp' : unwrap(al.imp_1.times_)})
    window          = 15*fs # sec
    overlap         = 10*fs # sec
    window_center   = 5*fs # sec
    count           = 1
    
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
            
            if imp_times.shape[0]>0:
                imp_seg     = imp_times.loc[(imp_times['imp']>times[imin])
                                            &(imp_times['imp']<times[min(imax, len(times)-1)])]
            else:
                imp_seg = imp_times
            
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
            if imp_seg.shape[0]>0:
                plt.axvline(imp_seg['imp'][0], label = 'Impedance', c='r', linestyle = '--')
            plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
            plt.xticks([])
            plt.legend(fontsize=fontsize)
            plt.subplot(212)
            plt.plot(tseg, ecgf_seg, label='Filtered')        
            if imp_seg.shape[0]>0:
                plt.axvline(imp_seg['imp'][0], label = 'Impedance', c='r', linestyle = '--')
            plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
            plt.xticks([])
            plt.legend(fontsize=fontsize)
            # date_savefriendly = str(tseg[imin_center])[:13]+'_'+str(tseg[imin_center])[14:16]+'_'+str(tseg[imin_center])[17:19]
            plt.title(end_user+' '+str(tseg[imin_center])[:19])
            plt.savefig(PATH_IMAGE +str(count)+'.jpg')
            plt.show()
            plt.close('all')
    
            
            count+=1
    
    # Dataset
    #concat
    dfnew = pd.concat([df_old, df])
    # df.to_excel(PATH_DATA + 'data.xls', index=False)
    dfnew.to_excel(PATH_DATA + 'data.xls', index=False)
    
    
#%% getting data from integrity data september

pathbase     = "C:/Users/blandrieu/OneDrive - Passage innovation/Documents"
df_integ     = pd.read_pickle(pathbase+"/ECG_peaks/pickle_intergity_data/all_users_nkcustom.pickle")
path_api_ids = 'C:/Users/blandrieu/OneDrive - Passage innovation/Documents/GitCode/api' #'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'


#load previous excel and get count of last recorded point
df_old = pd.read_excel(PATH_DATA + 'data.xls')
count = df_old.loc[df_old.shape[0]-1,'seg_id'] +1


 
df_integ['user'].unique()
df_integ.columns
user_ID = ['3ooPJw', '7k6Hs3', '5T3YW2', '3sBZGq', '3ovYko']
for u, user in enumerate( [ 'Fernando', 'Adriana', 'Ninon', 'Salma', 'Viviane']): # the others are already in the data set
    data_u = df_integ.loc[df_integ['user']==user].copy()
    data_u.index =[x for x in range(data_u.shape[0])]
    

    
    ### getting the impedance
    name            = user
    name_user       = user
    end_user        = user_ID[u]
    from_time       = str(data_u.loc[0,'time_start'])
    to_time         = str(data_u.loc[data_u.shape[0]-1,'time_stop'])
    time_zone       = 'CEST' #
    print(name,end_user )
    
    
    params = {'path_ids': path_api_ids, 'api_version': 2,
              'end_user': end_user, 
              'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
              'device_model': 'tshirt',
              'flag_acc': False, 'flag_breath': False, 
              'flag_ecg': False, 'flag_temp': False, 'flag_temp_valid': False,
              'flag_imp': True,  'activity_types': '',
              }
    
    al = Apilife(params)
    print('Getting...')
    al.get()
    print('Parsing...')
    al.parse()
    print('filtering...')
    al.filt()

    df_old = pd.read_excel(PATH_DATA + 'data.xls') 
    # % Create dataset
    # Init Dataframe
    df = pd.DataFrame(columns=['seg_id', 'user_id', 'start_at', 'stop_at'])
    
    for min in [2,7,12,17,22,27,32,37,42,47,52,57]: # 12 min per subject, in the different phases, in order to explore more shapes of ECG

        # Figure parameters
        alpha       = 0.1
        facecolor   = 'blue'
        fontsize    = 16
         
        # Signals
        fs        = 200
        length    = 500*fs # sec
        ecg     = data_u.loc[min,'ECG_raw']
        ecgf     = data_u.loc[min,'ECG_filt'] #   al.ecg.sig_filt_
        times     = [  pd.to_datetime(t) for t in data_u.loc[min,'ECG_time'] ] #al.ecg.sig_
        
    
        
        
        imp_times = pd.DataFrame({'imp' : unwrap(al.imp_1.times_)})
        window          = 15*fs # sec
        overlap         = 10*fs # sec
        window_center   = 5*fs # sec
        #count           = 1

        
        
        
        for iw in range(0, len(ecgf[:length]), window-overlap):  
            # Main window
            imin        = iw 
            imax        = imin + window 
            
            if imp_times.shape[0]>0:
                maxlen = len(times)-1             
                imp_seg     = imp_times.loc[(imp_times['imp']>times[imin])
                                            &(imp_times['imp']<times[np.min([imax, len(times)-1])])]
            else:
                imp_seg = imp_times
            
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
            if imp_seg.shape[0]>0:
                plt.axvline(imp_seg['imp'].values[0], label = 'Impedance', c='r', linestyle = '--')                
                
            plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
            plt.xticks([])
            plt.legend(fontsize=fontsize)
            plt.subplot(212)
            plt.plot(tseg, ecgf_seg, label='Filtered')        
            if imp_seg.shape[0]>0:
                plt.axvline(imp_seg['imp'].values[0], label = 'Impedance', c='r', linestyle = '--')
            plt.axvspan(tseg[imin_center], tseg[imiax_center], facecolor=facecolor, alpha=alpha)
            plt.xticks([])
            plt.legend(fontsize=fontsize)
            # date_savefriendly = str(tseg[imin_center])[:13]+'_'+str(tseg[imin_center])[14:16]+'_'+str(tseg[imin_center])[17:19]
            plt.title(end_user+' '+str(tseg[imin_center])[:19])
            plt.savefig(PATH_IMAGE +str(count)+'.jpg')
            plt.show()
            plt.close('all')
    
            
            count+=1
    
        # Dataset
        #concat
        dfnew = pd.concat([df_old, df])
        # df.to_excel(PATH_DATA + 'data.xls', index=False)
        dfnew.to_excel(PATH_DATA + 'data.xls', index=False)                 

#%%


df_old.columns
for user in dfnew['user_id'].unique():
    usdf = dfnew.loc[dfnew['user_id']== user ]
    print('user', user, 'start', usdf['seg_id'].values[0], 'stop', usdf['seg_id'].values[-1])
    

