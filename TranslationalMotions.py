import math
import vtk

class PerkEvaluatorMetric:

  VELOCITY_THRESHOLD = 7.5 #mm/s

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Translational Motions"
    
  def GetMetricUnit( self ):
    return "count"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.numMotions = 0
    
    self.rateTransformPrev = None
    
    self.timePrev = None
    self.matrixPrev = None
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( self.timePrev == None or self.matrixPrev == None ):
      self.timePrev = time
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
    
    currVelocity = [ 0, 0, 0 ]
    currChangeTransform.GetPosition( currVelocity )
    vtk.vtkMath().MultiplyScalar( currVelocity, 1 / ( time - self.timePrev ) )
    
    currAngle = [ 0, 0, 0, 0 ]
    currChangeTransform.GetOrientationWXYZ( currAngle )
    currAngle[ 0 ] = currAngle[ 0 ] / ( time - self.timePrev )
    
    currRateTransform = vtk.vtkTransform()
    currRateTransform.Translate( currVelocity )
    currRateTransform.RotateWXYZ( currAngle[ 0 ], currAngle[ 1 ], currAngle[ 2 ], currAngle[ 3 ] )
    
    if ( self.rateTransformPrev == None ):
      self.rateTransformPrev = vtk.vtkTransform()
      self.rateTransformPrev.DeepCopy( currRateTransform )
      return
    
    invertRateTransformPrev = vtk.vtkTransform()
    invertRateTransformPrev.DeepCopy( self.rateTransformPrev )
    invertRateTransformPrev.Inverse()
    
    totalVelocityChangeTransform = vtk.vtkTransform()
    totalVelocityChangeTransform.PostMultiply()
    totalVelocityChangeTransform.Concatenate( currRateTransform )
    totalVelocityChangeTransform.Concatenate( invertRateTransformPrev )
    
    velocityChange = [ 0, 0, 0 ]
    totalVelocityChangeTransform.GetPosition( velocityChange )
    
    if ( vtk.vtkMath().Norm( velocityChange ) > PerkEvaluatorMetric.VELOCITY_THRESHOLD ):
      self.numMotions += 1
      self.rateTransformPrev = vtk.vtkTransform()
      self.rateTransformPrev.DeepCopy( currRateTransform )
    
    self.timePrev = time
    self.matrixPrev = vtk.vtkMatrix4x4()
    self.matrixPrev.DeepCopy( matrix )

    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.numMotions