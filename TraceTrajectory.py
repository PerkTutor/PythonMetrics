import math
import vtk
import slicer

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Display Trajectory"
    
  def GetMetricUnit( self ):
    return "display"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    
    self.curvePoints = vtk.vtkPoints()
    self.curveLines = vtk.vtkCellArray()
    self.curvePolyData = vtk.vtkPolyData()
    self.counter = 0
    
    self.curvePolyData.SetPoints( self.curvePoints )
    self.curvePolyData.SetLines( self.curveLines )
    

    
    
  def AddTimestamp( self, time, matrix, point ):
  
    # Some initialization for the first point
    if ( self.curveLines.GetNumberOfCells() == 0 ):
      self.curvePoints.InsertNextPoint( point[ 0 ], point[ 1 ], point[ 2 ] )
      self.curveLines.InsertNextCell( 1 )
      self.curveLines.InsertCellPoint( 0 )
  
    self.curvePoints.InsertPoint( self.counter + 1, point[ 0 ], point[ 1 ], point[ 2 ] )
    
    self.curveLines.InsertNextCell( 2 ) # Because there are two points in the cell
    self.curveLines.InsertCellPoint( self.counter )
    self.curveLines.InsertCellPoint( self.counter + 1 )
    self.counter += 1

    
  def Finalize( self ):
    # Turn the polydata into a model    
    curveModel = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelNode" )
    curveModel.SetAndObservePolyData( self.curvePolyData )
    curveModel.SetName( "TrajectoryTrace" )
    curveModel.SetScene( slicer.mrmlScene )
  
    curveModelDisplay = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelDisplayNode" )
    curveModelDisplay.SetScene( slicer.mrmlScene )
    curveModelDisplay.SetInputPolyDataConnection( curveModel.GetPolyDataConnection() )
  
    slicer.mrmlScene.AddNode( curveModelDisplay )
    slicer.mrmlScene.AddNode( curveModel )
  
    curveModel.SetAndObserveDisplayNodeID( curveModelDisplay.GetID() )
    
  def GetMetric( self ):
    return 0