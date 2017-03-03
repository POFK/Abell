#!/usr/bin/env python
# coding=utf-8
import ctypes
import numpy as np


def Dt():
    return np.dtype([('Rank', np.int32, 1),
                     ('Sx', np.float32, 1),
                     ('Sy', np.float32, 1),
                     ('Sz', np.float32, 1),
                     ('Len', np.int32, 1),
                     ('MostBoundId', np.int64, 1),
                     ])


def ReadGroup(N=1):
    # N: group rank
    Gnum = 4386162
    dt = Dt()
    so = ctypes.CDLL('./pylib.so')

    pos = np.empty(shape=[Gnum * 3], dtype=np.float32)
    Sxyz = np.empty(shape=[3], dtype=np.float32)
    MostBoundId = np.empty(shape=[1], dtype=np.int64)
    Len = so.Mill(0,
                  N,
                  pos.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
                  Sxyz.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
                  MostBoundId.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
                  )
    print "=" * 80
    data = np.empty([1], dtype=dt)
    data['Rank'] = N
    data['Sx'] = Sxyz[0]
    data['Sy'] = Sxyz[1]
    data['Sz'] = Sxyz[2]
    data['Len'] = Len
    data['MostBoundId'] = MostBoundId[0]
    return data
    #a = pos.reshape([Gnum[N], 3])
    # a.tofile('./data/group%d_pos.bin'%N,format='f4')
    # np.save('./data/group%d_pos.npy'%N,a)

if __name__ == '__main__':
    dt = Dt()
    data = np.empty([50], dtype=dt)
    print data.dtype
    for i in np.arange(50):
        data[i] = ReadGroup(N=i)
        print data[i]
    np.savetxt('./data/MostBoundId.txt', data)
    np.save('./data/MostBoundId.npy', data)
    print data.dtype
    print data
