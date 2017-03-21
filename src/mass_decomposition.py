#!/usr/bin/env python
# coding=utf-8
'''
Calculating the mass of different parts:
1. mass in 150kpc
2. in 2*R_half
3. in 2*R_200
4. all other particles in 30Mpc
'''
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
    subcat = tms.SubSelect(R=1.3, L=L, range=0)
    subcat = subcat[subcat['SubLen'] >= 100]
    sort = np.argsort(subcat['SubLen'])[::-1]
    subcat = subcat[sort]
#--------------------- test -----------------------------------------------------
#   print HaloMostBound
#   print subcat.dtype
#   print subcat
#   exit()
#--------------------------------------------------------------------------------
    #****************************************
    # load particles:
    tms.LoadPPos()
    HaloMostBound=subcat[SelectedSubNum]['SubPos']
    distance=tms.pos-HaloMostBound
    tms.pos[distance>250.]=tms.pos[distance>250.]-500.
    tms.pos[distance<-250.]=tms.pos[distance<-250.]+500.
    print tms.pos.shape
    tms.pos=tms.pos[(np.abs(tms.pos-HaloMostBound)[:,0]<L*tms.h)*(np.abs(tms.pos-HaloMostBound)[:,1]<L*tms.h)*(np.abs(tms.pos-HaloMostBound)[:,2]<L*tms.h)]
    print tms.pos.shape
    print (tms.pos[:,1].min()-HaloMostBound[1])/tms.h
    print (tms.pos[:,1].max()-HaloMostBound[1])/tms.h
    #================================================================================
    def remove_mean_mass(r=0.,l=0.,mode=1):
        '''input r and l with unit (Mpc)
        output mass with (M_dot/h)
        such as :
            remove_mean_mass(0.15,15.0,2)
            '''
        r=r*tms.h
        l=l*tms.h
        if mode=='sphere':
            return 4./3.*np.pi*r**3.*tms.rho_crit*tms.Omega0
        elif mode=='cylinder':
            return np.pi*r**2.*2.*l*tms.rho_crit*tms.Omega0
        else:
            print '=' * 40 + sys._getframe().f_code.co_name + '=' * 40
            print 'Error!\n' 
    dt = np.dtype([
        ('GroupNum', np.int32, 1),
        ('SubNum', np.int32, 1),
        ('Axis', np.int32, 1),
        ('SubMostBoundID', 'u8', 1), 
        ('SubLen', 'i4', 1), 
        ('SubPos_x', '<f4', 1), 
        ('SubPos_y', '<f4', 1), 
        ('SubPos_z', '<f4', 1), 
        ('Subhalfmass', 'f4', 1),
        ('Projected_mass', np.float32, 1),
        ('PM_Part1', np.float32, 1),
        ('PM_Part2', np.float32, 1),
        ('PM_Part3', np.float32, 1),
        ('PM_Part4', np.float32, 1),
        ('ratio_Part1', np.float32, 1),
        ('ratio_Part2', np.float32, 1),
        ('ratio_Part3', np.float32, 1),
        ('ratio_Part4', np.float32, 1),
        ])
    tms.result = np.zeros([1], dtype=dt)
    tms.result['GroupNum']=tms.Par['GroupNum']
    tms.result['SubNum']=SelectedSubNum
    tms.result['Axis']=tms.Par['Axis']
    tms.result['SubMostBoundID']=subcat[SelectedSubNum]['SubMostBoundID']
    tms.result['SubLen']=subcat[SelectedSubNum]['SubLen']
    tms.result['Subhalfmass']=subcat[SelectedSubNum]['Subhalfmass']
    tms.result['SubPos_x']=subcat[SelectedSubNum]['SubPos'][0]
    tms.result['SubPos_y']=subcat[SelectedSubNum]['SubPos'][1]
    tms.result['SubPos_z']=subcat[SelectedSubNum]['SubPos'][2]
    # ****************************************
    print '='*60
    # mass of particles (projected)
    axis=tms.Par['Axis']
    Axis=[0,1,2]
    Axis.remove(axis)
    bool1 = np.abs(tms.pos[:, axis] - HaloMostBound[axis]) < L*tms.h
    DR = tms.pos - HaloMostBound
    bool2 = (DR[:, Axis[0]]**2 + DR[:, Axis[1]]**2) < Aperture**2.
    sele = tms.pos[bool1 * bool2]
    print HaloMostBound
    print (sele.min(axis=0)-HaloMostBound)/tms.h
    print (sele.max(axis=0)-HaloMostBound)/tms.h
    tms.result['Projected_mass'] = sele.shape[0] * tms.ParticleM - remove_mean_mass(r=0.15,l=L,mode='cylinder')
    print tms.result['Projected_mass']/tms.h
    # ****************************************
    # mass of particles (part 1)
    print 'part 1:'
    sele = tms.pos[np.sum((tms.pos - HaloMostBound)**2, axis=1) < Aperture**2]
    print sele.shape
    tms.PM_150kpc = sele.shape[0] * tms.ParticleM - remove_mean_mass(r=0.15,l=0,mode='sphere')
    print '150kpc',tms.PM_150kpc/tms.h
    tms.result['PM_Part1']=tms.PM_150kpc
    # ****************************************
    # mass of particles (part 2)
    print 'part 2:'
    print subcat[SelectedSubNum]['Subhalfmass']
    bool1 = np.abs(tms.pos[:, axis] - HaloMostBound[axis]) < subcat[SelectedSubNum]['Subhalfmass']
    DR = tms.pos - HaloMostBound
    bool2 = (DR[:, Axis[0]]**2 + DR[:, Axis[1]]**2) < Aperture**2.
    sele = tms.pos[bool1 * bool2]
    tms.PM_2Rhalf = sele.shape[0] * tms.ParticleM - remove_mean_mass(r=0.15,l=subcat[SelectedSubNum]['Subhalfmass'],mode='cylinder')
    print 'Rhalf',tms.PM_2Rhalf/tms.h
