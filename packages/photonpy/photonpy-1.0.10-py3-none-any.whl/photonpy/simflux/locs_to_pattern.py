# -*- coding: utf-8 -*-


import os
import numpy as np
import matplotlib.pyplot as plt

from photonpy.utils.picasso_hdf5 import load as load_hdf5
from photonpy.utils.findpeak1D import quadraticpeak
from photonpy.utils.dftpeak import dft_points

from photonpy.cpp.lib import SMLM
from photonpy.cpp.context import Context
from photonpy.cpp.gaussian import Gaussian



def compute_k(angle,pitch):
    k = 2*np.pi/pitch
    kx = np.cos(angle)*k
    ky = np.sin(angle)*k
    return kx,ky




def compute_mod(pattern_frames, angles, pitch, phase, depth, relint):
    mod = np.zeros( (np.array(pattern_frames).size, 5) )
    for i,af in enumerate(pattern_frames):
        kx,ky = compute_k(angles[i],pitch[i])
        mod[af,0] = kx
        mod[af,1] = ky
        mod[af,2] = depth[i]
        mod[af,3] = phase[i]
        mod[af,4] = relint[i]
    return mod

def mod_angle_and_pitch(mod, pattern_frames):
    angles = np.zeros(len(pattern_frames))
    pitch = np.zeros(len(pattern_frames))
    for i in range(len(pattern_frames)):
        kx = np.mean(mod[pattern_frames[i],0])
        ky = np.mean(mod[pattern_frames[i],1])
        angles[i] = np.arctan2(ky,kx)
        freq = np.sqrt(kx**2+ky**2)
        pitch[i] = 2*np.pi/freq
    return angles,pitch
    
def result_dir(path):
    dir, fn = os.path.split(path)
    return dir + "/results/" + os.path.splitext(fn)[0] + "/"

def _spots_per_frame(frame_indices):
    """
    Returns a list of arrays k=0..K-1, where each array k holds the spot indices for frame k
    """
    if len(frame_indices) == 0: 
        numFrames = 0
    else:
        numFrames = np.max(frame_indices)+1
    
    frames = [[] for i in range(numFrames)]
    for k in range(len(frame_indices)):
        frames[frame_indices[k]].append(k)
    for f in range(numFrames):
        frames[f] = np.array(frames[f], dtype=int)
    return frames
    
def _draw_spots(img, x, y, I, sigmaX, sigmaY, smlm:SMLM):
    # Spots is an array with rows: [ x,y, sigmaX, sigmaY, intensity ]
    img = np.ascontiguousarray(img, dtype=np.float32)

    spots = np.zeros((len(x), 5), dtype=np.float32)
    spots[:, 0] = x
    spots[:, 1] = y
    spots[:, 2] = sigmaX
    spots[:, 3] = sigmaY
    spots[:, 4] = I

    ctx=Context(smlm)
    return Gaussian(ctx).Draw(img, spots)




def _find_dft2_peak(spots, peak_xy, frames,num_patterns, pattern_indices, smlm:SMLM, outdir):
    S = 0.02
    kxrange = np.linspace(peak_xy[0]-S, peak_xy[0]+S, 50)
    kyrange = np.linspace(peak_xy[1]-S, peak_xy[1]+S, 50)

    img = np.zeros((len(kyrange),len(kxrange)))
    for ep in pattern_indices:
        indices = np.concatenate(frames[ep::num_patterns])
        xyI = spots[indices][:, [0,1,2]]
        sig = dft_points(xyI, kxrange, kyrange, smlm, useCuda=True)
        img += np.abs(sig**2)
        
    plt.imsave(outdir + f"pattern-{pattern_indices}-FFT-peak.png", img)
    
    peak = np.argmax(img)
    peak = np.unravel_index(peak, img.shape)

    kx_peak = quadraticpeak(img[peak[0], :], kxrange, npts=11, plotTitle=None)#='X peak')
    ky_peak = quadraticpeak(img[:, peak[1]], kyrange, npts=11, plotTitle=None)#='Y peak')

    return kx_peak, ky_peak


