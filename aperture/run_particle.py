#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import h5py
from TMS import TMS
tms = TMS(path='./parameter',GroupNum=23)
tms.Par['Axis'] = 0
tms.LoadPPos()
HaloMostBound = []
HaloMostBound.append(tms.Par['MostBoundX'])
HaloMostBound.append(tms.Par['MostBoundY'])
HaloMostBound.append(tms.Par['MostBoundZ'])
HaloMostBound = np.array(HaloMostBound)
distance = tms.pos - HaloMostBound
tms.pos[distance > 500.] = tms.pos[distance > 500.] - 1000.
tms.pos[distance < -500.] = tms.pos[distance < -500.] + 1000.

GridNum = 512
Ngrid = [GridNum, GridNum, GridNum]
Ngrid[tms.Par['Axis']] = 1
datag = tms.ParticleGridingNGP(Ngrid=Ngrid, R=1.3, L=15)
datag = datag.reshape(GridNum, GridNum)
H = 1.3 * 2 / GridNum
Dindex = 0.15 / H
print Dindex
print 'all mass:', datag.sum() / tms.h
#========================================
#sigma = [0.001,0.002,0.003,0.004,0.005]
sigma = [0.001]
# MassLimitArr=np.arange(46)*10**12+5*10**12
MassLimitArr = [5*10**13]  # unit is M_odot

# f=h5py.File('./output/SubNumber_group0.hdf5',mode='w')
for i in sigma:
    result = np.zeros(shape=[2], dtype=np.float32)
    pdata = tms.PeakFinder(datag, sigma=0.001, R=1.3, N=GridNum, Aperture=0.15)
    pdata[:, 2] /= tms.h
    pdata = pdata[pdata[:, 2] > MassLimitArr[0]]
    Pnum = len(pdata)
    result[0] = MassLimitArr[0]
    result[1] = float(Pnum)
    print 'sigma:', i
    print result
