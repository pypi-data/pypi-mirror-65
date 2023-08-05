# -*- coding: utf-8 -*-

import ctypes
import scipy.io
import numpy as np
import numpy.ctypeslib as ctl

from . import estimator
from .context import Context

Theta = ctypes.c_float * 5
FisherMatrix = ctypes.c_float * 16


class CSpline_Calibration(ctypes.Structure):
    _fields_ = [
        ("n_voxels_x", ctypes.c_int),
        ("n_voxels_y", ctypes.c_int),
        ("n_voxels_z", ctypes.c_int),
        ("nmeth", ctypes.c_int),
        ("z_min", ctypes.c_float),
        ("z_max", ctypes.c_float),
        ("coefs", ctl.ndpointer(np.float32, flags="aligned, c_contiguous")),
    ]

    def __init__(self, n_voxels_x, n_voxels_y, n_voxels_z, nmeth, z_min, z_max,
                 coefs, n_zslices:int, n_pixels:int, z_range:float):
        if nmeth:
            coefs = np.asfortranarray(coefs, dtype=np.float32)
            #coefs = np.ascontiguousarray(coefs, dtype=np.float32)

        else:
            coefs = np.ascontiguousarray(coefs, dtype=np.float32)
        self.coefsx = coefs  # Hack to make sure the array doesn't get GCed

        self.coefs = coefs.ctypes.data
        self.n_voxels_x = n_voxels_x
        self.n_voxels_y = n_voxels_y
        self.n_voxels_z = n_voxels_z
        self.nmeth = nmeth
        self.z_min = z_min
        self.z_max = z_max
        self.zrange = [z_min,z_max] # also available for other calibration objects

        # this parameters are available ONLY from python
        #   number of z slices in one PSF
        self.n_zslices = n_zslices
        #   ROI size
        self.n_pixels = n_pixels
        #   full z range in nm. PSF changes in interval [-z_range/2, +z_range/2]
        self.z_range = z_range
        ###

    @classmethod
    def from_file(cls, filename):
        if filename.endswith('.mat'):
            return cls.from_file_nmeth(filename)

        calibration = np.load(filename, allow_pickle=True)

        # Calibration file has z in nm, we use um
        z_min = calibration["zmin"] * 1e-3
        z_max = calibration["zmax"] * 1e-3

        coefs = calibration["coeff"]
        n_voxels_x = coefs.shape[0] + 1
        n_voxels_y = coefs.shape[1] + 1
        n_voxels_z = coefs.shape[2] + 1

        return cls(n_voxels_x, n_voxels_y, n_voxels_z, 0, z_min, z_max, coefs,
                   n_zslices=None, n_pixels=None, z_range=z_max-z_min)

    @classmethod
    def from_file_nmeth(cls, filename):
        mat = scipy.io.loadmat(filename)
        try:
            spline = mat["SXY"]['cspline'].item()
            coefs = spline['coeff'].item()
            dz = float(spline['dz'].item())
        except KeyError:
            spline = mat['cspline'].item()
            coefs = spline[0]
            dz = float(spline[1])

        # reading additional parameters from .mat file from Nature methods paper
        try:
            dz = float( mat['parameters']['dz'][0][0] )
            # full z range in nm. PSF changes in [-z_range/2, +z_range/2]
            z_range = float( mat['parameters']['gaussrange'][0][0][0][1] ) * 2.0
            n_zslices = int( z_range / dz + 1 )
            n_pixels = int( mat['parameters']['ROIxy'][0][0] )
            z_range *= 0.001
        except KeyError:
            raise Exception( "Required parameters for C-spline can\'t be"
                             " found in the .mat file" )
        ###

        nz = float(coefs.shape[2])
        z_min = -nz * dz * 1e-3 / 2
        z_max = (nz-1) * dz * 1e-3 / 2

        n_voxels_x = coefs.shape[0] + 1
        n_voxels_y = coefs.shape[1] + 1
        n_voxels_z = coefs.shape[2] + 1
        print(f"Z min={z_min}, max={z_max}" )
        print(f"Voxels X:{n_voxels_x}, Y:{n_voxels_y}, Z:{n_voxels_z}")
        return cls(n_voxels_x, n_voxels_y, n_voxels_z, 1, z_min, z_max, coefs,
                   n_zslices, n_pixels, z_range)

    def __str__( self ):
        """Print the parameters"""

        s = f'n_zslices = {self.n_zslices}\n'
        s += f'full z range = {self.z_range} um\n'
        s += f'z_min = {self.z_min} um\n'
        s += f'z_max = {self.z_max} um\n'
        s += f'n_voxels X = {self.n_voxels_x}\n'
        s += f'n_voxels Y = {self.n_voxels_y}\n'
        s += f'n_voxels Z = {self.n_voxels_z}\n'
        s += f'NMethods is used = {self.nmeth}\n'

        return s


class CSplinePSF(estimator.Estimator):
    def __init__(self, ctx:Context, inst, calib):
        super().__init__(ctx, inst, calib)
        
        
class CSpline:
    def __init__(self, ctx: Context):
        smlmlib = ctx.smlm.lib
        self.ctx = ctx

        self._CSpline_CreatePSF_XYZIBg = smlmlib.CSpline_CreatePSF_XYZIBg
        self._CSpline_CreatePSF_XYZIBg.argtypes = [
                ctypes.c_int32,
                ctypes.POINTER(CSpline_Calibration),
                ctypes.c_float,
                ctypes.c_int32,
                ctypes.c_void_p]
        self._CSpline_CreatePSF_XYZIBg.restype = ctypes.c_void_p

    def CreatePSF_XYZIBg(self, roisize, calib: CSpline_Calibration, cuda, LM_lambda=1) -> estimator.Estimator:
        inst = self._CSpline_CreatePSF_XYZIBg(roisize, calib, LM_lambda, cuda, self.ctx.inst)
        return CSplinePSF(self.ctx, inst, calib)
    
    


