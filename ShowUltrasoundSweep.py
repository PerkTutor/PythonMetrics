import math
import vtk
from PythonMetricsCalculator import PerkEvaluatorMetric

class ShowUltrasoundSweep( PerkEvaluatorMetric ):

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
    return ""
  
  @staticmethod
  def GetTransformRoles():
    return [ "Ultrasound" ]
    
  @staticmethod
  def GetAnatomyRoles():
    return { "OutputModel": "vtkMRMLModelNode" }
    
    
  # Instance methods  
  def __init__( self ):
    PerkEvaluatorMetric.__init__( self )
    
    self.outputPolyData = vtk.vtkAppendPolyData()
    
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetOrigin( PerkEvaluatorMetric.IMAGE_X_MIN, PerkEvaluatorMetric.IMAGE_Y_MIN, 0 )
    planeSource.SetPoint1( PerkEvaluatorMetric.IMAGE_X_MAX, PerkEvaluatorMetric.IMAGE_Y_MIN, 0 )
    planeSource.SetPoint2( PerkEvaluatorMetric.IMAGE_X_MIN, PerkEvaluatorMetric.IMAGE_Y_MAX, 0 )
    planeSource.Update()
    self.planePolyData = planeSource.GetOutput()
    
  def SetAnatomy( self, role, node ):   
    if ( role == "OutputModel" ):
      node.SetAndObservePolyData( self.outputPolyData )
      if ( node.GetModelDisplayNode() is None ):
        node.CreateDefaultDisplayNodes()
      modelDisplayNode = node.GetModelDisplayNode()
      modelDisplayNode.FrontfaceCullingOff()
      modelDisplayNode.BackfaceCullingOff() 
      return True
      
    return False
    
  def AddTimestamp( self, time, matrix, point, role ):  
    worldTransform = vtk.vtkTransform()
    worldTransform.SetMatrix( matrix )
  
    planeSweepTransformPolyData = vtk.vtkTransformPolyDataFilter()
    planeSweepTransformPolyData.SetTransform( worldTransform )
    planeSweepTransformPolyData.SetInputData( self.planePolyData )
    planeSweepTransformPolyData.Update()
  
    self.outputPolyData.AddInputData( planeSweepTransformPolyData.GetOutput() )
    self.outputPolyData.Update()