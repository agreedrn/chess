import pygame as pg
from pygame.locals import *
from chessBoard import Board
import sys
import ctypes
ctypes.windll.user32.SetProcessDPIAware()  # fix windows scaling issue

pg.init()

fps = 60
fpsClock = pg.time.Clock()

width, height = 800, 800
screen = pg.display.set_mode((width, height), pg.SCALED)
pg.display.set_caption("PyChess")
pg.display.set_icon(pg.image.load("images/black_king.png"))

board = Board(screen)

board.createBoard()
board.resetBoardToStart()

# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    # Update.

    board.updatePiecePosition()

    # Draw.
    board.drawBoard()
    board.drawPieces()

    pg.display.flip()
    fpsClock.tick(fps)
