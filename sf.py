#! /usr/bin/env python

import numpy as np
try:
    import mdscatter
    have_ext = True
except ImportError as e:
    have_ext = False
    print('Failed to import mdscatter')

def structure_factor(qx, qy, qz, locations):

    if not have_ext:
        sf = np.zeros(qx.shape, dtype=np.complex) 
        for loc in locations:
            sf += np.exp(-1j * (qx * loc[0] + qy * loc[1] + qz * loc[2]))
    else:
        shape = qx.shape
        qvals = np.array([qx.ravel(), qy.ravel(), qz.ravel()]).T
        sf = mdscatter.gpudft(locations, qvals)
        return sf.reshape(shape)
