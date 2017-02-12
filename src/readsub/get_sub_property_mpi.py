#!/usr/bin/env python
# coding=utf-8
import numpy as np
from mpi4py import MPI
from read_subgroup import ReadSub
import h5py

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

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
MPI_array_num=np.array_split(np.arange(5),size)[rank]
print rank,MPI_array_num
if rank==0:
    with h5py.File('./test.hdf5',mode='a') as f:
        f.create_dataset(name='subP',dtype=dt,data=result)
        f.close()
    print result.dtype

for i in MPI_array_num:
    print rank,i,':'
    MostBoundId=result[i]['MostBoundId']
    findGroupNum(MostBoundId=MostBoundId,Num=i)
    print result[i]

f=h5py.File('./test.hdf5',mode='a')
r_data=f['subP'].[MPI_array_num]
r_data[:]=result[MPI_array_num][:]
f.flush()
 
