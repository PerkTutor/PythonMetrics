

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Timestamps"
    
  def GetMetricUnit( self ):
    return "count"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.numTimestamps = 0
    
  def AddTimestamp( self, time, matrix, point ):
    print time
    self.numTimestamps += 1
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.numTimestamps