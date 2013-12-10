import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Time in Tissue"
    
  def GetMetricUnit( self ):
    return "s"
    
  def RequiresTissueNode( self ):
    return True
    
  def RequiresNeedle( self ):
    return False

  def Initialize( self, tissueNode ):
    self.tissueNode = tissueNode
    if ( self.tissueNode != None ):
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
      self.enclosedFilter.Initialize( tissueNode.GetPolyData() )
      
    self.tissueTime = 0
    
    self.timePrev = None
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( self.tissueNode != None and self.timePrev != None ):
      if ( self.enclosedFilter.IsInsideSurface( point[0], point[1], point[2] ) ):
        self.tissueTime = self.tissueTime + ( time - self.timePrev )
        
    self.timePrev = time
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.tissueTime