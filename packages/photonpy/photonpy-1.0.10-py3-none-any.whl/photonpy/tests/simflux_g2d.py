import numpy as np
import matplotlib.pyplot as plt

import photonpy.smlm.util as su
from photonpy.cpp.context import Context
import photonpy.cpp.gaussian as gaussian

from photonpy.cpp.simflux import SIMFLUX

mod = np.array([
           [0, 1.8, 0,  0.95, 0, 1/6],
           [1.9, 0, 0,0.95, 0, 1/6],
           [0, 1.8, 0,  0.95, 2*np.pi/3, 1/6],
           [1.9, 0, 0,0.95, 2*np.pi/3, 1/6],
           [0, 1.8,0,   0.95, 4*np.pi/3, 1/6],
           [1.9, 0, 0,0.95, 4*np.pi/3, 1/6]
          ])

with Context() as ctx:
    g = gaussian.Gaussian(ctx)

    sigma=1.5
    roisize=10
    theta=[[roisize//2, roisize//2, 1000, 5]]
    theta=np.repeat(theta,6,0)
    
#    with g.CreatePSF_XYZIBg(roisize, calib, True) as psf:
    psf = g.CreatePSF_XYIBg(roisize, sigma, True)
    img = psf.ExpectedValue(theta)
    smp = np.random.poisson(img)
    
    s = SIMFLUX(ctx)

    gloc = psf.Estimate(smp)[0]
#        su.imshow_hstack(smp)
    
    sf_psf = s.CreateEstimator_Gauss2D(sigma, mod, roisize, len(mod), True)
    estim,diag,traces = sf_psf.Estimate([smp])
    
    IBg = np.reshape(diag, (len(mod),4))
    print(f"Intensities (unmodulated): {IBg[:,0]}")
    
    ev = sf_psf.ExpectedValue(theta[5])
    crlb = sf_psf.CRLB(theta[5])
    crlb_g = psf.CRLB(theta[5])
    print(f"Simflux CRLB: { crlb}")
    print(f"2D Gaussian CRLB: {crlb_g}")
    smp = np.random.poisson(ev)
    
    su.imshow_hstack(smp[0])


    deriv = psf.Derivatives(theta) 
       