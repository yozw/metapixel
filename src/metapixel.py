"""Metapixel main file."""

import argparse
import logger

from grid import TemplateImage
from image_library import ImageLibrary
from distance_matrix import constructDistanceMatrix
from collage_optimizer import optimizeCollage
from collage_renderer import renderCollage

def size(string):
  """Parse a size argument."""
  try:
    width, height = [int(item) for item in string.split('x')]
    return (width, height)
  except:
    raise argparse.ArgumentTypeError(
        'Invalid size specification: %s. Size must specified as wxh.' % string)


def main():
  """Metapixel entry point."""
  parser = argparse.ArgumentParser(description='Metapixel.')
  parser.add_argument('inputFile', help='input file name')
  parser.add_argument('outputFile', help='output file name')
  parser.add_argument('-c', metavar='alpha', type=float, default=0.2, dest='cheatFactor',
                     help='overlay the input image on top with alpha')
  parser.add_argument('-d', metavar='dist', type=int, default=10, dest='minimumDistance',
                     help='minimum distance between copies of the same image')
  parser.add_argument('-l', metavar='filespec', dest='inputSpec',
                     help='path and file mask for input sub-images (e.g. *.jpg)')
  parser.add_argument('-n', metavar='size', type=size, default=(20, 20), dest='subImageCount',
                     help='dimensions of the collage (default 20x20)')
  parser.add_argument('-m', metavar='size', type=size, default=(6, 6), dest='sampleSize',
                     help='size to scale input images down to for image matching (default 6x6)')
  parser.add_argument('-s', metavar='size', type=size, default=(20, 20), dest='subImageSize',
                     help='size of input images in the output collage (default 50x50)')

  args = parser.parse_args()

  logger.info('Generating a %d x %d collage.' % args.subImageCount)
  logger.info('Sub-images are resized to %d x %d for image matching.' % args.sampleSize)
  logger.info('Sub-images are rendered at size %d x %d.' % args.subImageSize)
  logger.info('Cheating factor alpha = %0.2f.', args.cheatFactor)
  logger.info('Minimum distance of repeated images = %d.', args.minimumDistance)
  logger.info('-' * 70)

  templateImage = TemplateImage()
  templateImage.load(args.inputFile)
  sampleGrid = templateImage.chop(args.subImageCount, args.sampleSize)
  outputGrid = templateImage.chop(args.subImageCount, args.subImageSize)

  logger.info('Output collage will be %d x %d.' % outputGrid.size)

  imageLibrary = ImageLibrary()
  imageLibrary.load(args.inputSpec)
  logger.info('Loaded %d images into image library.', imageLibrary.size())

  dist = constructDistanceMatrix(sampleGrid, imageLibrary)

  solution = optimizeCollage(dist,
                             sampleGrid,
                             imageLibrary,
                             args.minimumDistance)
  renderCollage(solution,
                outputGrid,
                sampleGrid,
                imageLibrary,
                cheatFactor=args.cheatFactor,
                outputFile=args.outputFile)

  logger.info('Finished.')

if __name__ == '__main__':
  main()