def _estimate_angle_and_pitch_dft(imgshape, spots, frames, num_patterns, pattern_indices, smlm:SMLM, freq_minmax, outdir):
    h,w=imgshape

    zoom = 6
    sigma = 1
    ft_sum = np.zeros((h*zoom,w*zoom))
    for ep in pattern_indices:
        indices = np.concatenate(frames[ep::num_patterns])
        img = np.zeros((h*zoom,w*zoom))
        img = _draw_spots(img,spots[indices,0]*zoom,spots[indices,1]*zoom,spots[indices,2],sigma,sigma,smlm)
        ft_img = smlm.FFT2(img)
        ft_sum += np.abs(ft_img**2)
    ft_sum = np.fft.fftshift(ft_sum)
    
    freq = np.fft.fftshift( np.fft.fftfreq(h*zoom) )*zoom*2*np.pi
    XFreq, YFreq = np.meshgrid(freq,freq)
    Freq = np.sqrt(XFreq**2+YFreq**2)
    
    mask = (Freq>freq_minmax[0]) & (Freq<freq_minmax[1])
    plt.imsave(outdir + f"pattern-{pattern_indices}-FFT-mask.png", mask)
    plt.imsave(outdir + f"pattern-{pattern_indices}-FFT.png", ft_sum)
    ft_sum[~mask] = 0
    
    max_index = np.argmax(ft_sum)
    max_indices = np.unravel_index(max_index, ft_sum.shape)

    yx = freq[list(max_indices)]
    xy = _find_dft2_peak(spots, yx[[1,0]], frames, num_patterns, pattern_indices, smlm, outdir)
    
    ang = np.arctan2(xy[1],xy[0])
    freq = np.sqrt(xy[0]**2+xy[1]**2)
    return ang,2*np.pi/freq
    



def estimate_pitch_and_angle(locs_hdf5_fn, patterns_per_angle, freq_minmax=[1.8,1.9]):
    num_patterns = np.size(patterns_per_angle)
    estim, framenum, crlb, imgshape = load_hdf5(locs_hdf5_fn)
    frames = _spots_per_frame(framenum)
    
    outdir = result_dir(locs_hdf5_fn)
    os.makedirs(outdir,exist_ok=True)

    num_angles = len(patterns_per_angle)
    angles = np.zeros(num_angles)
    pitch = np.zeros(num_angles)
    
    with SMLM() as smlm:
        for i,p in enumerate(patterns_per_angle):
            angles[i],pitch[i] = _estimate_angle_and_pitch_dft(imgshape, estim, frames, num_patterns, p, smlm, freq_minmax, outdir)
            print(f"Frames {p}: Angle: {angles[i]:.5f} rad, Pitch: {pitch[i]:.5f}, Freq={2*np.pi/pitch[i]:.5f}" )

    return angles,pitch



def get_shifts(phases):
    shifts = (np.diff(phases[-1::-1]) % (2*np.pi))
    shifts[shifts > np.pi] = 2*np.pi - shifts[shifts>np.pi]
    return shifts


def _estimate_phase_and_depth_simple(spots, angle, pitch, ep, frames, num_patterns):
    idx = np.concatenate(frames[ep::num_patterns])
    
    kx,ky = compute_k(angle,pitch)
    
    spotPhaseField = spots[idx,0]*kx+spots[idx,1]*ky

    I0 = np.sum(spots[idx, 2])
    Iw = np.sum(spots[idx, 2] * np.exp(-1j * spotPhaseField))

    phase = -np.angle(Iw / I0 * 1j)
    depth = 2 * np.abs(Iw / I0)
    return phase, depth

def estimate_phase_and_depth(locs_hdf5_fn, angle, pitch, pattern_frames):
    num_patterns = np.size(pattern_frames)

    estim, framenum, crlb, imgshape = load_hdf5(locs_hdf5_fn)
    framespots = _spots_per_frame(framenum)

    num_phase_steps = len(pattern_frames[0])
    phase = np.zeros((len(angle),num_phase_steps))
    depth = np.zeros((len(angle),num_phase_steps))
    relint = np.zeros((len(angle),num_phase_steps))

    for a,pf in enumerate(pattern_frames):
        for step, fr in enumerate(pf):
            phase[a,step],depth[a,step] = _estimate_phase_and_depth_simple(estim, angle[a], pitch[a], fr, framespots, num_patterns)
            spot_indices = np.concatenate(framespots[fr::num_patterns])
            relint[a,step] = np.sum(estim[spot_indices,2])

    relint /= np.sum(relint)

    for a,pf in enumerate(pattern_frames):
        for step, fr in enumerate(pf):
            print(f"Angle {angle[a]:.3f} rad: Step {step}: Phase={np.rad2deg(phase[a,step]):.3f}, Depth={depth[a,step]:.3f}" )
        with np.printoptions(precision=3, suppress=True):
            print(f"Shifts: {np.rad2deg(get_shifts(phase[a]))}")
   
    return phase, depth, relint


def estimate_phase_depth_adv(spots, angle, pitch, ibg, pattern_frames):
    ...
    