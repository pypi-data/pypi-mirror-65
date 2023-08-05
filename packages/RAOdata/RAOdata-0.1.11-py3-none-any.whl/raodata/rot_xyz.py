# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:27:42 2016

@author: Alexey Kochanov, kochanov@iszf.irk.ru
"""

"""Rotational matrices for right-handed coordinate system"""
import numpy as np
    
def rotx(angle):
    sin, cos = np.sin(angle), np.cos(angle)
    map =  np.array([[    1.0   ,       0.0  ,       0.0  ],
                    [     0.0   ,       cos  ,       sin  ],
                    [     0.0   ,      -sin  ,       cos  ]])
    return map
    
def roty(angle):
    sin, cos = np.sin(angle), np.cos(angle)
    map =  np.array([[    cos   ,       0.0  ,      -sin  ],
                    [     0.0   ,       1.0  ,       0.0  ],
                    [     sin   ,       0.0  ,       cos  ]])
    return map

def rotz(angle):
    sin, cos = np.sin(angle), np.cos(angle)
    map =  np.array([[    cos   ,      sin  ,       0.0  ],
                    [    -sin   ,      cos  ,       0.0  ],
                    [     0.0   ,       0.0  ,       1.0  ]])
    return map
