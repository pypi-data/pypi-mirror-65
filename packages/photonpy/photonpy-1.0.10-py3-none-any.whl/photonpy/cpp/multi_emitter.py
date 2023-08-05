# -*- coding: utf-8 -*-

import ctypes
import numpy as np
import numpy.ctypeslib as ctl

from .estimator import Estimator
from .context import Context

def create_estimator(psf:Estimator, numEmitters, ctx:Context):
    smlmlib = ctx.smlm.lib
        
    InstancePtrType = ctypes.c_void_p

    fn = smlmlib.MultiEmitter_CreateEstimator
    fn.argtypes = [
        InstancePtrType,
        ctypes.c_int32,
        ctypes.c_void_p]
    fn.restype = ctypes.c_void_p
    
    inst = fn(psf.inst, numEmitters, ctx.inst)
    
    return Estimator(ctx, inst)
    
