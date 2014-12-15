

class PerkEvaluatorMetric:

  def __init__( self ):
    pass
  
  def GetMetricName( self ):
    return "Elapsed Time"
    
  def GetMetricUnit( self ):
    return "s"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return []
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def Initialize( self ):
    self.elapsedTime = 0
    self.timePrev = None
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( self.timePrev != None ):
      self.elapsedTime = self.elapsedTime + ( time - self.timePrev )
      
    self.timePrev = time
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.elapsedTime