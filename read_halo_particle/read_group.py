#!/usr/bin/env python
# coding=utf-8
import ctypes
import numpy as np

Gnum=[4386162,3831945,2162498,2117511,2117472,1838697,1838697]
N=1  # group rank
so = ctypes.CDLL('./pylib.so')

pos = np.empty(shape=[Gnum[N]* 3], dtype=np.float32)
Sxyz = np.empty(shape=[3], dtype=np.float32)
MostboundId = np.empty(shape=[1], dtype=np.int64)

Len=so.Mill(1,
        N,
        pos.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        Sxyz.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        MostboundId.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
       )
print Sxyz
print Len
print MostboundId
#a = pos.reshape([Gnum[N], 3])
#a.tofile('./data/group%d_pos.bin'%N,format='f4')
#np.save('./data/group%d_pos.npy'%N,a)
