#!/usr/bin/env python
# coding=utf-8

#!/usr/bin/env python
# coding=utf-8
from TMS import TMS
import sys
import numpy as np
import h5py
#================================================================================
tms = TMS(path='./parameter')
#tms.Par['Axis'] = 0 # z-axis
#SelectedSubNum=2
L=15.0 # Mpc
Aperture=0.15*tms.h #Mpc/h
tms.SubPro=tms.Par['SubProperty']
#print tms.SubPro.dtype
#print tms.SubPro
#==================== load data and NFW fit =====================================
def f(def_Axis=0,SelectedSubNum=0):
    tms.Par['Axis'] = def_Axis  # z-axis
    # load subhalos:
    tms.LoadSubCat()
    HaloMostBound=[]
    HaloMostBound.append(tms.Par['MostBoundX'])
    HaloMostBound.append(tms.Par['MostBoundY'])
    HaloMostBound.append(tms.Par['MostBoundZ'])
    HaloMostBound=np.array(HaloMostBound)
    distance=tms.subcat['SubPos']-HaloMostBound
    tms.subcat['SubPos'][distance>250.]=tms.subcat['SubPos'][distance>250.]-500.
    tms.subcat['SubPos'][distance<-250.]=tms.subcat['SubPos'][distance<-250.]+500.
    subcat = tms.SubSelect(R=L, L=L, range=0)
    subcat = subcat[subcat['SubLen'] >= 1000]
    sort = np.argsort(subcat['SubLen'])[::-1]
    subcat = subcat[sort]
    #print subcat.dtype
    #print subcat[SelectedSubNum]
    #****************************************
    # load particles:
    tms.LoadPPos()
    HaloMostBound=subcat[SelectedSubNum]['SubPos']
    distance=tms.pos-HaloMostBound
    tms.pos[distance>250.]=tms.pos[distance>250.]-500.
    tms.pos[distance<-250.]=tms.pos[distance<-250.]+500.
    print tms.pos.shape
    #================================================================================
    # mass of particles (part 1)
    R_half=subcat[SelectedSubNum]['Subhalfmass']
    R_150kpc=0.15*tms.h
    R200=tms.SubPro['Halo_R_Crit200']
    tms.pos=tms.pos[(np.abs(tms.pos-HaloMostBound)[:,0]<R200)*(np.abs(tms.pos-HaloMostBound)[:,1]<R200)*(np.abs(tms.pos-HaloMostBound)[:,2]<R200)]
    print tms.pos.shape
    print '#'*80
    R=10**np.linspace(-2,np.log10(tms.SubPro['Halo_R_Crit200']),200)
    Mass=[tms.pos[np.sum((tms.pos - HaloMostBound)**2, axis=1) < r**2].shape[0] for r in R]
    Mass=np.array(Mass,dtype=np.float32)
    Mass=np.hstack([Mass,np.array([tms.pos[np.sum((tms.pos - HaloMostBound)**2, axis=1) < R_150kpc**2].shape[0]],dtype=np.float32)])
    Mass=np.hstack([Mass,np.array([tms.pos[np.sum((tms.pos - HaloMostBound)**2, axis=1) < R_half**2].shape[0]],dtype=np.float32)])
    Mass*=tms.ParticleM
    R=np.hstack([R,np.array([R_150kpc,R_half])])
    print Mass
    print R.shape
    print Mass.shape
    return np.c_[R,Mass]
data=f(def_Axis=0,SelectedSubNum=0)
#order=np.argsort(data[:,1])
#data=data[order]
np.save('./output/massfunc_group0.npy',data)
