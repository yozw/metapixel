"""Code for calculating distances between images (in terms of mean squared error)."""

from array import array
import os
import pickle
import logger
import numpy

CACHE_FILE = "cache/distances.bin"

def imageMSE(imageA, imageB):
  """Calculates the mean squared error between two images."""
  dataA = numpy.array(imageA)
  dataB = numpy.array(imageB)
  difference = dataA.astype(int) - dataB.astype(int)
  return (numpy.linalg.norm(difference) / 256.0) ** 2


def loadDistancesFromCache():
  if not os.path.isfile(CACHE_FILE):
    return {}
  data = {}
  logger.info("Reading distance matrix from cache ...")
  with open(CACHE_FILE, "rb") as f:
    try:
      while True:
        fromIdArray = array("B")
        fromIdArray.fromfile(f, 512 / 8)
        fromId = fromIdArray.tostring()
        toIdArray = array("B")
        toIdArray.fromfile(f, 512 / 8)
        toId = toIdArray.tostring()
        valueArray = array('d')
        valueArray.fromfile(f, 1)
        value = valueArray[0]
        data[fromId, toId] = value
    except EOFError:
      return data


def saveDistancesToCache(data):
  logger.info("Saving distance matrix to cache ...")
  with open(CACHE_FILE, "wb") as f:
    for fromId, toId in data:
      array("B", fromId).tofile(f)
      array("B", toId).tofile(f)
      array('d', [data[fromId, toId]]).tofile(f)


def constructDistanceMatrix(grid, imageLibrary):
  """Constructs a distance matrix for the images in the given grid and all
  images in the image library."""

  data = loadDistancesFromCache()

  logger.info("Resizing sub-images to %d x %d...", grid.imageWidth, grid.imageHeight)
  resizedImages = []
  for i in range(len(imageLibrary.images)):
    logger.progress(i, len(imageLibrary.images))
    image = imageLibrary.images[i]
    resizedImage = image.get(grid.imageWidth, grid.imageHeight)
    resizedImage.keepInMemory()
    resizedImages.append(resizedImage)

  logger.info("Constructing distance matrix ...")
  dist = {}
  for k in range(len(resizedImages)):
    logger.progress(k, len(resizedImages))
    for i in range(grid.imageCountX):
      for j in range(grid.imageCountY):
        fromId = grid[i, j].digest()
        toId = resizedImages[k].digest()
        if not (fromId, toId) in data:
          data[fromId, toId] = imageMSE(grid[i, j].get(), resizedImages[k].get())
        dist[i, j, k] = data[fromId, toId]
    resizedImages[k].free()

  saveDistancesToCache(data)

  return dist

