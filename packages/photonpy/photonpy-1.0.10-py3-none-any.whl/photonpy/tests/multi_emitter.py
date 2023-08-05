# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:00:46 2020

@author: jcnossen1
"""

from photonpy.cpp.context import Context
import numpy as np
import matplotlib.pyplot as plt
import photonpy.cpp.multi_emitter as multi_emitter
from photonpy.cpp.gaussian import Gaussian, Gauss3D_Calibration

with Context(debugMode=True) as ctx:
    sigma = 1.8
    roisize = 16
    E = 2
    N = 5
    psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), True) 
    estim = multi_emitter.create_estimator(psf, E, ctx)
    
    pts = np.zeros((N,E*4+1))
    pts[:,0] = 10 #bg
    for k in range(E):
        pos = np.random.uniform([-4,-4,-0.5,600],[4,4,0.5,2000],size=(N,4))
        pos[:,[0,1]] += roisize*0.5
        pts[:,np.arange(4)+k*4+1] = pos
    
    ev = estim.ExpectedValue(pts)
    deriv, ev = estim.Derivatives(pts)
    
    plt.figure()
    plt.imshow(np.concatenate(ev,-1))

    plt.figure()
    plt.imshow(np.concatenate(deriv[0],-1))
    