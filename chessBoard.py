import json
import pygame as pg
from pygame.locals import *


# contains board functions, critical functions of the game
class Board:
    def __init__(self, screen):
        self.pieceImages = self.importPieceImages()
        self.boardPositions = {}
        self.rows = '87654321'
        self.cols = 'abcdefgh'
        self.boardColors = [(238, 238, 210), (118, 150, 86)]
        self.currentDrawingColor = self.boardColors[0]
        self.pieceSelected = ''
        self.frameCount = {0: False}
        self.screen = screen  # pygame screen
        self.legalGen = self.legalMoveGenerator()
        self.turn = 'white'

    # Generate legal moves
    class legalMoveGenerator:
        def __init__(self):
            self.cols = 'abcdefgh'
            self.rows = '87654321'
            self.legalMoves = []

        def generateLegalMoves(self, boardPositions, pieceSelected):
            col = list(pieceSelected)[0]
            row = list(pieceSelected)[1]
            pieceDetails = boardPositions[pieceSelected]['piece'].split('_')
            match pieceDetails[1]:
                case 'pawn':
                    legalMoves = self.generatePawnMoves(boardPositions, col, row, pieceDetails)
                    self.legalMoves = []
                    return legalMoves
                case 'bishop':
                    legalMoves = self.generateBishopMoves(boardPositions, col, row, pieceDetails)
                    self.legalMoves = []
                    return legalMoves
                case 'rook':
                    legalMoves = self.generateRookMoves(boardPositions, col, row, pieceDetails)
                    self.legalMoves = []
                    return legalMoves
                case 'queen':
                    legalMoves = self.generateQueenMoves(boardPositions, col, row, pieceDetails)
                    self.legalMoves = []
                    return legalMoves
                case 'knight':
                    legalMoves = self.generateKnightMoves(boardPositions, col, row, pieceDetails)
                    self.legalMoves = []
                    return legalMoves
                case _:
                    print('Not a valid piece')
                    return []

        def generatePawnMoves(self, boardPositions, col, row, pieceDetails):
            getPiece = lambda x: boardPositions.get(x, {}).get('piece', '')  # makes life easy

            if pieceDetails[0] == 'white':
                if row == '2':
                    if getPiece(f'{col}3') == '':
                        if getPiece(f'{col}4') == '':
                            self.legalMoves.append(f'{col}3')
                            self.legalMoves.append(f'{col}4')
                if getPiece(f'{col}{int(row) + 1}') == '' and row != '8':
                    self.legalMoves.append(f'{col}{int(row) + 1}')
                # check if diagonal kills are available for pawn
                if col != 'h':
                    if getPiece(f'{self.cols[self.cols.index(col) + 1]}{int(row) + 1}') != '':
                        self.legalMoves.append(f'{self.cols[self.cols.index(col) + 1]}{int(row) + 1}')
                if col != 'a':
                    if getPiece(f'{self.cols[self.cols.index(col) - 1]}{int(row) + 1}') != '':
                        self.legalMoves.append(f'{self.cols[self.cols.index(col) - 1]}{int(row) + 1}')
            elif pieceDetails[0] == 'black':
                if row == '7':
                    if getPiece(f'{col}6') == '':
                        if getPiece(f'{col}5') == '':
                            self.legalMoves.append(f'{col}6')
                            self.legalMoves.append(f'{col}5')
                if getPiece(f'{col}{int(row) - 1}') == '' and row != '1':
                    self.legalMoves.append(f'{col}{int(row) - 1}')
                # check if diagonal kills are available for pawn
                if col != 'a':
                    if getPiece(f'{self.cols[self.cols.index(col) - 1]}{int(row) - 1}') != '':
                        self.legalMoves.append(f'{self.cols[self.cols.index(col) - 1]}{int(row) - 1}')
                if col != 'h':
                    if getPiece(f'{self.cols[self.cols.index(col) + 1]}{int(row) - 1}') != '':
                        self.legalMoves.append(f'{self.cols[self.cols.index(col) + 1]}{int(row) - 1}')
            for i in self.legalMoves:
                if getPiece(i).split('_')[0] == pieceDetails[0]:
                    self.legalMoves.remove(i)
            return list(set(self.legalMoves))

        def generateBishopMoves(self, boardPositions, col, row, pieceDetails):
            colCursor = col
            rowCursor = self.rows.index(row)

            while colCursor != 'a' and rowCursor > -2 and rowCursor < 7:
                colCursor = self.cols[self.cols.index(colCursor) - 1]
                rowCursor += 1
                pieceCursor = boardPositions[f'{colCursor}{self.rows[rowCursor]}']['piece']
                if pieceCursor == '':
                    self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                else:
                    if pieceCursor.split('_')[0] != pieceDetails[0]:
                        self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                    break
            colCursor = col
            rowCursor = self.rows.index(row)
            while colCursor != 'h' and rowCursor > -2 and rowCursor < 7:
                colCursor = self.cols[self.cols.index(colCursor) + 1]
                rowCursor += 1
                pieceCursor = boardPositions[f'{colCursor}{self.rows[rowCursor]}']['piece']
                if pieceCursor == '':
                    self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                else:
                    if pieceCursor.split('_')[0] != pieceDetails[0]:
                        self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                    break
            colCursor = col
            rowCursor = self.rows.index(row)
            while colCursor != 'a' and rowCursor > 0 and rowCursor < 9:
                colCursor = self.cols[self.cols.index(colCursor) - 1]
                rowCursor -= 1
                pieceCursor = boardPositions[f'{colCursor}{self.rows[rowCursor]}']['piece']
                if pieceCursor == '':
                    self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                else:
                    if pieceCursor.split('_')[0] != pieceDetails[0]:
                        self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                    break
            colCursor = col
            rowCursor = self.rows.index(row)
            while colCursor != 'h' and rowCursor > 0 and rowCursor < 9:
                colCursor = self.cols[self.cols.index(colCursor) + 1]
                rowCursor -= 1
                pieceCursor = boardPositions[f'{colCursor}{self.rows[rowCursor]}']['piece']
                if pieceCursor == '':
                    self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                else:
                    if pieceCursor.split('_')[0] != pieceDetails[0]:
                        self.legalMoves.append(f'{colCursor}{self.rows[rowCursor]}')
                    break
            return self.legalMoves

        def generateQueenMoves(self, boardPositions, col, row, pieceDetails):
            self.generateBishopMoves(boardPositions, col, row, pieceDetails)
            self.generateRookMoves(boardPositions, col, row, pieceDetails)
            return self.legalMoves

    def importPieceImages(self):
        pieceImages = {}

        for color in ['white', 'black']:
            for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                pieceImages[f'{color}_{piece}'] = pg.image.load(f'./images/{color}_{piece}.png')
        return pieceImages

    # Create chess board rects (init for draw)
    def createBoard(self):
        currentPosX = 0
        currentPosY = 0

        for row in self.rows:
            for col in self.cols:
                squareRect = pg.Rect(currentPosX, currentPosY, 100, 100)
                self.boardPositions[f'{col}{row}'] = {'squareRect': squareRect}
                self.boardPositions[f'{col}{row}']['selected'] = [False, False, False]
                currentPosX += 100
            currentPosX = 0
            currentPosY += 100

    # Reset board to starting position
    def resetBoardToStart(self):
        for row in self.rows:
            for col in self.cols:
                self.boardPositions[f'{col}{row}']['piece'] = ''

        with open('./startingPosition.json') as startingPosFile:
            startingPos = json.load(startingPosFile)

            for position in startingPos:
                self.boardPositions[position]['piece'] = f'{startingPos[position]["color"]}_{startingPos[position]["piece"]}'

    def drawPieces(self):
        for row in self.rows:
            for col in self.cols:
                piece = self.boardPositions[f'{col}{row}']['piece']
                squareRect = self.boardPositions[f'{col}{row}']['squareRect']

                if piece != '':
                    imageRect = self.pieceImages[piece].get_rect()
                    imageRect.center = squareRect.center
                    self.screen.blit(self.pieceImages[piece], imageRect)

    def updatePiecePosition(self):
        l, m, r = pg.mouse.get_pressed()

        if l == 1:
            self.frameCount[next(reversed(self.frameCount.keys())) + 1] = True  # Add new frame to frameCount, adding if mouse was pressed or not
        else:
            self.frameCount[next(reversed(self.frameCount.keys())) + 1] = False

        if self.pieceSelected:
            for row in self.rows:
                for col in self.cols:
                    if self.boardPositions[f'{col}{row}']['squareRect'].collidepoint(pg.mouse.get_pos()):
                        legalMoves = self.legalGen.generateLegalMoves(self.boardPositions, self.pieceSelected)
                        if l == 1 and self.frameCount[next(reversed(self.frameCount.keys())) - 1] is False:  # Check if mouse was pressed last frame, to avoid duplicates and complications
                            if f'{col}{row}' in legalMoves:
                                self.boardPositions[f'{col}{row}']['piece'] = self.boardPositions[self.pieceSelected]['piece']
                                self.boardPositions[self.pieceSelected]['piece'] = ''
                                print(self.boardPositions[f'{col}{row}']['piece'])
                                print(self.boardPositions[self.pieceSelected]['piece'])
                                self.deselectLegalMoves(legalMoves, self.pieceSelected)
                                self.pieceSelected = ''
                                self.turn = 'black' if self.turn == 'white' else 'white'
                                break
                            else:
                                print("Illegal move, pawn deselected")
                                if self.boardPositions[f'{col}{row}']['piece'].split('_')[0] == self.turn and f'{col}{row}' != self.pieceSelected:
                                    self.deselectLegalMoves(legalMoves, self.pieceSelected)
                                    self.pieceSelected = f'{col}{row}'
                                    self.selectLegalMoves(self.legalGen.generateLegalMoves(self.boardPositions, self.pieceSelected), self.pieceSelected)
                                    print('new piece selected')
                                else:
                                    self.deselectLegalMoves(legalMoves, self.pieceSelected)
                                    self.pieceSelected = ''
                                break
                        elif self.pieceSelected == f'{col}{row}' and l == 1 and self.frameCount[next(reversed(self.frameCount.keys())) - 1] is False:
                            print("pawn deselected")
                            self.deselectLegalMoves(legalMoves, self.pieceSelected)
                            self.pieceSelected = ''
                            break
        else:
            for row in self.rows:
                for col in self.cols:
                    piece = self.boardPositions[f'{col}{row}']['piece']
                    squareRect = self.boardPositions[f'{col}{row}']['squareRect']
                    if piece != '' and squareRect.collidepoint(pg.mouse.get_pos()) and l == 1 and self.frameCount[next(reversed(self.frameCount.keys())) - 1] is False and self.turn == piece.split('_')[0]:
                        self.pieceSelected = f'{col}{row}'
                        legalMoves = self.legalGen.generateLegalMoves(self.boardPositions, self.pieceSelected)
                        self.selectLegalMoves(legalMoves, self.pieceSelected)
                        print(self.pieceSelected)
                        print(self.legalGen.generateLegalMoves(self.boardPositions, self.pieceSelected))
                        break

    def selectLegalMoves(self, legalMoves, pieceSelected):
        self.boardPositions[pieceSelected]['selected'] = [False, False, False]
        self.boardPositions[pieceSelected]['selected'][0] = True
        for move in legalMoves:
            self.boardPositions[move]['selected'] = [False, False, False]
            if self.boardPositions[move]['piece'] != '':
                self.boardPositions[move]['selected'][2] = True
            else:
                self.boardPositions[move]['selected'][1] = True

    def deselectLegalMoves(self, legalMoves, pieceSelected):
        self.boardPositions[pieceSelected]['selected'] = [False, False, False]
        for move in legalMoves:
            self.boardPositions[move]['selected'] = [False, False, False]

    def drawBoard(self):
        # Draw chess board on screen
        for row in self.rows:
            for col in self.cols:
                if self.boardPositions[f'{col}{row}']['selected'][1]:
                    pg.draw.rect(self.screen, self.currentDrawingColor, self.boardPositions[f'{col}{row}']['squareRect'])
                    if self.currentDrawingColor == self.boardColors[0]:
                        pg.draw.circle(self.screen, (214, 214, 189), self.boardPositions[f'{col}{row}']['squareRect'].center, 15)
                    else:
                        pg.draw.circle(self.screen,(106, 135, 77), self.boardPositions[f'{col}{row}']['squareRect'].center, 15)
                    self.currentDrawingColor = self.boardColors[0] if self.currentDrawingColor == self.boardColors[1] else self.boardColors[1]
                elif self.boardPositions[f'{col}{row}']['selected'][0]:
                    pg.draw.rect(self.screen, (246, 246, 105), self.boardPositions[f'{col}{row}']['squareRect'])
                    self.currentDrawingColor = self.boardColors[0] if self.currentDrawingColor == self.boardColors[1] else self.boardColors[1]
                elif self.boardPositions[f'{col}{row}']['selected'][2]:
                    pg.draw.rect(self.screen, self.currentDrawingColor, self.boardPositions[f'{col}{row}']['squareRect'])
                    if self.currentDrawingColor == self.boardColors[0]:
                        pg.draw.circle(self.screen, (214, 214, 189), self.boardPositions[f'{col}{row}']['squareRect'].center, 50)
                    else:
                        pg.draw.circle(self.screen,(106, 135, 77), self.boardPositions[f'{col}{row}']['squareRect'].center, 50)
                    self.currentDrawingColor = self.boardColors[0] if self.currentDrawingColor == self.boardColors[1] else self.boardColors[1]
                else:
                    pg.draw.rect(self.screen, self.currentDrawingColor, self.boardPositions[f'{col}{row}']['squareRect'])
                    # switching color back and forth (to draw)
                    self.currentDrawingColor = self.boardColors[0] if self.currentDrawingColor == self.boardColors[1] else self.boardColors[1]

            # switch color once more after all cols done (because chess board)
            self.currentDrawingColor = self.boardColors[0] if self.currentDrawingColor == self.boardColors[1] else self.boardColors[1]