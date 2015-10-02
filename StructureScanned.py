import math
import vtk

class PerkEvaluatorMetric:

  # Image extent
  IMAGE_X_MIN = 173 #pixels
  IMAGE_X_MAX = 793 #pixels
  IMAGE_Y_MIN = 153 #pixels
  IMAGE_Y_MAX = 625 #pixels

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Structure Scanned?"
    
  @staticmethod
  def GetMetricUnit():
    return "True/False"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Ultrasound" ]
  
  @staticmethod  
  def GetRequiredAnatomyRoles():
    return { "Target": "vtkMRMLModelNode" }
    
    
  # Instance methods  
  def __init__( self ):
    self.structureScanned = 0  
    
  def AddAnatomyRole( self, role, node ):
    if ( node == None or self.GetRequiredAnatomyRoles()[ role ] != node.GetClassName() ):
      return False
    
    if ( role == "Tissue" and node.GetPolyData() != None ):
      self.targetNode = node
      self.bspTree = vtk.vtkModifiedBSPTree()
      self.bspTree.SetDataSet( self.targetNode.GetPolyData() )
      self.bspTree.BuildLocator()      
      return True
      
    return False
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.targetNode == None or self.bspTree == None ):
      return
      
    # To speed things up, if the structure has already been scanned, then skip
    if ( self.structureScanned == 1 ):
      return

    # Assume the matrix is ImageToRAS
    
    # For each scan line
    # Assume the x-axis is equivalent to the marked-unmarked axis
    for i in range( PerkEvaluatorMetric.IMAGE_X_MIN, PerkEvaluatorMetric.IMAGE_X_MAX ):
      # Find end points of the current scan line in the Image coordinate system
      startPoint_Image = [ i, PerkEvaluatorMetric.IMAGE_Y_MIN, 0, 1 ]
      endPoint_Image = [ i, PerkEvaluatorMetric.IMAGE_Y_MAX, 0, 1 ]
      
      # Transform the end points into the RAS coordinate system
      startPoint_RAS = [ 0, 0, 0, 1 ]
      endPoint_RAS = [ 0, 0, 0, 1 ]
      matrix.MultiplyPoint( startPoint_Image, startPoint_RAS )
      matrix.MultiplyPoint( endPoint_Image, endPoint_RAS )
      startPoint_RAS = [ startPoint_RAS[ 0 ], startPoint_RAS[ 1 ], startPoint_RAS[ 2 ] ]
      endPoint_RAS = [ endPoint_RAS[ 0 ], endPoint_RAS[ 1 ], endPoint_RAS[ 2 ] ]
      
      # Check for intersection with the model
      # These parameters 
      INTERSECTION_POINT = [ 0, 0, 0 ]
      INTERSECTION_TOLERANCE = 0.001
      P_COORDS = [ 0, 0, 0 ]
      T = vtk.mutable(0)
      SUB_ID = vtk.mutable(0)
      
      scanlineIntersection = self.bspTree.IntersectWithLine( startPoint_RAS, endPoint_RAS, INTERSECTION_TOLERANCE, T, INTERSECTION_POINT, P_COORDS, SUB_ID )
      
      if ( scanlineIntersection == 1 ):
        self.structureScanned = 1
        return

    
  def GetMetric( self ):
    return self.structureScanned