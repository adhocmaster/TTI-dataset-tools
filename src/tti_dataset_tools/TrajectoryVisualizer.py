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

    
    def show3D(self, df: pd.DataFrame, idCol, xCol, yCol, trackIds=None, colorCol=None):
        
        fig = plt.figure(figsize=(10, 10))

        plot_axis = plt.axes (projection = '3d')
        if trackIds is None:
            trackIds = df[idCol].unique()

        for trackId in trackIds:
            trackDf = df[df[idCol] == trackId]
            timeSpace = np.linspace(0, len(trackDf), len(trackDf))
            if colorCol is None:
                plot_axis.plot3D(trackDf[xCol], trackDf[yCol], timeSpace)
            else:
                plot_axis.scatter3D(trackDf[xCol], trackDf[yCol], timeSpace, s=1, c=trackDf[colorCol].astype(int).tolist())

            # plot direction
            lastRow = trackDf.tail(1)
            endPoint = (lastRow[xCol] , lastRow[yCol])
            plot_axis.plot3D(endPoint[0], endPoint[1], marker='x')
        
        plot_axis.set_aspect('equal', adjustable='box')
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
