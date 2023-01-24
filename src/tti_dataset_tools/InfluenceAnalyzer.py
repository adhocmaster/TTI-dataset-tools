import pandas as pd
from typing import *
import math
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor
import numpy as np
from itertools import product

# InfluenceGrid = List[List[int]]
InfluenceGrid = np.ndarray

class InfluenceAnalyzer(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)

        self.influencePoints = {
            0.5: 5,
            1: 5,
            2: 5,
            # 3: 5
        }

        self.unitMultiplier = 10


    def updateInfluencePoints(
            self, 
            row: pd.Series,
            grid: InfluenceGrid,
            influencePoints: Dict[float, int]
        ):
        x, y = self.getGridCoordinates(grid, row)
        grid[x, y] += influencePoints[0.5] 

        for k in self.influencePoints:
            radius = int(k * self.unitMultiplier)
            self.updateInfluencePointsInRadius(grid, x, y, radius, influencePoints[k])

        pass

    def updateInfluencePointsInRadius(self, grid: InfluenceGrid, x: int, y: int, radius: int, point: int):
        w, h = grid.shape
        # for i in range(-radius, radius + 1):
        #     if x + i >= 0 and x + i < w:
        #         for j in range(-radius, radius + 1):
        #             if y + j >= 0 and y + j < h:
        #                 if i**2 + j**2 <= radius**2:
        #                     grid[x + i, y + j] += point
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i**2 + j**2 <= radius**2:
                    if y + j >= 0 and y + j < h:
                        grid[x + i, y + j] += point
        pass

    def updateInfluencePointsInRadius2(self, grid: InfluenceGrid, x: int, y: int, radius: int, point: int):
        w, h = grid.shape
        # for i in range(-radius, radius + 1):
        #     if x + i >= 0 and x + i < w:
        #         for j in range(-radius, radius + 1):
        #             if y + j >= 0 and y + j < h:
        #                 if i**2 + j**2 <= radius**2:
        #                     grid[x + i, y + j] += point
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i**2 + j**2 <= radius**2:
                    if y + j >= 0 and y + j < h:
                        grid[x + i, y + j] += point
        pass

    def getGridCoordinates(self, grid: InfluenceGrid, row: pd.Series) -> Tuple[int, int]:
        # return int(row[self.xCol] * self.unitMultiplier), int(row[self.yCol] * self.unitMultiplier)
        w, h = grid.shape
        return int(row[self.localXCol] * self.unitMultiplier) + w//2, int(row[self.localYCol] * self.unitMultiplier)
    
    def generateGrid(
            self,
            size: Tuple[float, float]
        ) -> InfluenceGrid:
        """
        Generate a grid of influence points.

        Parameters
        ----------
        size : Tuple[float, float]
            The size of the grid in meter, meter

        Returns
        -------
        InfluenceGrid
            The grid of influence points at the resolution of centimeters.
        """ 

        w = math.ceil(size[0] * self.unitMultiplier) * 2
        h = math.ceil(size[1] * self.unitMultiplier) 

        return np.zeros((w, h))        
        

    def getInfluenceHeatMap(self,
            tracksDf: pd.DataFrame,
            size: Tuple[float, float]
        ) -> InfluenceGrid:

        grid = self.generateGrid(size)
        for index, row in tracksDf.iterrows():
            self.updateInfluencePoints(row, grid, self.influencePoints)
        
        w, h = grid.shape
        # transform to a dataframe
        X = np.arange(-w // 2, w // 2, 1)
        Y = np.arange(0, h, 1)
        Z = np.log([
            grid[i+w // 2, j] for i, j in product(X, Y)
        ])
        Z = [
            grid[i+w // 2, j] for i, j in product(X, Y)
        ]

        df1 = pd.DataFrame(list(product(X, Y)), columns=["X", "Y"])
        dfz = pd.DataFrame(Z, columns=["Density"])
        df2 = pd.concat([
                    df1,
                    dfz
                ], axis=1)
        dfH = df2.pivot("Y", "X", "Density")

        return dfH

