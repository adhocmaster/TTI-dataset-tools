class ColMapper:
    
    def __init__(self,
            idCol, 
            xCol, 
            yCol,
            xVelCol, 
            yVelCol, 
            speedCol,
            displacementXCol='displacementX',
            displacementYCol='displacementY'
        ):
        
        self.idCol = idCol
        self.xCol = xCol
        self.yCol = yCol
        self.xVelCol = xVelCol
        self.yVelCol = yVelCol
        self.speedCol = speedCol
        self.displacementXCol = displacementXCol
        self.displacementYCol = displacementYCol
        
        pass