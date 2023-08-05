import ctypes as ct
import numpy as np
import numpy.ctypeslib as ctl
from .lib import NullableFloatArrayType
from .context import Context


class EstimatorProperties(ct.Structure):
    _fields_ = [
	#int numParams, sampleCount, numDiag, numConst, sampleIndexDims;
        ("numParams", ct.c_int),
        ("sampleCount", ct.c_int),
        ("numDiag", ct.c_int),
        ("numConst", ct.c_int),
        ("sampleIndexDims", ct.c_int)
    ]
    

class Estimator:
    def __init__(self, ctx:Context, psfInst, calib=None):
        self.inst = psfInst
        self.ctx = ctx
        self.calib = calib
        lib = ctx.smlm.lib

        InstancePtrType = ct.c_void_p

        self._Estimator_Delete = lib.Estimator_Delete
        self._Estimator_Delete.argtypes = [InstancePtrType]

        self._Estimator_ParamFormat = lib.Estimator_ParamFormat
        self._Estimator_ParamFormat.restype = ct.c_char_p
        self._Estimator_ParamFormat.argtypes = [InstancePtrType]
        
        self._Estimator_GetProperties = lib.Estimator_GetProperties
        self._Estimator_GetProperties.argtypes = [
            InstancePtrType,
            ct.POINTER(EstimatorProperties)
        ]
        
        self._Estimator_SampleDims = lib.Estimator_SampleDims
        self._Estimator_SampleDims.argtypes = [
            InstancePtrType,
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous")
        ]        

        # CDLL_EXPORT void Estimator_ComputeExpectedValue(PSF* psf, int numspots, const float* params, const float* constants, const int* spotpos, float* ev);
        self._Estimator_ComputeExpectedValue = lib.Estimator_ComputeExpectedValue
        self._Estimator_ComputeExpectedValue.argtypes = [
            InstancePtrType,
            ct.c_int32,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), #Param 
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # constants
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # spotpos
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # ev
        ]

        # CDLL_EXPORT void Estimator_ComputeFisherMatrix(PSF* psf, int numspots, const float* params, const float* constants,const int* spotpos,  float* fi);
        self._Estimator_ComputeFisherMatrix = lib.Estimator_ComputeFisherMatrix
        self._Estimator_ComputeFisherMatrix.argtypes = [
            InstancePtrType,
            ct.c_int32,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # spotpos
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), #fi
        ]

        # CDLL_EXPORT void Estimator_ComputeDerivatives(PSF* psf, int numspots, const float* Param, const float* constants, const int* spotpos, float* derivatives, float* ev);
        self._Estimator_ComputeDerivatives = lib.Estimator_ComputeDerivatives
        self._Estimator_ComputeDerivatives.argtypes = [
            InstancePtrType,
            ct.c_int32,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # spotpos
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),
        ]
        
        self.fitInfoDType = np.dtype([('likelihood', '<f4'), ('iterations', '<i4')])

        # CDLL_EXPORT void Estimator_ComputeMLE(PSF* psf, int numspots, const float* sample, const float* constants,const int* spotpos, 
        # const float* initial, float* params, int* iterations, int maxiterations, float levmarAlpha, float* trace, int traceBufLen);
        self._Estimator_Estimate = lib.Estimator_Estimate
        self._Estimator_Estimate.argtypes = [
            InstancePtrType,
            ct.c_int32,
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # sample
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # constants
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # spotpos
            NullableFloatArrayType,  # initial
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # Param
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # diagnostics
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # iterations
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # tracebuf [params*numspots*tracebuflen]
            ct.c_int32,
        ]
        
        props = EstimatorProperties()
        self._Estimator_GetProperties(self.inst, props)
        
        self.numparams = props.numParams
        self.numconst = props.numConst
        self.samplecount = props.sampleCount
        self.indexdims = props.sampleIndexDims
        self.sampleshape = np.zeros(self.indexdims,dtype=np.int32)
        self._Estimator_SampleDims(self.inst, self.sampleshape)
        self.numdiag = props.numDiag
        self.fmt = self.ParamFormat()
        self.colnames = [s.strip() for s in self.fmt.split(',')]

        #print(f"Created PSF Parameters: {self.fmt}, #const={self.numconst}. #diag={self.numdiag} samplesize={self.sampleshape}." )

    def _checkparams(self, params, constants, roipos):
        params = np.array(params)
        if len(params.shape) == 1:
            params = [params]
        params = np.ascontiguousarray(params, dtype=np.float32)
        numspots = len(params)
        if constants is None:
            constants = np.zeros((numspots, self.numconst), dtype=np.float32)
        else:
            constants = np.ascontiguousarray(constants, dtype=np.float32)
            assert(np.array_equal(constants.shape, [numspots, self.numconst]))
        if roipos is None:
            roipos = np.zeros((numspots, self.indexdims), dtype=np.int32)
        else:
            roipos = np.ascontiguousarray(roipos, dtype=np.int32)
            assert(np.array_equal( roipos.shape, [numspots, self.indexdims]))

        if params.shape[1] != self.numparams:
            print(f"{self.fmt} expected, {params.shape[1]} parameters given")
            assert(params.shape[1]==self.numparams)
        return params,constants,roipos

    def ExpectedValue(self, params, roipos=None, constants=None):
        params,constants,roipos=self._checkparams(params,constants,roipos)
        ev = np.zeros((len(params), *self.sampleshape), dtype=np.float32)
        if len(params)>0:
            self._Estimator_ComputeExpectedValue(self.inst, len(params), params, constants, roipos, ev)
        return ev

    def GenerateSample(self, params, roipos=None, constants=None):
        ev = self.ExpectedValue(params, roipos, constants)
        return np.random.poisson(ev)

    def FisherMatrix(self, params, roipos=None, constants=None):
        params,constants,roipos=self._checkparams(params,constants,roipos)
        fi = np.zeros((len(params), self.numparams, self.numparams), dtype=np.float32)
        if len(params)>0:
            self._Estimator_ComputeFisherMatrix(self.inst, len(params), params, constants, roipos, fi)
        return fi

    def CRLB(self, params, roipos=None, constants=None):
        fisher = self.FisherMatrix(params, roipos, constants)
        var = np.linalg.inv(fisher)
        crlb = np.sqrt(np.abs(var[:,np.arange(self.numparams),np.arange(self.numparams)]))
        return crlb
    
    def Derivatives(self, params, roipos=None, constants=None):
        params,constants,roipos=self._checkparams(params,constants,roipos)
        deriv = np.zeros((len(params), self.numparams, *self.sampleshape), dtype=np.float32)
        ev = np.zeros((len(params), *self.sampleshape), dtype=np.float32)
        if len(params)>0:
            self._Estimator_ComputeDerivatives(self.inst, len(params), params, constants, roipos, deriv, ev)
        return deriv, ev
    
    def NumDeriv(self, params, roipos=None, constants=None, eps=1e-6):
        """
        Compute numerical derivate based on the output of ExpectedValue
        """
        params,constants,roipos=self._checkparams(params,constants,roipos)
        ev = self.ExpectedValue(params,roipos,constants)
        deriv = np.zeros((len(params), self.numparams, *self.sampleshape), dtype=np.float32)
        
        for k in range(self.numparams):
            params_min = params*1
            params_min[:,k] -= eps
            params_max = params*1
            params_max[:,k] += eps
            ev_min = self.ExpectedValue(params_min, roipos, constants)
            ev_max = self.ExpectedValue(params_max, roipos, constants)
            deriv[:,k] = (ev_max-ev_min)/(2*eps)
        
        return deriv, ev
    
    def NumCRLB(self, params, roipos=None, constants=None, eps=1e-4, useNumDeriv=True):
        if useNumDeriv:
            deriv,ev = self.NumDeriv(params,roipos,constants,eps)
        else:
            deriv,ev = self.Derivatives(params,roipos,constants)

        K = self.numparams
        deriv = np.reshape(deriv, (len(params), K, self.samplecount))
        ev[ev<1e-9] = 1e-9
        fi = np.zeros((len(params), K,K))
        for i in range(K):
            for j in range(K):
                fi[:,i,j] = np.sum(1/ev * (deriv[:,i] * deriv[:,j]), axis=1)
        var = np.linalg.inv(fi)
        return np.sqrt(np.abs(var[:,np.arange(self.numparams),np.arange(self.numparams)]))

    def Estimate(self, imgs, roipos=None, constants=None, initial=None, maxiterations=50, levmarInitialAlpha=0.1):
        numspots = len(imgs)
        
        imgs = np.ascontiguousarray(imgs, dtype=np.float32)
        assert np.array_equal(imgs.shape, [numspots, *self.sampleshape])
        traceBufLen = maxiterations
        iterations = np.zeros(numspots, np.int32)
        params = np.zeros((numspots, self.numparams), dtype=np.float32)
        trace = np.zeros((numspots, traceBufLen, self.numparams), dtype=np.float32)
        diag = np.zeros((numspots, self.numdiag), dtype=np.float32)

        params,constants,roipos = self._checkparams(params,constants,roipos)

        if initial is not None:
            initial = np.ascontiguousarray(initial, dtype=np.float32)
            assert len(initial) == numspots

        if numspots>0:
            self._Estimator_Estimate(
                self.inst,
                numspots,
                imgs,
                constants,
                roipos,
                initial,
                params,
                diag,
                iterations,
                trace,
                traceBufLen
            )

        traces = []
        for k in range(numspots):
            traces.append(trace[k, 0 : iterations[k], :])

        return params, diag, traces

    def Destroy(self):
        if self.inst is not None:
            self._Estimator_Delete(self.inst)
            self.inst = None

    def NumConstants(self):
        return self.numconst

    def ParamFormat(self):
        return self._Estimator_ParamFormat(self.inst).decode("utf-8") 
    
    def ParamIndex(self, paramName):
        if type(paramName)==list:
            return [self.colnames.index(n) for n in paramName]
        return self.colnames.index(paramName)

    def NumParams(self):
        return self.numparams

    def SampleCount(self):
        return self.samplecount
    
    def NumDiag(self):
        return self.numdiag
    
    def Draw(self, image, params, roiposYX, constants=None):
        rois = self.ExpectedValue(params, roiposYX, constants)
        return self.ctx.smlm.DrawROIs(image, rois, roiposYX)
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.Destroy()


    @staticmethod 
    def CopyROI_Create(psf, ctx:Context):
        _CopyROI_CreatePSF = ctx.smlm.lib.CopyROI_CreatePSF
        _CopyROI_CreatePSF.argtypes = [
                ct.c_void_p,
                ct.c_void_p]
        _CopyROI_CreatePSF.restype = ct.c_void_p

        inst = _CopyROI_CreatePSF(psf.inst, ctx.inst if ctx else None)
        psf = Estimator(ctx, inst)
        return psf
