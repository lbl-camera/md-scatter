#! /usr/bin/env python

import sys
import os
import numpy as np
import loader
import henke
import sf
from detector import Pilatus1M
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <filename.xyz>' % sys.argv[0]) 
        exit(1)

    filename = os.path.basename(sys.argv[1])
    basename = os.path.splitext(filename)[0]
    #datafile = os.path.join('data', basename + '.npy')
    imgfile = os.path.join('data', basename + '.png')
    time_steps = loader.loadXYZ(sys.argv[1])
    
    det = Pilatus1M()
    qx, qy, qz = det.qvectors(3, (512, 512), 10) 
    qval = np.sqrt(qx**2 + qy**2 + qz**2)
    
    scat = np.zeros(qx.shape, dtype=np.complex)
    img = np.zeros(qx.shape, dtype=np.float)
    for idx, ts in enumerate(time_steps):
        elems = ts.keys()
        if 'H' in elems: elems.remove('H')

        for el in elems:
            ff = henke.table.ff.compute(el, qval)
            scat += ff * sf.structure_factor(qx, qy, qz, ts.locs(el))

        datafile = os.path.join('data', basename + str(idx).zfill(4) + '.npy')
        np.save(datafile, scat)
        img = img + np.abs(scat)**2
        if idx > 200: break 

    plt.imshow(np.log(img))
    plt.savefig(imgfile)
