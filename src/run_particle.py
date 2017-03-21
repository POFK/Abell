#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import h5py
from TMS import TMS
tms = TMS(path='./parameter')
tms.Par['Axis'] = 2
tms.Par['MassLimit'] = 5e13

tms.LoadPPos()
HaloMostBound=[]
HaloMostBound.append(tms.Par['MostBoundX'])
HaloMostBound.append(tms.Par['MostBoundY'])
HaloMostBound.append(tms.Par['MostBoundZ'])
HaloMostBound=np.array(HaloMostBound)
distance=tms.pos-HaloMostBound
tms.pos[distance>250.]=tms.pos[distance>250.]-500.
tms.pos[distance<-250.]=tms.pos[distance<-250.]+500.

GridNum = 256
Ngrid = [GridNum, GridNum, GridNum]
Ngrid[tms.Par['Axis']] = 1
datag = tms.ParticleGridingNGP(Ngrid=Ngrid, R=1.3, L=15)
datag = datag.reshape(GridNum, GridNum)
H = 1.3 * 2 / GridNum
Dindex = 0.15 / H
print Dindex
print 'all mass:',datag.sum()/tms.h
#========================================
#sigma = [0.001,0.002,0.003,0.004,0.005]
sigma = [0.001]
#MassLimitArr=np.arange(46)*10**12+5*10**12
MassLimitArr=10**np.linspace(11,15,200)  # unit is M_odot

#f=h5py.File('./output/SubNumber_group0.hdf5',mode='w')
for i in sigma:
    result=np.zeros(shape=[len(MassLimitArr),2],dtype=np.float32)
    pdata = tms.PeakFinder(datag, sigma=i, R=1.3, N=GridNum, Aperture=0.15)
    pdata[:,2]/=tms.h
    np.save('./output/massfunc_pdata_group%d_axis_%d.npy'%(tms.Par['GroupNum'],tms.Par['Axis']),pdata)
    for j in np.arange(len(MassLimitArr)):
        pdata = pdata[pdata[:, 2] > MassLimitArr[j]]
        Pnum=len(pdata)
        result[j,0]=MassLimitArr[j]
        result[j,1]=float(Pnum)
    print 'sigma:',i
    print result
#   f.create_dataset(name='Axis%d/sigma%.3f'%(tms.Par['Axis'],i),
#                    dtype=np.float32,
#                    data=result)
    np.save('./output/massfunc_group%d_axis_%d.npy'%(tms.Par['GroupNum'],tms.Par['Axis']),result)
#f.close()



