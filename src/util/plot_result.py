#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
#[('SubMostBoundID', '<u8'), ('SubLen', '<i4'), ('SubPos', '<f4', (3,)), ('Subhalfmass', '<f4'), ('delta_c', '<f4'), ('rs', '<f4'), ('Particle_mass', '<f4'), ('Projected_mass', '<f4'), ('NFW_mass', '<f4'), ('MainSub_mass_effect', '<f4')]
h=0.73
Particle_mass=8.61*10**8
Aper=150
L=15
data=np.load('./group0_axis2_Aperture%d_L%d.npy'%(Aper,L))
plt.plot(data['SubLen']*Particle_mass/h, data['Particle_mass']/h,'or-',label='Particle')
plt.plot(data['SubLen']*Particle_mass/h, data['Projected_mass']/h,'og-',label='Projected particle')
plt.plot(data['SubLen']*Particle_mass/h, data['NFW_mass']/h,'ob-',label='NFW_subhalo')
plt.xscale('log')
plt.yscale('log')
plt.xlim([data['SubLen'].min()*Particle_mass/h*0.9,data['SubLen'].max()*Particle_mass/h*1.1])
plt.xlabel(r'$\mathrm{M_{sub}\ [M_{\odot}}]$')
plt.ylabel(r'$\mathrm{Mass\ [M_{\odot}]}$')
plt.title('Depth %dMpc Aperture %dkpc'%(L,Aper))
plt.legend()
#plt.show()
plt.savefig('./group0_axis2_Aperture%d_L%d.eps'%(Aper,L))
