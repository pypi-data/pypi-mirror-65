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

#from calibration.utils import frequency_to_qs
from raodata.Frame import Frame


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
