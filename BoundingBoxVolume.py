import math

class PerkEvaluatorMetric:

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Bounding Box Volume"
  
  @staticmethod  
  def GetMetricUnit():
    return "mm^3"
    
  @staticmethod
  def GetAcceptedTransformRoles():
    return [ "Any" ]
    
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
    
    
  # Instance methods
  def __init__( self ):
    self.minX = None
    self.minY = None
    self.minZ = None
    self.maxX = None
    self.maxY = None
    self.maxZ = None
    
    self.volume = None
    
  def AddAnatomyRole( self, role, node ):
    pass

    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.minX == None or self.minY == None or self.minZ == None or self.maxX == None or self.maxY == None or self.maxZ == None ):
      self.minX = point[ 0 ]
      self.minY = point[ 1 ]
      self.minZ = point[ 2 ]
      self.maxX = point[ 0 ]
      self.maxY = point[ 1 ]
      self.maxZ = point[ 2 ]
      
    if ( point[ 0 ] < self.minX ):
      self.minX = point[ 0 ]
    if ( point[ 1 ] < self.minY ):
      self.minY = point[ 1 ]
    if ( point[ 2 ] < self.minZ ):
      self.minZ = point[ 2 ]
    if ( point[ 0 ] > self.maxX ):
      self.maxX = point[ 0 ]
    if ( point[ 1 ] > self.maxY ):
      self.maxY = point[ 1 ]
    if ( point[ 2 ] > self.maxZ ):
      self.maxZ = point[ 2 ]
    
  def GetMetric( self ):
    return ( self.maxX - self.minX ) * ( self.maxY - self.minY ) * ( self.maxZ - self.minZ )