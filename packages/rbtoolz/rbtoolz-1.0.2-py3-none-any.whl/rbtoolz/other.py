#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Helper functions primarily for data analysis

"""


__author__ = 'Ross Bonallo'
__license__ = 'MIT Licence'
__version__ = '1.0.1'


import pandas as pd
import numpy as np

def seag(df,period='M'):
    if period == 'M':
        _df = pd.pivot_table(df,index=df.index.day,columns=df.index.month,
                aggfunc=np.sum,fill_value=0)
    elif period == 'W':
        _df = pd.pivot_table(df,index=df.index.dayofweek,columns=df.week.year,
                aggfunc=np.sum,fill_value=0)
    elif period == 'Y':
        _df = pd.pivot_table(df,index=df.index.day,columns=df.week.year,
                aggfunc=np.sum,fill_value=0)
    return _df