#   tms.result['PM_Part2']=(tms.PM_2Rhalf-tms.PM_150kpc)
    tms.result['PM_Part2']=(tms.PM_2Rhalf)
    # ****************************************
    # mass of particles (part 3)
    print 'part 3:'
    print tms.SubPro['Halo_R_Crit200']
    bool1 = np.abs(tms.pos[:, axis] - HaloMostBound[axis]) < tms.SubPro['Halo_R_Crit200']
    DR = tms.pos - HaloMostBound
    bool2 = (DR[:, Axis[0]]**2 + DR[:, Axis[1]]**2) < Aperture**2.
    sele = tms.pos[bool1 * bool2]
    tms.PM_2R200 = sele.shape[0] * tms.ParticleM-remove_mean_mass(r=0.15,l=tms.SubPro['Halo_R_Crit200'],mode='cylinder')
    print 'R200',tms.PM_2R200/tms.h
#   tms.result['PM_Part3']=(tms.PM_2R200-tms.PM_2Rhalf)
    tms.result['PM_Part3']=(tms.PM_2R200)
    # ****************************************
    # mass of particles (part 4)
    print 'part 4:'
    tms.PM_residual = tms.result['Projected_mass']-tms.PM_2R200
    tms.result['PM_Part4']=tms.PM_residual
#================================================================================
    tms.result['PM_Part1']/=tms.h
    tms.result['PM_Part2']/=tms.h
    tms.result['PM_Part3']/=tms.h
    tms.result['PM_Part4']/=tms.h
    tms.result['Projected_mass']/=tms.h
    tms.result['ratio_Part1']=tms.result['PM_Part1']/tms.result['Projected_mass']
    tms.result['ratio_Part2']=tms.result['PM_Part2']/tms.result['Projected_mass']
    tms.result['ratio_Part3']=tms.result['PM_Part3']/tms.result['Projected_mass']
    tms.result['ratio_Part4']=tms.result['PM_Part4']/tms.result['Projected_mass']
    print '*'*80
    print tms.result['PM_Part1'],tms.result['PM_Part1']/(tms.result['Projected_mass'])
    print tms.result['PM_Part2'],tms.result['PM_Part2']/(tms.result['Projected_mass'])
    print tms.result['PM_Part3'],tms.result['PM_Part3']/(tms.result['Projected_mass'])
    print tms.result['PM_Part4'],tms.result['PM_Part4']/(tms.result['Projected_mass'])
#----------------------------------------
for n_subnum in np.arange(8):
    for n_axis in np.arange(3):
        f(def_Axis=n_axis,SelectedSubNum=n_subnum)
        if n_subnum==0 and n_axis==0:
            result=tms.result
        else:
            result=np.row_stack((result,tms.result))
print result.dtype
print result
np.save('output/mass_decomposition_group%d.npy'%tms.Par['GroupNum'],result)
