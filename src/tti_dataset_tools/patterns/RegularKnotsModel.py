import pandas as pd
from collections import defaultdict
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from itertools import product
from typing import *
from ..ColMapper import ColMapper
from ..TrajectoryProcessor import TrajectoryProcessor
from ..TrajectoryUtils import TrajectoryUtils
import logging
import matplotlib.pyplot as plt
import seaborn as sns



class RegularKnotsModel(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        super().__init__(colMapper)
    
    def getSingleKnotData(self, allPedDf: pd.DataFrame, midY: float, midYTolerance: float, plot=True) -> pd.DataFrame:
        """
        Get the data for a single knot from the dataframe of all pedestrians.

        Parameters
        ----------
        allPedDf : pd.DataFrame
            Dataframe of all pedestrians.

        Returns
        -------
        pd.DataFrame
            Dataframe of the single knot.
        """
        # midY = 3.0
        # midYTolerance = 0.5
        pedSource = allPedDf
        pedIds = pedSource[self.idCol].unique()
        rows = []
        # print(pedSource)
        for pedId in pedIds:
            # print(pedId)
            pedDf = pedSource[pedSource[self.idCol] == pedId]
            # print(pedDf.head())
            candidatesForX = TrajectoryUtils.getAllXAtYBreakpoint(pedDf, self.localXCol, self.localYCol, midY, midYTolerance)
            midX = np.mean(candidatesForX)
            if midX < 0:
                midX = min(candidatesForX)
            else:
                midX = max(candidatesForX)
            # print(midX, candidatesForX)
            
            finalX, finalY = pedDf.iloc[-1][self.localXCol], pedDf.iloc[-1][self.localYCol]
            
            slope1 = np.log(midY / midX)
            
            finalYDiff = (finalY - midY)

            if abs(finalYDiff) < 0.000001:
                logging.warn(f"finalYDiff is very low {finalYDiff}")
                # finalYDiff = 0.000001
            finalXDiff = (finalX - midX)
            if abs(finalXDiff) < 0.000001:
                logging.warn(f"finalXDiff is very low {finalXDiff}")
                # finalXDiff = 0.000001

            slope2 = np.log((finalY - midY) / (finalX - midX))
            # slope2 = (finalY - midY) / (finalX - midX)
                
            rows.append((pedId, midX, midY, finalX, finalY, slope1, slope2))
            if plot:
                plt.plot([0, midX, finalX], [0, midY, finalY], zorder=1)

        # print(rows)
            
        df = pd.DataFrame(rows, columns=[self.idCol, "midX", "midY", "finalX", "finalY", "log-slope1", "log-slope2"])

        if plot:
            sns.scatterplot(df, x="midX", y="midY")
            ax = sns.scatterplot(df, x="finalX", y="finalY", zorder = 2)
            ax.set_ylim(0, 6)
        
        return df