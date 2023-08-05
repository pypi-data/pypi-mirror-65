"""
PSF Utilities
"""


from photonpy.cpp.estimator import Estimator
import numpy as np
import matplotlib.pyplot as plt


def psf_to_zstack(psf:Estimator, zrange, intensity=1, bg=0, plot=False):
    
    assert psf.numparams == 5
    
    params = np.zeros((len(zrange),5))
    params[:,0] = psf.sampleshape[0]/2
    params[:,1] = psf.sampleshape[1]/2
    params[:,2] = zrange
    params[:,3] = intensity
    params[:,4] = bg
    
    ev = psf.ExpectedValue(params)
    
    if plot:
        plt.figure()
        plt.imshow(np.concatenate(ev,-1))
        plt.colorbar()
    
    return ev