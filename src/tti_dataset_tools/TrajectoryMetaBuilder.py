import pandas as pd
from typing import *
import math
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor
from .TrajectoryUtils import TrajectoryUtils
from .TrackClass import TrackClass

class TrajectoryMetaBuilder(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)
    
    def getMetaDictForTracks(self, tracksDf: pd.DataFrame, xCol: str, yCol: str):


        meta = {
            self.idCol: [],
            "initialFrame": [],
            "finalFrame": [],
            "numFrames": [],
            "class": [],
            "horizontalDirection": [],
            "verticalDirection": []
        }

        if len(tracksDf) == 0:
            return meta

        ids = tracksDf[self.idCol].unique()

        for trackId in ids:
            trackDf = tracksDf[tracksDf[self.idCol] == trackId]
            # print(trackId, len(trackDf))
            firstRow = trackDf.iloc[0]
            lastRow = trackDf.iloc[-1]

            vert, hort = TrajectoryUtils.getTrack_VH_Directions(
                trackDf, xCol, yCol)

            meta[self.idCol].append(trackId)
            meta["initialFrame"].append(firstRow["frame"])
            meta["finalFrame"].append(lastRow["frame"])
            meta["numFrames"].append(len(trackDf))
            if "class" in trackDf:
                meta["class"].append(firstRow["class"])
            else:
                meta["class"].append(TrackClass.Pedestrian.value)
            meta["horizontalDirection"].append(hort.value)
            meta["verticalDirection"].append(vert.value)

        return meta
    
    def build(
            self,
            dfs: List[pd.DataFrame],
            xCol: str, 
            yCol: str
        ):
        metas = [pd.DataFrame(self.getMetaDictForTracks(tracksDf, xCol, yCol)) for tracksDf in dfs]
        return pd.concat(metas, ignore_index=True)
        
