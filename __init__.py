import importlib

# The list of all the core metrics
# Note: To add a "Core" metric, simply add its name to the list (note the dot at the beginning of the name)
PerkTutorCoreMetricNames = [
  ".ElapsedTime",
  ".PathLength",
  ".TissueDamage",
  ".TissuePath",
  ".TissueTime"
]

def GetFreshCoreMetrics():
  PerkTutorCoreMetrics = []

  for metricName in PerkTutorCoreMetricNames:
    metricModule = importlib.import_module( metricName, __name__ )
    PerkTutorCoreMetrics.append( metricModule.PerkEvaluatorMetric() )
  
  return PerkTutorCoreMetrics