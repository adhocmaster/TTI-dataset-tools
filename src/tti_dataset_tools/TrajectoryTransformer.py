import pandas as pd
from typing import *
import math
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor

class TrajectoryTransformer(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)

    
    def translateOneToLocalSource(self, trackDf:pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """For a single track only. We cannot make parallel updates for multiple pedestrians as the query would require sql.

        Args:
            trackDf (pd.DataFrame): _description_
            xCol (_type_): _description_
            yCol (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        firstRow = trackDf.iloc[0]
        originX = firstRow[self.xCol]
        originY = firstRow[self.yCol]
        # trackDf["localX"] = trackDf[xCol] - originX
        # trackDf["localY"] = trackDf[yCol] - originY

        return trackDf[self.xCol] - originX, trackDf[self.yCol] - originY
        

    def translateAllToLocalSource(self,
            tracksDf:pd.DataFrame
        ):
        """Will group by idCol and translate based on the first row of each track. 
        We cannot make parallel updates for multiple pedestrians as the query would require sql.
        Assumes all tracks start on a sidewalk

        Args:
            trackDf (pd.DataFrame): _description_
            idCol (_type_): track id column. 
            xCol (_type_): _description_
            yCol (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        # TODO pass

        allTrackIds = tracksDf[self.idCol].unique()

        localXSeres = []
        localYSeres = []

        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            X, Y = self.translateOneToLocalSource(trackDf)
            localXSeres.append(X)
            localYSeres.append(Y)
        

        tracksDf[self.localXCol] = pd.concat(localXSeres)
        tracksDf[self.localYCol] = pd.concat(localYSeres)

        pass

    # derived cols
    def deriveSpeed(self,
            tracksDf:pd.DataFrame
        ):

        tracksDf["speed"] = tracksDf.apply(
            lambda row: math.sqrt(row[self.xVelCol] ** 2 + row[self.yVelCol] ** 2),
            axis=1
        )


    def deriveDisplacements(self,
            tracksDf:pd.DataFrame
        ):

        # displacement wrt the first row
        firstRow = tracksDf.iloc[0]
        firstX = firstRow[self.xCol]
        firstY = firstRow[self.yCol]

        tracksDf[self.displacementXCol] = tracksDf.apply(
            lambda row: abs(firstX - row[self.xCol]),
            axis=1
        )

        tracksDf[self.displacementYCol] = tracksDf.apply(
            lambda row: abs(firstY - row[self.yCol]),
            axis=1
        )

    
    def rotate(self, trackDf: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """rotation is y=-y and x=-x. Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track
        """

        raise NotImplemented("Not implemented error")
    
    def rotate180(self, trackDf: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """rotation is y=-y and x=-x. Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track
        """

        X = -trackDf[self.localXCol]
        Y = -trackDf[self.localYCol]

        return X, Y

    def flipAlongY(self, trackDf: pd.DataFrame):
        """Flips along the y axis (negates x coordinates). Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track

        """
        # TODO
        
        pass

    def flipAlongX(self, trackDf: pd.DataFrame):
        """Flips along the x axis (negates y coordinates). Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track

        """
        # TODO
        pass

    
    

        
