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

from raodata.SRHFits import SRHFits
from raodata.Frame import Frame
from raodata.FrameSet import FrameSet

class SRHFolder:
    def __init__(self, path=''):
        filenames= sorted([i for i in glob.glob(os.path.join(os.path.abspath(path), "*"))])
        self._raw_files = []

        for filename in filenames:
            self._raw_files.append(SRHFits(filename))

        t =[]
        file_index = []
        index_in_file = []
        for i, raw in enumerate(self._raw_files):
            t.append(raw.time.jd)
            sh = np.shape(raw.time)
            file_index.append(np.full(sh[1],i))
            index_in_file.append(np.arange(sh[1]))

        self.time = Time(np.concatenate(t, axis = 1), format = 'jd')
        self._file_index = np.concatenate(file_index)
        self._index_in_file = np.concatenate(index_in_file)

        self._frequency = self._raw_files[0]._frequency

    def _get_frame_by_index(self, time_index = 0, frequency_index = 0):
        time_ind = int(self._index_in_file[time_index])
        raw_file = self._raw_files[int(self._file_index[time_index])]
        return(raw_file._get_frame_by_index(time_index = time_ind, \
                           frequency_index = frequency_index))

    def get_frames_by_time_range(self, time_start, time_stop, frequency_index = 0, skip = 0):
        """
        Returns array of the data frames in the specified time range

        Parameters:
        ----------
        time_start -- start time. Should be instance of astropy.time.Time
        time_stop  -- stop  time. Should be instance of astropy.time.Time

        Keyword parameters:
        ------------------
        frequency_index -- frequency channel number (defualt:0)
        skip -- number of frames to skip. skip = 3 means that every 4-th frame will be extracted
        """
        
        cad = skip + 1
        
        t =self.time[frequency_index,:]
        ind = np.argwhere(np.logical_and(time_start < t, t < time_stop))
        result = []
        for i in ind:
            if ((ind[0] - i) % cad == 0) :
                result.append(self._get_frame_by_index(time_index = i, \
                               frequency_index = frequency_index))
        return(FrameSet(result))
    def get_frame_by_time(self, time, frequency_index = 0):
        """
        Returns data frame closest to the specified time
        
        Parameters:
        ----------
        time -- Time of interest. Should be the instance of astropy.time.Time
        
        Keyword parameters:
        ------------------
        frequency_index -- frequency channel number (defualt:0)
        """
        t =self.time[frequency_index,:]
        ind = np.argmin( abs(t - time))
        return self._get_frame_by_index(time_index = ind,\
                     frequency_index = frequency_index)
