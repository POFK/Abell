#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from TMS import TMS

tms=TMS(path='../parameter')
num=0

def fig(n):
    tms.Par['Path']='/home/maotx/mycode/gadget/src/read_group/data/spherical_region_coordinates_group%d_20Mpc.bin'%n
    tms.LoadPPos()


    plt.figure('group%d_xy'%n)
    plt.plot(tms.pos[:,0],tms.pos[:,1],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$x\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$y\ [\mathrm{Mpc}/h]$')
    plt.xlim([tms.pos[:,0].min(),tms.pos[:,0].max()])
    plt.ylim([tms.pos[:,1].min(),tms.pos[:,1].max()])
    plt.savefig('region_group%d_xy.png'%n)
    
    plt.figure('group%d_yz'%n)
    plt.plot(tms.pos[:,1],tms.pos[:,2],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$y\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$z\ [\mathrm{Mpc}/h]$')
    plt.xlim([tms.pos[:,1].min(),tms.pos[:,1].max()])
    plt.ylim([tms.pos[:,2].min(),tms.pos[:,2].max()])
    plt.savefig('region_group%d_yz.png'%n)
    
    plt.figure('group%d_zx'%n)
    plt.plot(tms.pos[:,2],tms.pos[:,0],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$z\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$x\ [\mathrm{Mpc}/h]$')
    plt.xlim([tms.pos[:,2].min(),tms.pos[:,2].max()])
    plt.ylim([tms.pos[:,0].min(),tms.pos[:,0].max()])
    plt.savefig('region_group%d_zx.png'%n)

fig(0)
fig(1)
fig(2)
