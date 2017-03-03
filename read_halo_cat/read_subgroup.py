#!/usr/bin/env python
# coding=utf-8
import numpy as np
class ReadSub():
    def __init__(self,SimNum,filenum=0):
        self.num=filenum
	n1,n2,n3=self.ConvertSimNum(SimNum)
        self.buf = "/datascope/indra%d_/%d_%d_%d/postproc_052/sub_tab_052.%d" %(n1,n1,n2,n3,self.num)
        self.SubDtype()
    @classmethod
    def ConvertSimNum(self,SimNum=0):
        a=SimNum/8/8
        b=SimNum%64/8
        c=SimNum%64%8
	return a,b,c

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
        self.Ngroups=DataSub[0]['Ngroups']
        self.Nsubgroups=DataSub[0]['Nsubgroups']
	self.header=DataSub
#       print self.num,DataSub
#       print DataSub.dtype

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
        return DataSub[0]

if __name__=='__main__':
    test=ReadSub(SimNum=0)
    data=test.LoadSub()
    print test.header
    print test.header.dtype



'''
test=DataSub[0]["SubMostBoundID"]
id=7298858190
if id in test:
    tt=test.tolist()
    index=tt.index(id)
    print index
    print i
    break
'''
