# -*- coding: utf-8 -*-


import ctypes as ct
import numpy as np
import numpy.ctypeslib as ctl
import time
import copy

from .estimator import Estimator
from .lib import NullableFloatArrayType, NullableIntArrayType

from photonpy.smlm.picasso_hdf5 import save as save_hdf5

class EstimQueue_Results:
    def __init__(self, colnames, sampleshape, estim, diag, fi, crlb, 
                 iterations, ll, roipos, samples, ids):
        self.estim = estim
        self.sampleshape = sampleshape
        self.diagnostics = diag
        self.fisher = fi
        self.crlb = crlb
        self.roipos = roipos
        self.iterations = iterations
        self.ll = ll
        self.ids = ids
        self.samples = samples
        self.colnames = colnames

    def CRLB(self):
        K = self.estim.shape[1]
        var = np.linalg.inv(self.fisher)
        return np.sqrt(np.abs(var[:,np.arange(K),np.arange(K)]))
    
    def SortByID(self, isUnique=False):
        if isUnique:
            order = np.arange(len(self.ids))
            order[self.ids] = order*1
        else:
            order = np.argsort(self.ids)
        self.Filter(order)
        return order       
        
    def Filter(self, indices):
        if indices.dtype == bool:
            indices = np.nonzero(indices)[0]
        
        if len(indices) != len(self.ids):
            print(f"Removing {len(self.ids)-len(indices)}/{len(self.ids)}")
        self.estim = self.estim[indices]
        self.diagnostics = self.diagnostics[indices]
        self.fisher = self.fisher[indices]
        self.roipos = self.roipos[indices]
        self.iterations = self.iterations[indices]
        self.ll = self.ll[indices]
        self.ids = self.ids[indices]
        if self.samples is not None:
            self.samples = self.samples[indices]
        
#        if self.crlb is not None:
 #           self.crlb = self.crlb[indices]
        return indices
        
    def FilterXY(self, minX, minY, maxX, maxY):
        return self.Filter(np.where(
            np.logical_and(
                np.logical_and(self.estim[:,0]>minX, self.estim[:,1]>minY),
                np.logical_and(self.estim[:,0]<maxX, self.estim[:,1]<maxY)))[0])

    def Clone(self):
        return copy.deepcopy(self)
    
    def ColIdx(self, *names):
        return np.squeeze(np.array([self.colnames.index(n) for n in names],dtype=np.int))
        
    @staticmethod
    def Merge(result_list):
        estim=[] 
        diag=[]
        fi=[]
        roipos=[]
        it=[]
        ids=[]
        ll=[]
        for r in result_list:
            estim.append(r.estim)
            diag.append(r.diag)
            fi.append(r.fi)
            roipos.append(r.roipos)
            it.append(r.it)
            ids.append(r.ids)
            ll.append(r.ll)
            
        return EstimQueue_Results(result_list[0].colnames, result_list[0].sampleshape,
                 estim=np.concatenate(estim),
                 diag=np.concatenate(diag),
                 fi=np.concatenate(fi),
                 iterations=np.concatenate(it),
                 ll=np.concatenate(ll),
                 roipos=np.concatenate(roipos),
                 samples=None,
                 ids=np.concatenate(ids))
     
    def SaveHDF5(self,fn, imgshape):        
        idx = self.ColIdx('x','y','I','bg')
        crlb = self.CRLB()
        
        if 'sigma' in self.colnames:
            sx=sy=self.estim[:,self.colnames.index('sigma')]
        elif 'sx' in self.colnames:
            sx=self.estim[:,self.colnames.index('sx')]
            sy=self.estim[:,self.colnames.index('sy')]
        else:
            sx=sy=np.median(crlb[:,self.ColIdx('x','y')])
            
        xyIBg = self.estim[:,idx] * 1
        xyIBg[:,[0,1]] += self.roipos[:,[-1,-2]]
        
        #def save(fn, xyIBg, crlb, framenum, imgshape, sigmaX, sigmaY, extraColumns=None):   
        save_hdf5(fn, xyIBg, crlb[:,idx], self.ids, imgshape, sx, sy)


EstimResultDType = np.dtype([
    ('id','<i4'),('ll','<i4'),('iterations','<i4')
])


class EstimQueue:
    def __init__(self, estim:Estimator, batchSize=256, maxQueueLenInBatches=5, numStreams=-1,ctx=None):
        if ctx is None:
            self.ctx = estim.ctx
        else:
            self.ctx = ctx
        lib = self.ctx.smlm.lib
        self.estim = estim
        self.batchSize = batchSize

        InstancePtrType = ct.c_void_p

#        DLL_EXPORT LocalizationQueue* EstimQueue_CreateQueue(PSF* psf, int batchSize, int maxQueueLen, int numStreams);
        self._EstimQueue_Create = lib.EstimQueue_Create
        self._EstimQueue_Create.argtypes = [
                InstancePtrType, 
                ct.c_int32,
                ct.c_int32,
                ct.c_int32,
                ct.c_void_p]
        self._EstimQueue_Create.restype = InstancePtrType
        
#        DLL_EXPORT void EstimQueue_Delete(LocalizationQueue* queue);
        self._EstimQueue_Delete= lib.EstimQueue_Delete
        self._EstimQueue_Delete.argtypes = [InstancePtrType]
        
#        DLL_EXPORT void EstimQueue_Schedule(LocalizationQueue* q, int numspots, const int *ids, const float* h_samples,
 #       	const float* h_constants, const int* h_roipos);

        self._EstimQueue_Schedule = lib.EstimQueue_Schedule
        self._EstimQueue_Schedule.argtypes = [
                InstancePtrType,
                ct.c_int32,
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"), # ids
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # samples
            NullableFloatArrayType, #initial
            NullableFloatArrayType, #const
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # roipos
                ]
            
