import math
import vtk
import slicer

class PerkEvaluatorMetric:

  # Get the image X and Y extents
  IMAGE_X_MIN = 173 #pixels
  IMAGE_X_MAX = 793 #pixels
  IMAGE_Y_MIN = 153 #pixels
  IMAGE_Y_MAX = 625 #pixels

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Display Ultrasound Sweep"
  
  @staticmethod  
  def GetMetricUnit():
    return "display"
  
  @staticmethod
  def GetAcceptedTransformRoles():
    return [ "Ultrasound" ]
    
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
    
    
  # Instance methods  
  def __init__( self ):
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetOrigin( PerkEvaluatorMetric.IMAGE_X_MIN, PerkEvaluatorMetric.IMAGE_Y_MIN, 0 )
    planeSource.SetPoint1( PerkEvaluatorMetric.IMAGE_X_MAX, PerkEvaluatorMetric.IMAGE_Y_MIN, 0 )
    planeSource.SetPoint2( PerkEvaluatorMetric.IMAGE_X_MIN, PerkEvaluatorMetric.IMAGE_Y_MAX, 0 )
    planeSource.Update()
    
    self.planePolyData = planeSource.GetOutput()
    
    self.sweptPolyData = vtk.vtkAppendPolyData()
    
    sweepModel = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelNode" )
    sweepModel.SetAndObservePolyData( self.sweptPolyData.GetOutput() )
    sweepModel.SetName( "UltrasoundSweep" )
    sweepModel.SetScene( slicer.mrmlScene )
  
    sweepModelDisplay = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelDisplayNode" )
    sweepModelDisplay.FrontfaceCullingOff()
    sweepModelDisplay.BackfaceCullingOff()
    sweepModelDisplay.SetScene( slicer.mrmlScene )
    sweepModelDisplay.SetInputPolyDataConnection( sweepModel.GetPolyDataConnection() )
  
    slicer.mrmlScene.AddNode( sweepModelDisplay )
    slicer.mrmlScene.AddNode( sweepModel )
  
    sweepModel.SetAndObserveDisplayNodeID( sweepModelDisplay.GetID() )
    
  def AddAnatomyRole( self, role, node ):
    pass

    
  def AddTimestamp( self, time, matrix, point ):
  
    worldTransform = vtk.vtkTransform()
    worldTransform.SetMatrix( matrix )
  
    planeSweepTransformPolyData = vtk.vtkTransformPolyDataFilter()
    planeSweepTransformPolyData.SetTransform( worldTransform )
    planeSweepTransformPolyData.SetInputData( self.planePolyData )
    planeSweepTransformPolyData.Update()
  
    self.sweptPolyData.AddInputData( planeSweepTransformPolyData.GetOutput() )
    self.sweptPolyData.Update()  

    
  def GetMetric( self ):
    return 0