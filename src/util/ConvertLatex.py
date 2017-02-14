#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pandas as pd
data=np.load('./mass_decomposition_group5.npy')
#s=pd.DataFrame({"a":a['a'], "b":a['a']})
def convertLatex(data):
    s=pd.DataFrame()
    dt=data.dtype
    num=len(dt.descr)
    for i in np.arange(num):
        key=dt.descr[i][0]
#       if key=='SubPos':
#           s[key+'_x']=data[key][:,0]
#           s[key+'_y']=data[key][:,1]
#           s[key+'_z']=data[key][:,2]
        if 'SubPos' in key or 'SubMostBoundID' in key:
            pass
        else:
#           s[key]=data[key]
            s[key]=data[key][:,0]
    print s.to_latex()
if __name__=='__main__':
    convertLatex(data)
