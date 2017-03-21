#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS
tms=TMS(path='./parameter')
tms.LoadPPos()
tms.Par['Axis']=1
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
H=1.3*2/GridNum
Dindex=0.15/H
print Dindex

pdata=tms.PeakFinder2(datag,sigma=0.001,R=1.3,N=GridNum,Aperture=0.15,MassLimit=5*10**13)
pdata[:,2]/=tms.h
pdata[:,2]-=tms.MeanCritMass(R=0.15,L=15.0)
pdata = pdata[pdata[:, 2] > 5*10**13]
print pdata
#exit()
#tms.PeakFinder(datag,sigma=0.002)
#tms.PeakFinder(datag,sigma=0.003)
print pdata.shape
#fig, (ax0, ax1) = plt.subplots(ncols=2)
fig, ax0 = plt.subplots(ncols=1)
ax0.imshow(datag.T)
#ax1.imshow(datag.T)
for i in range(len(pdata)):
    ax0.add_artist(plt.Circle((pdata[i,0], pdata[i,1]), Dindex, color='k', fill=False))
#   ax1.add_artist(plt.Circle((pind[i,0], pind[i,1]), Dindex, color='k', fill=False))

plt.show()
#plt.savefig('show_apertrue.eps')
np.save('./Test/datag.npy',datag)
np.save('./Test/pdata.npy',pdata)
