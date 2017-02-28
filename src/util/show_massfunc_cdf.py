#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
path='../output/massfunc_group0_axis_0.npy'
def getName(GroupNum,axis):
    return '../output/massfunc_group%d_axis_%d.npy'%(GroupNum,axis)
def getNFWName(GroupNum,axis):
    return '../output/massfuncNFW_group%d_axis_%d.npy'%(GroupNum,axis)
def load(PATH):
    data=np.load(PATH)
    return data
def loaddata(GroupNum):
    data=np.zeros_like(load(getName(GroupNum,0)))
    data+=load(getName(GroupNum,0))
    data+=load(getName(GroupNum,1))
    data+=load(getName(GroupNum,2))
    return data/3.
def loadNFW(GroupNum):
    data=np.zeros_like(load(getName(GroupNum,0)))
    data+=load(getNFWName(GroupNum,0))
    data+=load(getNFWName(GroupNum,1))
    data+=load(getNFWName(GroupNum,2))
    return data/3.
M200=np.array([2.14*10**15,2.36*10**15,1.23*10**15,1.09*10**15,5.06*10**14,6.30*10**14])
M200/=0.73
g0=loaddata(0)
g1=loaddata(1)
g2=loaddata(2)
g5=loaddata(5)
g17=loaddata(17)
g27=loaddata(27)
gN0=loadNFW(0)
gN1=loadNFW(1)
gN2=loadNFW(2)
gN5=loadNFW(5)

len=len(g0[g0[:,0]<(5*10**12)])
#print g0nfw
#data=[g0,g1,g2,g5,g0nfw]
data=[g0,g1,g2,g5,g17,g27]
#dataNFW=[gN0,gN1,gN2,gN5]
label=[0,1,2,5,17,27]
color=['r','g','b','k','m','y']
M200_label=np.array([2.14*10**15,2.36*10**15,1.23*10**15,1.09*10**15,5.06*10**14,6.30*10**14])/0.73
for i in np.arange(6):
    plt.plot(data[i][len:,0]/M200[i],data[i][len:,1],color[i]+'-',label='$%.2G\ h^{-1}\mathrm{M_{\odot}}$'%(M200_label[i]),linewidth=1.5)
    plt.vlines(x=5.*10**13/M200[i],ymin=0.1,ymax=100,colors=color[i],linestyles='dashed')

#   plt.plot(dataNFW[i][len:,0]/M200[i],dataNFW[i][len:,1],color[i]+'--',linewidth=3)
#   plt.plot(data[i][len:,0],data[i][len:,1],color[i]+'-',label='$%.2G\ h^{-1}\mathrm{M_{\odot}}$'%(M200_label[i]),linewidth=1.5)
#   plt.plot(dataNFW[i][len:,0],dataNFW[i][len:,1],color[i]+'--',linewidth=3)
plt.vlines(x=5.*10**13/(3.6*10**15),ymin=0.1,ymax=100,colors='k',linestyles='solid')
plt.scatter(x=5.*10**13/(3.6*10**15),y=3,marker='*',c='red',s=50)
#plt.xlim([10**11,10**14])
plt.xscale('log')
plt.yscale('log')
#plt.xlabel('M [$\mathrm{M_{\odot}}$]')
plt.xlabel('M/M$_{200}$')
plt.ylabel('N')
plt.ylim([0.1,100])
#plt.xlim([5*10**12,10**14])
plt.xlim([2*10**-3,0.1])
#plt.legend(loc='upper right',ncol=1)
plt.legend(loc='lower left',ncol=2)
#plt.show()
plt.savefig('../showresult/massfunc_0227.eps')
#plt.savefig('../showresult/massfunc.eps')
#plt.savefig('../showresult/massfunc_M200.eps')
