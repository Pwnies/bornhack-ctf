#!/usr/bin/python3

from random import choice, randint, seed
import copy
import datetime


#!/usr/bin/python3


class CheckTetrisGame:

    def __init__(self, checkSchema, returnedFrame, figures):
        self.checkSchema = checkSchema
        self.returnedFrame = returnedFrame

        self.figures = figures

    def findFigures(self):
        # check xout'ed


        fieldFILO = list()
        figureNo = 0
        curFigure = []
        figuresFound = {}

        for frameRow in range(len(self.returnedFrame)):
            for frameColumn in range(len(self.returnedFrame[frameRow])):
                if (self.checkSchema[frameRow][frameColumn] != 'X'):
                    continue
                figureNo += 1
                figureId = self.returnedFrame[frameRow][frameColumn]
                curFigure = self.findFigure(frameRow, frameColumn, figureId)
                if curFigure:
                    figuresFound[figureNo] = curFigure

        return figuresFound

    def findFigure(self, startRow, startColumn, figureId):
        fieldFILO = list()
        fieldFILO.append((startRow, startColumn))
        figureCoordinates = []

        # while messages in FILO
        while fieldFILO:
            curRow, curColumn = fieldFILO.pop()
            for neighborRow, neighborColumn in self.returnNeighbors(curRow, curColumn):
                if self.checkSchema[neighborRow][neighborColumn] != 'X':
                    continue
                if self.returnedFrame[neighborRow][neighborColumn] != figureId:
                    continue
                self.checkSchema[neighborRow][neighborColumn] = figureId
                figureCoordinates.append((neighborRow, neighborColumn))
                fieldFILO.append((neighborRow, neighborColumn))

        if (len(figureCoordinates) != 4):
            return False

        return figureCoordinates

    def returnNeighbors(self, row, column):
        neighbors = []
        if(row > 0):
            neighbors.append((row-1, column))
        if(column > 0):
            neighbors.append((row, column-1))
        if(row < len(self.returnedFrame)-1):
            neighbors.append((row+1, column))
        if(column < len(self.returnedFrame[0])-1):
            neighbors.append((row, column+1))

        return neighbors


class TetrisGame:
    FIGURE1_DATA = [[1],
                    [1],
                    [1],
                    [1]]

    FIGURE2_DATA = [[2,2],
                    [2,2]]

    FIGURE3_DATA = [[3,3,0],
                    [0,3,3]]

    FIGURE4_DATA = [[0,4,4],
                    [4,4,0]]

    FIGURE5_DATA = [[0,5,0],
                    [5,5,5]]

    FIGURE6_DATA = [[6,6],
                    [0,6],
                    [0,6]]

    FIGURE7_DATA = [[7,7],
                    [7,0],
                    [7,0]]

    def __init__(self, frame):
        self.frame = frame
        self.figures = [TetrisFigure(self.FIGURE1_DATA, "figure1"),
                        TetrisFigure(self.FIGURE2_DATA, "figure2"),
                        TetrisFigure(self.FIGURE3_DATA, "figure3"),
                        TetrisFigure(self.FIGURE4_DATA, "figure4"),
                        TetrisFigure(self.FIGURE5_DATA, "figure5"),
                        TetrisFigure(self.FIGURE6_DATA, "figure6"),
                        TetrisFigure(self.FIGURE7_DATA, "figure7")]
        self.curFigure = self.figures[0]
        self.curFigureNo = 0
        self.rotationDegree = 0
        self.stepsThrown = -1
        self.freeSpaceRowNo = -1
        seed()

    def decideThrowColumns(self):
        columnsToThrowIn = len(self.frame.frameData[0]) - self.curFigure.getMaxWidth()
        columnsToThrowInList = [i for i in range(columnsToThrowIn + 1)]
        nextToThrowInList = [i for i in range(columnsToThrowIn + 1)]
        isFreeSpace = False
        freeSpaceRowNo = 0
        for frameRowNo in range(len(self.frame.frameData)):
            isFreeSpace = False
            for column in columnsToThrowInList:
                isCurFreeSpace = self.throwOne(column, frameRowNo)
                if not isCurFreeSpace:
                    nextToThrowInList.remove(column)
                else:
                    isFreeSpace = True

            if not isFreeSpace:
                break
            columnsToThrowInList = nextToThrowInList.copy()
            self.freeSpaceRowNo = frameRowNo

        if not len(columnsToThrowInList):
            return -1

        return choice(columnsToThrowInList)

    def setCurFigure(self):
        self.curFigureNo = randint(0, len(self.figures) - 1)
        self.curFigure = self.figures[self.curFigureNo]

    def setRotationDegree(self):
        self.rotationDegree = randint(0, 3)

    def rotateCurFigure(self):
        self.curFigure.rotate(self.rotationDegree)

    def throwFigure(self):
        self.setCurFigure()
        self.setRotationDegree()
        self.rotateCurFigure()
        columnsToThrowIn = self.decideThrowColumns()
        if columnsToThrowIn == -1:
            return
        self.frame.drawTetrisFigure(columnsToThrowIn, self.curFigure, self.freeSpaceRowNo)

    def throwOne(self, frameColumn, frameRowNo):
        for row in range(self.curFigure.getMaxHeight()-1, -1, -1):
            if (frameRowNo < 0):
                break
            firstSquareCoordinate = self.curFigure.getFirstSquareCoordinate(row) + frameColumn
            width = self.curFigure.measureWidth(row)
            if not self.frame.isFreeSpace(frameRowNo, firstSquareCoordinate, width):
                return False
            frameRowNo -= 1
        return True


