from PythonMetricsCalculator import PerkEvaluatorMetric

class ElapsedTime( PerkEvaluatorMetric ):
  
  # Static methods
  @staticmethod
  def GetMetricName():
    return "Elapsed Time"
    
  @staticmethod
  def GetMetricUnit():
    return "s"
    
  @staticmethod
  def IsPervasive():
    return True
    
  @staticmethod
  def IsShared():
    return True
    
  
  # Instance methods
  def __init__( self ):
    PerkEvaluatorMetric.__init__( self )
    
    self.elapsedTime = 0
    self.timePrev = None
    
  def AddTimestamp( self, time, matrix, point, role ):  
    if ( self.timePrev != None ):
      self.elapsedTime = self.elapsedTime + ( time - self.timePrev )
      
    self.timePrev = time
    
  def GetMetric( self ):
    return self.elapsedTime