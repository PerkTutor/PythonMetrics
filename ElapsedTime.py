

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Elapsed Time"
    
  def GetMetricUnit( self ):
    return "s"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
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