class TetrisFrame:
    FRAME_WIDTH = 10
    FRAME_HEIGHT = 10
    frameData = []

    def __init__(self, frameData=[]):
        self.frameData = [['0' for i in range(self.FRAME_WIDTH)] for j in range(self.FRAME_HEIGHT)]
        self.curFigureChar = 'a'

    def compareFrame(self, otherFrame):
        if (len(self.frameData) != len(otherFrame.frameData)):
            return False
        for frameRow in range(self.FRAME_HEIGHT):
            if (len(self.frameData[frameRow]) != len(otherFrame.frameData[frameRow])):
                return False
            for frameColumn in range(self.FRAME_WIDTH):
                if (self.frameData[frameRow][frameColumn]):
                    if (otherFrame.frameData[frameRow][frameColumn] != 'X'):
                        return False
                else:
                    if (otherFrame.frameData[frameRow][frameColumn] != '0'):
                        return False

        return True
    
    def drawTetrisFigure(self, column, figure, freeSpaceRowNo):
        figureRowNo = figure.getMaxHeight() - 1
        figureColumnNo = 0
        for frameRowNo in range(freeSpaceRowNo, freeSpaceRowNo - figure.getMaxHeight(), -1):
            for frameColumnNo in range(column, column + figure.getMaxWidth()):
                if (figure.fieldData[figureRowNo][figureColumnNo]):
                    self.frameData[frameRowNo][frameColumnNo] = self.curFigureChar 
                figureColumnNo += 1
            figureRowNo -= 1
            figureColumnNo = 0
        self.curFigureChar = chr(ord(self.curFigureChar) + 1)

    def getXout(self):
        xoutFrameData = copy.deepcopy(self.frameData)
        for frameRow in range(self.FRAME_HEIGHT):
            for frameColumn in range(self.FRAME_WIDTH):
                if (self.frameData[frameRow][frameColumn] != '0'):
                    xoutFrameData[frameRow][frameColumn] = 'X'
        return xoutFrameData

    def isFreeSpace(self, frameRow, startColumn, width):
        for column in range(startColumn, startColumn+width):
            if (self.frameData[frameRow][column] != '0'):
                return False
        return True

    def __str__(self):
        output = ""
        for row in range(len(self.frameData)):
            for column in range(len(self.frameData[row])):
                output += str(self.frameData[row][column])
            output += '\n'
        return output


