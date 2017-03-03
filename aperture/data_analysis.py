import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS
import os
sigma=0.001
GroupNum=1
axis=0
tms = TMS(path='./parameter',GroupNum=GroupNum)
Dir='/datascope/indra4/Cluster/result/S%.3f/'%sigma
ProjectMass=np.load(Dir+'ProjectedMass.npy')
halocat=np.load('/datascope/indra4/Cluster/halocat/halocat_selected.npy')
#================================================================================
#pdata=np.load(Dir+'Axis%d_'%axis+tms.LoadGroupCat(GroupNum)[:-4]+'.npy')
#Nsub=len(pdata)
#print Nsub
#exit()
#================================================================================
dt=np.dtype([('GroupNum',np.int32,1),
        ('Axis',np.int32,1),
        ('ProjectedMass',np.float64,1),
        ('Halo_M_Crit200',np.float64,1),
        ('Halo_R_Crit200',np.float64,1),
        ('Subhalfmass',np.float64,1),
        ('NumSub',np.int32,1),
        ])
result=np.empty(shape=[len(ProjectMass)],dtype=dt)
result['GroupNum']=ProjectMass['GroupNum']
result['Axis']=ProjectMass['Axis']
result['ProjectedMass']=ProjectMass['ProjectedMass']

NumSub=np.empty(shape=[len(ProjectMass)],dtype=np.int32)
M200=np.empty(shape=[len(ProjectMass)],dtype=np.float64)
R200=np.empty(shape=[len(ProjectMass)],dtype=np.float64)
Mhalf=np.empty(shape=[len(ProjectMass)],dtype=np.float64)
for i in np.arange(len(ProjectMass)):
    axis=ProjectMass[i]['Axis']
    GroupNum=ProjectMass[i]['GroupNum']
    pdata=np.load(Dir+'Axis%d_'%axis+tms.LoadGroupCat(GroupNum)[:-4]+'.npy')
    NumSub[i]=len(pdata)
    M200[i]=halocat[ProjectMass[i]['GroupNum']]['Halo_M_Crit200']
    R200[i]=halocat[ProjectMass[i]['GroupNum']]['Halo_R_Crit200']
    Mhalf[i]=halocat[ProjectMass[i]['GroupNum']]['Subhalfmass']
result["Halo_M_Crit200"]=M200
result['Halo_R_Crit200']=R200
result['Subhalfmass']=Mhalf
result['NumSub']=NumSub
print result
print result.dtype
#np.save('/datascope/indra4/Cluster/result/result.npy',result)
np.save('./result.npy',result)
