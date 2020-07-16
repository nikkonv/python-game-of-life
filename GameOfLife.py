import numpy as np
import pygame
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

# number of cells in x and y
nxC, nyC = 50, 50

dimCW = width/nxC
dimCH = height/nyC

# cell states, alive = 1, dead = 0
gameState = np.zeros((nxC, nyC))

# initial state

gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# execution flow
pauseExect = False

# execution block
while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            if newGameState[cellX, cellY] == 0:
                newGameState[cellX, cellY] = 1
            else:
                newGameState[cellX, cellY] = 0

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                # calculate n nearest neighbours
                n_neig = gameState[(x-1) % nxC, (y-1) % nyC] + \
                    gameState[(x) % nxC, (y-1) % nyC] + \
                    gameState[(x+1) % nxC, (y-1) % nyC] + \
                    gameState[(x-1) % nxC, (y) % nyC] + \
                    gameState[(x+1) % nxC, (y) % nyC] + \
                    gameState[(x-1) % nxC, (y+1) % nyC] + \
                    gameState[(x) % nxC, (y+1) % nyC] + \
                    gameState[(x+1) % nxC, (y+1) % nyC]

                # rule 1: one dead cell with three neighbours alive, come back lo life
                if gameState[x, y] == 0 and n_neig == 3:
                    newGameState[x, y] = 1
                # rule 2: one alive cell with less than two or more than three alive neighbours, die
                elif gameState[x, y] == 1 and (n_neig < 2 or n_neig > 3):
                    newGameState[x, y] = 0

            # polygon of each cell to draw
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                ((x) * dimCW, (y+1) * dimCH)
            ]

            # lets draw the cell for each x,y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    # update game state
    gameState = np.copy(newGameState)
    # update screen
    pygame.display.flip()
