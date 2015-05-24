import logger

from Grid import MainImage
from ImageLibrary import ImageLibrary
from DistanceMatrix import constructDistanceMatrix
from CollageOptimizer import optimizeCollage
from CollageRenderer import renderCollage

cheatFactor = 0.2
minimumDistance = 10
outputFile = "output.png"

subImageCount = (40, 40)
subImageSize = (50, 50)
sampleSize = (6, 6)

inputSpec = "../input/*.jpg"
inputFile = "../input.png"

  
if __name__ == "__main__":
  logger.info("Cheating factor = %0.2f", cheatFactor)
  logger.info("Minimum distance of repeated images = %d", minimumDistance)
  mainImage = MainImage()
  mainImage.load(inputFile)
  sampleGrid = mainImage.chop(subImageCount, sampleSize)
  outputGrid = mainImage.chop(subImageCount, subImageSize)
  
  logger.info("Output will be %d x %d" % outputGrid.size)
  
  imageLibrary = ImageLibrary()
  imageLibrary.load(inputSpec)
  logger.info("Loaded %d images", imageLibrary.size())  

  dist = constructDistanceMatrix(sampleGrid, imageLibrary)
  solution = optimizeCollage(dist, sampleGrid, imageLibrary, minimumDistance)
  renderCollage(solution, outputGrid, sampleGrid, imageLibrary, cheatFactor = cheatFactor, outputFile = outputFile)
            
  logger.info("Finished")

