"""Collage renderer."""

import itertools
import logger
import numpy

from PIL import Image, ImageEnhance
from distance_matrix import imageMSE

ENABLE_POST_OPTIMIZATION = True

def adjustImage(image, parameters):
  """Adjusts the brightness, contrast, and saturation of the given image."""
  (brightness, contrast, saturation) = parameters
  newImage = ImageEnhance.Brightness(image).enhance(brightness)
  newImage = ImageEnhance.Contrast(newImage).enhance(contrast)
  newImage = ImageEnhance.Color(newImage).enhance(saturation)
  return newImage


def postOptimize(image, goalImage):
  """Adjusts the brightness, contrast, and saturation of the given image in such
  a way that the MSE between the adjusted image and the goal image is minimized."""
  if not ENABLE_POST_OPTIMIZATION:
    return (1, 1, 1)

  # Vary brightness, saturation, contrast to better match the goal image
  brightnessSet = numpy.arange(0.6, 1.3, 0.05)
  contrastSet = numpy.arange(0.9, 1.2, 0.05)
  saturationSet = numpy.arange(1.0, 1.3, 0.05)
  settings = itertools.product(brightnessSet, contrastSet, saturationSet)

  bestMSE = None
  for parameters in settings:
    newImage = adjustImage(image, parameters)
    MSE = imageMSE(newImage, goalImage)
    if not bestMSE or MSE < bestMSE:
      bestMSE = MSE
      bestParameters = parameters

  if not bestParameters:
    raise Exception("Post-optimization failed")

  return bestParameters


def renderCollage(solution, grid, sampleGrid, imageLibrary, outputFile, cheatFactor=0):
  """Post-optimizes the solution and renders the output."""
  logger.info("Post-optimizing ...")
  optimalParameters = {}
  for i in range(grid.imageCountX):
    logger.progress(i, grid.imageCountX)
    for j in range(grid.imageCountY):
      imageIndex = solution[i, j]
      image = imageLibrary.images[imageIndex]
      sampleImage = image.get(sampleGrid.imageWidth, sampleGrid.imageHeight).get()
      optimalParameters[i, j] = postOptimize(sampleImage, sampleGrid[i, j].get())

  logger.info("Rendering collage ...")
  background = Image.new("RGB", grid.size, "white")
  collage = Image.new("RGB", grid.size, "white")
  for i in range(grid.imageCountX):
    logger.progress(i, grid.imageCountX)
    for j in range(grid.imageCountY):
      offset = (i * grid.imageWidth, j * grid.imageHeight)
      imageIndex = solution[i, j]
      image = imageLibrary.images[imageIndex]
      subImage = image.get(grid.imageWidth, grid.imageHeight).get()
      image = adjustImage(subImage, optimalParameters[i, j])
      background.paste(grid[i, j].get(), offset)
      collage.paste(image, offset)

  logger.info("Saving ...")
  output = Image.blend(collage, background, cheatFactor)
  output.save(outputFile)

