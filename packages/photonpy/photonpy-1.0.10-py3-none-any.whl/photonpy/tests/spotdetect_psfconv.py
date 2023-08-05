import numpy as np
import matplotlib.pyplot as plt

from photonpy.cpp.context import Context
from photonpy.cpp.cspline import CSpline_Calibration, CSpline
from photonpy.cpp.gaussian import Gaussian,Gauss3D_Calibration
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetectionMethods, SpotDetector
import photonpy.utils.multipart_tiff as tiff
import math
from photonpy.smlm.psf import psf_to_zstack
from photonpy.smlm.util import imshow_hstack

def generate_storm_movie(psf:Estimator, xyzI, numframes=100, 
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

images=[]

def debugImage(img,label):
    images.append((img,label))
    
def viewDebugImages():
    import napari
    with napari.gui_qt():
        viewer = napari.Viewer()
        
        for img,label in images:
            viewer.add_image(img, name=label)

def plotDebugImages():
    for img,label in images:
        plt.figure()
        plt.imshow( np.concatenate(img,-1) )
        plt.colorbar()
        plt.title(label)


roisize = 12
w = 64
N = 4
numframes = 100
R = np.random.normal(0, 0.2, size=N) + w * 0.3
angle = np.random.uniform(0, 2 * math.pi, N)

xyzI = np.zeros((N,4))
xyzI[:,0] = R * np.cos(angle) + w / 2
xyzI[:,1] = R * np.sin(angle) + w / 2
xyzI[:,2] = np.linspace(-3,3,N)
xyzI[:,3] = 3200
    
with Context(debugMode=False) as ctx:
    psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), cuda=True)
    
    print("Generating SMLM example movie")
    mov_expval, on_counts = generate_storm_movie(psf, xyzI, numframes, 
                                          imgsize=w,bg=10, p_on=0.99)#1 / N)
    print("Applying poisson noise")
    mov = np.random.poisson(mov_expval)

    plt.figure()
    plt.imshow(mov[0])
    plt.title("Frame 0")
    plt.colorbar()

    bgimg = mov[0]*0
    psfstack = psf_to_zstack(psf, np.linspace(-3,3,5))
        
    ctx.smlm.SetDebugImageCallback(debugImage)

    sd = PSFConvSpotDetector(psfstack, bgimg, minPhotons=50, maxFilterSizeXY=5, debugMode=True)
    rois,corners,scores,spotz=SpotDetectionMethods(ctx).ProcessFrame(mov[0], sd, roisize, maxSpotsPerFrame=200)
    
    plt.hist(spotz)

    print(f"#spots: {len(rois)}")
    
    imshow_hstack(rois)

    #viewDebugImages()
    plotDebugImages()