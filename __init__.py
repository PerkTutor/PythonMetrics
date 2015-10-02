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

def GetFreshCoreMetricModules():
  metricModulesList = []

  for metricName in PerkTutorCoreMetricNames:
    try:
      # If it can't load properly, then just ignore
      currentMetricModule = importlib.import_module( metricName, __name__ )
      metricModulesList.append( currentMetricModule.PerkEvaluatorMetric ) # This implicitly tests whether the class is defined
    except:
      print "Could not load metric: ", metricName, "."
  
  return metricModulesList