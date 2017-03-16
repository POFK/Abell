import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS
import os
sigma=0.001
GroupNum=1
axis=0
tms = TMS(path='./parameter',GroupNum=GroupNum)

ListDir=os.listdir('/datascope/indra4/Cluster/result/')
ListDir=[i for i in ListDir if os.path.isdir('/datascope/indra4/Cluster/result/'+i)]
print len(ListDir)
print ListDir
filenum=10
print ListDir[filenum]
Dir='/datascope/indra4/Cluster/result/'+ListDir[filenum]+'/'
ProjectMass=np.load(Dir+'ProjectedMass.npy')
halocat=np.load('/datascope/indra4/Cluster/halocat/halocat_selected.npy')
rank=np.argsort(halocat['Halo_M_Crit200'])[::-1]
halocat=halocat[rank]
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
result['ProjectedMass']=ProjectMass['ProjectedMass']-tms.MeanCritMass(R=1.3,L=15.0)

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
np.save('/datascope/indra4/Cluster/result/'+ListDir[filenum]+'.npy',result)
#np.save('./result/'+ListDir[filenum]+'.npy',result)
np.save('./result/'+ListDir[filenum]+'.npy',result)
