

class PerkEvaluatorMetric:

  def __init__( self ):
    self.numTimestamps = 0
  
  def GetMetricName( self ):
    return "Timestamps"
    
  def GetMetricUnit( self ):
    return "count"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return []
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def AddTimestamp( self, time, matrix, point ):
    self.numTimestamps += 1
    
  def GetMetric( self ):
    return self.numTimestamps