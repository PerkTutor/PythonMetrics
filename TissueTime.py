import math
import vtk

class PerkEvaluatorMetric:

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Time in Tissue"
  
  @staticmethod  
  def GetMetricUnit():
    return "s"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Needle" ]
  
  @staticmethod  
  def GetRequiredAnatomyRoles():
    return { "Tissue": "vtkMRMLModelNode" }
  
  
  # Instance methods
  def __init__( self ):
    self.tissueTime = 0    
    self.timePrev = None
    
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
  
    if ( self.tissueNode != None and self.timePrev != None ):
      if ( self.enclosedFilter.IsInsideSurface( point[0], point[1], point[2] ) ):
        self.tissueTime = self.tissueTime + ( time - self.timePrev )
        
    self.timePrev = time
    
  def GetMetric( self ):
    return self.tissueTime