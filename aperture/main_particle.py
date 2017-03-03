#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS
import os
sigma=0.005
OutDir='/datascope/indra4/Cluster/S%.3f/'%sigma
if not os.path.exists(OutDir):
    os.makedirs(OutDir)
def run(GN=0,axis=0):
    print '-'*80
    print 'GroupNum:%d',GN
    print 'Axis:%d',axis
    print '-'*80
    tms = TMS(path='./parameter',GroupNum=GN)
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
    
    GridNum = 256
    Ngrid = [GridNum, GridNum, GridNum]
    Ngrid[tms.Par['Axis']] = 1
    datag = tms.ParticleGridingNGP(Ngrid=Ngrid, R=1.3, L=15)
    datag = datag.reshape(GridNum, GridNum)
    halo_projected_mass=datag.sum()/tms.h
    print 'all mass:', datag.sum() / tms.h
    H = 1.3 * 2 / GridNum
    Dindex = 0.15 / H
    
    pdata = tms.PeakFinder(datag, sigma=sigma, R=1.3, N=GridNum, Aperture=0.15)
    pdata[:, 2] /= tms.h
    pdata = pdata[pdata[:, 2] > 5 * 10**13]
    np.save(OutDir+'Axis%d_'%axis+tms.LoadGroupCat(tms.Par['GroupNum'])[:-4]+'.npy',pdata)
    print pdata.shape
    fig, (ax0, ax1) = plt.subplots(ncols=2)
#   fig, ax0 = plt.subplots(ncols=1)
    cax0=ax0.imshow(datag.T)
#   fig.colorbar(cax0)
    datas=tms.Smooth2D(datag,L=1.3,N=GridNum,sigma=sigma)
    cax1=ax1.imshow(datas.T)
#   fig.colorbar(cax1)
    for i in range(len(pdata)):
        ax0.add_artist(
            plt.Circle(
                (pdata[
                    i, 0], pdata[
                    i, 1]), Dindex, color='k', fill=False))
        ax1.add_artist(
            plt.Circle(
                (pdata[
                    i, 0], pdata[
                    i, 1]), Dindex, color='k', fill=False))
    #   ax1.add_artist(plt.Circle((pind[i,0], pind[i,1]), Dindex, color='k', fill=False))
    # plt.show()
    plt.savefig(OutDir+'Axis%d_'%axis+tms.LoadGroupCat(tms.Par['GroupNum'])[:-4]+'.eps')
    return GN,axis,halo_projected_mass
dt=np.dtype([('GroupNum',np.int32,1),
        ('Axis',np.int32,1),
        ('ProjectedMass',np.float64,1)])
all_mass=np.empty(shape=[36],dtype=dt)
for i in np.arange(36):
    for axj in np.arange(3):
        gn,ais,pm=run(GN=i,axis=axj)
        all_mass[i]['GroupNum']=gn
        all_mass[i]['Axis']=ais
        all_mass[i]['ProjectedMass']=pm
        plt.cla()
        plt.clf()
np.save(OutDir+'ProjectedMass.npy',all_mass)

