class ColMapper:
    
    def __init__(self,
            idCol, 
            xCol, 
            yCol,
            xVelCol, 
            yVelCol, 
            speedCol,
            fps,
            displacementXCol='displacementX',
            displacementYCol='displacementY',
            localXCol='localX',
            localYCol='localY',
        
        ):
        
        self.idCol = idCol
        self.xCol = xCol
        self.yCol = yCol
        self.xVelCol = xVelCol
        self.yVelCol = yVelCol
        self.speedCol = speedCol
        self.fps = fps
        
        self.displacementXCol = displacementXCol
        self.displacementYCol = displacementYCol

        self.localXCol = localXCol
        self.localYCol = localYCol

        pass