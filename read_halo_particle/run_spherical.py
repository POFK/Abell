#!/usr/bin/env python
# coding=utf-8

import numpy as np
import os

a=np.load('/datascope/indra4/Cluster/halocat/halocat_selected.npy')
print a.dtype
print a.shape
rank=np.argsort(a['Halo_M_Crit200'])[::-1]
a=a[rank]
print a
Rad=60
def run(i=0):
    s=a[i]
    SimNum=s['SimNum']
    Sx=s['SubPos_x']
    Sy=s['SubPos_y']
    Sz=s['SubPos_z']
    Mrank=i
    print SimNum,Sx,Sy,Sz,Rad,Mrank
    os.system("./run %d %f %f %f %f %d"%(SimNum, Sx,Sy,Sz,Rad,Mrank))
[run(i) for i in np.arange(a.shape[0])]    
#for i in np.arange(a.shape[0]):