#        DLL_EXPORT void EstimQueue_Flush(LocalizationQueue* q);
        self._EstimQueue_Flush = lib.EstimQueue_Flush
        self._EstimQueue_Flush.argtypes = [InstancePtrType]
        
#        DLL_EXPORT bool EstimQueue_IsIdle(LocalizationQueue* q);
        self._EstimQueue_IsIdle = lib.EstimQueue_IsIdle
        self._EstimQueue_IsIdle.argtypes = [InstancePtrType]
        self._EstimQueue_IsIdle.restype = ct.c_bool
        
#        DLL_EXPORT int EstimQueue_GetResultCount(LocalizationQueue* q);
        self._EstimQueue_GetResultCount = lib.EstimQueue_GetResultCount
        self._EstimQueue_GetResultCount.argtypes = [InstancePtrType]
        self._EstimQueue_GetResultCount.restype = ct.c_int32

        self._EstimQueue_GetQueueLength = lib.EstimQueue_GetQueueLength
        self._EstimQueue_GetQueueLength.argtypes = [InstancePtrType]
        self._EstimQueue_GetQueueLength.restype = ct.c_int32
        
#        // Returns the number of actual returned localizations. 
 #       // Results are removed from the queue after copying to the provided memory
#        DLL_EXPORT int EstimQueue_GetResults(LocalizationQueue* q, int maxresults, float* estim, float* diag, float *fi);
        self._EstimQueue_GetResults = lib.EstimQueue_GetResults
        self._EstimQueue_GetResults.argtypes = [
                InstancePtrType,
                ct.c_int32,
                ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # estim
                NullableFloatArrayType, # diag
                NullableFloatArrayType, # fi
                NullableFloatArrayType, # crlb
                ctl.ndpointer(np.int32, flags="aligned, c_contiguous"), # roipos
                NullableFloatArrayType, # samples
                ctl.ndpointer(EstimResultDType, flags="aligned, c_contiguous"), # results
                ]
        self._EstimQueue_GetResults.restype = ct.c_int32
        
        self.colnames = estim.colnames
        
        self.inst = self._EstimQueue_Create(estim.inst,batchSize, maxQueueLenInBatches, numStreams, 
                                           self.ctx.inst if self.ctx else None)
        if not self.inst:
            raise RuntimeError("Unable to create PSF MLE Queue with given PSF")
            
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.Destroy()

    def Destroy(self):
        self._EstimQueue_Delete(self.inst)
        
    def Flush(self):
        self._EstimQueue_Flush(self.inst)
        
    def WaitUntilDone(self):
        self.Flush()
        while not self.IsIdle():
            time.sleep(0.05)

        
    def IsIdle(self):
        return self._EstimQueue_IsIdle(self.inst)
    
    def Schedule(self, samples, roipos=None, ids=None, initial=None, constants=None):
        samples = np.ascontiguousarray(samples,dtype=np.float32)
        numspots = len(samples)

        if roipos is None:
            roipos = np.zeros((numspots,self.estim.indexdims),dtype=np.int32)
            
        if constants is not None:
            constants = np.ascontiguousarray(constants,dtype=np.float32)
            if (self.estim.numconst>0):
                assert(np.array_equal(constants.shape, [numspots, self.estim.numconst]))
        else:
            assert(self.estim.numconst==0)
            
        if initial is not None:
            initial = np.ascontiguousarray(initial, dtype=np.float32)
            assert(np.array_equal(initial.shape, [numspots, self.estim.numparams]))

        roipos = np.ascontiguousarray(roipos, dtype=np.int32)
        assert(np.array_equal(roipos.shape, [numspots, self.estim.indexdims]))
        assert(np.array_equal(self.estim.sampleshape, samples.shape[1:]))
        
        if ids is None:
            ids = np.zeros(numspots,dtype=np.int32)
        else:
            assert len(ids) == len(samples)
            ids = np.ascontiguousarray(ids,dtype=np.int32)
        
        self._EstimQueue_Schedule(self.inst, numspots, ids, samples, initial, constants, roipos)
        
    def GetQueueLength(self):
        return self._EstimQueue_GetQueueLength(self.inst)
    
    def GetResultCount(self):
        return self._EstimQueue_GetResultCount(self.inst)
        
    def GetResults(self,maxResults=None, getSampleData=False) -> EstimQueue_Results:
        count = self._EstimQueue_GetResultCount(self.inst)
        
        if maxResults is not None and count>maxResults:
            count=maxResults
        
        K = self.estim.NumParams()
        estim = np.zeros((count, K),dtype=np.float32)
        diag = np.zeros((count, self.estim.NumDiag()), dtype=np.float32)
        fi = np.zeros((count, K,K), dtype=np.float32)
        crlb = np.zeros((count, K), dtype=np.float32)
        roipos = np.zeros((count, self.estim.indexdims),dtype=np.int32)
        results = np.zeros(count, dtype=EstimResultDType)
        
        if getSampleData:
            samples = np.zeros((count, *self.estim.sampleshape), dtype=np.float32)
        else:
            samples = None

        copied = self._EstimQueue_GetResults(self.inst, count, estim, 
                                             diag, fi, crlb, roipos, samples, results)
        assert(count == copied)
        
        r = EstimQueue_Results(self.colnames, self.estim.sampleshape, 
                                 estim, diag, fi, crlb, results['iterations'], 
                                 results['ll'], roipos, samples, results['id'])
                    
        return r
        


