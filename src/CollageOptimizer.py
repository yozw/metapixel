import logger
import random

def optimizeCollage(dist, grid, imageLibrary, minimumDistance):
  logger.info("Optimizing collage ...")
  rows = range(grid.imageCountX)
  cols = range(grid.imageCountY)
  images = range(imageLibrary.size())

  # Sort images by goodness-of-fit for each of the grid cells
  candidates = {}
  for r in rows:
    for c in cols:
      candidates[r, c] = sorted(images, key = lambda(k): dist[r, c, k])

  # Start with a solution at which every cell is assigned the best possible candidate
  sol = {}
  maxObjectiveValue = 0
  for r in rows:
    for c in cols:
      sol[r, c] = 0
      maxObjectiveValue += dist[r, c, candidates[r, c][0]]

  allCells = [(r, c) for r in rows for c in cols]
  changedCells = allCells
  while len(changedCells) > 0:
    logger.progress(len(allCells) - len(changedCells), len(allCells))

    newChangedCells = set()
    
    changedCells = list(changedCells)
    random.shuffle(changedCells)
    for c1 in changedCells:
      random.shuffle(allCells)
      for c2 in allCells:
        if c1 == c2:
          continue
        if (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 >= minimumDistance ** 2:
          continue

        image1 = candidates[c1][sol[c1]]
        image2 = candidates[c2][sol[c2]]
        if image1 == image2:
          nextImage1 = candidates[c1][sol[c1] + 1]
          nextImage2 = candidates[c2][sol[c2] + 1]
          bump1 = dist[c1[0], c1[1], nextImage1] + dist[c1[0], c1[1], image2]
          bump2 = dist[c1[0], c1[1], image1] + dist[c1[0], c1[1], nextImage2]
          if bump1 < bump2:
            sol[c1] += 1
            newChangedCells.add(c1)
          else:
            sol[c2] += 1
            newChangedCells.add(c2)
    changedCells = list(newChangedCells)
    
  # Store optimization solution
  usedImages = set()
  solution = {}
  objectiveValue = 0
  for r in rows:
    for c in cols:
      imageIndex = candidates[r, c][sol[r, c]]
      usedImages.add(imageIndex)
      solution[r, c] = imageIndex
      objectiveValue += dist[r, c, imageIndex]
  
  logger.info("Quality = %0.1f%%", 100 * maxObjectiveValue / objectiveValue)
  logger.info("Using %d out of %d images", len(usedImages), len(imageLibrary.images))
  return solution

