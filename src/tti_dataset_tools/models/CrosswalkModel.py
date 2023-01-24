import pandas as pd
from collections import defaultdict
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from itertools import product
from typing import *
from ..ColMapper import ColMapper
from ..TrajectoryProcessor import TrajectoryProcessor



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
        
        yTolerance = 0.1
        breakpointXVals = self.getAllLocalXAtLocalYBreakpoints(
                tracksDf = tracksDf,
                yBreakpoints = yBreakpoints,
                yTolerance = yTolerance
            )



    def generatePolygonFromBreakpointVals(
            self,
            breakpointXVals: Dict[float, List[float]]
        ) -> Polygon: 

        yBreakpoints = list(breakpointXVals.keys())
        yBreakpoints.sort() # dict keys not sorted
        # with min-max 
        minVals = [min(breakpointXVals[y]) for y in yBreakpoints]
        maxVals = [max(breakpointXVals[y]) for y in yBreakpoints]

        # first mins bot to top, then max top to bottom
        minPoints = list(zip(minVals, yBreakpoints))
        maxPoints = list(zip(maxVals, yBreakpoints))
        maxPoints.reverse()
        
        return Polygon(minPoints + maxPoints)
    
    def generate7pointPolygonFromBreakpointVals(
            self,
            tracksDf: pd.DataFrame,
            roadWidth: float,
            interval: float,
        ) -> Polygon: 


        yBreakpoints = [1, roadWidth - 1, roadWidth]
        
        yTolerance = 0.1
        breakpointXVals = self.getAllLocalXAtLocalYBreakpoints(
                tracksDf = tracksDf,
                yBreakpoints = yBreakpoints,
                yTolerance = yTolerance
            )

        # with min-max 
        minVals = [min(breakpointXVals[y]) for y in yBreakpoints]
        maxVals = [max(breakpointXVals[y]) for y in yBreakpoints]

        # starting section
        # minVals are left, maxVals are right
        leftSpline = LineString([
            (0, minVals[0]),
            (minVals[0], minVals[1]),
            (minVals[1], minVals[2])
        ])

        rightSpline = LineString([
            (0, maxVals[0]),
            (maxVals[0], maxVals[1]),
            (maxVals[1], maxVals[2])
        ])

    
    



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

    def getAllLocalXAtLocalYBreakpoints(
            self,
            tracksDf: pd.DataFrame,
            yBreakpoints: List[float],
            yTolerance: float
        ) -> Optional[List[float]]:

        breakpointXVals = defaultdict(lambda : [])
        for yBreakpoint in yBreakpoints:
            xVals = self.getAllLocalXAtLocalYBreakpoint(tracksDf, yBreakpoint, yTolerance)
            if xVals is None:
                raise Exception(f"no point at y-breakpoint {yBreakpoint}")
            breakpointXVals[yBreakpoint].extend(xVals)
        
        return breakpointXVals


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



    

