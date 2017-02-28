#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
path='../output/massfunc_pdata_group0_axis_0.npy'
def getName(GroupNum,axis):
    return '../output/massfunc_pdata_group%d_axis_%d.npy'%(GroupNum,axis)
def load(PATH):
    data=np.load(PATH)[:,2]
    return data
Mrange=10**np.linspace(11,15,50)  # unit is M_odot
def Massfunc(data,Mrange=Mrange):
    dn,_=np.histogram(data,bins=Mrange)
    dm=np.log(Mrange[1:]-Mrange[:-1])
    return dn/dm
def loaddata(GroupNum):
    data1=Massfunc(load(getName(GroupNum,0)))
    data2=Massfunc(load(getName(GroupNum,1)))
    data3=Massfunc(load(getName(GroupNum,2)))
    return (data1+data2+data3)/3.

M=(Mrange[1:]+Mrange[:-1])/2
g0=loaddata(0)
g1=loaddata(1)
g2=loaddata(2)
g5=loaddata(5)
data=[g0,g1,g2,g5]
label=[0,1,2,5]
for i in np.arange(4):
    bool=data[i]!=0
    plt.plot(M[bool],data[i][bool],label='group %d'%label[i])
#plt.xlim([10**11,10**14])
plt.xscale('log')
plt.yscale('log')
plt.xlabel('M [$\mathrm{M_{\odot}}$]')
plt.ylabel('M dn/dM')
plt.legend()
plt.show()
#plt.savefig('../showresult/massfunc.eps')

