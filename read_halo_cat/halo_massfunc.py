import numpy as np
from read_subgroup import ReadSub
class rs(ReadSub):
    pass
h=0.704
Path=lambda x:'/datascope/indra4/Cluster/halocat/halocat_%d_%d_%d.npy'%(rs.ConvertSimNum(x))
data=[np.load(Path(i)) for i in np.arange(128)]
data=np.hstack(data)
M200=data['Halo_M_Crit200']/h*10**10
print M200.max()
bool=(M200>2.8*10**15)#*(M200<3.6*10**15)
print M200[bool].shape
data_selected=data[bool]
np.save('/datascope/indra4/Cluster/halocat/halocat_selected.npy',data_selected)
hist,edge=np.histogram(M200,bins=100)
edge=edge[:-1]+(edge[1]-edge[0])/2
massfunc=np.c_[edge,hist]
np.save('/datascope/indra4/Cluster/halocat/massfunc.npy',massfunc)
