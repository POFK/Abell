#!/usr/bin/env python
# coding=utf-8
group=1
axis=2
#path='SubNumber_group%d.hdf5'%group
path='./NFW_SubNumber_group%d.hdf5'%group
import h5py
import matplotlib.pyplot as plt
def loaddata(sigma=0.001,axis=axis,path=path):
    f=h5py.File(path,mode='r')
    data=f['Axis%d/sigma%.3f'%(axis,sigma)][...]
    f.close()
    return data

data=loaddata(sigma=0.001,path=path)
plt.plot(data[:,0],data[:,1],'r-',linewidth=2,label=r'$\sigma=1\mathrm{kpc}$',drawstyle='steps')
data=loaddata(sigma=0.002,path=path)
plt.plot(data[:,0],data[:,1],'g-',linewidth=2,label=r'$\sigma=2\mathrm{kpc}$',drawstyle='steps')
data=loaddata(sigma=0.003,path=path)
plt.plot(data[:,0],data[:,1],'b-',linewidth=2,label=r'$\sigma=3\mathrm{kpc}$',drawstyle='steps')
data=loaddata(sigma=0.004,path=path)
plt.plot(data[:,0],data[:,1],'k-',linewidth=2,label=r'$\sigma=4\mathrm{kpc}$',drawstyle='steps')
data=loaddata(sigma=0.005,path=path)
plt.plot(data[:,0],data[:,1],'m-',linewidth=2,label=r'$\sigma=5\mathrm{kpc}$',drawstyle='steps')
plt.xlim([data[0,0],data[-1,0]])
plt.ylim([0,20])
plt.xlabel(r'Mass $\ [h^{-1}\mathrm{M_{\odot}}]$')
plt.ylabel(r'Number')
plt.legend()
plt.show()
#plt.savefig('compare_particle_group%d_axis%d.eps'%(group,axis))
#plt.savefig('compare_subhaloNFW_group%d_axis%d.eps'%(group,axis))
