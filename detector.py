#! /usr/bin/env python

import numpy as np

class Detector:
    def __init__(self, name, shape, pixle_size):
        self.name = name
        self.shape = shape
        self.pixle_size = pixle_size

    def qvectors(self, sdd, center, energy, alpha=0., theta=0.):


        # detector angles
        cos_a = np.cos(alpha)
        sin_a = np.sin(alpha)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # gridding
        nrow = self.shape[0]
        ncol = self.shape[1]
        y, x = np.mgrid[0:nrow, 0:ncol]

        # shift coordinate with center
        x = (x - center[1]) * self.pixle_size[0]
        y = (y - center[0]) * self.pixle_size[1]

        # angles 
        # theta
        tmp = np.sqrt(x**2 + sdd**2)
        cos_th = cos_t * (sdd / tmp) - sin_t * (x / tmp)
        sin_th = cos_t * (x / tmp) + sin_t * (sdd / tmp)

        # alpha
        tmp2 = np.sqrt(y**2 + tmp**2)
        cos_al = cos_a * (tmp / tmp2) - sin_a * (y / tmp2)
        sin_al = cos_a * (y / tmp2) + sin_a * (tmp / tmp2)

        # radius of the Ewald's sphere
        wave = 0.123984E+04 / energy
        k0 = 2 * np.pi / wave

        # q-vector
        qx = k0 * (cos_al * cos_th - 1)
        qy = k0 * (cos_al * sin_th)
        qz = k0 * (sin_al)
        return qx, qy, qz

    def qvalues(self, sdd, center, energy, alpha=0., theta=0.):
        qx, qy, qz = self.qvectors(sdd, center, energy, alpha, theta)
        return np.sqrt(qx**2 + qy**2 + qz**2)


class Lambda750k(Detector):
    def __init__(self):
        self.name = 'Lambda 750k'
        self.shape = (512, 1536)
        self.pixle_size = (55.E-06, 55.E-06)

class Square512(Detector):
    def __init__(self):
        self.shape = (512, 512)
        self.name = 'Virtual Detector'

class Pilatus1M(Detector):
    def __init__(self):
        self.name = 'Pilatus 1M'
        self.shape = (1043, 981)
        self.pixle_size = (172.E-06, 172.E-06)

class ImpossibleDet(Detector):
    def __init__(self):
        self.name = 'Impossible Detector'
        self.shape = (1024, 1024)
        self.pixle_size = (50.E-06, 50.E-06)
