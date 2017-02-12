#!/usr/bin/env python
# coding=utf-8
import numpy as np
import h5py
#================================================================================
#DataSub = DataSub.byteswap()
Outfile=lambda name: '/data/dell1/userdir/maotx/data/Millennium/' + name
Infile=lambda num: "/data/rw9/Millennium/snapdir_063/snap_millennium_063.%d" % num
print Outfile('Millennium_All_particles_pos.npy')
print Infile(3)
dt = np.dtype([('head', np.int32, 1),
                    ('npart', np.int32, 6),
                    ('massarr', np.float64, 6),
                    ('time', np.float64),
                    ('redshift', np.float64),
                    ('flag_sfr', np.int32),
                    ('flag_feedback', np.int32),
                    ('npartall', np.int32, 6),
                    ('flag_cooling', np.int32),
                    ('Nsubfiles', np.int32),
                    ('BoxSize', np.float64),
                    ('Omega0', np.float64),
                    ('OmegaL', np.float64),
                    ('H', np.float64),
                    ('flag_stellarage', np.int32),
                    ('flag_metals', np.int32),
                    ('hashtabsize', np.int32),
                    ])
npart=0
for i in np.arange(512):
    with open(Infile(i)) as f:
        header=np.fromfile(f,dtype=dt,count=1)
        header=header.byteswap()
        if i==0:
            print header['npart']
    npart+=header['npart'][0,1]
POS=np.empty(shape=[npart,3],dtype=np.float32)
Npos=0 
for i in np.arange(512):
    print Infile(i)
    with open(Infile(i)) as f:
        #skip header
        dummy=np.fromfile(f,dtype=np.int32,count=1).byteswap()[0]
        f.seek(dummy,1)
        dummy=np.fromfile(f,dtype=np.int32,count=1).byteswap()[0]
        #read position
        dummy1=np.fromfile(f,dtype=np.int32,count=1).byteswap()[0]
        pos=np.fromfile(f,dtype=np.float32,count=dummy1/4).byteswap()
        dummy2=np.fromfile(f,dtype=np.int32,count=1).byteswap()[0]
        f.close()
        if dummy1!=dummy2:
            print 'error!'
            exit()
        POS[Npos:Npos+dummy1/12]=pos.reshape(dummy1/12,3)[:]
#       print POS[Npos:Npos+dummy1/12]
        Npos+=dummy1/12
print POS.shape
print POS[POS==0.].shape
POS.tofile(Outfile('Millennium_All_particles_pos.bin'))
