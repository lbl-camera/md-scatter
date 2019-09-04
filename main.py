#! /usr/bin/env python

import sys

import numpy as np
import loader
import henke
import sf
from detector import Square512
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <filename.xyz>' % sys.argv[0]) 
        exit(1)

    time_steps = loader.loadXYZ(sys.argv[1])
    det = Square512()
    qx, qy, qz = det.qvectors(0.1, (256, 256), 10) 
    qval = np.sqrt(qx**2 + qy**2 + qz**2)
    
    scat = np.zeros(qx.shape, dtype=np.complex)
    for idx, ts in enumerate(time_steps):
        elems = ts.keys()
        if 'H' in elems: elems.remove('H')

        for el in elems:
            ff = henke.table.ff.compute(el, qval)
            scat += ff * sf.structure_factor(qx, qy, qz, ts.locs(el))

        img = np.abs(scat)**2
        plt.imshow(np.log(img))
        filename = 'ts%06d.png' % idx
        plt.savefig('data/' + filename)
        if idx > 10: break 
