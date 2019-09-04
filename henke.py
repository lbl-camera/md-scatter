#! /usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


header = [ 'a1', 'b1', 'a2', 'b2', 'a3', 'b3', 'a4', 'b4', 'c' ]

@pd.api.extensions.register_dataframe_accessor("ff")
class Formfactor:
    def __init__(self, pd_obj):
        self._validate(pd_obj)
        self._obj = pd_obj

    @staticmethod
    def _validate(obj):
        if not all([ key in obj.columns for key in header ]):
            raise AttributeError('Missing required keys from dataframe')

    def compute(self, elem, q):
        fq = np.zeros_like(q)
        coef = self._obj.loc[elem]
        for i in range(4):
            fq += coef[2*i] * np.exp(-coef[2*i+1] * (q/4/np.pi)**2)
        return fq + coef[8] 


table = pd.read_csv('table.csv', delimiter='\t', index_col=0)
