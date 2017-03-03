'''to check the redshift for each snapshot'''
import numpy as np
path=lambda x: '/datascope/indra0_/0_0_0/snapdir_%03d'%x+'/snapshot_%03d.0'%x
print path(63)
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
                    ])
def read_redshift(n):
    f = open(path(n), 'r')
    Info = np.fromfile(file=f, dtype=dt, count=1)
    f.close()
    print n,Info['redshift']
    return n,Info

n,info=read_redshift(52)
print info.dtype
print info
#for i in np.arange(64):
#    read_redshift(i)

