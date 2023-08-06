#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:47:33 2020

Bind Pandas methods to dataframe for simpler use. 

@author: jcl
"""

import pandas as pd
from pandas import DataFrame # import DataFrame separately to act on 

def xTab(self, vertical, horizontal):
    """
    Parameters
    ----------
    vertical: string
        column name for vertical.
    horizontal: string
        column name for horizontal.

    Returns
    -------
    Dataframe representing the crosstab of self.vertical, self.horizontal
    """

    try:
        return pd.crosstab(self[vertical], self[horizontal])
    except:
        return None

DataFrame.xTab = xTab # give the xTab method to DataFrame

if __name__ == "__main__":
    exampleD = {"sv": "a a a a a b b b b b".split() \
                , "x": [1, 2, 3, 2, 3, 4, 4, 5, 6, 1]}
    exampleR = DataFrame(exampleD) 
    # print(exampleR)
    # print ()
    
    # classic crosstab calls are messy
    classicR = pd.crosstab(exampleR.query("x < 6").x \
                           , exampleR.query("x < 6").sv)
    # xTab calls are neater
    simpleR = exampleR.query("x < 6").xTab("x", "sv")

    # showing that the crosstabs are the same
    print ((simpleR == classicR).min().min())
