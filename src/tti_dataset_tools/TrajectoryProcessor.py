import numpy as np
import pandas as pd
from .ColMapper import ColMapper

class TrajectoryProcessor:

    def __init__(self,
            colMapper: ColMapper
        ):
        self.idCol = colMapper.idCol
        self.xCol = colMapper.xCol
        self.yCol = colMapper.yCol
        self.xVelCol = colMapper.xVelCol
        self.yVelCol = colMapper.yVelCol
        self.speedCol = colMapper.speedCol
        
        self.displacementXCol = colMapper.displacementXCol
        self.displacementYCol = colMapper.displacementYCol
