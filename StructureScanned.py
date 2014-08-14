import math
import vtk

class PerkEvaluatorMetric:

  # Image extent
  IMAGE_X_EXTENT = 1000 #pixels
  IMAGE_Y_EXTENT = 1000 #pixels

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
      self.bspTree = vtk.vtkModifiedBSPTree()
      self.bspTree.SetDataSet( self.tissueNode.GetPolyData() )
      self.bspTree.BuildLocator()
      
    self.structureScanned = 0    
    
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.tissueNode == None or self.bspTree == None ):
      return
      
    # To speed things up, if the structure has already been scanned, then skip
    if ( self.structureScanned == 1 ):
      return

    # Assume the matrix is ImageToRAS
    
    # For each scan line
    # Assume the x-axis is equivalent to the marked-unmarked axis
    for i in range( PerkEvaluatorMetric.IMAGE_X_EXTENT ):
      # Find end points of the current scan line in the Image coordinate system
      startPoint_Image = [ i, 0, 0, 1 ]
      endPoint_Image = [ i, PerkEvaluatorMetric.IMAGE_Y_EXTENT, 0, 1 ]
      
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
    
  def Finalize( self ):
    pass
    
  def GetMetric( self ):
    return self.structureScanned