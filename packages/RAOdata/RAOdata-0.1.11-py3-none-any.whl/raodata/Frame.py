from astropy.io import fits
from datetime import timedelta
import numpy as np
from scipy import optimize
from scipy.optimize import minimize
from astropy.time import Time, TimeDelta
import glob, os, time, requests
import os.path
import ephem
from matplotlib import pyplot as plt

def get_circle(xs, ys, cx, cy, r):
    x = np.arange(xs) # x values
    y = np.arange(ys) # y values
    xx, yy = np.meshgrid(x, y) # combine both vectors


    condition = (xx-cx)**2 + (yy-cy)**2 <= r**2
    model = np.exp(-(((xx-cx)**2 + (yy-cy)**2)/r**2)**100)
    return model


class Frame:

    def get_visibilities(self, original = False):
        vis_cal_r=np.zeros(self._vis_r.shape, dtype=self._vis_r.dtype)
        vis_cal_l=np.zeros(self._vis_r.shape, dtype=self._vis_r.dtype)
        vis_cal_r[:]=1.0
        vis_cal_l[:]=1.0
        na = np.max(self._ant1)+1
        gains_r = self.gains_r
        gains_l = self.gains_l
        amp_r = self._amp_r
        amp_l = self._amp_l

        #Van VLeck correction
        vis_r = self._vis_r.copy()
        vis_l = self._vis_l.copy()

        vis_r.real = np.sin(np.pi * 0.5 * vis_r.real)
        vis_r.imag = np.sin(np.pi * 0.5 * vis_r.imag)

        vis_l.real = np.sin(np.pi * 0.5 * vis_l.real)
        vis_l.imag = np.sin(np.pi * 0.5 * vis_l.imag)

        if original:
            gains_r = gains_r*0. + 1.
            gains_l = gains_l*0. + 1.
        for i in range(0, na):
            items_0 = np.where(self._ant1 == i)[0]
            vis_cal_r[items_0] =\
            vis_cal_r[items_0]*gains_r[i]*np.sqrt(amp_r[i])
            vis_cal_l[items_0] =\
            vis_cal_l[items_0]*gains_l[i]*np.sqrt(amp_l[i])
            items_1 = np.where(self._ant2 == i)[0]
            vis_cal_r[ items_1] =\
            vis_cal_r[ items_1]*np.conj(gains_r[i])#*np.sqrt(amp_r[i])
            vis_cal_l[ items_1] =\
            vis_cal_l[ items_1]*np.conj(gains_l[i])#*np.sqrt(amp_l[i])
        return(vis_r * vis_cal_r, vis_l * vis_cal_l)

    def get_correlation_coefficient(self):
        #self._uvw_calculate()
        #uv_dist = np.sqrt(self._uvw[0,:]**2 + self._uvw[1,:]**2)
        #thr = np.min(uv_dist)*3.
        #ind = np.where(uv_dist < thr)
        vis_r, vis_l = self.get_visibilities()
        cor_I = np.sum(np.abs(vis_r + vis_l))
        cor_V = np.sum(np.abs(vis_r - vis_l))
        return(cor_I, cor_V)

    def update_mask(self, threshold = 10.):
        abs_gr = np.abs(self.gains_r)
        abs_gl = np.abs(self.gains_l)
        abs_gr /= np.median(abs_gr)
        abs_gl /= np.median(abs_gl)
        ant1 = self._ant1
        ant2 = self._ant2
        n_bases = ant1.shape[0]

        self.mask_r = np.ones(n_bases, dtype = np.float)
        self.mask_l = np.ones(n_bases, dtype = np.float)
        self.mask_r[0] = 0.
        self.mask_l[0] = 0.
        self.mask_r[512:] = 0.
        self.mask_l[512:] = 0.

        for i in range(n_bases):
            crit_r = abs_gr[ant1[i]] * abs_gr[ant2[i]]
            crit_l = abs_gl[ant1[i]] * abs_gl[ant2[i]]
            if crit_r > threshold:
                self.mask_r[i] = 0.
            if crit_l > threshold:
                self.mask_l[i] = 0.


class FrameSet:
    def __init__(self, frames):
        self._frames = frames
        time = []
        for frame in frames:
            time.append(frame.time)
        self.time = Time(time)

    def __getitem__(self, key):
        return(self._frames[key])

    def __len__(self):
        return(len(self._frames))

    def get_gains(self):
        n = len(self._frames)
        na = self._frames[0]._ant1
        gains_r = np.ones([n,na],dtype = np.complex128)
        gains_l = np.ones([n,na],dtype = np.complex128)

        for i in range(n):
            gains_r[i,:] = self._frames[i].gains_r
            gains_l[i,:] = self._frames[i].gains_l
        return(gains_r, gains_l)

    def get_correlation_coefficient(self):
        n = len(self._frames)
        cor_I = np.zeros(n)
        cor_V = np.zeros(n)
        for i in range(0,n):
            cor_I[i], cor_V[i] = self._frames[i].get_correlation_coefficient()
        return(cor_I, cor_V, self.time)