class TetrisFigure:
    name = ""
    fieldData = []

    def __init__(self, fieldData, name):
        self.fieldData = fieldData
        self.name = name

    def getFirstSquareCoordinate(self, row):
        for column in range(len(self.fieldData[row])):
            if(self.fieldData[row][column]):
                return column

    def getLowestSquareCoordinate(self, column):
        for row in range(len(self.fieldData)):
            if(self.fieldData[row][column]):
                return row

    def getMaxHeight(self):
        return len(self.fieldData)

    def getMaxWidth(self):
        return len(self.fieldData[0])

    def deleteFoundShape(self, figure, startRow, startColumn):
        for row in range(len(figure.fieldData)):
            for column in range(len(figure.fieldData[row])):
                if (figure.fieldData)[row][column]:
                    self.fieldData[startRow + row][startColumn + column] = '-'

    def measureHeight(self, column):
        if (len(self.fieldData) < 1):
            raise IndexError('fielData for TetrisFigure ' + self.name + ' is empty')
        if (column > len(self.fieldData[0])-1):
            raise IndexError('column number ' + str(column) + ' is greater than the number of columns in ' +\
                             'TetrisFigure ' + self.name + ' ' + str(len(self.fieldData[0]) - 1))
        
        figureMaxHeight = len(self.fieldData)
        figureHeight = 0
        # Measue the hight
        for i in range(figureMaxHeight):
            if(self.fieldData[i][column]):
                figureHeight += 1

        return figureHeight

    def measureWidth(self, row):
        if (len(self.fieldData) < 1 or len(self.fieldData[0]) < 1):
            raise IndexError('fielData for TetrisFigure ' + self.name + ' is empty or unfinished')
        if (row > len(self.fieldData)):
            raise IndexError('row number is greater than the number of rows in ' +\
                             'TetrisFigure ' + self.name)

        figureMaxWidth = len(self.fieldData[0])
        figureWidth = 0
        # Measue the width
        for i in range(figureMaxWidth):
            if(self.fieldData[row][i]):
                figureWidth += 1

        return figureWidth

    def rotate(self, times):
        for i in range(times):
            self.rotateOne()

    def rotateOne(self):
        rotatedData = []

        if (len(self.fieldData) < 1 or len(self.fieldData[0]) < 1):
            raise IndexError('fielData for TetrisFigure ' + self.name + ' is empty or unfinished')
        
        for newRowNo in range(len(self.fieldData[0])-1, -1, -1):
            newRow = []
            for newColumnNo in range(len(self.fieldData)):
                newRow.append(self.fieldData[newColumnNo][newRowNo])
            rotatedData.append(newRow)

        self.fieldData = rotatedData

    def __str__(self):
        output = ''
        output += self.name + '\n'
        for i in range(len(self.fieldData)):
            for j in range(len(self.fieldData[i])):
                output += str(self.fieldData[i][j])
            output += '\n'
        return output

    def subFigure(self, startRow, startColumn, figure, checkShape):
        subFigure = []

        for curRow in range(len(figure.fieldData)):
            newRow = []
            for curColumn in range(len(figure.fieldData[curRow])):
                if(figure.fieldData[curRow][curColumn]):
                    if(checkShape.fieldData[startRow + curRow][startColumn + curColumn] == '-'):
                        return False
                    newRow.append(self.fieldData[startRow + curRow][startColumn + curColumn])
                else:
                    newRow.append(0)
            subFigure.append(newRow)

        return subFigure

    __repr__ = __str__


def createTetrisFrame():
    FIGURES_TO_THROW = 10
    tetrisFrame = TetrisFrame()
    tetrisGame = TetrisGame(tetrisFrame)
    for i in range(FIGURES_TO_THROW):
        tetrisGame.throwFigure()
        print(tetrisGame.frame)

    xoutFrame = copy.deepcopy(tetrisGame.frame)
    xout = xoutFrame.getXout()
    xoutFrame.frameData = xout
    print(xoutFrame)

    checker = CheckTetrisGame(xout, tetrisGame.frame.frameData, tetrisGame.figures)
    figures = checker.findFigures()
    print(figures)
    
    match = False
    if (len(figures) == FIGURES_TO_THROW):
        match = True

    print("Match: " + str(match))


if __name__ == "__main__":
    createTetrisFrame()
