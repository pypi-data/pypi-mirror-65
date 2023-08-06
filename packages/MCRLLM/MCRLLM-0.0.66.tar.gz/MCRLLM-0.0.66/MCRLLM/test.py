# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:28:32 2020

@author: Yannick
"""

import numpy as np
from mcrllm import *
import matplotlib.pyplot as plt


data = np.load('data1.npy')


#%%
nb_c = 3

dim1 = np.shape(data)[0]
dim2 = np.shape(data)[1]
nb_level = np.shape(data)[2]

x_sum = np.sum(data, axis = 2)

X = np.reshape(data, [dim1*dim2 , nb_level])

plt.imshow(x_sum)
plt.pause(5)
plt.close()


#%%

#mettons une vingtaine de pixel random à 0

rand = np.random.randint(0,dim1*dim2,20)
    
X[rand,:] = 0

rand2 = np.random.randint(0,nb_level , 20)

X[:,rand2] = 0
  

#%%

decomp = mcrllm(X,nb_c,init = 'Kmeans', nb_iter=1)


#%%

C = decomp.C
S = decomp.S

#%%

Csum = np.sum(C , axis = 1)

print(rand , np.where(Csum == 0))

#%%


plt.plot(np.arange(len(S[0,:])) , S[0,:])
plt.plot(np.arange(len(S[0,:])) , S[1,:])
plt.plot(np.arange(len(S[0,:])) , S[2,:])


#%%

C  = np.reshape(C, [dim1,dim2,nb_c])

fig , (ax1,ax2,ax3) = plt.subplots(1,3)
ax1.imshow(C[:,:,0])
ax2.imshow(C[:,:,1])
ax3.imshow(C[:,:,2])
    





    
    