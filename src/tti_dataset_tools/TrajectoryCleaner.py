import numpy as np
import pandas as pd
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor

class TrajectoryCleaner(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper,
            minSpeed,
            maxSpeed,
            minYDisplacement,
            maxXDisplacement,
        ):
        
        super().__init__(colMapper)
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.minYDisplacement = minYDisplacement
        self.maxXDisplacement = maxXDisplacement


        pass

    #region outliers

    def getOutliersByCol(self, 
            tracksDf:pd.DataFrame, 
            col: str,
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        maxVals = tracksDf[[self.idCol, col]].groupby([self.idCol]).max()

        if byIQR:
            Q3 = np.quantile(maxVals[col], 0.75)
            Q1 = np.quantile(maxVals[col], 0.25)
            IQR = Q3 - Q1
            lowerBoundary = Q1 - 1.5 * IQR
            higherBoundary = Q3 + 1.5 * IQR

            print("IQR value for column %s is: %s" % (col, IQR))
            print(f"using range ({lowerBoundary}, {higherBoundary})")
            

        else:
            raise NotImplementedError("Not implemented non IQR yet")




        criterion = maxVals[col].map(
            lambda val: val < lowerBoundary or val > higherBoundary)

        outliers = maxVals[criterion]

        if returnVals:
            return outliers
        else:
            return outliers.index


    def getOutliersBySpeed(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        if byIQR:
            return self.getOutliersByCol(
                tracksDf,
                self.speedCol,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            print(f"using range ({self.minSpeed}, {self.maxSpeed})")
            maxVals = tracksDf[[self.idCol, self.speedCol]].groupby([self.idCol]).max()
            criterion = maxVals[self.speedCol].map(
                lambda val: val < self.minSpeed or val > self.maxSpeed)

            outliers = maxVals[criterion]

            if returnVals:
                return outliers
            else:
                return outliers.index

    
    def getOutliersByYDisplacement(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:

        if byIQR:
            return self.getOutliersByCol(
                tracksDf,
                col = self.displacementY,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            pass


    
    def cleanBySpeed(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersBySpeed(
            tracksDf, 
            byIQR
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()


        



    