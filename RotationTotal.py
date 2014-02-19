import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Rotation Total"
    
  def GetMetricUnit( self ):
    return "deg"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.rotationTotal = 0
    self.matrixPrev = None
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( self.matrixPrev == None or self.matrixPrev == None ):
      self.matrixPrev = vtk.vtkMatrix4x4()
      self.matrixPrev.DeepCopy( matrix )
      return
    
    invertPrev = vtk.vtkMatrix4x4()
    invertPrev.DeepCopy( self.matrixPrev )
    invertPrev.Invert()
    
    currChangeMatrix = vtk.vtkMatrix4x4()
    vtk.vtkMatrix4x4().Multiply4x4( matrix, invertPrev, currChangeMatrix )

    currChangeTransform = vtk.vtkTransform()
    currChangeTransform.SetMatrix( currChangeMatrix )
	
    angleChange = [ 0, 0, 0, 0 ]
    currChangeTransform.GetOrientationWXYZ( angleChange )

    currAngleChange = min( angleChange[ 0 ], 360 - angleChange[ 0 ] )
    self.rotationTotal += currAngleChange
	
    self.matrixPrev = vtk.vtkMatrix4x4()
    self.matrixPrev.DeepCopy( matrix )

    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.rotationTotal