import sys

sys.path.append("..")
import matplotlib.pyplot as plt
import numpy as np
import time


from photonpy.cpp.context import Context
from photonpy.cpp.cspline import CSpline_Calibration, CSpline
from photonpy.cpp.gaussian import Gaussian,Gauss3D_Calibration
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetectionMethods
import photonpy.utils.multipart_tiff as tiff
import math
from photonpy.smlm.psf import psf_to_zstack
from photonpy.smlm.util import imshow_hstack
import time
import os
import numpy as np
import matplotlib.pyplot as plt

import math
import time
import os

def cspline_calib_fn():
    cspline_fn = 'cspline-nm-astig.mat'
    #cspline_fn = 'Tubulin-A647-cspline.mat'
    import os
    if not os.path.exists(cspline_fn):
        try:
            import urllib.request
            url=f'http://homepage.tudelft.nl/f04a3/{cspline_fn}'
            print(f"Downloading {url}")
            urllib.request.urlretrieve(url, cspline_fn)
            
            if not os.path.exists(cspline_fn):
                print('Skipping CSpline 3D PSF (no coefficient file found)')
                cspline_fn = None
        finally:
            ...
    
    return cspline_fn



def generate_storm_movie(psf, xyzI, numframes=100, 
                         imgsize=512, bg=5, p_on=0.1):
    
    frames = np.zeros((numframes, imgsize, imgsize), dtype=np.float32)
    on_counts = np.zeros(numframes, dtype=np.int32)

    for f in range(numframes):
        on = np.random.binomial(1, p_on, len(xyzI))

        roisize = psf.sampleshape[0]
        roipos = np.clip((xyzI[:,[1,0]] - roisize/2).astype(int), 0, imgsize-roisize)
        theta = np.zeros((len(xyzI),5)) # assuming xyzIb
        theta[:,0:4] = xyzI
        theta[:,[1,0]] -= roipos
        on_spots = np.nonzero(on)[0]

        rois = psf.ExpectedValue(theta[on_spots])
        
        frames[f] = ctx.smlm.DrawROIs((imgsize,imgsize), rois, roipos[on_spots])
        frames[f] += bg
        on_counts[f] = np.sum(on)

    return frames, on_counts

def view_movie(mov):
    import napari    
    
    with napari.gui_qt():
        napari.view_image(mov)



def generate_ground_truth_cross(img_width, num_molecules, object_size_um, pixelsize, emitter_intensity):
    N = num_molecules
    pixelsize = 0.1 #um/pixel
            
    xyzI = np.zeros((N,5))
    pos = np.random.uniform(0,object_size_um,N) - object_size_um/2
    xyzI[:,0] = pos / pixelsize + img_width*0.5
    xyzI[:,1] = np.random.uniform(0.2,0.8,N) * img_width
    xyzI[:,2] = pos
    xyzI[:,3] = emitter_intensity
    xyzI[:N//2,2] = -xyzI[:N//2,2]

    return xyzI    

def generate_ground_truth_cylinder(img_width, num_molecules, object_size_um, pixelsize, emitter_intensity):
    N = num_molecules
    pixelsize = 0.1 #um/pixel
    angle = np.random.uniform(0, 2 * math.pi, N)
            
    xyzI = np.zeros((N,5))
    xyzI[:,0] = object_size_um/2 / pixelsize * np.cos(angle) + img_width / 2
    xyzI[:,1] = np.linspace(0.2,0.8,N) * img_width
    xyzI[:,2] = np.sin(angle) * object_size_um/2
    xyzI[:,3] = emitter_intensity
    
    """
    plt.figure()
    plt.scatter(xyzI[:,0],xyzI[:,2])
    plt.title(f"Ground truth")
    """
    
    return xyzI


def view_movie(mov):
    import napari    
    
    with napari.gui_qt():
        napari.view_image(mov)



with Context() as ctx:

    roisize = 20
    
    # Use cubic spline PSFs (needs calibration file), or a default astigmatic Gaussian?
    if False:
        psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), cuda=True)
    else:
        fn = cspline_calib_fn()
        cspline_calib = CSpline_Calibration.from_file_nmeth(fn)
        psf = CSpline(ctx).CreatePSF_XYZIBg(roisize, cspline_calib, cuda=True, LM_lambda=1)
        
    img_width = 20
    pixelsize = 0.100 # um/pixel
    background = 5 # photons/pixel
    object_size_um = 1 #um
    xyzI = generate_ground_truth_cross(img_width, 1000, object_size_um,
                                 pixelsize, emitter_intensity=1000)
    xyzI[:,4]=background
    
    smp = psf.GenerateSample(xyzI)
    
    estim = psf.Estimate(smp)[0]
    
    plt.figure()    
    plt.scatter(estim[:,0]*pixelsize, estim[:,2],s=1, label='Estimated')
    plt.scatter(xyzI[:,0]*pixelsize, xyzI[:,2], s=1,label='Ground truth')
    plt.xlabel('X [microns]'); plt.ylabel('Z [microns]')
    plt.xlim([img_width*0.5*pixelsize-object_size_um*0.6, img_width*0.5*pixelsize+object_size_um*0.6])
    plt.ylim([-object_size_um*0.7,object_size_um*0.7])
    plt.legend()
    plt.title(f'X-Z section [{len(estim)} spots]')
    
    print(f"#spots: {len(estim)}")

    
    