# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:56:05 2022

@author: blandrieu
"""

ECG_samples_1=[]

#### High BPM

RigsHigh1 = {'name'             : 'Rigs_H_1',
            'name_user'         : '2XrQn3_2',
              'end_user'        : '2XrQN3' ,
              'from_time'       : "2022-06-16 09:00:00",
              'to_time'         : "2022-06-16 11:00:00",
              'time_zone'       : 'UTC'}
RigsHigh2 = {'name'             : 'Rigs_H_2',
            'name_user'         : '2XrQn3_2',
              'end_user'        : '2XrQN3' ,
              'from_time'       : "2022-06-14 12:30:00",
              'to_time'         : "2022-06-14 13:30:00",
              'time_zone'       : 'UTC'}

patients_BPMH = [RigsHigh1,RigsHigh2 ]


#### middle BPM
Fli  = {'name'            : 'Keesensev2Tests_RoFli',
              'name_user'       : 'Fli',
              'end_user'        : '26UTVi' ,
              'from_time'       : "2022-09-13 14:47:30",
              'to_time'         : "2022-09-13 15:54:30" ,
              'offset_id'       : '1',
              'date_tag'        : '22091300',
              'seq_seconds'     : [61, 600, 30, 600, 30, 600, 90, 600, 60, 600, 90, 600,80],
              'time_zone'       : 'CEST'}


Fra = {'name'            : 'Keesensev2Tests_RoFra',
              'name_user'         : 'Fra',
              'end_user'        : '47bGiF' ,
              'from_time'       : "2022-09-09 10:55:30",
              'to_time'         : "2022-09-09 12:01:55" ,
              'offset_id'       : '1',
              'date_tag'        : '22090900',
              'seq_seconds'     : [1, 600, 30, 600, 55, 600, 88, 600, 60, 600, 90, 600,2],
              'time_zone'       : 'CEST'
              }
patients_BPMM = [Fli, Fra ]


#### Low BPM

Keesensev2Tests_Ro  = {'name'            : 'Keesensev2Tests_Ro',
              'name_user'       : '5hHc6X',
              'end_user'        : '5hHc6X' ,
              'from_time'       : "2022-09-16 13:12:00",
              'to_time'         : "2022-09-16 14:19:00" ,
              'offset_id'       : '1',
              'date_tag'        : '22091600',
              'seq_seconds'     :[61, 600, 30, 600, 30, 600, 90, 600, 60, 600, 30, 600,60],
              'time_zone'       : 'CEST'}

patients_BPML = [Keesensev2Tests_Ro ]


#### patients with Tshirt too big

Blandine_nuit1  = {'name'            : 'Blandine_nuit1',
              'name_user'         : 'Blandine ',
              'end_user'        : '5dqvVy' ,
              'from_time'       : "2022-09-22 00:30:00",
              'to_time'         : "2022-09-22 02:30:00" ,
              'time_zone'       : 'CEST'
              }
Blandine_nuit2  = {'name'            : 'Blandine_nuit2',
              'name_user'         : 'Blandine ',
              'end_user'        : '5dqvVy' ,
              'from_time'       : "2022-09-22 04:30:00",
              'to_time'         : "2022-09-22 06:30:00" ,
              'time_zone'       : 'CEST'
              }

Michel = {    'name'            : 'Michel',
              'name_user'       : 'Michel',
              'end_user'        : '26BFU1' ,
              'from_time'       : "2022-09-19 01:00:00",
              'to_time'         : "2022-09-19 03:00:00" ,
              'time_zone'       : 'CEST'}
Michel2 = {    'name'            : 'Michel',
              'name_user'       : 'Michel',
              'end_user'        : '26BFU1' ,
              'from_time'       : "2022-09-18 21:00:00",
              'to_time'         : "2022-09-18 23:00:00" ,
              'time_zone'       : 'CEST'}


Alexandra = {    'name'            : 'Alexandra',
              'name_user'       : 'Alexandra',
              'end_user'        : '5yh9V2' ,
              'from_time'       : "2022-09-20 23:00:00",
              'to_time'         : "2022-09-21 02:00:00" ,
              'time_zone'       : 'CEST'}
patients_continuity = [Blandine_nuit1, Blandine_nuit2 , Michel, Michel2, Alexandra]