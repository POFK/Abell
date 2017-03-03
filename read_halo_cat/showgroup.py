import numpy as np
from read_subgroup import ReadSub
MassLim=1000. #10**12 M_\odot
SimNum=3
def loadSim(SimNum=0):
    readsub=ReadSub(SimNum=SimNum,filenum=0)
    TotNgroups=readsub.header['TotNgroups'][0]
    dt_halocat=np.dtype([
                   ('SimNum', np.int32, 1),
                   ('SubFileNum', np.int32, 1),
                   ('SubMostBoundID', np.uint64, 1),
                   ('SubParentHalo', np.int32, 1),
                   ('Halo_M_Crit200', np.float32, 1),
                   ('Halo_R_Crit200', np.float32, 1),
                   ('SubPos_x', np.float32, 1),
                   ('SubPos_y', np.float32, 1),
                   ('SubPos_z', np.float32, 1),
                   ('Subhalfmass', np.float32, 1),
    		])
    halocat=np.empty(shape=[TotNgroups],dtype=dt_halocat)
    offset=0
    for i in np.arange(readsub.header['NTask'][0]):
        readsub.__init__(SimNum=SimNum,filenum=i)
        data=readsub.LoadSub()
    
        Ngroups=readsub.header['Ngroups'][0]
        bool=data['Halo_M_Crit200']>MassLim
        suboffset=data['FirstSubOfHalo']
        suboffset=suboffset[bool]
        haloN=len(suboffset)
    
        halocat['SimNum'][offset:offset+haloN]=SimNum
        halocat['SubFileNum'][offset:offset+haloN]=i
        halocat['SubMostBoundID'][offset:offset+haloN]=data['SubMostBoundID'][suboffset]
        halocat['SubParentHalo'][offset:offset+haloN]=data['SubParentHalo'][suboffset]
        halocat['Halo_M_Crit200'][offset:offset+haloN]=data['Halo_M_Crit200'][bool]
        halocat['Halo_R_Crit200'][offset:offset+haloN]=data['Halo_R_Crit200'][bool]
        halocat['SubPos_x'][offset:offset+haloN]=data['SubPos'][suboffset*3]
        halocat['SubPos_y'][offset:offset+haloN]=data['SubPos'][suboffset*3+1]
        halocat['SubPos_z'][offset:offset+haloN]=data['SubPos'][suboffset*3+2]
        halocat['Subhalfmass'][offset:offset+haloN]=data['Subhalfmass'][suboffset]
        offset+=haloN
    print 'Sim %d, length of halocat:'%SimNum,offset 
    halocat=halocat[:offset]
    OutPath='/datascope/indra4/Cluster/halocat/halocat_%d_%d_%d.npy'%(readsub.ConvertSimNum(SimNum))
    np.save(OutPath,halocat)
[loadSim(i) for i in np.arange(128)]
