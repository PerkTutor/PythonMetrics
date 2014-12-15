import math

class PerkEvaluatorMetric:

  def __init__( self ):
    pass
  
  def GetMetricName( self ):
    return "Average Velocity"
    
  def GetMetricUnit( self ):
    return "mm/s"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return []
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def Initialize( self ):
    self.velocitySum = 0
    self.timestampCount = 0
    self.averageVelocity = 0
    
    self.timePrev = None
    self.pointPrev = None
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( time == self.timePrev ):
      return
  
    if ( self.timePrev != None and self.pointPrev != None ):
      currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )
      self.velocitySum = self.velocitySum + currPath / ( time - self.timePrev )
      self.timestampCount = self.timestampCount + 1
      
    self.timePrev = time
    self.pointPrev = point[:] # Require element copy 
    
  def Finalize( self ):
    self.averageVelocity = self.velocitySum / self.timestampCount
    
  def GetMetric( self ):
    return self.averageVelocity