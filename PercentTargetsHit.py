import math
import vtk
import slicer

class PerkEvaluatorMetric:

  # A structure is "in" the imaging plane if it is within some small threshold of the plane
  IMAGE_PLANE_THRESHOLD = 5 #mm (since scaling should be uniform)
  # And is within the depth
  IMAGE_X_MIN = 173 #pixels
  IMAGE_X_MAX = 793 #pixels
  IMAGE_Y_MIN = 153 #pixels
  IMAGE_Y_MAX = 625 #pixels

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Targets Hit"
  
  @staticmethod  
  def GetMetricUnit():
    return "%"
  
  @staticmethod
  def GetAcceptedTransformRoles():
    return [ "Ultrasound" ]
  
  @staticmethod
  def GetRequiredAnatomyRoles():
    return { "POIs": "vtkMRMLMarkupsFiducialNode" }
    
    
  # Instance methods    
  def __init__( self ):
    pass
    
  def AddAnatomyRole( self, role, node ):
    if ( node == None or self.GetRequiredAnatomyRoles()[ role ] != node.GetClassName() ):
      return False
    
    if ( role == "POIs" ):
      self.targets = node  
      self.hitTargets = [ 0 ] * self.targets.GetNumberOfFiducials()
      
      return True
      
    return False

    
  def AddTimestamp( self, time, matrix, point ):
  
    for i in range( self.targets.GetNumberOfFiducials() ):
    
      # Find the centre of the fiducial
      centerPoint = [ 0, 0, 0 ]
      self.targets.GetNthFiducialPosition( i, centerPoint )
      centerPoint_RAS = [ centerPoint[ 0 ], centerPoint[ 1 ], centerPoint[ 2 ], 1 ]
      
      # Assume the matrix is ImageToRAS
      # We know the center of mass of the structure in the RAS coordinate system
      # Transform the center of mass into the image coordinate system
      RASToImageMatrix = vtk.vtkMatrix4x4()
      RASToImageMatrix.DeepCopy( matrix )
      RASToImageMatrix.Invert()
    
      centerPoint_Image = [ 0, 0, 0, 1 ]
      RASToImageMatrix.MultiplyPoint( centerPoint_RAS, centerPoint_Image )
    
      # Assumption is the imaging plane is in the Image coordinate system's XY plane    
      if ( centerPoint_Image[0] < PerkEvaluatorMetric.IMAGE_X_MIN or centerPoint_Image[0] > PerkEvaluatorMetric.IMAGE_X_MAX ):
        return
      
      if ( centerPoint_Image[1] < PerkEvaluatorMetric.IMAGE_Y_MIN or centerPoint_Image[1] > PerkEvaluatorMetric.IMAGE_Y_MAX ):
        return
    
      # Note: This only works for similarity matrix (i.e. uniform scale factor)
      scaleFactor = math.pow( vtk.vtkMatrix4x4().Determinant( matrix ), 1.0 / 3.0 )
    
      # Now check if the z-coordinate of the point in the image coordinate system is below some threshold value (i.e. 2mm)
      if ( abs( centerPoint_Image[2] ) < PerkEvaluatorMetric.IMAGE_PLANE_THRESHOLD / scaleFactor ):
        self.hitTargets[ i ] = 1
    
    
  def GetMetric( self ):
    return 100 * float( sum( self.hitTargets ) ) / len( self.hitTargets )