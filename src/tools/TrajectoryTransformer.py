import pandas as pd
from typing import *
import math

class TrajectoryTransformer:

    
    def translateOneToLocalSource(self, trackDf:pd.DataFrame, xCol, yCol) -> Tuple[pd.Series, pd.Series]:
        """For a single track only. We cannot make parallel updates for multiple pedestrians as the query would require sql.

        Args:
            trackDf (pd.DataFrame): _description_
            xCol (_type_): _description_
            yCol (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        firstRow = trackDf.iloc[0]
        originX = firstRow[xCol]
        originY = firstRow[yCol]
        # trackDf["localX"] = trackDf[xCol] - originX
        # trackDf["localY"] = trackDf[yCol] - originY

        return trackDf[xCol] - originX, trackDf[yCol] - originY
        

    def translateManyToLocalSource(self,
            tracksDf:pd.DataFrame, 
            idCol, 
            xCol, 
            yCol
        ):
        """Will group by idCol and translate based on the first row of each track. We cannot make parallel updates for multiple pedestrians as the query would require sql.

        Args:
            trackDf (pd.DataFrame): _description_
            idCol (_type_): track id column. 
            xCol (_type_): _description_
            yCol (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        # TODO pass

        allTrackIds = tracksDf[idCol].unique()

        localXSeres = []
        localYSeres = []

        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[idCol] == trackId]
            X, Y = self.translateOneToLocalSource(trackDf, xCol, yCol)
            localXSeres.append(X)
            localYSeres.append(Y)
        

        tracksDf["localX"] = pd.concat(localXSeres)
        tracksDf["localY"] = pd.concat(localYSeres)

        pass

    # region velocity
    def deriveSpeed(self,
            tracksDf:pd.DataFrame, 
            idCol, 
            xVelCol, 
            yVelCol
        ):

        tracksDf["speed"] = tracksDf.apply(
            lambda row: math.sqrt(row[xVelCol] ** 2 + row[yVelCol] ** 2),
            axis=1
        )
        
