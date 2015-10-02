import math

class PerkEvaluatorMetric:
  
  # Static methods
  @staticmethod
  def GetMetricName():
    return "Path Length"

  @staticmethod
  def GetMetricUnit():
    return "mm"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Any" ]
  
  @staticmethod  
  def GetRequiredAnatomyRoles():
    return {}
    
  
  # Instance methods
  def __init__( self ):
    self.pathLength = 0
    self.pointPrev = None
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.pointPrev != None ):
      currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )
      self.pathLength = self.pathLength + currPath

    self.pointPrev = point[:] # Require element copy 
       
  def GetMetric( self ):
    return self.pathLength