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


def uvw_calculate(frame):
    #from .utils.rot_xyz import rotx, rotz
    from raodata.rot_xyz import rotx, rotz
    from datetime import timedelta
    import ephem
    from sunpy.coordinates import sun as sunpy_sun

    cs = 299792458.0
    lam= cs/(frame.frequency/1e3*1e9)

    badary = ephem.Observer()
    badary.lon = ephem.degrees(frame._header['OBS-LONG'])
    badary.lat = ephem.degrees(frame._header['OBS-LAT'])
    badary.elev = float(frame._header['OBS-ALT'])
    badary.pressure = 0

    badary.date = frame.time.iso.replace('-','/')

    NORTH = -frame._antx
    EAST  =  frame._anty
    UP    =  frame._antz
    ENU = [EAST, NORTH, UP]

    sun = ephem.Sun()
    sun.compute(badary)

    az = np.pi-sun.az
    alt= np.pi/2.0-sun.alt
    xyz = np.dot(rotz(az), ENU)
    xyz = np.dot(rotx(alt), xyz)
    xyz = np.dot(rotz(sun.parallactic_angle()), xyz)  

    solar_P = sunpy_sun.P(frame.time)
    xyz = np.dot(rotz(-solar_P), xyz)

    x=xyz[0]
    y=xyz[1]
    z=xyz[2]

    n_bases = len(frame._anta)

    x1 =np.zeros(n_bases)
    x2 =np.zeros(n_bases)

    y1 =np.zeros(n_bases)
    y2 =np.zeros(n_bases)

    z1 =np.zeros(n_bases)
    z2 =np.zeros(n_bases)
        # Diagonal baselines 0:511, redundant 512:557, double redundant 558:601
    for ind in range(len(frame._anta[0:n_bases])):
        if frame._anta[ind] != 0:
            item_index = np.where(frame._antenna==frame._anta[ind])
            x1[ind] = x[item_index[0]]
            y1[ind] = y[item_index[0]]
            z1[ind] = z[item_index[0]]

    for ind in range(len(frame._antb[0:n_bases])):
        if frame._antb[ind] != 0:   
            item_index = np.where(frame._antenna==frame._antb[ind])
            x2[ind] = x[item_index[0]]
            y2[ind] = y[item_index[0]]
            z2[ind] = z[item_index[0]]

    bx=x1-x2
    by=y2-y1
    bz=z1-z2
    b0=[bx,by,bz]
    frame._uvw =b0/lam 

    #Calculating Antenna cross indexes
    np.where(frame._antenna ==  frame._anta[0])[0][0]
    frame._ant1 = np.zeros(n_bases,np.int16)
    frame._ant2 = np.zeros(n_bases,np.int16)
    for i in range(1, n_bases):
        frame._ant1[i] = np.where(frame._antenna ==  frame._anta[i])[0][0]
        frame._ant2[i] = np.where(frame._antenna ==  frame._antb[i])[0][0]

def frequency_to_qs(frequency):
    from os.path import dirname
    file = dirname(__file__) + "/tb_qs.txt"
    data = np.loadtxt(file)
    ref_frequency = data[:,0]
    ref_temperature = data[:,1]
    result = np.interp(frequency, ref_frequency, ref_temperature)
    return(result)


class SRHFits:
    def __init__(self, filename):
        self._header = fits.getheader(filename)
        self._data  = fits.getdata(filename, 'SRH_DAT')
        srh_ant   = fits.getdata(filename, 'SRH_ANT')
        self._frequency=self._data['FREQUENCY']    
        self.time = Time(self._header['DATE-OBS'].replace('/','-')) + TimeDelta(self._data['TIME']  , format = 'sec')

        #Reading antenna information
        self._antenna  =srh_ant['ANTENNA'].reshape(srh_ant['ANTENNA'].shape[1])
        self._anta     =srh_ant['ANTA'].reshape(srh_ant['ANTA'].shape[1]) 
        self._antb     =srh_ant['ANTB'].reshape(srh_ant['ANTB'].shape[1])         
        self._antx     =srh_ant['ANTX'].reshape(srh_ant['ANTX'].shape[1])       
        self._anty     =srh_ant['ANTY'].reshape(srh_ant['ANTY'].shape[1])       
        self._antz     =srh_ant['ANTZ'].reshape(srh_ant['ANTZ'].shape[1])

    def _get_frame_by_index(self, time_index = 0, frequency_index = 0):
        frame = Frame()
        frame.n_channels = len(self._frequency)
        frame.channel = frequency_index
        frame.frequency = self._frequency[frequency_index]
        frame.time = self.time[frequency_index,time_index]

        n_bases = 558



        amp_r = self._data['AMP_RCP']
        vis_r = self._data['VIS_RCP']
        amp_l = self._data['AMP_LCP']
        vis_l = self._data['VIS_LCP']

        amp_r = amp_r.reshape((self._frequency.shape[0], self.time.shape[1], self._antenna.shape[0]))
        vis_r = vis_r.reshape((self._frequency.shape[0], self.time.shape[1], vis_r.shape[1]//self.time.shape[1]))
        amp_l = amp_l.reshape((self._frequency.shape[0], self.time.shape[1], self._antenna.shape[0]))
        vis_l = vis_l.reshape((self._frequency.shape[0], self.time.shape[1], vis_l.shape[1]//self.time.shape[1]))

        frame._amp_r = amp_r[frequency_index,time_index,:]
        frame._vis_r = vis_r[frequency_index,time_index,:n_bases]
        frame._amp_l = amp_l[frequency_index,time_index,:]
        frame._vis_l = vis_l[frequency_index,time_index,:n_bases]

        frame._antenna = self._antenna
        frame._anta = self._anta[:n_bases]
        frame._antb = self._antb[:n_bases]
        frame._antx = self._antx
        frame._anty = self._anty
        frame._antz = self._antz
        frame._header = self._header

        #gains
        n_ant = len(self._antenna)
        frame.gains_r = np.ones(n_ant, dtype = np.complex)
        frame.gains_l = np.ones(n_ant, dtype = np.complex)

        qs_reference = frequency_to_qs(frame.frequency * 1e-3)
        frame.q_sun = qs_reference
        frame.qs_sigma = qs_reference*0.33

        uvw_calculate(frame)
        frame.update_mask()
        return frame
