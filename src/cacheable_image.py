import os
import hashlib
from PIL import Image

CACHE_DIR = 'cache/'

class CacheableImage(object):
  def __init__(self, getter, *args):
    self._args = args
    self._getter = getter
    self._image = None
    self._keepInMemory = False
    self._getCount = 0

  def keepInMemory(self):
    self._keepInMemory = True

  def free(self):
    self._image = None

  def get(self):
    if self._keepInMemory and self._image:
      return self._image

    self._getCount += 1
    if self._getCount > 10:
      print "Warning: loading the same file %s over and over again" % self.identifier()

    cacheFile = self.cachePng()
    if os.path.isfile(cacheFile):
      image = Image.open(cacheFile)
    else:
      image = self._getter()
      image.save(cacheFile)

    if self._keepInMemory:
      self._image = image

    return image

  def digest(self):
    h = hashlib.new('sha512')
    h.update(str(self._args))
    return h.digest()

  def hashKey(self):
    h = hashlib.new('sha512')
    h.update(str(self._args))
    return h.hexdigest()

  def identifier(self):
    return str(self._args)

  def cacheFileName(self):
    key = self.hashKey()
    if not os.path.exists(CACHE_DIR):
      os.makedirs(CACHE_DIR)
    return os.path.join(CACHE_DIR, key)

  def cachePng(self):
    return self.cacheFileName() + ".png"

  def crop(self, box):
    return CacheableImage(
               lambda: self.get().crop(box).convert('RGB'),
               self.identifier(), box)

