#! /usr/bin/env python

import sys
import os
import numpy as np
import loader
import henke
import sf
import edges
import json
from detector import Pilatus1M, ImpossibleDet
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s <filename.xyz> <json obj>' % sys.argv[0]) 
        exit(1)

    filename = os.path.basename(sys.argv[1])
    basename = os.path.splitext(filename)[0]
    #imgfile = os.path.join('data', basename + '.png')
    time_steps = loader.loadXYZ(sys.argv[1], max_steps = 200)

    # experiment setup
    if len(sys.argv) == 3:
        v = json.loads(sys.argv[2])
    else:
        print('running default setup ...')
        with open('.exp.json') as fp:
            v = json.load(fp)
    sdd = v['sdd']
    center = v['center']
    energy = v['energy']
    theta = np.radians(v['theta'])
    alpha = np.radians(v['alpha'])

    datafile = os.path.join('data', basename + str(energy) + '.npy')
    det = Pilatus1M()
    qx, qy, qz = det.qvectors(sdd, center, energy, theta = theta, alpha = alpha)
    qp = np.sqrt(qx**2 + qy**2) * np.sign(qy)
   
    qval = np.sqrt(qx**2 + qy**2 + qz**2)
    
    scat = np.zeros(qx.shape, dtype=np.complex)
    img = np.zeros(qx.shape, dtype=np.float)

    ev_tables = {}
    for idx, ts in enumerate(time_steps):
        elems = ts.keys()
        if 'H' in elems: elems.remove('H')
        for el in elems:
            if not el in ev_tables:
                ev_tables[el] = edges.EnergyDepFormFactor(el)

        for el in elems:
            ff = henke.table.ff.compute(el, qval)
            f1 = ev_tables[el].f1(energy)
            f2 = ev_tables[el].f2(energy)
            scat += (ff + f1 - 1j * f2) * sf.structure_factor(qx, qy, qz, ts.locs(el))
        tempname = basename + '_' + str(energy)
        datafile = os.path.join('data', tempname  + '.npy')
        img = img + np.abs(scat)**2
    np.save(datafile, img)
