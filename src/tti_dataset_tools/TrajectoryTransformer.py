import pandas as pd
from typing import *
import math
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor
from .TrajectoryMetaBuilder import TrajectoryMetaBuilder

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
            # print(f"translating track {trackId}")
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            X, Y = self.translateOneToLocalSource(trackDf)
            localXSeres.append(X)
            localYSeres.append(Y)
        

        tracksDf[self.localXCol] = pd.concat(localXSeres)
        tracksDf[self.localYCol] = pd.concat(localYSeres)


        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            self.__validateLocalSource(trackDf)

        pass

    def __validateLocalSource(self, trackDf: pd.DataFrame):
        firstRow = trackDf.iloc[0]
        if firstRow[self.localXCol] != 0.0 or firstRow[self.localYCol] != 0.0:
            raise Exception(f"track {firstRow[self.idCol]} has incorrect local source {firstRow[self.localXCol]}, {firstRow[self.localYCol]}")
        

    # derived cols
    
    
    def getTimeDerivativeForOne(self, aTrack: pd.DataFrame, onCol):
        derivativeSeries = aTrack[onCol].rolling(window=2).apply(
            lambda values: (values.iloc[0] - values.iloc[1]) / (1 / self.fps))
        derivativeSeries.iloc[0] = derivativeSeries.iloc[1]
        # print(derivativeSeries)
        return derivativeSeries

    def getVelocitySeriesForOne(self, aTrack: pd.DataFrame, onCol):
        return self.getTimeDerivativeForOne(aTrack, onCol)
        
    def getVelocitySeriesForAll(self, tracksDf: pd.DataFrame, onCol):
        individualSeres = []
        # for trackId in tqdm(tracksDf[self.idCol].unique(), desc=f"deriving velocity on {onCol} at fps {fps}", position=0):
        for trackId in tracksDf[self.idCol].unique():
            aTrack = tracksDf[tracksDf[self.idCol] == trackId]
            individualSeres.append(
                self.getTimeDerivativeForOne(aTrack, onCol))

        velSeries = pd.concat(individualSeres)
        return velSeries

    def getAccelerationSeriesForAll(self, tracksDf: pd.DataFrame, onCol):
        individualSeres = []
        # for trackId in tqdm(tracksDf[self.idCol].unique(), desc=f"deriving acceleration on {onCol} at fps {fps}", position=0):
        for trackId in tracksDf[self.idCol].unique():
            aTrack = tracksDf[tracksDf[self.idCol] == trackId]
            individualSeres.append(
                self.getTimeDerivativeForOne(aTrack, onCol))

        accSeries = pd.concat(individualSeres)
        return accSeries

    def getAccelerationSerieFromVelocityForOne(self, velocitySeries: pd.Series):
        seriesAcc = velocitySeries.rolling(window=2).apply(
            lambda values: (values.iloc[0] - values.iloc[1]) / (1 / self.fps))
        seriesAcc.iloc[0] = seriesAcc.iloc[1]
        return seriesAcc

        pass

    def trimHeadAndTailForAll(self, tracksDf: pd.DataFrame):
        trimmedTracks = []
        # for trackId in tqdm(tracksDf[self.idCol].unique(), desc=f"trimming trajectories"):
        for trackId in tracksDf[self.idCol].unique():
            aTrack = tracksDf[tracksDf[self.idCol] == trackId]
            trimmedTracks.append(aTrack.iloc[2: len(aTrack) - 2, :]) # 4 frames to exclude invalid acceleration and velocities
        
        return pd.concat(trimmedTracks)

        
    def deriveAxisVelocities(self,
            tracksDf:pd.DataFrame
        ):
        tracksDf[self.xVelCol] = self.getVelocitySeriesForAll(tracksDf, self.xCol)
        tracksDf[self.yVelCol] = self.getVelocitySeriesForAll(tracksDf, self.yCol)
        pass

    def deriveSpeed(self,
            tracksDf:pd.DataFrame
        ):

        tracksDf["speed"] = tracksDf.apply(
            lambda row: math.sqrt(row[self.xVelCol] ** 2 + row[self.yVelCol] ** 2),
            axis=1
        )
    
    def smoothenSpeed(self,
            tracksDf:pd.DataFrame,
            targetFps: float = 2.5
        ):

        windowSize = int(self.fps / targetFps)
        
        allTrackIds = tracksDf[self.idCol].unique()
        smoothSeres = []
        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            smoothVals = trackDf['speed'].rolling(window=windowSize, win_type='gaussian', min_periods=1, center=True).mean(std=1)
            smoothVals.fillna(0, inplace=True)
            smoothSeres.append(smoothVals)
        
        # print(smoothSeres)
        tracksDf['speedSmooth'] = pd.concat(smoothSeres)


    def deriveDisplacementsForOne(self, trackDf: pd.DataFrame):
        xCol = self.xCol
        yCol = self.yCol
        firstRow = trackDf.iloc[0]
        firstX = firstRow[xCol]
        firstY = firstRow[yCol]

        return (trackDf[self.xCol] - firstX).abs(), (trackDf[self.yCol] - firstY).abs()

    def deriveDisplacements(self,
            tracksDf:pd.DataFrame,
            localAxis=False
        ):
        """
        Derives the displacements from the first point of each track
        """

        xCol = self.xCol
        yCol = self.yCol

        if localAxis:
            xCol = self.localXCol
            yCol = self.localYCol

        # # displacement wrt the first row
        # firstRow = tracksDf.iloc[0]
        # firstX = firstRow[xCol]
        # firstY = firstRow[yCol]

        # tracksDf[self.displacementXCol] = tracksDf.apply(
        #     lambda row: abs(firstX - row[xCol]),
        #     axis=1
        # )

        # tracksDf[self.displacementYCol] = tracksDf.apply(
        #     lambda row: abs(firstY - row[yCol]),
        #     axis=1
        # )

        allTrackIds = tracksDf[self.idCol].unique()

        dXSeres = []
        dYSeres = []

        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            X, Y = self.deriveDisplacementsForOne(trackDf)
            dXSeres.append(X)
            dYSeres.append(Y)
        

        tracksDf[self.displacementXCol] = pd.concat(dXSeres)
        tracksDf[self.displacementYCol] = pd.concat(dYSeres)

        for trackId in allTrackIds:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            self.__validateDisplacement(trackDf)

    
    def deriveDisplacementsInLC(self,
            tracksDf:pd.DataFrame
        ):
        """In local coordinate system

        Args:
            tracksDf (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        return self.deriveDisplacements(tracksDf, localAxis=True)


        
    def __validateDisplacement(self, trackDf: pd.DataFrame):
        
        firstRow = trackDf.iloc[0]
        if firstRow[self.displacementXCol] != 0.0 or firstRow[self.displacementYCol] != 0.0:
            raise Exception(f"track {firstRow[self.idCol]} has incorrect local source displacement {firstRow[self.displacementXCol]}, {firstRow[self.displacementYCol]}")
        
        

    def rotate(self, trackDf: pd.DataFrame, xCol: str, yCol: str) -> Tuple[pd.Series, pd.Series]:
        """rotation is y=-y and x=-x. Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track
        """

        raise NotImplemented("Not implemented error")
    
    def rotate180(self, trackDf: pd.DataFrame, xCol: str, yCol: str) -> Tuple[pd.Series, pd.Series]:
        """rotation is y=-y and x=-x. Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track
        """

        X = -trackDf[xCol]
        Y = -trackDf[yCol]

        return X, Y
    

    def flipAlongY(self, trackDf: pd.DataFrame, xCol: str, yCol: str):
        """Flips along the y axis (negates x coordinates). Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track

        """
        # TODO
        
        pass

    def flipAlongX(self, trackDf: pd.DataFrame, xCol: str, yCol: str):
        """Flips along the x axis (negates y coordinates). Does inplace transformation on localX, localY

        Args:
            trackDf (pd.DataFrame): A single track

        """
        # TODO
        pass


    # region direction transfomations
    def convertTracksToNorth(self,
            tracksDf:pd.DataFrame,
            xCol: str,
            yCol: str,
            tracksMeta: pd.DataFrame = None,
        ) -> Tuple[List[int], pd.DataFrame]:
        
        if tracksMeta is None:
            metaBuilder = TrajectoryMetaBuilder(self.colMapper)
            tracksMeta = metaBuilder.build([tracksDf], xCol, yCol)

        copiedDf = tracksDf.copy()
        allPedIds = self.getIds(copiedDf)

        southIds = []
        for pedId in allPedIds:
            trackDf = copiedDf[copiedDf[self.idCol] == pedId]
            trackMeta = self.getMeta(tracksMeta, pedId)
            # print(trackMeta[self.verticalDirectionCol])
            if trackMeta[self.verticalDirectionCol] == "SOUTH":
                southIds.append(pedId)
                # print(trackMeta[self.idCol])
                X, Y = self.rotate180(trackDf, xCol=xCol, yCol=yCol)
                copiedDf.loc[copiedDf[self.idCol] == pedId, xCol] = X
                copiedDf.loc[copiedDf[self.idCol] == pedId, yCol] = Y
        
        return southIds, copiedDf
    # endregion

    
    

        
