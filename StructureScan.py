import math
import vtk

class PerkEvaluatorMetric:

  # A structure is "in" the imaging plane if it is within some small threshold of the plane
  IMAGE_PLANE_THRESHOLD = 2 #mm (since scaling should be uniform)
  # And is within the depth
  IMAGE_X_EXTENT = 512 #pixels
  IMAGE_Y_EXTENT = 512 #pixels

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Structure Scanned?"
    
  def GetMetricUnit( self ):
    return "True/False"
    
  def RequiresTissueNode( self ):
    return True
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.tissueNode = tissueNode
    if ( self.tissueNode != None ):
      comFilter = vtk.vtkCenterOfMass()
      comFilter.SetInputData( tissueNode.GetPolyData() )
      comFilter.SetUseScalarsAsWeights( False )
      comFilter.Update()
      
      self.centerPoint = comFilter.GetCenter()
      self.centerPoint_RAS = [ self.centerPoint[0], self.centerPoint[1], self.centerPoint[2], 1 ]
      
    self.structureScanned = 0
    
  def AddTimestamp( self, time, matrix, point ):
    
    # Assume the matrix is ImageToRAS
    # We know the center of mass of the structure in the RAS coordinate system
    # Transform the center of mass into the image coordinate system
    RASToImageMatrix = vtk.vtkMatrix4x4()
    RASToImageMatrix.DeepCopy( matrix )
    RASToImageMatrix.Invert()
    
    centerPoint_Image = [ 0, 0, 0, 1 ]
    RASToImageMatrix.MultiplyPoint( self.centerPoint_RAS, centerPoint_Image )
    
    # Assumption is the imaging plane is in the Image coordinate system's XY plane    
    if ( centerPoint_Image[0] < 0 or centerPoint_Image[0] > PerkEvaluatorMetric.IMAGE_X_EXTENT ):
      return
      
    if ( centerPoint_Image[1] < 0 or centerPoint_Image[1] > PerkEvaluatorMetric.IMAGE_Y_EXTENT ):
      return
    
    # Note: This only works for similarity matrix (i.e. uniform scale factor)
    scaleFactor = math.pow( vtk.vtkMatrix4x4().Determinant( matrix ), 1.0 / 3.0 )
    
    # Now check if the z-coordinate of the point in the image coordinate system is below some threshold value (i.e. 2mm)
    if ( abs( centerPoint_Image[2] ) < PerkEvaluatorMetric.IMAGE_PLANE_THRESHOLD / scaleFactor ):
      self.structureScanned = 1
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.structureScanned