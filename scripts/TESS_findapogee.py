#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:37:20 2019

@author: cjburke
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import spiceypy as spice
import glob
import matplotlib as mpl
from astropy.coordinates import SkyCoord, ICRS, FK4, Angle, GCRS
from astropy.time import Time
from astropy import units as u
from astropy.io import fits
#from tess_stars2px import tess_stars2px_function_entry
from astropy.coordinates.attributes import (TimeAttribute,
                          CartesianRepresentationAttribute)
from astropy.coordinates import solar_system_ephemeris

if __name__ == '__main__':
    REARTH = 1.0/6371.0
#    ephemFiles = glob.glob('TESS_EPH_DEF_2018*.bsp')
    ephemFiles = ['TESS_EPH_PRE_LONG_2018235_01.bsp']
    tlsFile = 'tess2018338154046-41240_naif0012.tls'
    solarSysFile = 'de438.bsp'
#    solarSysFile = 'tess2018338154429-41241_de430.bsp'

    print(spice.tkvrsn('TOOLKIT'))
    for ephFil in ephemFiles:
        spice.furnsh(ephFil)
    spice.furnsh(tlsFile)
    spice.furnsh(solarSysFile)


    # JD time start 
#    tStartJD = 2458410.8
#    tStartJD = 2458424.55
#    tEndJD = 2458437.85
    tStartJD = 2458424.0
    tEndJD = 2458436.0
    allTJD = np.arange(tStartJD, tEndJD, 1.0/(12*24))
    nT = len(allTJD)
    allET = np.zeros((nT,), dtype=np.float)
    for i,t in enumerate(allTJD):
        allET[i] = spice.unitim(t, 'JDTDB', 'ET')

#   Calculate position and velocity of TESS relative to Earth geocenter    
    xposs = np.zeros_like(allET)
    yposs = np.zeros_like(allET)
    zposs = np.zeros_like(allET)
    vxs = np.zeros_like(allET)
    vys = np.zeros_like(allET)
    vzs = np.zeros_like(allET)
    for i, et in enumerate(allET):
        outTuple = spice.spkezr('Mgs Simulation', et, 'J2000', \
                                'NONE', 'Earth')
        xposs[i] = outTuple[0][0]
        yposs[i] = outTuple[0][1]
        zposs[i] = outTuple[0][2]
        vxs[i] = outTuple[0][3]
        vys[i] = outTuple[0][4]
        vzs[i] = outTuple[0][5]
    

    earthsep = np.sqrt(xposs*xposs + yposs*yposs + zposs*zposs)
    ia = np.argmax(earthsep)
    print('Apogee {0:12.4f} Sep: {1:8.4f}'.format(allTJD[ia], earthsep[ia]))
    plt.plot(allTJD-245700.0, earthsep, '.')
    plt.show()
    