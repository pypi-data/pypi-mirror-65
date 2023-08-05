import hashlib
import os
from dateutil import parser
import types
from raodata.File import File
from raodata.SRH_frames import SRH_frames
from raodata.Data import Data
from raodata.Frame import Frame
from raodata.FrameSet import FrameSet
import requests_mock
from astropy.time import Time


class TestSRH_frames:

    def test_frame_by_time(self):

        frame = SRH_frames().get_frame_by_time("2018-05-17 03:00:14")
        assert type(frame) is Frame
        assert frame.time.value == Time("2018-05-17 03:00:17.695").value

    def test_frame_by_time_range(self):

        frames = SRH_frames().get_frames_by_time_range("2018-05-17 03:00:14", "2018-05-17 03:30:14")
        assert type(frames) is FrameSet
