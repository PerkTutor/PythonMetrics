import math
import vtk

class PerkEvaluatorMetric:

  # Note: An action is defined as a time period where the absolute angular velocity of motion is greater than some threshold
  ANGULAR_VELOCITY_THRESHOLD = 50 #deg/s
  TIME_THRESHOLD = 0.2 #s

  def __init__( self ):
    pass
  
  def GetMetricName( self ):
    return "Rotational Actions"
    
  def GetMetricUnit( self ):
    return "count"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return []
    
  def AddAnatomyRole( self, role, node ):
    pass
    
  def Initialize( self ):
    self.numActions = 0
    
    self.actionState = 0
    self.completeActionTime = 0
    
    self.timePrev = None
    self.matrixPrev = None
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    if ( time == self.timePrev ):
      return
    
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
    
    currAngularVelocity = [ 0, 0, 0, 0 ]
    currChangeTransform.GetOrientationWXYZ( currAngularVelocity )
    
    # Deal make range -180 to 180
    if ( currAngularVelocity[ 0 ] > 180 ):
      currAngularVelocity[ 0 ] = currAngularVelocity[ 0 ] - 360
   
    currAngularVelocity[ 0 ] = currAngularVelocity[ 0 ] / ( time - self.timePrev )
    
    currAbsAngularVelocity = abs( currAngularVelocity[ 0 ] )    
    currentTestState = ( currAbsAngularVelocity > PerkEvaluatorMetric.ANGULAR_VELOCITY_THRESHOLD )
    
    if ( currentTestState == self.actionState ):
      self.completeActionTime = time
    else:
      if ( ( time - self.completeActionTime ) > PerkEvaluatorMetric.TIME_THRESHOLD ):
        self.actionState = currentTestState
        self.completeActionTime = time
        if ( currentTestState == 1 ):
          self.numActions += 1
        
    self.timePrev = time
    self.matrixPrev = vtk.vtkMatrix4x4()
    self.matrixPrev.DeepCopy( matrix )

    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.numActions