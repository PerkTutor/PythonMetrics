import math
import vtk

flashTimes = []

class PerkEvaluatorMetric:

  # Notes...
  NEIGHBOURHOOD = 0.15 #s
  MIN_PEAK_DIFFERENCE = 0 #deg/s
  MIN_PEAK_HEIGHT = 20 #deg/s

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Rotational Velocity Peaks"
  
  @staticmethod  
  def GetMetricUnit():
    return "count"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Any" ]
    
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
    
    
  # Instance methods  
  def __init__( self ):
    self.velocityPeaks = 0
    
    self.beforeVelocities = [ ]
    self.beforeTimes = [ ]
    
    self.afterVelocities = [ ]
    self.afterTimes = [ ]
    
    self.presentVelocities = [ ]
    self.presentTimes = [ ]
    
    self.timePrev = None
    self.matrixPrev = None
    
  def AddAnatomyRole( self, role, node ):
    pass
    
   
  def AddTimestamp( self, time, matrix, point ):
  
    if ( time == self.timePrev ):
      return
    
    if ( self.timePrev == None or self.matrixPrev == None ):
      self.timePrev = time
      self.matrixPrev = vtk.vtkMatrix4x4()
      self.matrixPrev.DeepCopy( matrix )
      return
    
    # Calculate the velocity at the current timestamp
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
    
    # Find the before/present/after times
    self.afterTimes.append( time )
    self.afterVelocities.append( currAbsAngularVelocity )
    
    while( len( self.afterTimes ) > 0 and ( self.afterTimes[ -1 ] - self.afterTimes[ 0 ] ) > PerkEvaluatorMetric.NEIGHBOURHOOD ):
      self.presentTimes.append( self.afterTimes.pop( 0 ) )
      self.presentVelocities.append( self.afterVelocities.pop( 0 ) )
      
    # Find the max in each list
    beforeMax = 0
    presentMax = 0
    afterMax = 0
    
    if( len( self.beforeVelocities ) > 0 ):
      beforeMax = max( self.beforeVelocities )
    if( len( self.presentVelocities ) > 0 ):
      presentMax = max( self.presentVelocities )
    if( len( self.beforeVelocities ) > 0 ):
      afterMax = max( self.afterVelocities )
      
    # Check if the largest is present. If so, then it is a peak    
    if ( ( presentMax - beforeMax ) > PerkEvaluatorMetric.MIN_PEAK_DIFFERENCE and ( presentMax - afterMax ) > PerkEvaluatorMetric.MIN_PEAK_DIFFERENCE and presentMax > PerkEvaluatorMetric.MIN_PEAK_HEIGHT ):
      self.velocityPeaks += 1
      
    # Find the before times
    while( len( self.presentTimes ) > 0 ):
      self.beforeTimes.append( self.presentTimes.pop( 0 ) )
      self.beforeVelocities.append( self.presentVelocities.pop( 0 ) )
      
    while( len( self.beforeTimes ) > 0 and ( self.beforeTimes[ -1 ] - self.beforeTimes[ 0 ] ) > PerkEvaluatorMetric.NEIGHBOURHOOD ):
      self.beforeTimes.pop( 0 )
      self.beforeVelocities.pop( 0 )
           
    self.timePrev = time
    self.matrixPrev = vtk.vtkMatrix4x4()
    self.matrixPrev.DeepCopy( matrix )

  def GetMetric( self ):
    return self.velocityPeaks