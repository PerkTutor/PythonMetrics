

class PerkEvaluatorMetric:

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Timestamps"
  
  @staticmethod  
  def GetMetricUnit():
    return "count"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Any" ]
    
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
  
  
  # Instance methods  
  def __init__( self ):
    self.numTimestamps = 0
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def AddTimestamp( self, time, matrix, point ):
    self.numTimestamps += 1
    
  def GetMetric( self ):
    return self.numTimestamps