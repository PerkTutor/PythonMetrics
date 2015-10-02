

class PerkEvaluatorMetric:
  
  # Static methods
  @staticmethod
  def GetMetricName():
    return "Elapsed Time"
    
  @staticmethod
  def GetMetricUnit():
    return "s"
    
  @staticmethod
  def GetAcceptedTransformRoles():
    return [ "Any" ]
    
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
    
  
  # Instance methods
  def __init__( self ):
    self.elapsedTime = 0
    self.timePrev = None
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( self.timePrev != None ):
      self.elapsedTime = self.elapsedTime + ( time - self.timePrev )
      
    self.timePrev = time
    
  def GetMetric( self ):
    return self.elapsedTime