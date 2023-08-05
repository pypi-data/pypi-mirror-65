import numpy as np
import matplotlib.pyplot as plt

from photonpy.cpp.context import Context
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetectionMethods
from photonpy.cpp.roi_queue import ROIQueue
from photonpy.smlm.util import imshow_hstack
import time


import skimage
from skimage import io, exposure, img_as_uint, img_as_float


def process_movie(mov, spotDetector, roisize, ctx:Context):
    mov = np.ascontiguousarray(mov,dtype=np.uint16)
    imgshape = mov[0].shape
    roishape = [roisize,roisize]
    
    img_queue, roi_queue = SpotDetectionMethods(ctx).CreateQueue(imgshape, roishape, spotDetector)
    
    t0 = time.time()

    for img in mov:
        img_queue.PushFrame(img)
   
    while img_queue.NumFinishedFrames() < len(mov):
        time.sleep(0.1)
    
    dt = time.time() - t0
    print(f"Processed {len(mov)} frames in {dt:.2f} seconds. {len(mov)/dt:.1f} fps")

    rois, data = roi_queue.Fetch()
    return rois,data

def coordinates(name,size,spacing=0):
    grid = np.zeros((size,size))
    if name == 'grid':
        x = np.linspace(0+spacing/2,size-1-spacing/2,(size//spacing)) 
        y = np.linspace(0+spacing/2,size-1-spacing/2,(size//spacing))
        xv, yv = np.meshgrid(x, y)
        positions = np.vstack([xv.ravel(), yv.ravel()])

    elif name == 'random':
        grid = grid
    else:
        grid = grid
      
    return positions,grid

def simspots(pos,grid,model):
    size = grid.shape[0]
    xfull = np.linspace(0, size-1, size)
    yfull = np.linspace(0, size-1, size)
    xv, yv = np.meshgrid(xfull, yfull)
    gout = np.zeros((size,size))
    if model == 'gauss':
        for i in range(pos.shape[1]):
                sigx = np.sqrt(1.8)
                sigy = np.sqrt(1.8)
                gouttemp = 1000*np.exp(-1*((((xv-pos[0,i])**2)/(2*(sigx**2)))+(((yv-pos[1,i])**2)/(2*(sigy**2)))))
                gout=gout+gouttemp

    
    return gout
        
        
def hextransform(spotlist,radius):
    hexspotlist =[]
    hexspotlist.append(spotlist)
    x = [0,60,120,180,240,300]
    for i in range(6):
        dx = radius*np.cos(x[i]*np.pi/180)
        dy = radius*np.sin(x[i]*np.pi/180)
        xtemp = spotlist[0,:]+dx
        ytemp = spotlist[1,:]+dy
        hexspotlist.append(np.vstack([xtemp,ytemp]))
    return hexspotlist


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

with Context(debugMode=False) as ctx:
    pos,grid = coordinates('grid',100,50)
    gout = simspots(pos,grid,'gauss')
    hexspotlist = hextransform(pos,8)
    gouthex = simspots(np.hstack(hexspotlist[1:]),grid,'gauss')
    lx = int(pos[0,0]-12)
    ux= int(pos[0,0]+12)
    ly = int(pos[1,0]-12)
    uy= int(pos[1,0]+12)
#    gouthexn = skimage.util.random_noise(gouthex.astype(np.uint16),mode='poisson',seed=None, clip=True)
    io.imsave('test.tiff',gouthex.astype(dtype=np.uint16))
    template = gouthex[lx:ux,ly:uy]
    roisize =template.shape[0]
        
    plt.figure(); plt.imshow(template); plt.title('template')
    
    template = template/np.sum(template)

    template = template[np.newaxis,:,:]
    template = template.astype(dtype=np.float32)
    
    ctx.smlm.SetDebugImageCallback(debugImage)
        
    bghex = np.zeros((100,100)).astype(dtype=np.int32)
    sd = PSFConvSpotDetector(template, bghex, minPhotons=300, maxFilterSizeXY=10, debugMode=False)
    
    rois,data = process_movie([gouthex], sd, roisize, ctx)
    
    print(f"#spots: {len(rois)}")

    imshow_hstack(data)
    
