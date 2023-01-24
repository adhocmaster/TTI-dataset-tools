import pandas as pd
from collections import defaultdict
import numpy as np
from shapely.geometry import Point, Polygon
from typing import *
from tti_dataset_tools import TrajectoryProcessor, ColMapper, TrajectoryTransformer


class CrosswalkModel(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)


    def generateLocalPolygon(
            self,
            tracksDf: pd.DataFrame,
            roadWidth: float,
            interval: float,
        ) -> Polygon:
        """
        Generate a polygon from a dataframe of tracks.

        Parameters
        ----------
        tracksDf : pd.DataFrame
            Dataframe of tracks.
        roadWidth : float
            Width of the road.
        interval : float
            distance between two subsequent polygon points along the y axis / road width

        Returns
        -------
        shapely Polygon
        """

        yBreakpoints = list(range(interval, roadWidth, interval))
        if (yBreakpoints[-1] - roadWidth) < 0.2:
            yBreakpoints.append(roadWidth)
        

        # allTrackIds = tracksDf[self.idCol].unique()
        # for trackId in allTrackIds:
        #     trackDf = tracksDf[tracksDf[self.idCol] == trackId]
        yTolerance = 0.1
        breakpointXVals = defaultdict(lambda : [])
        for yBreakpoint in yBreakpoints:
            xVals = self.getAllLocalXAtLocalYBreakpoint(tracksDf, yBreakpoint, yTolerance)
            if xVals is None:
                raise Exception(f"no point at y-breakpoint {yBreakpoint}")
            breakpointXVals[yBreakpoint].extend(xVals)


    def getMeanLocalXAtLocalYBreakpoints(
            self,
            trackDf: pd.DataFrame,
            yBreakpoints: List[float]
        ) -> List[float]:

        # find localY values within range of breakpoint +- 0.1 meter. Get the average localX values
        yTolerance = 0.1
        X = []
        for yBreakpoint in yBreakpoints:
            x = self.getMeanLocalXAtLocalYBreakpoint(trackDf, yBreakpoint)
            if x is not None:
                X.append(x)
        
        return X


    def getMeanLocalXAtLocalYBreakpoint(
            self,
            trackDf: pd.DataFrame,
            yBreakpoint: float, 
            yTolerance: float
        ) -> Optional[List[float]]:

        # find localY values within range of breakpoint +- 0.1 meter. Get the average localX values

        yMin = yBreakpoint - yTolerance
        yMax = yBreakpoint + yTolerance
        
        criterion = trackDf[self.localYCol].map(
            lambda y: y >= yMin and y <= yMax
        )
        nearbyRows = trackDf[criterion]
        if len(nearbyRows) == 0:
            return None
        
        return nearbyRows[self.localXCol].mean()

    def getAllLocalXAtLocalYBreakpoint(
            self,
            tracksDf: pd.DataFrame,
            yBreakpoint: float, 
            yTolerance: float
        ) -> Optional[List[float]]:

        # find localY values within range of breakpoint +- 0.1 meter. Get the average localX values

        yMin = yBreakpoint - yTolerance
        yMax = yBreakpoint + yTolerance
        
        criterion = tracksDf[self.localYCol].map(
            lambda y: y >= yMin and y <= yMax
        )
        nearbyRows = tracksDf[criterion]
        if len(nearbyRows) == 0:
            return None
        
        return nearbyRows[self.localXCol]

    def generateScenePolygon(
            self,
            tracksDf: pd.DataFrame,
            roadWidth: float,
            crosswalkWidth: float,
            interval: float,
        ) -> Polygon:
        """
        Generate a polygon from a dataframe of tracks.

        Parameters
        ----------
        tracksDf : pd.DataFrame
            Dataframe of tracks.
        roadWidth : float
            Width of the road.
        crosswalkWidth : float
            Width of the crosswalk.
        interval : float
        """



    

