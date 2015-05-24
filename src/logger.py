import math
import sys

needOverwriteProgress = False

def info(*args):
  overwriteProgress()
  formatStr = args[0]
  print formatStr % tuple(args[1:])
  sys.stdout.flush()
  
def status(*args):
  formatStr = args[0]
  print "\r" + formatStr % tuple(args[1:]) + "\r", 
  sys.stdout.flush()

def overwriteProgress():
  global needOverwriteProgress
  if needOverwriteProgress:
    status(" " * 79)
    needOverwriteProgress = False
  
def progress(n, maximum):
  global needOverwriteProgress
  fraction = float(n) / float(maximum)
  if fraction > 1:
    fraction = 1
  elif fraction < 0:
    fraction = 0
  
  width = 70
  leftWidth = int(math.floor(width * fraction))
  rightWidth = width - leftWidth
  percentage = math.floor(100 * fraction)
  status("[%s%s] %d%%  ", "#" * leftWidth, "-" * rightWidth, percentage)
  needOverwriteProgress = True
   



