import pandas as pd
from typing import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class TrajectoryVisualizer:

    
    def show(self, df: pd.DataFrame, idCol, xCol, yCol, trackIds=None):
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
        if trackIds is None:
            trackIds = df[idCol].unique()

        for trackId in trackIds:
            trackDf = df[df[idCol] == trackId]
            plt.plot(trackDf[xCol], trackDf[yCol])

            # plot direction
            lastRow = trackDf.tail(1)
            endPoint = (lastRow[xCol] , lastRow[yCol])
            plt.plot(endPoint[0], endPoint[1], marker='x')
        
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    
    def showBreakpointVals(self, breakpointXVals:Dict[float, List[float]]):
        X = []
        Y = []
        for y in breakpointXVals:
            Y.extend([y] * len(breakpointXVals[y]))
            X.extend(breakpointXVals[y])
        ax = sns.scatterplot(x=X, y=Y, alpha=0.2)
        ax.set_aspect('equal', adjustable='box')
        plt.show()
