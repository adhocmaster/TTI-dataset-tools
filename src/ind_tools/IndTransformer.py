import pandas as pd
from typing import List
from tti_dataset_tools import TrajectoryProcessor, ColMapper, TrajectoryTransformer

class IndTransformer(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper
        ):
        
        super().__init__(colMapper)
        self.baseTransformer = TrajectoryTransformer(colMapper)
    
    def convertLocalToNorth(self,

            tracksDf:pd.DataFrame,
            tracksMeta: pd.DataFrame
        ) -> List[int]:
        """ 
        converts north-south trajectories into south-north. It does a 180 rotation on local x, y coordinates. Cannot call it repeatedly on the same dataframe
        """
        allPedIds = self.getIds(tracksDf)
        southIds = []
        for pedId in allPedIds:
            trackDf = tracksDf[tracksDf[self.idCol] == pedId]
            trackMeta = self.getMeta(tracksMeta, pedId)
            # print(trackMeta[self.verticalDirectionCol])
            if trackMeta[self.verticalDirectionCol] == "SOUTH":
                southIds.append(pedId)
                # print(trackMeta[self.idCol])
                X, Y = self.baseTransformer.rotate180(trackDf)
                tracksDf.loc[tracksDf[self.idCol] == pedId, self.localXCol] = X
                tracksDf.loc[tracksDf[self.idCol] == pedId, self.localYCol] = Y
        
        return southIds

