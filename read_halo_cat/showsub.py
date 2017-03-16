#!/usr/bin/env python
# coding=utf-8
import numpy as np
import h5py
from read_subgroup import ReadSub
readsub=ReadSub(SimNum=0,filenum=0)
dt_subcat=np.dtype([
    ('SubMostBoundID', np.uint64, 1),
    ('SubLen', np.int32, 1),
    ('SubPos', np.float32, 3),
    ('Subhalfmass', np.float32, 1),
])
#----------------------------------------
def run(simnum=0):
    print 'Simnum:',simnum
    TotNsubgroups=0
    for i in np.arange(readsub.header['NTask']):
        readsub.__init__(SimNum=simnum,filenum=i)
        TotNsubgroups+=readsub.Nsubgroups
    print 'TotNsubgroups:', TotNsubgroups
    subcat=np.empty(shape=[TotNsubgroups],dtype=dt_subcat)
    offset=0
    for i in np.arange(readsub.header['NTask']):
        readsub.__init__(SimNum=simnum,filenum=i)
        data=readsub.LoadSub()
        subcat['SubMostBoundID'][offset:offset+readsub.Nsubgroups]=data['SubMostBoundID'][:]
        subcat['SubLen'][offset:offset+readsub.Nsubgroups]=data['SubLen'][:]
        subcat['SubPos'][offset:offset+readsub.Nsubgroups]=data['SubPos'].reshape([-1,3])
        subcat['Subhalfmass'][offset:offset+readsub.Nsubgroups]=data['Subhalfmass'][:]
        offset+=readsub.Nsubgroups

    print subcat.shape
    print subcat.dtype
    with h5py.File('/datascope/indra4/Cluster/subcat/subcat%03d.hdf5'%simnum,mode='w') as f:
        f.create_dataset(name='subcat',dtype=subcat.dtype,data=subcat)
        f.close()

[run(simnum=i) for i in np.arange(128)]
#import matplotlib.pyplot as plt
#subcat=subcat[subcat['SubLen']>100]
#plt.plot(subcat['SubPos'][:,0],subcat['SubPos'][:,1],'.',ms=0.4,alpha=0.1)
#plt.show()

