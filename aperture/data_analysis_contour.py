#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
h=0.704
def Smooth2D(data,L=1.3,N=512,sigma=0.001):
        L=2*L*h
            sigma*=h
            
            Kf=2*np.pi/L
                x=np.fft.fftfreq(N,1./N)
        delta_k=np.fft.fft2(data)
        k=x[:,None]**2+x[None,:]**2
            smooth_kernal=np.exp(-0.5*Kf**2*k*k*sigma**2)
        smoothed_data=np.fft.ifft2(delta_k*smooth_kernal)
        return smoothed_data.real

        path1='Axis1_M200rank20_Sim106_X700.30_Y788.27_Z850.35_Rad60.00_datag.npy'
        path2='Axis1_M200rank20_Sim106_X700.30_Y788.27_Z850.35_Rad60.00.npy'
        path3='../Sub_200kpc/Axis1_M200rank20_Sim106_X700.30_Y788.27_Z850.35_Rad60.00.npy'
        datag=np.load(path1)
    dataP=np.load(path2)
    dataPs=np.load(path3)
    datas=Smooth2D(datag,L=1.3,N=256,sigma=0.001)
    plt.plot(dataP[:,0],dataP[:,1],'ko',ms=3)
    plt.plot(dataPs[:,0],dataPs[:,1],'k^',ms=3)
    #plt.imshow(datas.T)
    plt.contour(datas.T,linewidths=1)
    plt.colorbar()
    #plt.show()
    plt.savefig('test.eps')

