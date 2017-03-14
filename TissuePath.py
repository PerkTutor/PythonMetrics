import math
import vtk

class PerkEvaluatorMetric:

  # Static method
  @staticmethod
  def GetMetricName():
    return "Path in Tissue"
    
  @staticmethod
  def GetMetricUnit():
    return "mm"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Needle" ]
  
  @staticmethod
  def GetRequiredAnatomyRoles():
    return { "Tissue": "vtkMRMLModelNode" }
  
  
  # Instance methods
  def __init__( self ):
    self.tissuePathLength = 0    
    self.pointPrev = None
    
  def AddAnatomyRole( self, role, node ):
    if ( node == None or self.GetRequiredAnatomyRoles()[ role ] != node.GetClassName() ):
      return False
      
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