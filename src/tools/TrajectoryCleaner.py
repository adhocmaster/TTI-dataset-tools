import numpy as np
import pandas as pd
from .ColMapper import ColMapper

class TrajectoryCleaner:

    def __init__(self,
            minSpeed,
            maxSpeed,
            minYDisplacement,
            maxXDisplacement,
            
            colMapper: ColMapper
        ):
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.minYDisplacement = minYDisplacement
        self.maxXDisplacement = maxXDisplacement

        self.idCol = colMapper.idCol
        self.xCol = colMapper.xCol
        self.yCol = colMapper.yCol
        self.xVelCol = colMapper.xVelCol
        self.yVelCol = colMapper.yVelCol
        self.speedCol = colMapper.speedCol

        pass

    def getOutliersBySpeed(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnSpeed=False
        ):

        maxSpeeds = tracksDf[[self.idCol, self.speedCol]].groupby([self.idCol]).max()


        

        if byIQR:
            Q3 = np.quantile(maxSpeeds[self.speedCol], 0.75)
            Q1 = np.quantile(maxSpeeds[self.speedCol], 0.25)
            IQR = Q3 - Q1
            minSpeed = Q1 - 1.5 * IQR
            maxSpeed = Q3 + 1.5 * IQR

            print("IQR value for column %s is: %s" % (self.speedCol, IQR))
            print(f"using range ({minSpeed}, {maxSpeed})")
            

        else:
            pass




        criterion = maxSpeeds[self.speedCol].map(
            lambda speed: speed < minSpeed or speed > maxSpeed)

        outliers = maxSpeeds[criterion]
        
        if returnSpeed:
            return outliers
        else:
            return outliers.index

    
    def cleanBySpeed(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersBySpeed(
            tracksDf, 
            byIQR,
            returnSpeed = False
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()


        



    