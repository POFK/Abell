#!/usr/bin/env python
# coding=utf-8
import numpy as np
from read_subgroup import ReadSub

readsub=ReadSub(0)
TotNsubgroups=0
for i in np.arange(256):
    readsub.__init__(i)
    TotNsubgroups+=readsub.Nsubgroups
print 'TotNsubgroups:', TotNsubgroups
dt_subcat=np.dtype([
    ('SubMostBoundID', np.uint64, 1),
    ('SubLen', np.int32, 1),
    ('SubPos', np.float32, 3),
    ('Subhalfmass', np.float32, 1),
])
subcat=np.empty(shape=[TotNsubgroups],dtype=dt_subcat)
offset=0
for i in np.arange(512):
    readsub.__init__(i)
    data=readsub.LoadSub()
    subcat['SubMostBoundID'][offset:offset+readsub.Nsubgroups]=data['SubMostBoundID'][:]
    subcat['SubLen'][offset:offset+readsub.Nsubgroups]=data['SubLen'][:]
    subcat['SubPos'][offset:offset+readsub.Nsubgroups]=data['SubPos'].reshape([-1,3])
    subcat['Subhalfmass'][offset:offset+readsub.Nsubgroups]=data['Subhalfmass'][:]
    offset+=readsub.Nsubgroups

print subcat.shape
print subcat.dtype
import h5py
with h5py.File('subcatalogue.hdf5',mode='w') as f:
    f.create_dataset(name='subcat',dtype=subcat.dtype,data=subcat)
    f.close()

#import matplotlib.pyplot as plt
#subcat=subcat[subcat['SubLen']>100]
#plt.plot(subcat['SubPos'][:,0],subcat['SubPos'][:,1],'.',ms=0.4,alpha=0.1)
#plt.show()
