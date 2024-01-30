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
    
    def getSingleKnotData(self, pedSource: pd.DataFrame, midY: float, midYTolerance: float, plot=True) -> pd.DataFrame:
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
        pedIds = pedSource[self.idCol].unique()
        rows = []
        # print(pedSource)
        for pedId in pedIds:
            # print(pedId)
            pedDf = pedSource[pedSource[self.idCol] == pedId]
            # print(pedDf.head())
            
            midX = TrajectoryUtils.getExtremeXAtYBreakpoint(pedDf, self.localXCol, self.localYCol, midY, midYTolerance)
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
            ax.set_ylim(-0.2, midY * 2 + 0.2)
            plt.show()
            sns.displot(df, x="log-slope1", y="log-slope2")
        
        return df

    def getKnotData(self, pedSource: pd.DataFrame, yBreakpoints: List[float], yTolerance: float, plot=True, addFinal=True) -> pd.DataFrame:
        """Assumes origin is at (0, 0)

        Args:
            pedSource (pd.DataFrame): _description_
            yBreakpoints (List[float]): _description_
            yTolerance (float): _description_
            plot (bool, optional): _description_. Defaults to True.
            addFinal (bool, optional): _description_. Defaults to True.

        Returns:
            pd.DataFrame: _description_
        """
        
        pedIds = pedSource[self.idCol].unique()
        nSlopePoints = len(yBreakpoints)
        if addFinal:
            nSlopePoints += 1
        rows = []
        for pedId in pedIds:
            pedDf = pedSource[pedSource[self.idCol] == pedId]
            XY = [(0, 0)]
            for y in yBreakpoints:
                x = TrajectoryUtils.getExtremeXAtYBreakpoint(pedDf, self.localXCol, self.localYCol, y, yTolerance)
                XY.append((x, y))

            if addFinal:
                finalX, finalY = pedDf.iloc[-1][self.localXCol], pedDf.iloc[-1][self.localYCol]
                XY.append((finalX, finalY))
            
            slopes = []
            for i in range(1, len(XY)):
                yDiff = XY[i][1] - XY[i - 1][1]
                xDiff = XY[i][0] - XY[i - 1][0]

                if abs(xDiff) < 0.000001:
                    logging.warn(f"xDiff is very low {xDiff}")
                    # xDiff = 0.000001
                if abs(yDiff) < 0.000001:
                    logging.warn(f"yDiff is very low {yDiff}")
                    # yDiff = 0.000001
                slope = np.log(yDiff / xDiff)
                slopes.append(slope)
            
            rowData = [pedId]
            for i in range(1, len(XY)):
                rowData += [XY[i][0], XY[i][1], slopes[i - 1]]
            rows.append(rowData)

            if plot:
                X = [x for x, y in XY]
                Y = [y for x, y in XY]
                plt.plot(X, Y, zorder=1)
                plt.scatter(X, Y, zorder=2)
                plt.ylim(-0.2, max(Y)+0.2)

        colunmNames = [self.idCol]
        for i in range(nSlopePoints):
            colunmNames += [f"x{i+1}", f"y{i+1}", f"log-slope{i+1}"]
        
        df = pd.DataFrame(rows, columns=colunmNames)
        if plot:
            for i in range(1, nSlopePoints):
                sns.displot(df, x=f"log-slope{i}", y=f"log-slope{i+1}")
        return df
            





            
