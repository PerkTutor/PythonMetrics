import math

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Path Length"
    
  def GetMetricUnit( self ):
    return "mm"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.pathLength = 0
    self.pointPrev = None
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.pointPrev != None ):
      currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )
      self.pathLength = self.pathLength + currPath

    self.pointPrev = point[:] # Require element copy 
    
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.pathLength