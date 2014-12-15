import math

class PerkEvaluatorMetric:

  def __init__( self ):
    pass
  
  def GetMetricName( self ):
    return "RMS"
    
  def GetMetricUnit( self ):
    return "mm"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return []
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def Initialize( self ): 
    self.xList=[]
    self.yList=[]
    self.zList=[]
    
    self.pointCounter=0
	
	    
  def AddTimestamp( self, time, matrix, point ):
    #this does not need to be iterative because Finalize will work with the lists I am creating 	
    self.xList.append(point[0])
    self.yList.append(point[1])
    self.zList.append(point[2])
    self.pointCounter+=1
    
    
  def Finalize( self ):
    meanX=0
    meanY=0
    meanZ=0
    sumofcoordinates=0
    
    for i in range (0,len(self.xList)):
      meanX=meanX+(self.xList[i]/self.pointCounter)
    for i in range (0,len(self.yList)):
      meanY=meanY+(self.yList[i]/self.pointCounter)
    for i in range (0,len(self.zList)):
      meanZ=meanZ+(self.zList[i]/self.pointCounter)
	
    for i in range (0,len(self.xList)):
      sumofcoordinates=sumofcoordinates+((self.xList[i]-meanX)**2)+((self.yList[i]-meanY)**2)+((self.zList[i]-meanZ)**2)
    self.RMS=math.sqrt(sumofcoordinates/self.pointCounter)	
    
  def GetMetric( self ):
    return self.RMS