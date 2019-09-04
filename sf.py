#! /usr/bin/env python

import numpy as np

def structure_factor(qx, qy, qz, locations):
    sf = np.zeros(qx.shape, dtype=np.complex) 
    for loc in locations:
        sf += np.exp(-1j * (qx * loc[0] + qy * loc[1] + qz * loc[2]))
    return sf
