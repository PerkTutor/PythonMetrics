import math
import vtk
from PythonMetricsCalculator import PerkEvaluatorMetric

class TissuePath( PerkEvaluatorMetric ):

  # Static method
  @staticmethod
  def GetMetricName():
    return "Path in Tissue"
    
  @staticmethod
  def GetMetricUnit():
    return "mm"
    
  @staticmethod
  def IsShared():
    return True
  
  @staticmethod  
  def GetTransformRoles():
    return [ "Needle" ]
  
  @staticmethod
  def GetAnatomyRoles():
    return { "Tissue": "vtkMRMLModelNode" }
  
  
  # Instance methods
  def __init__( self ):
    PerkEvaluatorMetric.__init__( self )
    
    self.tissuePathLength = 0    
    self.pointPrev = None
    
  def SetAnatomy( self, role, node ):
    if ( role == "Tissue" and node.GetPolyData() != None ):
      self.tissueNode = node
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
      self.enclosedFilter.SetTolerance( 1e-12 )
      self.enclosedFilter.Initialize( self.tissueNode.GetPolyData() )      
      return True
      
    return False
    
  def AddTimestamp( self, time, matrix, point ):
    
    if ( self.tissueNode != None and self.pointPrev != None ):    
      if ( self.enclosedFilter.IsInsideSurface( point[0], point[1], point[2] ) ):
        currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )    
        self.tissuePathLength = self.tissuePathLength + currPath
        
    self.pointPrev = point[:] # Require element copy 
    
  def GetMetric( self ):
    return self.tissuePathLength