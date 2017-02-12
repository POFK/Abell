#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt


def fig(n):
    path='/home/maotx/mycode/gadget/src/read_group/data/group%d_pos.npy'%n
    pos=np.load(path)
    len=pos.shape[0]
    print len

    plt.figure('group%d_xy'%n)
    plt.plot(pos[:,0],pos[:,1],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$x\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$y\ [\mathrm{Mpc}/h]$')
    plt.savefig('group%d_xy.png'%n)
    
    plt.figure('group%d_yz'%n)
    plt.plot(pos[:,1],pos[:,2],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$y\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$z\ [\mathrm{Mpc}/h]$')
    plt.savefig('group%d_yz.png'%n)
    
    plt.figure('group%d_zx'%n)
    plt.plot(pos[:,2],pos[:,0],'k.',ms=0.05,alpha=0.1)
    plt.xlabel(r'$z\ [\mathrm{Mpc}/h]$')
    plt.ylabel(r'$x\ [\mathrm{Mpc}/h]$')
    plt.savefig('group%d_zx.png'%n)

fig(0)
fig(1)
fig(2)
