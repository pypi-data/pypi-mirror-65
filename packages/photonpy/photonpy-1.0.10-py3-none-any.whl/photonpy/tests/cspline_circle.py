import numpy as np
import matplotlib.pyplot as plt

from photonpy.cpp.context import Context
from photonpy.cpp.cspline import CSpline_Calibration, CSpline
from photonpy.cpp.gaussian import Gaussian,Gauss3D_Calibration
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetector, SpotDetectionMethods
import photonpy.utils.multipart_tiff as tiff
import math
from photonpy.smlm.psf import psf_to_zstack
from photonpy.smlm.util import imshow_hstack
import photonpy.cpp.com as com
import time
import os
import tqdm
import numpy as np
import matplotlib.pyplot as plt

import math
import time
import os
import tqdm


# Change this to your cubic spline PSF calibration file..

def cspline_calib_fn():
    return 'c:/data/cspline-nm-astig.mat'
    #return 'c:/data/sols/cspline_calib_astigmatism30_roi_37.mat'

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
        theta[:,0:4] = xyzI[:,:4]
        theta[:,[1,0]] -= roipos
        on_spots = np.nonzero(on)[0]

        img = np.zeros((imgsize,imgsize),dtype=np.float32)
        if len(on_spots>0):
            rois = psf.ExpectedValue(theta[on_spots])
            ctx.smlm.DrawROIs(img, rois, roipos[on_spots])        

        frames[f] = img 
        frames[f] += bg
        on_counts[f] = np.sum(on)

    return frames, on_counts

def view_movie(mov):
    import napari    
    
    with napari.gui_qt():
        napari.view_image(mov)


def process_movie(mov, spotDetector, roisize, ctx:Context):
    rois = []
    roiposXY = []
    framenum = []
    
    pf = SpotDetectionMethods(ctx).ProcessFrame
    for i in tqdm.trange(len(mov)):
        r = pf(mov[i], spotDetector, roisize, 200)
        rois.append(r[0])
        roiposXY.append(r[1][:,[1,0]])
        framenum.append(np.ones(len(r[0]))*i)
        
        if len(r[0])>1 or len(r[0]) == 0:
            print(f"frame {i} has {len(r[0])} emitters.")
    
    return np.concatenate(roiposXY), np.concatenate(rois), np.concatenate(framenum)



def generate_ground_truth_cylinder_xy(img_width, num_emitters, R, emitter_intensity):
    N = num_emitters
    angle = np.random.uniform(0, 2 * math.pi, N)
            
    xyzI = np.zeros((N,4))
    xyzI[:,0] = R * np.cos(angle) + img_width / 2 + 0.2
    xyzI[:,1] = R * np.sin(angle) + img_width / 2
    xyzI[:,2] = 0
    xyzI[:,3] = emitter_intensity
    
    return xyzI



def view_movie(mov):
    import napari    
    
    with napari.gui_qt():
        napari.view_image(mov)




with Context() as ctx:

    roisize = 14
    
    # Use cubic spline PSFs (needs calibration file), or a default astigmatic Gaussian?
    if True:
        psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), cuda=True)
        detection_threshold = 20
    else:
        fn = cspline_calib_fn()
        cspline_calib = CSpline_Calibration.from_file_nmeth(fn)
        psf = CSpline(ctx).CreatePSF_XYZIBg(roisize, cspline_calib, cuda=True)
        detection_threshold = 10
        
        
    np.random.seed(0)
    img_width = 20
    pixelsize = 0.100 # um/pixel
    background = 5 # photons/pixel
    R = 0 # img_width*0.25

    xyzI = generate_ground_truth_cylinder_xy(img_width, 1, R,
                                 emitter_intensity=1000)
    
    print("Generating SMLM example movie")
    mov_expval, on_counts = generate_storm_movie(psf, xyzI, numframes=500, 
                                          imgsize=img_width,bg=background, p_on=1)

    print("Applying poisson noise")
    mov = np.random.poisson(mov_expval)
    
    com_estim = com.create_estimator(roisize,ctx)
    sdcfg = SpotDetector(4, roisize, minIntensity=1)
    roipos, rois, framenum = process_movie(mov, sdcfg, roisize, ctx)
    #estim = com_estim.Estimate(rois)[0]
    estim = psf.Estimate(rois)[0]
    
    estim[:,[0,1]] += roipos[:,[0,1]]
    
    good = (estim[:,0] > 9.6) & (estim[:,0] < 10.7)
    
    roipos += roisize//2

    roi2 = mov[:,img_width//2-roisize//2:img_width//2+roisize//2,
               img_width//2-roisize//2:img_width//2+roisize//2]
    estim_roi = psf.Estimate(roi2)[0]
    estim_roi[:,[0,1]] += img_width/2 - roisize/2 + 1

    plt.figure()
    plt.scatter(estim[:,0], estim[:,1],s=1.5, label='Estimated')
    plt.scatter(roipos[:,0], roipos[:,1], label='roipos')
    plt.scatter(estim_roi[:,0], estim_roi[:,1],s=1.5, label='No spotdetect')
    #plt.scatter(xyzI[:,0], xyzI[:,1], s=0.7,label='Ground truth')
    plt.xlabel('X [pixelsize]'); plt.ylabel('Z [pixelsize]')
    plt.legend()
    plt.title(f'X-Z section [{len(estim)} spots]')
    
    print(f"#spots: {len(estim)}")

    imshow_hstack(rois)
    