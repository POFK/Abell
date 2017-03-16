import numpy as np
from TMS import TMS
import matplotlib.pyplot as plt
import os
sigma=0.001
OutDir='/datascope/indra4/Cluster/result/S%.3f_200kpc_4PlotFigure/'%sigma
#OutDir='./test/S%.3f/'%sigma
if not os.path.exists(OutDir):
    os.makedirs(OutDir)
GN=10
axis=0
#================================================================================
def run(GN=0,axis=0):
    tms = TMS(path='./parameter',GroupNum=GN)
    pdata=np.load(OutDir+'Axis%d_'%axis+tms.LoadGroupCat(tms.Par['GroupNum'])[:-4]+'.npy')
    tms.Par['Axis'] = axis
    tms.LoadPPos()
    HaloMostBound = []
    HaloMostBound.append(tms.Par['MostBoundX'])
    HaloMostBound.append(tms.Par['MostBoundY'])
    HaloMostBound.append(tms.Par['MostBoundZ'])
    HaloMostBound = np.array(HaloMostBound)
    distance = tms.pos - HaloMostBound
    tms.pos[distance > 500.] = tms.pos[distance > 500.] - 1000.
    tms.pos[distance < -500.] = tms.pos[distance < -500.] + 1000.
    def ParticleSelect(R=1.3,L=15.0,pdata=pdata):
        '''
        input :R 1.3Mpc   L 15Mpc
        Ngrid : [512,512,1]
        '''
        R=R*tms.h
        L=L*tms.h
        axis=tms.Par['Axis']
        Axis=[0,1,2]
        Axis.remove(axis)
        Axis.append(axis)
        Ngrids=[1024,1024,1024]
        Ngrids[axis]=1000
        Nx,Ny,Nz=Ngrids
        
        print 'Axis (r,r,l):' , Axis
        HaloMostBound=[]
        HaloMostBound.append(tms.Par['MostBoundX'])
        HaloMostBound.append(tms.Par['MostBoundY'])
        HaloMostBound.append(tms.Par['MostBoundZ'])
        data=tms.pos.copy()
        data=data[np.abs(data[:,Axis[0]]-HaloMostBound[Axis[0]])<R]
        data=data[np.abs(data[:,Axis[1]]-HaloMostBound[Axis[1]])<R]
        data=data[np.abs(data[:,Axis[2]]-HaloMostBound[Axis[2]])<L]
        print 'number of particles:', data.shape[0]
        D=np.array([R,R,L])
        bin_x=np.linspace(HaloMostBound[0]-D[Axis.index(0)],HaloMostBound[0]+D[Axis.index(0)],Nx+1)
        bin_y=np.linspace(HaloMostBound[1]-D[Axis.index(1)],HaloMostBound[1]+D[Axis.index(1)],Ny+1)
        bin_z=np.linspace(HaloMostBound[2]-D[Axis.index(2)],HaloMostBound[2]+D[Axis.index(2)],Nz+1)
    #   bin_x=bin_x[:-1]+(bin_x[1]-bin_x[0])/2.
    #   bin_y=bin_y[:-1]+(bin_y[1]-bin_y[0])/2.
    #   bin_z=bin_z[:-1]+(bin_z[1]-bin_z[0])/2.
        bins=[bin_x,bin_y,bin_z]
        Axis=np.array(Axis)
        bins[Axis[0]]=bins[Axis[0]][:-1]+(bins[Axis[0]][1]-bins[Axis[0]][0])/2.
        bins[Axis[1]]=bins[Axis[1]][:-1]+(bins[Axis[1]][1]-bins[Axis[1]][0])/2.
        pdata[:,0]=bins[Axis[0]][np.int32(pdata[:,0])]
        pdata[:,1]=bins[Axis[1]][np.int32(pdata[:,1])]
        return data,bins,pdata,Axis
    data,bins,pdata,Axis=ParticleSelect(R=1.3,L=15.0)
    #Axis[0], Axis[1]
    print pdata
    def get_par(subnum=0,bin=bins[Axis[2]]):
        print 'bin',bin.shape
        bool1=data[:,Axis[0]]-pdata[subnum,0]<0.15*tms.h
        bool2=data[:,Axis[1]]-pdata[subnum,1]<0.15*tms.h
        data_selected=data[bool1*bool2]
        nn,edges=np.histogram(data_selected,bins=bin)
        return nn
    result=np.zeros(shape=[1000,pdata.shape[0]])
    print result.shape
    for i in np.arange(pdata.shape[0]):
        result[:,i]=get_par(subnum=i)
    np.save(OutDir+'Axis%d_'%axis+tms.LoadGroupCat(tms.Par['GroupNum'])[:-4]+'_DDB.npy',result)
for i in np.arange(36):
    for axj in np.arange(3):
        run(GN=i,axis=axj)
