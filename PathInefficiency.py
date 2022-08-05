import math
import vtk

from PythonMetricsCalculator import PerkEvaluatorMetric

class PathInefficiency( PerkEvaluatorMetric ):

  @staticmethod
  def GetMetricName():
    return "Path Inefficiency"

  @staticmethod
  def GetMetricUnit():
    return "%"

  @staticmethod
  def GetAcceptedTransformRoles():
    return ["Any"]


  def __init__( self ):
    PerkEvaluatorMetric.__init__( self )

    self.startPoint = None
    self.prevPoint = None

    self.startFinishDistance = 0
    self.pathLength = 0

  def AddTimestamp( self, time, matrix, point ):
    if ( self.startPoint is None ):
      self.startPoint = point[:]
      
    self.startFinishDistance = math.sqrt( vtk.vtkMath.Distance2BetweenPoints( self.startPoint[:3], point[:3] ) )

    if ( self.prevPoint != None ):
      currPath = math.sqrt( math.pow( point[0] - self.prevPoint[0], 2 ) + math.pow( point[1] - self.prevPoint[1], 2 ) + math.pow( point[2] - self.prevPoint[2], 2 ) )
      self.pathLength = self.pathLength + currPath

    self.prevPoint = point[:] # Require element copy

  def GetMetric( self ):
    return 100 * ( self.pathLength / self.startFinishDistance - 1 )