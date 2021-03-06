#!/usr/bin/env python
# coding=utf-8
import sys
import numpy as np
import scipy.signal as signal
import h5py
from scipy.optimize import fsolve

class TMS():

    def __init__(self, path='./parameter'):
        self.ReadPar(path=path)
        self.ParticleM = 8.61 * 10**8  # M_solar/h
        self.h=0.73
        self.rho_crit=2.755*10**11 # h^2*M_solar/Mpc^3
        print self.Par

    def ReadPar(self, path='./parameter'):
        with open(path, 'r') as f:
            par = f.readlines()
        self.Par = {}
        for i in par:
            x = i.replace(' ', '').replace('\n', '').split(':')
            if x[0] == '' or x[0][0] == '#':
                continue
            self.Par[x[0]] = x[1]
        self.ConvertPar()

    def ConvertPar(self):
        self.Par['MostBoundX'] = float(self.Par['MostBoundX'])
        self.Par['MostBoundY'] = float(self.Par['MostBoundY'])
        self.Par['MostBoundZ'] = float(self.Par['MostBoundZ'])
        self.Par['Axis'] = int(self.Par['Axis'])
        MassLimit = self.Par['MassLimit'].split('E')
        self.Par['MassLimit'] = float(MassLimit[0])*10**int(MassLimit[1])

    def LoadPPos(self):
        '''load Parh, or the position of particles.'''
        print '=' * 20 + sys._getframe().f_code.co_name + '=' * 20
        print self.Par['Path']
        with open(self.Par['Path'], 'rb') as f:
            pos = np.fromfile(f, dtype='f4')
        self.pos = pos.reshape(pos.shape[0] / 3, 3)
        print 'number of particles:', self.pos.shape[0]

    def ParticleGridingNGP(self,Ngrid,R=1.3,L=15.0):
        '''
        input :R 1.3Mpc   L 30Mpc
        Ngrid : [512,512,1]
        '''
        print '=' * 20 + sys._getframe().f_code.co_name + '=' * 20
        R=R*self.h
        L=L*self.h
        axis=self.Par['Axis']
        Axis=[0,1,2]
        Axis.remove(axis)
        Axis.append(axis)
        print 'Axis (r,r,l):' , Axis
        HaloMostBound=[]
        HaloMostBound.append(self.Par['MostBoundX'])
        HaloMostBound.append(self.Par['MostBoundY'])
        HaloMostBound.append(self.Par['MostBoundZ'])
        data=self.pos.copy()
        data=data[np.abs(data[:,Axis[0]]-HaloMostBound[Axis[0]])<R]
        data=data[np.abs(data[:,Axis[1]]-HaloMostBound[Axis[1]])<R]
        data=data[np.abs(data[:,Axis[2]]-HaloMostBound[Axis[2]])<L]
        print 'number of particles:', data.shape[0]
        Ngrid[Ngrid.index(1)]=np.max(Ngrid)
        Ngrid[Axis[2]]=1
        print Ngrid
        dataG=self.ParticleNGP(data,Ngrid[0],Ngrid[1],Ngrid[2])
        return dataG

    def ParticleNGP(self,data,Nx,Ny,Nz):
        print '=' * 20 + sys._getframe().f_code.co_name + '=' * 20
        bin_x=np.linspace(data[:,0].min()-10**-5,data[:,0].max()+10**-5,Nx+1)
        bin_y=np.linspace(data[:,1].min()-10**-5,data[:,1].max()+10**-5,Ny+1)
        bin_z=np.linspace(data[:,2].min()-10**-5,data[:,2].max()+10**-5,Nz+1)
        Lx=data[:,0].max()-data[:,0].min()
        Ly=data[:,1].max()-data[:,1].min()
        Lz=data[:,2].max()-data[:,2].min()
        print "L:",Lx,Ly,Lz
        print "N:",Nx,Ny,Nz
        nn,edges=np.histogramdd(data,bins=(bin_x,bin_y,bin_z))
        nn*=self.ParticleM
        return nn

    def Smooth2D(self,data,L=1.3,N=512,sigma=0.001):
        print '=' * 20 + sys._getframe().f_code.co_name + '=' * 20
        L=2*L*self.h
        sigma*=self.h

        Kf=2*np.pi/L
        x=np.fft.fftfreq(N,1./N)
        delta_k=np.fft.fft2(data)
        k=x[:,None]**2+x[None,:]**2
        smooth_kernal=np.exp(-0.5*Kf**2*k*k*sigma**2)
        smoothed_data=np.fft.ifft2(delta_k*smooth_kernal)
        return smoothed_data.real

    def PeakFinder(self,datag,sigma=0.15):
