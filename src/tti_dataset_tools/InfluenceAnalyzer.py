import pandas as pd
from typing import *
import math
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor
import numpy as np

# InfluenceGrid = List[List[int]]
InfluenceGrid = np.ndarray

class InfluenceAnalyzer(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)

        self.influencePoints = {
            0.5: 10,
            1: 5,
            2: 1
        }


    def updateInfluencePoints(
            self, 
            row: pd.Series,
            grid: InfluenceGrid,
            influencePoints: Dict[float, int]
        ):
        x, y = self.getGridCoordinates(row)
        grid[x, y] += influencePoints[0.5]

        self.updateInfluencePointsInRadius(grid, x, y, 50, influencePoints[0.5])

        # within 1 meter
        self.updateInfluencePointsInRadius(grid, x, y, 100, influencePoints[1])


        # within 2 meters
        self.updateInfluencePointsInRadius(grid, x, y, 200, influencePoints[2])

        pass

    def updateInfluencePointsInRadius(self, grid: InfluenceGrid, x: int, y: int, radius: int, point: int):
        w, h = grid.shape
        for i in range(-radius, radius + 1):
            if x + i >= 0 and x + i < w:
                for j in range(-radius, radius + 1):
                    if y + j >= 0 and y + j < h:
                        if i**2 + j**2 <= radius**2:
                            grid[x + i, y + j] += point
        pass

    def getGridCoordinates(self, row: pd.Series) -> Tuple[int, int]:
        return int(row[self.localXCol] * 100), int(row[self.localYCol] * 100)
    
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

        w = math.ceil(size[0] * 100)
        h = math.ceil(size[1] * 100)

        return np.zeros((w, h))        
        

    def getInfluenceHeatMap(self,
            tracksDf: pd.DataFrame,
            size: Tuple[float, float]
        ) -> InfluenceGrid:

        grid = self.generateGrid(size)
        for index, row in tracksDf.iterrows():
            self.updateInfluencePoints(row, grid, self.influencePoints)
        
        return grid

