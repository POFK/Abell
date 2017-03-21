#!/usr/bin/env python
# coding=utf-8
import numpy as np
class ReadSub():
    def __init__(self,num=0):
        self.num=num
        self.buf = "/data/rw9/Millennium/postproc_063/sub_tab_063.%d" % self.num
        self.SubDtype()

    def SubDtype(self):
        self.dt_header = np.dtype([
            ('Ngroups', np.int32, 1),
            ('Nids', np.int32, 1),
            ('TotNgroups', np.int32, 1),
            ('NTask', np.int32, 1),
            ('Nsubgroups', np.int32, 1),
        ])
        f = open(self.buf, 'r')
        DataSub = np.fromfile(file=f, dtype=self.dt_header, count=1)
        f.close()
        DataSub = DataSub.byteswap()
        self.Ngroups=DataSub[0]['Ngroups']
        self.Nsubgroups=DataSub[0]['Nsubgroups']
#       print self.num,DataSub

    def LoadSub(self):
        self.dt= np.dtype([
            ('NsubPerHalo', np.int32, self.Ngroups),
            ('FirstSubOfHalo', np.int32, self.Ngroups),
            ('SubLen', np.int32, self.Nsubgroups),
            ('SubOffset', np.int32, self.Nsubgroups),
            ('SubParentHalo', np.int32, self.Nsubgroups),
            ('Halo_M_Mean200', np.float32, self.Ngroups),
            ('Halo_R_Mean200', np.float32, self.Ngroups),
            ('Halo_M_Crit200', np.float32, self.Ngroups),
            ('Halo_R_Crit200', np.float32, self.Ngroups),
            ('Halo_M_TopHat200', np.float32, self.Ngroups),
            ('Halo_R_TopHat200', np.float32, self.Ngroups),
            ('SubPos', np.float32, 3*self.Nsubgroups),
            ('SubVel', np.float32, 3*self.Nsubgroups),
            ('SubVelDisp', np.float32, self.Nsubgroups),
            ('SubVmax', np.float32, self.Nsubgroups),
            ('SubSpin', np.float32, 3*self.Nsubgroups),
            ('SubMostBoundID', np.uint64, self.Nsubgroups),
            ('Subhalfmass', np.float32, self.Nsubgroups),
        ])
        
        f = open(self.buf, 'r')
        DataSub = np.fromfile(file=f, dtype=self.dt_header, count=1)
        DataSub = np.fromfile(file=f, dtype=self.dt, count=1)
        f.close()
        DataSub = DataSub.byteswap()
        return DataSub[0]

if __name__=='__main__':
    test=ReadSub(0)
    for i in np.arange(5):
        print '='*80
        print i
        test.__init__(i)
        data=test.LoadSub()
        print data['NsubPerHalo'][:10]
        exit()
        suboffset=data['FirstSubOfHalo']
        a=data['Halo_M_Crit200']
        bool=a>10**2
        print a[bool]
        print suboffset[bool]
        order=np.argsort(a)[::-1]
