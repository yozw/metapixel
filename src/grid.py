import logger
from PIL import Image, ImageFilter

class Grid(object):
  def __init__(self, count, images):
    self.images = images
    self.imageSize = images[0, 0].size
    self.imageWidth = self.imageSize[0]
    self.imageHeight = self.imageSize[1]
    self.imageCount = count
    self.imageCountX = count[0]
    self.imageCountY = count[1]
    self.size = (self.imageCountX * self.imageWidth, self.imageCountY * self.imageHeight)

  def __getitem__(self, key):
    return self.images[key]


class TemplateImage(object):
  def __init__(self):
    pass

  def load(self, fileName):
    self.image = Image.open(fileName)
    self.image.convert('RGB')

  def chop(self, subImageCount, subImageSize):
    logger.info("Template image has size %d x %d" % self.image.size)

    size = (subImageCount[0] * subImageSize[0], subImageCount[1] * subImageSize[1])
    logger.info("Resizing template image to %d x %d" % size)
    image = self.image.resize(size, Image.ANTIALIAS)

    logger.info("Chopping up template image into %d x %d subimages of size %d x %d",
        subImageCount[0], subImageCount[1], subImageSize[1], subImageSize[1])

    subImageWidth = subImageSize[0]
    subImageHeight = subImageSize[1]
    subImagesX = subImageCount[0]
    subImagesY = subImageCount[1]

    images = {}
    for i in range(subImagesX):
      for j in range(subImagesY):
        x = i * subImageWidth
        y = j * subImageHeight
        box = (x, y, x + subImageWidth, y + subImageHeight)
        cropped = image.crop(box).convert('RGB')
        images[i, j] = cropped

    return Grid(subImageCount, images)

