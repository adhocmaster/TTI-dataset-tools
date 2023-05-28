import pandas as pd
from typing import List, Tuple
from tti_dataset_tools import TrajectoryProcessor, ColMapper, TrajectoryTransformer, TrajectoryMetaBuilder

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
        return self.baseTransformer.convertTracksToNorth(
            tracksDf, 
            xCol=self.localXCol, 
            yCol=self.localYCol, 
            tracksMeta=tracksMeta
        )
    
    def convertSceneTracksToNorth(self,
            tracksDf:pd.DataFrame,
            tracksMeta: pd.DataFrame = None
        ) -> Tuple[List[int], pd.DataFrame]:
        """ 
        converts north-south trajectories into south-north. It does a 180 rotation on local x, y coordinates. Cannot call it repeatedly on the same dataframe
        """
        return self.baseTransformer.convertTracksToNorth(
            tracksDf, 
            xCol="sceneX", 
            yCol="sceneY", 
            tracksMeta=tracksMeta
        )

