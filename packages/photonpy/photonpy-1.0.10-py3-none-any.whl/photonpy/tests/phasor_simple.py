import matplotlib.pyplot as plt
import numpy as np
import time

import photonpy.smlm.util as su
from photonpy.cpp.context import Context
import photonpy.cpp.gaussian as gaussian
from photonpy.cpp.calib import sCMOS_Calib

from photonpy.cpp.phasor import localize, create_estimator

with Context() as ctx:
    g = gaussian.Gaussian(ctx)

    sigma=1.6
    roisize=7

    psf = g.CreatePSF_XYIBg(roisize, sigma, False)
    theta = [4,4,10000,10]

    plt.figure()
    img = psf.GenerateSample([theta])
    plt.figure()
    plt.set_cmap('inferno')
    plt.imshow(img[0])
    
    localize(img[0])
    
    com = PSF.CenterOfMassEstimator(roisize,ctx)
    phasor = create_estimator(roisize,ctx)
    
    com_estim = com.ComputeMLE(img)[0]
    print(f"COM: {com_estim}")
    
    phasor_estim = phasor.ComputeMLE(img)[0]
    print(f"Phasor: {phasor_estim}")
    