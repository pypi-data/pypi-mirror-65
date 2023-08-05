import numpy as np
import matplotlib.pyplot as plt

from photonpy.cpp.context import Context
from photonpy.cpp.cspline import CSpline_Calibration, CSpline
from photonpy.cpp.gaussian import Gaussian,Gauss3D_Calibration
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetector,  SpotDetectionMethods
import photonpy.utils.multipart_tiff as tiff
import math
from photonpy.smlm.psf import psf_to_zstack
from photonpy.smlm.util import imshow_hstack
import time
import os
import tqdm

# Change this to your cubic spline PSF calibration file..
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

def view_movie(mov):
    import napari    
    
    with napari.gui_qt():
        napari.view_image(mov)



def process_movie(mov, spotDetector, roisize, ctx:Context):
    imgshape = mov[0].shape
    roishape = [roisize,roisize]

    if True: # using queues  
        img_queue, roi_queue = SpotDetectionMethods(ctx).CreateQueue(imgshape, roishape, spotDetector)
        
        t0 = time.time()
    
        for img in mov:
            img_queue.PushFrame(img)
       
        while img_queue.NumFinishedFrames() < len(mov):
            time.sleep(0.1)
        
        dt = time.time() - t0
        print(f"Processed {len(mov)} frames in {dt:.2f} seconds. {len(mov)/dt:.1f} fps")
        
        rois, data = roi_queue.Fetch()
        roipos = np.array([rois['x'],rois['y'],rois['z']]).T
        return roipos, data
    
    else:
        rois = []
        roipos = []
        
        pf = SpotDetectionMethods(ctx).ProcessFrame
        for i in tqdm.trange(len(mov)):
            r = pf(mov[i], spotDetector, roisize, 200)
            
            xyz = np.zeros((len(r[0]),3),dtype=np.int32)
            cornerYX = r[1]
            xyz[:,0] = cornerYX[:,1]
            xyz[:,1] = cornerYX[:,0]
            xyz[:,2] = r[3]
            
            rois.append(r[0])
            roipos.append(xyz)
        
        return np.concatenate(roipos), np.concatenate(rois)
    
    
def localization(psf, rois, initial_guess):
    
    estim = psf.Estimate(rois, initial=initial_guess)
    
    return estim, np.arange(len(rois))
     

def generate_ground_truth_cross_xy(img_width, num_emitters, object_size_um, pixelsize, emitter_intensity):
    N = num_emitters
    pixelsize = 0.1 #um/pixel
            
    xyzI = np.zeros((N,4))
    pos = np.random.uniform(-object_size_um/2,object_size_um/2,N)
    xyzI[:,0] = pos / pixelsize + img_width*0.5
    xyzI[:,1] = pos / pixelsize + img_width*0.5#np.random.uniform(0.2,0.8,N) * img_width
    xyzI[:,2] = np.random.uniform(-0.2,0.2, N) 
    xyzI[:,3] = emitter_intensity
    xyzI[:N//2,1] = -pos[:N//2] / pixelsize + img_width*0.5
    return xyzI    



def generate_ground_truth_cylinder_xy(img_width, num_emitters, object_size_um, pixelsize, emitter_intensity):
    N = num_emitters
    pixelsize = 0.1 #um/pixel
    angle = np.random.uniform(0, 2 * math.pi, N)
            
    xyzI = np.zeros((N,4))
    xyzI[:,0] = object_size_um/2 / pixelsize * np.cos(angle) + img_width / 2
    xyzI[:,1] = object_size_um/2 / pixelsize * np.sin(angle) + img_width / 2
    xyzI[:,2] = 0.2
    xyzI[:,3] = emitter_intensity
    
    return xyzI




with Context(debugMode=False) as ctx:

    roisize = 18
    
    # Use cubic spline PSFs (needs calibration file), or a default astigmatic Gaussian?
    if False:
        psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), cuda=True)
        detection_threshold = 20
    else:
        fn = cspline_calib_fn()
        cspline_calib = CSpline_Calibration.from_file_nmeth(fn)
        psf = CSpline(ctx).CreatePSF_XYZIBg(roisize, cspline_calib, cuda=True)
        detection_threshold = 10
        
    img_width = 64
    pixelsize = 0.100 # um/pixel
    background = 5 # photons/pixel
    object_size_um = 1 #um
    N = 5
    xyzI = np.zeros((N, 5))
    
    
    print("Generating SMLM example movie")
    mov_expval, on_counts = generate_storm_movie(psf, xyzI, numframes=1000, 
                                          imgsize=img_width,bg=background, p_on=1 / len(xyzI))

    print("Applying poisson noise")
    mov = np.random.poisson(mov_expval)
    
    #view_movie(mov)

    plt.figure()
    plt.imshow(mov[0])
    plt.title("Frame 0")
    plt.colorbar()

    bgimg = mov[0]*0
    psf_zrange = np.linspace(-object_size_um*0.8, object_size_um*0.8, 100)
    psfstack = psf_to_zstack(psf, psf_zrange)

    # this sets up the template-based spot detector. MinPhotons is not actually photons, still just AU.
    sd = PSFConvSpotDetector(psfstack, bgimg, minPhotons=detection_threshold, maxFilterSizeXY=5, debugMode=False)
    #sd = SpotDetector(4, roisize, 20)
    
    roipos, rois = process_movie(mov, sd, roisize, ctx)
    
    initial_guess = np.ones((len(rois), 5)) * [roisize/2,roisize/2,0,0,1]
    initial_guess[:,2] = psf_zrange[roipos[:,2]]
    initial_guess[:,3] = np.sum(rois,(1,2))
    
    plt.figure()
    hist = np.histogram(roipos[:,2],bins=len(psf_zrange),range=[0,len(psf_zrange)])
    plt.bar(psf_zrange, hist[0], width=(psf_zrange[-1]-psf_zrange[0])/len(hist[0]))
    plt.xlabel('Z position [um]')
    plt.title('Z position initial estimate from PSF convolutions')

    imshow_hstack(rois)

    estim, ids = localization(psf, rois, initial_guess)
    rois = rois[ids]
    roipos = roipos[ids]
    
    # Filter out all ROIs with chi-square, this gets rid of ROIs with multiple spots.
    expval = psf.ExpectedValue(estim)
    chisq = np.sum( (rois-expval)**2 / (expval+1e-9), (1,2))
    
    std_chisq = np.sqrt(2*psf.samplecount + np.sum(1/np.mean(expval,0)))

    # Filter out all spots that have a chi-square > expected value + 2 * std.ev.
    chisq_threshold = psf.samplecount + 2*std_chisq
    sel = chisq < chisq_threshold
    print(f"Chi-Square threshold: {chisq_threshold:.1f}. Removing {np.sum(sel==False)}/{len(rois)} spots")
    
    view_movie(mov)
    view_movie(rois[sel])
        
    plt.figure()
    plt.hist(chisq,bins=100,range=[0,1000])
    plt.gca().axvline(chisq_threshold,color='r', label='threshold')
    plt.title('Chi-Square values for each localization')
    plt.legend()

    estim[:,[0,1]] += roipos[:,[0,1]]

    estim = estim[sel]
        
    if True:
        plt.figure()    
        plt.scatter(estim[:,0], estim[:,1],s=1.5, label='Estimated')
        plt.scatter(xyzI[:,0], xyzI[:,1], s=1,label='Ground truth')
        plt.legend()
    
    print(f"#spots: {len(estim)}")

    
    
    