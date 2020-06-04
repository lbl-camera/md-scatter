import re
import os
import pandas as pd
import numpy as np

class EnergyDepFormFactor:
    def __init__(self, elem):
        val = re.search('val', elem)
        ion = re.search('\d', elem)

        if val:
            n = val.start(0)
        elif ion:
            n = ion.start(0)
        else:
            n = None

        f = os.path.join('sf', elem[:n].lower() + '.nff')
        if not os.path.isfile(f):
            raise OSError('file not found')

        df = pd.read_csv(f, delimiter='\t', header=0, index_col=False, dtype=float)
        self.df = df.set_index('E(eV)')

    def f1(self, energy):
        if energy < 20.1: return 0
        loc = self.df.index.get_loc(energy, method='nearest')
        s = slice(loc-2, loc+2)
        sub = self.df.iloc[s]
        return np.interp(energy, sub.index.values, sub.f1.values)

    def f2(self, energy):
        loc = self.df.index.get_loc(energy, method='nearest')
        s = slice(loc-2, loc+2)
        sub = self.df.iloc[s]
        return np.interp(energy, sub.index.values, sub.f2.values)
