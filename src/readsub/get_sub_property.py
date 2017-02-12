#!/usr/bin/env python
# coding=utf-8
import numpy as np
from read_subgroup import ReadSub
data = np.load('/home/maotx/mycode/gadget/src/read_group/data/MostBoundId.npy')
dt = np.dtype([('Rank', np.int32, 1),
               ('Sx', np.float32, 1),
               ('Sy', np.float32, 1),
               ('Sz', np.float32, 1),
               ('Len', np.int32, 1),
               ('MostBoundId', np.uint64, 1),
               ('SubFileNum', np.int32, 1),
               ('SubParentHalo', np.int32, 1),
               ('SubLen', np.int32, 1),
               ('SubOffset', np.int32, 1),
               ('Halo_M_Crit200', np.float32, 1),
               ('Halo_R_Crit200', np.float32, 1),
               ('SubPos_x', np.float32, 1),
               ('SubPos_y', np.float32, 1),
               ('SubPos_z', np.float32, 1),
               ('Subhalfmass', np.float32, 1),
               ])

result=np.empty([len(data)],dtype=dt)
keys=[i[0] for i in data.dtype.descr]
for i in keys:
    result[i][:]=data[i][:]

RS=ReadSub(0)
def findGroupNum(MostBoundId=0,Num=0):
    for filenum in np.arange(512):
        RS.__init__(filenum)
        data=RS.LoadSub()
        if MostBoundId in data['SubMostBoundID'].tolist():
            index=data['SubMostBoundID'].tolist().index(MostBoundId)
            result[Num]['SubFileNum']=filenum
            result[Num]['SubParentHalo']=data['SubParentHalo'][index]
            result[Num]['SubLen']=data['SubLen'][index]
            result[Num]['SubOffset']=data['SubOffset'][index]
            result[Num]['Halo_M_Crit200']=data['Halo_M_Crit200'][data['SubParentHalo'][index]]
            result[Num]['Halo_R_Crit200']=data['Halo_R_Crit200'][data['SubParentHalo'][index]]
            result[Num]['SubPos_x']=data['SubPos'][index*3+0]
            result[Num]['SubPos_y']=data['SubPos'][index*3+1]
            result[Num]['SubPos_z']=data['SubPos'][index*3+2]
            result[Num]['Subhalfmass']=data['Subhalfmass'][index]
            break

print result.dtype
for i in np.arange(50):
    MostBoundId=result[i]['MostBoundId']
    findGroupNum(MostBoundId=MostBoundId,Num=i)
    print result[i]
np.save('./SubProperty.npy',result)
