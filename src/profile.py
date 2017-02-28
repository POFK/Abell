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
#sub: posx,posy,posz,r_half,rs,delta_c
sub=[[29.63056755065918, 212.3602752685547, 447.57623291015625,1.17453932762146,0.5124983191490173, 5120.2138671875],
     [31.213180541992188, 210.1891632080078, 448.07000732421875,0.3273561894893646,0.2565038502216339, 8411.46484375]]

def f(def_Axis=1,SelectedSubNum=0):
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
    tms.NFW_fit(subcat)
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
    # added:
    def rho(r,rs,delta_c):
        return tms.rho_crit*delta_c*rs/(r*(1.+r/rs)**2)
    def f_NFW(r,SelectedSubNum):
        path=tms.Par['SubPathSave']
        with h5py.File(path,mode='r') as f:
            subcat=f['subcat'][...]
            NFW_par=f['NFW_par'][...]
            f.close()
        rs,delta_c=NFW_par[SelectedSubNum]
        NFW_f=lambda x: np.log(1+x)-x/(1.+x)
        M=4*np.pi*tms.rho_crit*delta_c*rs**3*NFW_f(r/rs)
        return M
    MassNFW=f_NFW(R,SelectedSubNum)
    return np.c_[R,Mass,MassNFW]
data=f(def_Axis=1,SelectedSubNum=1)
#order=np.argsort(data[:,1])
#data=data[order]
np.save('./output/profile_group0_sub1.npy',data)
