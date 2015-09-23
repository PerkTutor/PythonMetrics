import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.tissueTime = 0    
    self.timePrev = None
  
  def GetMetricName( self ):
    return "Time in Tissue"
    
  def GetMetricUnit( self ):
    return "s"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Needle" ]
    
  def GetRequiredAnatomyRoles( self ):
    return [ "Tissue" ]
    
  def AddAnatomyRole( self, role, node ):
    if ( role == "Tissue" and node != None and node.GetClassName() == "vtkMRMLModelNode" ):
      self.tissueNode = node
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
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