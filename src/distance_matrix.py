"""Code for calculating distances between images (in terms of mean squared error)."""

import logger
import numpy

def imageMSE(imageA, imageB):
  """Calculates the mean squared error between two images."""
  dataA = numpy.array(imageA)
  dataB = numpy.array(imageB)
  difference = dataA.astype(int) - dataB.astype(int)
  return (numpy.linalg.norm(difference) / 256.0) ** 2


def constructDistanceMatrix(grid, imageLibrary):
  """Constructs a distance matrix for the images in the given grid and all
  images in the image library."""

  logger.info("Resizing sub-images to %d x %d...", grid.imageWidth, grid.imageHeight)
  resizedImages = []
  for i in range(len(imageLibrary.images)):
    logger.progress(i, len(imageLibrary.images))
    image = imageLibrary.images[i]
    resizedImage = image.get(grid.imageWidth, grid.imageHeight)
    resizedImages.append(resizedImage)

  logger.info("Constructing distance matrix ...")
  dist = {}
  for i in range(grid.imageCountX):
    logger.progress(i, grid.imageCountX)
    for j in range(grid.imageCountY):
      for k in range(len(resizedImages)):
        dist[i, j, k] = imageMSE(grid[i, j], resizedImages[k])

  return dist


