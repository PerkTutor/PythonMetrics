import math
import vtk

class PerkEvaluatorMetric:

  def __init__( self ):
    self.tissueDamage = 0
    
    self.matrixPrev = None
    self.pointPrev = None
  
  def GetMetricName( self ):
    return "Tissue Damage"
    
  def GetMetricUnit( self ):
    return "mm^2"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Needle" ]
    
  def GetRequiredAnatomyRoles( self ):
    return { "Tissue": "vtkMRMLModelNode" }
    
  def AddAnatomyRole( self, role, node ):
    if ( node == None or self.GetRequiredAnatomyRoles()[ role ] != node.GetClassName() ):
      return False
    
    if ( role == "Tissue" ):
      self.tissueNode = node
      self.enclosedFilter = vtk.vtkSelectEnclosedPoints()
      self.enclosedFilter.Initialize( self.tissueNode.GetPolyData() )
      
      self.bspTree = vtk.vtkModifiedBSPTree()
      self.bspTree.SetDataSet( self.tissueNode.GetPolyData() )
      self.bspTree.BuildLocator()
      
      return True
      
    return False 
    
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.tissueNode == None or self.matrixPrev == None or self.pointPrev == None ):
      self.matrixPrev = vtk.vtkMatrix4x4()
      self.matrixPrev.DeepCopy( matrix )
      self.pointPrev = point[:] # Require element copy
      return
    
    if ( self.enclosedFilter.IsInsideSurface( point[0], point[1], point[2] ) == False or self.enclosedFilter.IsInsideSurface( self.pointPrev[0], self.pointPrev[1], self.pointPrev[2] ) == False ):
      self.matrixPrev = vtk.vtkMatrix4x4()
      self.matrixPrev.DeepCopy( matrix )
      self.pointPrev = point[:] # Require element copy
      return
      
    # Find the base points (assume needle in y direction)
    NeedleBase = [ 300, 0, 0, 1 ]
    basePrev = [ 0, 0, 0, 1 ]
    baseCurr = [ 0, 0, 0, 1 ]
    self.matrixPrev.MultiplyPoint( NeedleBase, basePrev )
    matrix.MultiplyPoint( NeedleBase, baseCurr )
    
    # Make everything three elements long
    endPrev = [ 0, 0, 0 ]
    endCurr = [ 0, 0, 0 ]
    self.pointPrev = [ self.pointPrev[0], self.pointPrev[1], self.pointPrev[2] ]
    point = [ point[0], point[1], point[2] ]
    basePrev = [ basePrev[0], basePrev[1], basePrev[2] ]
    baseCurr = [ baseCurr[0], baseCurr[1], baseCurr[2] ]
    
    # Find the intersection between the needle and the surface tissue
    INTERSECTION_TOLERANCE = 0.001
    P_COORDS = [ 0, 0, 0 ]
    T = vtk.mutable(0)
    SUB_ID = vtk.mutable(0) 
    
    self.bspTree.IntersectWithLine( self.pointPrev, basePrev, INTERSECTION_TOLERANCE, T, endPrev, P_COORDS, SUB_ID )
    self.bspTree.IntersectWithLine( point, baseCurr, INTERSECTION_TOLERANCE, T, endCurr, P_COORDS, SUB_ID )
    
    # Calculate the first triangle area
    a1 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( point, self.pointPrev ) )   
    b1 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( point, endCurr ) )
    c1 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( endCurr, self.pointPrev ) )
    s1 = ( a1 + b1 + c1 ) / 2
    area1 = math.sqrt( s1 * ( s1 - a1 ) * ( s1 - b1 ) * ( s1 - c1 ) )
    
    # Calculate the second triangle area
    a2 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( endCurr, endPrev ) )   
    b2 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( endCurr, self.pointPrev ) )
    c2 = math.sqrt( vtk.vtkMath().Distance2BetweenPoints( self.pointPrev, endPrev ) )
    s2 = ( a2 + b2 + c2 ) / 2
    area2 = math.sqrt( s2 * ( s2 - a2 ) * ( s2 - b2 ) * ( s2 - c2 ) )
    
    self.tissueDamage = self.tissueDamage + area1 + area2
    
    self.matrixPrev = vtk.vtkMatrix4x4()
    self.matrixPrev.DeepCopy( matrix )
    self.pointPrev = point[:] # Require element copy 

    
  def GetMetric( self ):
    return self.tissueDamage