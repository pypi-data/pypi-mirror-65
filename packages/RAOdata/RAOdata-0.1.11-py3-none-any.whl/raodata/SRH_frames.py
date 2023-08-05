#!/usr/bin/env python3


from datetime import datetime
from raodata.Data import Data
from raodata.File import File
from raodata.SRHFits import SRHFits
from raodata.SRHFolder import SRHFolder
from raodata import exceptions
import logging
import zeep
from zeep import Client
import requests
import time
import numpy as np
from astropy.time import Time
from dateutil import parser
import os



class SRH_frames():
    '''This class is used to retrieve RAO archive meta data'''

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

        _files = Data().get_srh_in_time(parser.parse(time))
        time = Time(time)
        for _f in _files:
            _f.download()
            _file = SRHFits(_f.local_name)

        t = []
        file_index = []
        index_in_file = []

        t.append(_file.time.jd)
        sh = np.shape(_file.time)
        file_index.append(np.full(sh[1],1))
        index_in_file.append(np.arange(sh[1]))

        self._file_index = np.concatenate(file_index)
        self._index_in_file = np.concatenate(index_in_file)
        self.time = Time(np.concatenate(t, axis = 1), format = 'jd')

        t =self.time[frequency_index,:]
        time_index = np.argmin( abs(t - time))
        time_ind = int(self._index_in_file[time_index])

        return(_file._get_frame_by_index(time_index = time_ind, \
                           frequency_index = frequency_index))


    def get_frames_by_time_range(self, time_start, time_stop, frequency_index = 0, skip = 0):
        """
        Returns data frame closest to the specified time

        Parameters:
        ----------
        time -- Time of interest. Should be the instance of astropy.time.Time

        Keyword parameters:
        ------------------
        frequency_index -- frequency channel number (defualt:0)
        """

        _files = Data().get_files("SRH", "fits",
                                 parser.parse(time_start),
                                 parser.parse(time_stop))
        _files = list(_files)
        _files.append(list(Data().get_srh_in_time(parser.parse(time_start)))[0])
        _files.append(list(Data().get_srh_in_time(parser.parse(time_stop)))[0])
        time_start = Time(time_start)
        time_stop = Time(time_stop)

        for _f in _files:
            _f.download()

        data = SRHFolder(os.path.dirname((_files[0].local_name)))
        return data.get_frames_by_time_range(time_start, time_stop, frequency_index, skip = 0)

