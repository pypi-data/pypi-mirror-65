# -*- coding: utf-8 -*-

from .context import Context
from .estimator import Estimator
import ctypes as ct
    

def create_estimator(roisize, ctx: Context=None):
    smlmlib = ctx.smlm.lib

    fn = smlmlib.CreateCenterOfMassEstimator
    fn.argtypes = [
            ct.c_int32,
            ct.c_void_p]
    fn.restype = ct.c_void_p

    inst = fn(roisize, ctx.inst)
    return Estimator(ctx, inst)


