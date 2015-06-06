import os
import math
import logger

from glob import glob
from PIL import Image
from cacheable_image import CacheableImage

class SubImage(object):
  def __init__(self, fileName):
    self.fileName = fileName

  def __get(self, width, height, cx = 0.5, cy = 0.5, scale = 1):
    image = Image.open(self.fileName)
    image.convert('RGB')
    self.width = image.size[0]
    self.height = image.size[1]
    self.aspectRatio = self.width / self.height

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

    return image.crop((x1, y1, x2, y2)).resize((width, height), Image.ANTIALIAS)

  def get(self, width, height, cx = 0.5, cy = 0.5, scale = 1):
    return CacheableImage(
        lambda: self.__get(width, height, cx, cy, scale),
        self.fileName, width, height, cx, cy, scale)


class ImageLibrary(object):
  def __init__(self):
    self.images = []

  def load(self, fileSpec):
    for fileName in glob(fileSpec):
      self.images.append(SubImage(fileName))

  def size(self):
    return len(self.images)

