import numpy as np
import pandas as pd 
from typing import List
from .ColMapper import ColMapper

class TrajectoryProcessor:

    def __init__(self,
            colMapper: ColMapper
        ):
        self.colMapper = colMapper
        self.idCol = colMapper.idCol
        self.xCol = colMapper.xCol
        self.yCol = colMapper.yCol
        self.xVelCol = colMapper.xVelCol
        self.yVelCol = colMapper.yVelCol
        self.speedCol = colMapper.speedCol
        self.fps = colMapper.fps
        
        self.displacementXCol = colMapper.displacementXCol
        self.displacementYCol = colMapper.displacementYCol

        self.localXCol = colMapper.localXCol
        self.localYCol = colMapper.localYCol


        self.verticalDirectionCol = colMapper.verticalDirectionCol
        self.horizontalDirectionCol = colMapper.horizontalDirectionCol
    
    def getIds(self, 
            tracksDf:pd.DataFrame
        ) -> List[int]:

        return list(tracksDf[self.idCol].unique())
    
    def getMeta(self,
            tracksMeta: pd.DataFrame,
            trackId: int
        ) -> pd.Series:

        return tracksMeta[tracksMeta[self.idCol] == trackId].iloc[0]

