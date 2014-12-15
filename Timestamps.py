

class PerkEvaluatorMetric:

  def __init__( self ):
    pass
  
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
    
  def Initialize( self ):
    self.numTimestamps = 0
    
  def AddTimestamp( self, time, matrix, point ):
    self.numTimestamps += 1
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.numTimestamps