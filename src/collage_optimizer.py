"""Collage optimizer."""

import logger
import random

def optimizeCollage(dist, grid, imageLibrary, minimumDistance):
  """Optimizes the collage using the given distane matrix, the sample grid,
  the image library, and a minimum distance between copies of the same image."""
  logger.info("Optimizing collage ...")
  rows = range(grid.imageCountX)
  cols = range(grid.imageCountY)
  images = range(imageLibrary.size())

  # Sort images by goodness-of-fit for each of the grid cells
  candidates = {}
  for row in rows:
    for col in cols:
      candidates[row, col] = sorted(images, key=lambda(k): dist[row, col, k])

  # Start with a solution at which every cell is assigned the best possible candidate
  cIdx = {}
  maxObjectiveValue = 0
  for row in rows:
    for col in cols:
      cIdx[row, col] = 0
      maxObjectiveValue += dist[row, col, candidates[row, col][0]]

  allCells = [(row, col) for row in rows for col in cols]
  changedCells = allCells
  while len(changedCells) > 0:
    logger.progress(len(allCells) - len(changedCells), len(allCells))

    newChangedCells = set()

    changedCells = list(changedCells)
    random.shuffle(changedCells)
    for cell1 in changedCells:
      random.shuffle(allCells)
      for cell2 in allCells:
        if cell1 == cell2:
          continue
        if (cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2 >= minimumDistance ** 2:
          continue

        image1 = candidates[cell1][cIdx[cell1]]
        image2 = candidates[cell2][cIdx[cell2]]
        if image1 == image2:
          nextImage1 = candidates[cell1][cIdx[cell1] + 1]
          nextImage2 = candidates[cell2][cIdx[cell2] + 1]
          bump1 = dist[cell1[0], cell1[1], nextImage1] + dist[cell1[0], cell1[1], image2]
          bump2 = dist[cell1[0], cell1[1], image1] + dist[cell1[0], cell1[1], nextImage2]
          if bump1 < bump2:
            cIdx[cell1] += 1
            newChangedCells.add(cell1)
          else:
            cIdx[cell2] += 1
            newChangedCells.add(cell2)
    changedCells = list(newChangedCells)

  # Store optimization solution
  usedImages = set()
  solution = {}
  objectiveValue = 0
  for row in rows:
    for col in cols:
      imageIndex = candidates[row, col][cIdx[row, col]]
      usedImages.add(imageIndex)
      solution[row, col] = imageIndex
      objectiveValue += dist[row, col, imageIndex]

  logger.info("Quality = %0.1f%%", 100 * maxObjectiveValue / objectiveValue)
  logger.info("Using %d out of %d images", len(usedImages), len(imageLibrary.images))
  return solution

