from collections.abc import Iterable
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from re import split
from sys import float_info

class StaticUtils:
   @staticmethod
   def getIntersection(line1, line2):
      a1 = (line1[0][1] - line1[1][1]) / (line1[0][0] - line1[1][0])
      b1 = line1[0][1] - (a1 * line1[0][0])

      a2 = (line2[0][1] - line2[1][1]) / (line2[0][0] - line2[1][0])
      b2 = line2[0][1] - (a2 * line2[0][0])
      
      if abs(a1 - a2) < float_info.epsilon:
         raise ValueError()
      
      x = (b2 - b1) / (a1 - a2)
      y = a1 * x + b1
      
      return StaticUtils.round((x, y))
   
   @staticmethod
   def getOrSetIfAbsent(obj, key, default):
      if key not in obj:
         obj[key] = default
      
      return obj[key]
   
   @staticmethod
   def isIterable(obj, ignore = (str,)):
      return not isinstance(obj, ignore) and isinstance(obj, Iterable)
   
   @staticmethod
   def mergeJson(a, b, overwrite = False):
      c = deepcopy(a)
      
      for key, value in b.items():
         splitKey = split("[\[\]]", key)
         l = len(splitKey)
         
         if l == 1:
            if (key not in c) or overwrite:
               c[key] = value
            
            else:
               invalidType = type(c[key]) if not isinstance(c[key], dict) else type(value) if not isinstance(value, dict) else None
               
               if invalidType:
                  raise ValueError(f"'{key}' exists in both JSONs but is a '{invalidType}' in one of them")
               
               c[key] = mergeJson(c[key], b[key])
         
         elif l == 3 and not len(splitKey[2]):
            c[splitKey[0]][int(splitKey[1])] = value
         
         else:
            raise ValueError(f"Something terrible happened: {key}, {splitKey}")
      
      return c
   
   @staticmethod
   def round(value):
      return [StaticUtils.round(val) for val in value] if StaticUtils.isIterable(value) else int(Decimal(value).to_integral_value(ROUND_HALF_UP))
