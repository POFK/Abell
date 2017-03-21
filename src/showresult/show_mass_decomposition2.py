#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
#GroupNum=5
subhalos=True
NUM=3*6
def getName(GroupNum):
    return '../output/mass_decomposition_group%d.npy'%GroupNum
def load(PATH):
    if subhalos==True:
        data=np.load(PATH)[3:NUM]
    else:
        data=np.load(PATH)[:NUM]
    return data
data=load(getName(0))
data=np.vstack([data,load(getName(1))])
data=np.vstack([data,load(getName(2))])
data=np.vstack([data,load(getName(5))])
data=np.vstack([data,load(getName(17))])
data=np.vstack([data,load(getName(27))])
data=data[:,0]
print data.shape
print data.dtype
#data['Projected_mass']
#data['PM_Part1']
#data['PM_Part3']
def get_midvalue(data,NUM):
    '''return middle, maximum, minimum value.'''
    a=data[np.argsort(data)]
    print a
    if NUM%2==1:
        return [a[NUM/2],a[-1],a[0]]
    elif NUM%2==0:
        return [a[NUM/2-1:NUM/2+1].mean(),a[-1],a[0]]
#print data['ratio_Part4'][:,0]
#print data.shape
#print get_midvalue(data['ratio_Part4'][:,0],NUM)

print data.dtype.descr
result=np.empty([3,3])
NUM=data.shape[0]
print NUM
P1=data['PM_Part1']/data['Projected_mass']
P2=(data['PM_Part3']-data['PM_Part1'])/data['Projected_mass']
P3=(data['Projected_mass']-data['PM_Part3'])/data['Projected_mass']
result[0,:]=get_midvalue(P1,NUM)
result[1,:]=get_midvalue(P2,NUM)
result[2,:]=get_midvalue(P3,NUM)
print result
print result[:,0]
#=============== plot ===========================================================
yerr=[result[:,0]-result[:,2],result[:,1]-result[:,0]]
#yerr=[result[:,2],result[:,1]]
width=0.5
ind=np.arange(3)
fig, ax = plt.subplots()
rects1 = ax.bar(ind, result[:,0], width, color='b')
ax.errorbar(ind+width/2,result[:,0],yerr=yerr,ecolor='r',fmt='r.',elinewidth=1.0,)
print result[:,0]
print yerr

#ax.set_ylabel('Scores')
#ax.set_title('Group %d'%GroupNum)
ax.set_xticks(ind + width / 2,minor=False)
ax.set_xticklabels((r'$150\ \mathrm{kpc}$',  r'$\mathrm{R_{200}}$', r'$\mathrm{residual}$'))
ax.set_yticks(np.arange(0,11)*0.1)
ax.set_yticklabels((r'$0$',r'$0.1$',r'$0.2$',r'$0.3$',r'$0.4$',r'$0.5$',r'$0.6$',r'$0.7$',r'$0.8$',r'$0.9$',r'$1.0$',))
#ax.legend(rects1[0], 0)

#plt.title('subhalos')
plt.xlim([-0.5,3.0])
plt.ylim([0.0,1.0])
#plt.yscale('log')
#plt.show()
plt.savefig('mass_decomposition_all6groups_allsub.pdf')
