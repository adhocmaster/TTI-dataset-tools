import pandas as pd
from typing import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class TrajectoryVisualizer:

    
    def show(self, df: pd.DataFrame, idCol, xCol, yCol, trackIds=None, colorCol=None):
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
        if trackIds is None:
            trackIds = df[idCol].unique()

        for trackId in trackIds:
            trackDf = df[df[idCol] == trackId]
            if colorCol is None:
                plt.plot(trackDf[xCol], trackDf[yCol])
            else:
                plt.scatter(trackDf[xCol], trackDf[yCol], s=1, c=trackDf[colorCol].astype(int).tolist())

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
