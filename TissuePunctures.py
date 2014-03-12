import math
import vtk

class PerkEvaluatorMetric:

  PUNCTURE_THRESHOLD = 5 #mm

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Tissue Punctures"
    
  def GetMetricUnit( self ):
    return "count"
    
  def RequiresTissueNode( self ):
    return True
    
  def RequiresNeedle( self ):
    return True
    
  def Initialize( self, tissueNode ):
    self.tissueNode = tissueNode
    
    if ( self.tissueNode != None ):
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
      self.enclosedFilter.Initialize( tissueNode.GetPolyData() )
      
    self.tissuePunctures = 0
    self.punctureState = False  
    
    
  def AddTimestamp( self, time, matrix, point ):
      
    # Find the three key points on the needle
    NeedleTip = [ 0, 0, 0, 1 ]
    NeedleTipPosition = [ 0, 0, 0, 1 ]
    NeedleTipForward = [ -PerkEvaluatorMetric.PUNCTURE_THRESHOLD, 0, 0, 1 ]
    NeedleTipForwardPosition = [ 0, 0, 0, 1 ]
    NeedleTipBackward = [ PerkEvaluatorMetric.PUNCTURE_THRESHOLD, 0, 0, 1 ]
    NeedleTipBackwardPosition = [ 0, 0, 0, 1 ]
    
    matrix.MultiplyPoint( NeedleTip, NeedleTipPosition )
    matrix.MultiplyPoint( NeedleTipForward, NeedleTipForwardPosition )
    matrix.MultiplyPoint( NeedleTipBackward, NeedleTipBackwardPosition )
    
    print NeedleTipPosition
    print NeedleTipForwardPosition
    
    NeedleTipInside = self.enclosedFilter.IsInsideSurface( NeedleTipPosition[0], NeedleTipPosition[1], NeedleTipPosition[2] )
    NeedleTipForwardInside = self.enclosedFilter.IsInsideSurface( NeedleTipForwardPosition[0], NeedleTipForwardPosition[1], NeedleTipForwardPosition[2] )
    NeedleTipBackwardInside = self.enclosedFilter.IsInsideSurface( NeedleTipBackwardPosition[0], NeedleTipBackwardPosition[1], NeedleTipBackwardPosition[2] )
    
    if ( self.punctureState == False ):
      if ( NeedleTipInside and NeedleTipForwardInside and NeedleTipBackwardInside ):
        self.tissuePunctures += 1
        self.punctureState = True
        
    if ( self.punctureState ):
      if ( NeedleTipInside == False and NeedleTipForwardInside == False and NeedleTipBackwardInside == False ):
        self.punctureState = False
        
    print self.punctureState
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.tissuePunctures