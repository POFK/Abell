#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
#[('SubMostBoundID', '<u8'), ('SubLen', '<i4'), ('SubPos', '<f4', (3,)), ('Subhalfmass', '<f4'), ('delta_c', '<f4'), ('rs', '<f4'), ('Particle_mass', '<f4'), ('Projected_mass', '<f4'), ('NFW_mass', '<f4'), ('MainSub_mass_effect', '<f4')]
h=0.73
Particle_mass=8.61*10**8
data1=np.load('./group0_axis2_Aperture%d_L%d.npy'%(150,15))
data2=np.load('./group0_axis2_Aperture%d_L%d.npy'%(150,30))
data3=np.load('./group0_axis2_Aperture%d_L%d.npy'%(250,15))
data4=np.load('./group0_axis2_Aperture%d_L%d.npy'%(250,30))
#plt.plot(data1['SubLen']*Particle_mass/h, data1['Particle_mass']/h,'or-',label='Particle')
#plt.plot(data1['SubLen']*Particle_mass/h, data1['NFW_mass']/h,'ob-',label='NFW_subhalo')
plt.plot(data1['SubLen']*Particle_mass/h, data1['Projected_mass']/h,'.g-',label='Projected; L15 A150')

plt.plot(data2['SubLen']*Particle_mass/h, data2['Projected_mass']/h,'.r-',label='Projected; L30 A150')
plt.plot(data3['SubLen']*Particle_mass/h, data3['Projected_mass']/h,'.b-',label='Projected; L15 A250')
plt.plot(data4['SubLen']*Particle_mass/h, data4['Projected_mass']/h,'.k-',label='Projected; L30 A250')

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'$\mathrm{M_{sub}\ [M_{\odot}}]$')
plt.ylabel(r'$\mathrm{Mass\ [M_{\odot}]}$')
plt.xlim([data1['SubLen'].min()*Particle_mass/h*0.9,data1['SubLen'].max()*Particle_mass/h*1.1])
plt.legend(ncol=2)
#plt.show()
plt.savefig('./compare.eps')
