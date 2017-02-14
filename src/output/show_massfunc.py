#!/usr/bin/env python
# coding=utf-8
path='./massfunc_group0.npy'
import numpy as np
import matplotlib.pyplot as plt
data=np.load(path)
point=data[-3:,:]
print point
order=np.argsort(data[:,1])
data=data[order]
plt.plot(data[:,0],data[:,1],'b-')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'$<\mathrm{R}\ [\mathrm{Mpc}/h]$')
plt.ylabel(r'$\mathrm{Mass}\ [\mathrm{M_{\odot}}/h]$')
plt.vlines(x=point[0,0],ymin=data[:,1].min()*0.9,ymax=point[0,1],colors='r',label=r'$R_{200}$')
plt.vlines(x=point[2,0],ymin=data[:,1].min()*0.9,ymax=point[2,1],colors='k',label=r'$R_{\mathrm{half}}$')
plt.vlines(x=point[1,0],ymin=data[:,1].min()*0.9,ymax=point[1,1],colors='g',label=r'$R_{\mathrm{150kpc}}$')
plt.xlim([data[:,0].min()*0.9,data[:,0].max()*1.1])
plt.ylim([data[:,1].min()*0.9,data[:,1].max()*1.1])
plt.legend(loc='upper left')
#plt.show()
plt.savefig('massfunc_group0.eps')
