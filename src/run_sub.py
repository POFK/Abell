#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import h5py
from TMS import TMS
#********  sub  *****************************************************************
def run_nfw_sub(group=0,GridNum=256,axis=0):
    tms = TMS(path='./parameter')
    tms.Par['Axis'] = axis

    tms.LoadSubCat()
    subcat=tms.SubSelect(R=1.3,L=15.0)
    subcat=subcat[subcat['SubLen']>=1000]
    print subcat.shape
    tms.NFW_fit(subcat)
    
    path=tms.Par['SubPathSave']
    with h5py.File(path,mode='r') as f:
        subcat=f['subcat'][...]
        NFW_par=f['NFW_par'][...]
        f.close()
    # griding
    SavePath='./subgrids/SubGrids_group%d_axis%d.npy'%(group,tms.Par['Axis'])
    print SavePath
#   subGrids=tms.SubGriding(NG=GridNum,SavePath=SavePath)
    subGrids=np.load(SavePath)
    H=1.3*2/GridNum
    Dindex=0.15/H
    print Dindex
    datag=subGrids.sum(axis=tms.Par['Axis'])
    ##============= plot ====================
    def plotsub(datag,pdata,group,axis,sigma,mlim):
        if len(pdata)==0:
            return 0
        print len(pdata)
        plt.clf()
        plt.cla()
        fig, ax0 = plt.subplots(ncols=1)
        ax0.imshow(datag.T)
        for i in range(len(pdata)):
            ax0.add_artist(plt.Circle((pdata[i,0], pdata[i,1]), Dindex, color='k', fill=False))
        plt.title('number of aperture: %d'%len(pdata))
        plt.savefig('./Test/testsub/subhalo_group%d_axis%d_s%f_Mlim%.3g.eps'%(group,axis,sigma,mlim))
    ##============= result ==================
    sigma = [0.001,0.002,0.003,0.004,0.005]
    MassLimitArr=np.arange(46)*10**12+5*10**12
    f=h5py.File('NFW_SubNumber_group%d.hdf5'%group,mode='a')
    for i in sigma:
        result=np.zeros(shape=[len(MassLimitArr),2],dtype=np.float32)
        pdata = tms.PeakFinder(datag, sigma=i, R=1.3, N=GridNum, Aperture=0.15)
        for j in np.arange(len(MassLimitArr)):
            pdata0 = pdata[pdata[:, 2] > MassLimitArr[j]]
            Pnum=len(pdata0)
            result[j,0]=MassLimitArr[j]
            result[j,1]=float(Pnum)
            plotsub(datag,pdata0,group,tms.Par['Axis'],i,MassLimitArr[j])
        print 'sigma:',i
        print result
        f.create_dataset(name='Axis%d/sigma%.3f'%(tms.Par['Axis'],i),
                         dtype=np.float32,
                         data=result)
    f.close()
##********************************************************************************
run_nfw_sub(group=0,GridNum=256,axis=0)
run_nfw_sub(group=0,GridNum=256,axis=1)
run_nfw_sub(group=0,GridNum=256,axis=2)
