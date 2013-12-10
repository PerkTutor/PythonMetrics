import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Path in Tissue"
    
  def GetMetricUnit( self ):
    return "mm"
    
  def RequiresTissueNode( self ):
    return True
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.tissueNode = tissueNode
    if ( self.tissueNode != None ):
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
      self.enclosedFilter.Initialize( tissueNode.GetPolyData() )
      
    self.tissuePathLength = 0
    
    self.pointPrev = None
    
  def AddTimestamp( self, time, matrix, point ):
    
    if ( self.tissueNode != None and self.pointPrev != None ):    
      if ( self.enclosedFilter.IsInsideSurface( point[0], point[1], point[2] ) ):
        currPath = math.sqrt( math.pow( point[0] - self.pointPrev[0], 2 ) + math.pow( point[1] - self.pointPrev[1], 2 ) + math.pow( point[2] - self.pointPrev[2], 2 ) )    
        self.tissuePathLength = self.tissuePathLength + currPath
        
    self.pointPrev = point[:] # Require element copy 
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.tissuePathLength