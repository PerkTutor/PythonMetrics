import math
from PythonMetricsCalculator import PerkEvaluatorMetric

class PathLength( PerkEvaluatorMetric ):
  
  # Static methods
  @staticmethod
  def GetMetricName():
    return "Path Length"

  @staticmethod
  def GetMetricUnit():
    return "mm"
    
  @staticmethod
  def IsPervasive():
    return True
    
  @staticmethod
  def IsShared():
    return True
    
  
  # Instance methods
  def __init__( self ):
    PerkEvaluatorMetric.__init__( self )
    
    self.pathLength = 0
    self.pointPrev = None
    
  def AddTimestamp( self, time, matrix, point ):
    if ( self.pointPrev != None ):
      currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )
      self.pathLength = self.pathLength + currPath

    self.pointPrev = point[:] # Require element copy 
       
  def GetMetric( self ):
    return self.pathLength