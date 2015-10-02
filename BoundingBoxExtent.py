import math

class PerkEvaluatorMetric:

  def __init__( self ):
    self.minX = None
    self.minY = None
    self.minZ = None
    self.maxX = None
    self.maxY = None
    self.maxZ = None
    
    self.volume = None
  
  def GetMetricName( self ):
    return "Bounding Box Extent"
    
  def GetMetricUnit( self ):
    return "mm"
    
  def GetAcceptedTransformRoles( self ):
    return [ "Any" ]
    
  def GetRequiredAnatomyRoles( self ):
    return {}
    
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
    extent = [ self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ ]
    separator = "\t"    
    return separator.join( map( str, extent ) )