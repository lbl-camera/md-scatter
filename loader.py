#! /usr/bin/env python

import re
import math

INT = re.compile(u'(\d+)')
FLOAT = re.compile(u'(\d+)\.(\d+)')

class TimeStep():
    def __init__(self):
        self.locations = {}

    def keys(self):
        return list(self.locations.keys())

    def locs(self,elm):
        return self.locations[elm]

    def __repr__(self):
        rep = ''
        for elem in self.locations:
            rep += str(elem) + ' :\n'
            nloc = len(self.locations[elem])
            if nloc > 3: nloc = 3
            for i in range(nloc):
                rep  += ('\t %f, %f, %f \n' % self.locations[elem][i])
            rep += '\t ....... \n'
        return rep
 
def loadXYZ(filename, max_steps=math.nan):
    time_steps = []
    curr_step = None
    with open(filename) as fp:
        for line in fp:
            if re.match(INT, line):
                n_locs = int(line.strip('\n'))
                if curr_step:
                    time_steps.append(curr_step)
                    if len(time_steps) >= max_steps:
                        break
                curr_step = TimeStep()
            elif re.search(FLOAT, line):
                elem, x, y, z = line.split()
                if elem in curr_step.locations:
                    curr_step.locations[elem].append((float(x), float(y), float(z)))
                else:
                    curr_step.locations[elem] = [(float(x), float(y), float(z))]
            else:
                continue
    return time_steps

if __name__ == '__main__':
    steps = loadXYZ('8_8_22.103AA.xyz')
    print(steps[10])
     
