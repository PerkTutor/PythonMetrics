import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Depth Perception"
    
  def GetMetricUnit( self ):
    return "mm"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return True
    
  def Initialize( self, tissueNode ):
    self.depthPerception = 0 
    self.pointPrev = None    
    
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.pointPrev == None ):
      self.pointPrev = point[:]
      
    # Find the prev to current vector
    prevToCurrentVector = [ 0, 0, 0 ]
    vtk.vtkMath().Subtract( point[0:3], self.pointPrev[0:3], prevToCurrentVector )
    prevToCurrentVector = [ prevToCurrentVector[ 0 ], prevToCurrentVector[ 1 ], prevToCurrentVector[ 2 ] ]
    
    # Assume the needle is in the y-direction
    needleTip = [ point[ 0 ], point[ 1 ], point[ 2 ] ]
    needleBase = [ 0, 0, 0, 1 ]
    matrix.MultiplyPoint( [ 0, 1, 0, 1 ], needleBase )
    needleBase = [ needleBase[ 0 ], needleBase[ 1 ], needleBase[ 2 ] ]
    baseToTipVector = [ 0, 0, 0 ]
    vtk.vtkMath().Subtract( needleTip[0:3], needleBase[0:3], baseToTipVector )
    
    # Find the movement in the needle direction
    needleAxisMovement = vtk.vtkMath().Dot( prevToCurrentVector, baseToTipVector )
    
    self.depthPerception += math.fabs( needleAxisMovement )
    
    self.pointPrev = point[:]
    
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.depthPerception