# should be modified!
        '''
        run as:
        for sigma in np.linspace(0.001,0.15,15,endpoint=False):
            tms.PeakFinder(datag,sigma=sigma)
        pind=np.array(list(set([tuple(i) for i in tms.peakind])))
        '''
        datas=self.Smooth2D(datag,sigma=sigma)
        lmax0=signal.argrelmax(datas,axis=0)
        lmax1=signal.argrelmax(datas,axis=1)
        lmax0=np.c_[lmax0[0],lmax0[1]].tolist()
        lmax1=np.c_[lmax1[0],lmax1[1]].tolist()
        try:
            self.peakind=np.vstack([self.peakind,np.array([i for i in lmax0 if i in lmax1])])
        except AttributeError:
            self.peakind=np.array([i for i in lmax0 if i in lmax1])
        print sigma,len(self.peakind)

    def LoadSubCat(self):
        path=self.Par['SubPath']
        with h5py.File(path,mode='r') as f:
            self.subcat=f['subcat'][...]
            f.close()
   
    def SubSelect(self,R=1.3,L=15.0,range=5):
        '''
        input :R 1.3Mpc   L 30Mpc
        '''
        R=R*self.h
        L=L*self.h
        axis=self.Par['Axis']
        Axis=[0,1,2]
        Axis.remove(axis)
        Axis.append(axis)
        print 'Axis (r,r,l):' , Axis
        HaloMostBound=[]
        HaloMostBound.append(self.Par['MostBoundX'])
        HaloMostBound.append(self.Par['MostBoundY'])
        HaloMostBound.append(self.Par['MostBoundZ'])
        HaloMostBound=np.array(HaloMostBound)
        subdis=self.subcat['SubPos']-HaloMostBound
        subposlimit=self.subcat['Subhalfmass']*range
        poslimbool1=np.abs(subdis[:,Axis[0]])<subposlimit+R
        poslimbool2=np.abs(subdis[:,Axis[1]])<subposlimit+R
        poslimbool3=np.abs(subdis[:,Axis[2]])<subposlimit+L
        poslimbool=poslimbool1*poslimbool2*poslimbool3
        subcat=self.subcat[poslimbool]
        return subcat


    def NFW_fit(self,data,mode='relaxed'):
        print '=' * 20 + sys._getframe().f_code.co_name + '=' * 20
        rho_crit=self.rho_crit # h^2*M_solar/Mpc^3
        NFW_par=np.empty(shape=[len(data)],dtype=np.dtype([('rs',np.float32,1),('delta_c',np.float32,1)]))
        #----------------------------------------
        if mode=='relaxed':
            C_200=5.26*(1.34*data['SubLen']*self.ParticleM/10**14)**-0.10
        else:
            C_200=4.67*(1.34*data['SubLen']*self.ParticleM/10**14)**-0.11
        #----------------------------------------
        def f(x):
            return np.log(1.+x)-x/(1.+x)
        delta_c=200./3.*(C_200**3./f(C_200))
        Sbias=1./(8.*np.pi)*data['SubLen']*self.ParticleM/(rho_crit*delta_c)
        def Rs_fit(x,r_half,Sbias):
            '''
            input x: rs
            '''
            return x**3*f(r_half/x)-Sbias
        for i in np.arange(len(data)):
            rs_result=fsolve(Rs_fit,np.random.rand(),args=(data['Subhalfmass'][i],Sbias[i]))
            NFW_par['rs'][i]=rs_result[0]
            NFW_par['delta_c'][i]=delta_c[i]
    
        with h5py.File(self.Par['SubPathSave'],mode='w') as f:
            f.create_dataset(name='subcat',dtype=data.dtype,data=data)
            f.create_dataset(name='NFW_par',dtype=NFW_par.dtype,data=NFW_par)
            f.close()
        print 'number of subhalo:',len(NFW_par)

    def SubGriding(self,NG=128,R=1.3,L=15.0,range=5):
        R=R*self.h
        L=L*self.h
        axis=self.Par['Axis']
        Axis=[0,1,2]
        Axis.remove(axis)
        Axis.append(axis)
        with h5py.File(self.Par['SubPathSave'],mode='r') as f:
            subcat=f['subcat'][...]
            NFW_par=f['NFW_par'][...]
            f.close()
        def rho(r,rs,delta_c):
            return self.rho_crit*delta_c*rs/(r*(1.+r/rs)**2)
        Axis={Axis[0]: R, Axis[1]: R, Axis[2]: L}
        print 'Axis (r,r,l):' , Axis
        subgrids=np.zeros(shape=[NG,NG,NG],dtype=np.float32)
        axis_x=np.linspace(-Axis[0],Axis[0],NG)
        axis_y=np.linspace(-Axis[1],Axis[1],NG)
        axis_z=np.linspace(-Axis[2],Axis[2],NG)
        gridcoord_x= (axis_x+self.Par['MostBoundX'])[:,None,None]+subgrids
        gridcoord_y= (axis_y+self.Par['MostBoundY'])[None,:,None]+subgrids
        gridcoord_z= (axis_z+self.Par['MostBoundZ'])[None,None,:]+subgrids

        s0=0.
        for i in np.arange(len(subcat)):
            Distance=((subcat[i]['SubPos'][0]-gridcoord_x)**2+(subcat[i]['SubPos'][1]-gridcoord_y)**2+(subcat[i]['SubPos'][2]-gridcoord_z)**2)**0.5
            bool=Distance<(subcat[i]['Subhalfmass']*range)
            subgrids[bool]+=rho(Distance[bool],NFW_par[i]['rs'],NFW_par[i]['delta_c'])
            # for test ========
            s1=subgrids.sum()*(1.3**2*15.0*8*self.h**3)/NG**3-s0
            s2=subcat[i]['SubLen']*self.ParticleM
            print i,'of',len(subcat),':',s1,s2
            s0=subgrids.sum()*(1.3**2*15.0*8*self.h**3)/NG**3
            # for test ========
        dV=R*R*L*8.*self.h**3/NG**3.
        subgrids*=dV
        np.save('sub_grid.npy',subgrids)
        return subgrids




if __name__ == '__main__':
    a = TMS()
    a.ReadPar()
    a.LoadPPos()
    s=a.ParticleGridingNGP(Ngrid=[256,256,1]).reshape(256,256)
    print s.sum()
#   a.LoadSubCat()
#   subcat=a.SubSelect(R=1.3,L=15.0)
#   a.NFW_fit(data=subcat)
#   print a.subcat['SubLen']
#   print a.subcat['SubPos']
#   print a.subcat['Subhalfmass']
