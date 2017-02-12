#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS
tms=TMS(path='./parameter')
tms.LoadPPos()
tms.Par['Axis']=0
datag=tms.ParticleGridingNGP(Ngrid=[512,512,1],R=1.3,L=15)
datag=datag.reshape(512,512)

H=1.3*2/512
Dindex=0.25/H
print Dindex

#for sigma in np.linspace(0.001,0.15,20):
#for sigma in np.linspace(0.001,0.15,20):
#    tms.PeakFinder(datag,sigma=sigma)
tms.PeakFinder(datag,sigma=0.001)
tms.PeakFinder(datag,sigma=0.002)
tms.PeakFinder(datag,sigma=0.003)
pind=np.array(list(set([tuple(i) for i in tms.peakind])))
print 'number of peaks:', len(pind)
pdata=np.empty([len(pind),3],dtype=np.float32)
pdata[:,:2]=pind[:]
for i in np.arange(len(pind)):
    pdata[i,2]=datag[pind[i,0]-int(Dindex):pind[i,0]+int(Dindex+1),pind[i,1]-int(Dindex):pind[i,1]+int(Dindex+1)].sum()

pdata=pdata[pdata[:,2]>tms.Par['MassLimit']]
print pdata.shape
pdata=pdata[np.argsort(pdata[:,2])[::-1]]

loop=0
for i in np.arange(1,len(pdata)):
    Darr=pdata[i-loop]-pdata[:i-loop]
    Dbool=(Darr[:,0]**2+Darr[:,1]**2)<(Dindex**2)
    if Dbool.sum()>0:
        pdata=np.delete(pdata,i-loop,0)
        loop=loop+1

print pdata.shape
#fig, (ax0, ax1) = plt.subplots(ncols=2)
fig, ax0 = plt.subplots(ncols=1)
ax0.imshow(datag.T)
#ax1.imshow(datag.T)
for i in range(len(pdata)):
    ax0.add_artist(plt.Circle((pdata[i,0], pdata[i,1]), Dindex, color='k', fill=False))
#   ax1.add_artist(plt.Circle((pind[i,0], pind[i,1]), Dindex, color='k', fill=False))

plt.show()
