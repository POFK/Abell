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
GridNum = 256
Ngrid = [GridNum, GridNum, GridNum]
Ngrid[tms.Par['Axis']] = 1
datag = tms.ParticleGridingNGP(Ngrid=Ngrid, R=1.3, L=15)
datag = datag.reshape(GridNum, GridNum)
H = 1.3 * 2 / GridNum
Dindex = 0.15 / H
print Dindex
#========================================
#sigma = [0.001,0.002,0.003,0.004,0.005]
sigma = [0.005]
MassLimitArr=np.arange(46)*10**12+5*10**12

f=h5py.File('./output/SubNumber_group0.hdf5',mode='w')
for i in sigma:
    result=np.zeros(shape=[len(MassLimitArr),2],dtype=np.float32)
    pdata = tms.PeakFinder(datag, sigma=i, R=1.3, N=GridNum, Aperture=0.15)
    for j in np.arange(len(MassLimitArr)):
        pdata = pdata[pdata[:, 2] > MassLimitArr[j]]
        Pnum=len(pdata)
        result[j,0]=MassLimitArr[j]
        result[j,1]=float(Pnum)
    print 'sigma:',i
    print result
    f.create_dataset(name='Axis%d/sigma%.3f'%(tms.Par['Axis'],i),
                     dtype=np.float32,
                     data=result)
f.close()



