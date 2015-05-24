import os
import hashlib
import math
import logger

from glob import glob
from PIL import Image

CACHE_DIR = 'cache/'

def getHashKey(*args):
  h = hashlib.new('sha512')
  h.update(str(args))
  return h.hexdigest()


def getCacheFileName(*args):
  key = getHashKey(*args)
  if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
  return os.path.join(CACHE_DIR, key)


def getCachePng(*args):
  return getCacheFileName(*args) + ".png"


class SubImage(object):
  def __init__(self, fileName):
    self.fileName = fileName
    self.image = None
    
  def gc(self):
    del self.image
    self.image = None
    
  def load(self):
    if not self.image:
      self.image = Image.open(self.fileName)
      self.image.convert('RGB')
      self.width = self.image.size[0]
      self.height = self.image.size[1]
      self.aspectRatio = self.width / self.height
    
  def get(self, width, height, cx = 0.5, cy = 0.5, scale = 1):
    cacheFile = getCachePng(self.fileName, width, height, cx, cy, scale)
    if os.path.isfile(cacheFile):
      return Image.open(cacheFile)
      
    self.load()
    aspectRatio = width / height
    if self.aspectRatio < aspectRatio:
      targetWidth = scale * self.width
      targetHeight = targetWidth / aspectRatio
    else:
      targetHeight = scale * self.height
      targetWidth = targetHeight * aspectRatio
      
    x1 = int(round(cx * self.width - targetWidth / 2))
    x2 = int(round(cx * self.width + targetWidth / 2))
    y1 = int(round(cy * self.height - targetHeight / 2))
    y2 = int(round(cy * self.height + targetHeight / 2))
    
    result = self.image.crop((x1, y1, x2, y2)).resize((width, height), Image.ANTIALIAS)
    result.save(cacheFile)
    self.gc()
    return result
    

class ImageLibrary(object):
  def __init__(self):
    self.images = []
    
  def load(self, fileSpec):
    for fileName in glob(fileSpec):
      self.images.append(SubImage(fileName))

  def size(self):
    return len(self.images)
    


