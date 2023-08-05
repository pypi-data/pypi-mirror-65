import numpy as np
import os
import tqdm
import tifffile

imsave = tifffile.imsave

class MultipartTiffSaver:
    def __init__(self, fn):
        self.tifIdx=1
        self.tifFrame = 0
        self.fn = fn
        self.tif = tifffile.TiffWriter(fn)
        
        
    def save(self, img):
        max_tif_frames = 4000000000 // (img.shape[0]*img.shape[1]*2)
        
        if self.tifFrame == max_tif_frames:
            self.tif.close()
            fn2 = os.path.splitext(self.fn)[0] +f"_X{self.tifIdx}.tif"
            self.tifIdx +=1
            self.tif = tifffile.TiffWriter(fn2)
            self.tifFrame=0
            
        self.tif.save(np.ascontiguousarray(img, dtype=np.uint16))
        self.tifFrame+=1
        
    def close(self):
        self.tif.close()
        self.tif=None
                 
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()       
        
        
def get_tiff_mean(fn):
    mov = tifffile.imread(fn)
    return np.mean(mov,0)


def tiff_get_filenames(fn):
    if fn.find('.ome.tif') >= 0:
        fmt =  "_{0}.ome.tif"
        basefn = fn.replace('.ome.tif','')
    else:
        fmt = "_X{0}.tif"
        basefn = fn.replace('.tif' ,'')
        
    
    files=[fn]
    i = 1
    while True:
        file = basefn+fmt.format(i)
        if os.path.exists(file):
            files.append(file)
            i+=1
        else:
            break
    return files


def tiff_read_file(fn, startframe=0, maxframes=-1, update_cb=None):
    if update_cb is not None:
        update_cb("Enumerating tif files",0)
    numframes = 0
    filenames = tiff_get_filenames(fn)
    framecounts = []
    
    if maxframes>=0:
        maxframes += startframe
        
    for name in filenames:
        with tifffile.TiffFile(name) as tif:
            framecount = len(tif.pages)
            framecounts.append(framecount)
            numframes += framecount
            
    numframes -= startframe

    #print(f'reading tiff file: {maxframes}/{numframes}')

    if maxframes>=0 and maxframes<numframes: 
        numframes=maxframes
        
    with tqdm.tqdm(total=numframes) as pbar:
        index = 0
        for t,name in enumerate(filenames):
            # TODO: Fix bug when maxframes is >=0
            if startframe>=framecounts[t]:
                startframe-=framecounts[t]
                continue
            with tifffile.TiffFile(name) as tif:
                fn_ = name.replace(os.path.dirname(fn)+"/",'')
                pbar.set_description(f"Reading {fn_}")

                for i in np.arange(startframe,framecounts[t]):
                    pbar.update(1)
                    if index % 20 == 0 and update_cb is not None:
                        if not update_cb(f"Reading {fn_} - frame {index}/{numframes}", index/numframes):
                            print(f"Aborting reading tiff file..")
                            return
                        
                    yield index, tif.pages[i].asarray()
                    index += 1
                    
                    if index == maxframes:
                        return
                startframe=0


def tiff_get_image_size(fn):
    with tifffile.TiffFile(fn) as tif:
        shape = tif.pages[0].asarray().shape
        return shape

def tiff_get_movie_size(fn):
    names = tiff_get_filenames(fn)
    numframes = 0
    for name in names:
        with tifffile.TiffFile(name) as tif:
            numframes += len(tif.pages)
            shape = tif.pages[0].asarray().shape
    return shape, numframes
    

def tiff_read_all(fn):
    shape,nframes = tiff_get_movie_size(fn)

    mov = np.zeros((nframes,*shape), dtype=np.uint16)
    for i,f in tiff_read_file(fn):
        mov[i] = f
    return mov

    
            
        
    
