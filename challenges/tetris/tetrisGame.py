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

    def createMatrixFromFigure(self, shape):
        lowestRowNo = 100
        lowestColumnNo = 100
        highestRowNo = 0
        highestColumnNo = 0

        for row, column in shape:
            if(row < lowestRowNo):
                lowestRowNo = row
            if(column < lowestColumnNo):
                lowestColumnNo = column
            if(row > highestRowNo):
                highestRowNo = row
            if(column > highestColumnNo):
                highestColumnNo = column

        matrix = []
        
        for row in range(highestRowNo - lowestRowNo + 1):
            matrixRow = [0 for column in range(highestColumnNo - lowestColumnNo + 1)]
            matrix += [matrixRow]

        for row, column in shape:
            matrix[row - lowestRowNo][column - lowestColumnNo] = self.returnedFrame[row][column]

        return TetrisFigure(matrix, "curShape")


    def extractFigures(self, shape, figureNo):
        figure = copy.deepcopy(self.figures[figureNo-1])
        #print("FOUND figureNo: " + str(figureNo))
        #print(shape)

        squares = 0
        for row in range(len(shape.fieldData)):
            for column in range(len(shape.fieldData[0])):
                if(shape.fieldData[row][column]):
                    squares += 1

        if (squares % 4 != 0):
            #print("Not divisible by 4")
            #print(shape)
            #print(figure)
            return False
        if (squares == 4):
            for i in range(4):
                #print("tester figur")
                if shape.fieldData == figure.fieldData:
                    #print("MATCH FUNDET")
                    #print(shape)
                    #print(figure)
                    return True
                figure.rotate(1)
        #print("MERE EN 4 GRUPPE TODO")
        #print(shape)
        #print(figure)
        checkShape = TetrisFigure(copy.deepcopy(shape.fieldData), "checkShape")
        print(shape)
        return False

        #print("watch")
        #print(checkShape)

        """
        for row in range(len(shape.fieldData)):
            for column in range(len(shape.fieldData[row])):
                for i in range(4):
                    figureHeight = figure.getMaxHeight()
                    figureWidth = figure.getMaxWidth()
                    print("figHeight: " + str(figureHeight))
                    print("figWidth: " + str(figureWidth))
                    print("row" + str(row))
                    print("column" + str(column))
                    #if (checkShape.fieldData[row][column] == '-'):
                    #    print("zero")
                    #    continue
                    if (shape.getMaxHeight() < figureHeight or len(shape.fieldData)-row < figureHeight):
                        print("too small height")
                        continue
                    if (shape.getMaxWidth() < figureWidth or len(shape.fieldData[0])-column < figureWidth):
                        print("too small width")
                        continue

                    subShapeData = shape.subFigure(row, column, figure, checkShape)
                    #print("Subshape")
                    print(subShapeData)
                    if not subShapeData:
                        print("FILLED")
                        continue

                    if(subShapeData == figure.fieldData):
                        print("EQUALS")
                        checkShape.deleteFoundShape(figure, row, column)
                    #else:
                        #print("Not equal")
                        #print(subShapeData)
                        #print(figure)

                    figure.rotate(1)

        checkShape = self.splitShape(shape, figure, checkShape, 0, 0)

        if not checkShape:
            return False

        for row in range(len(checkShape.fieldData)):
            for column in range(len(checkShape.fieldData[row])):
                if(checkShape.fieldData[row][column] not in (0, '-')):
                    #print("checkShape ikke blanket")
                    #print(checkShape)
                    return False
        """
        return True

    def splitShape(self, shape, figure, checkShape, row, column):
        #for row in range(len(shape.fieldData)):
            #for column in range(len(shape.fieldData[row])):
        passed = False
        
        if (checkShape.fieldData[row][column] in (0, '-')):
            passed = True
    
        #print("row" + str(row))
        #print("column" + str(column))
        for i in range(4):
            figure.rotate(1)
            #print(figure)
            figureRow = 0
            figureColumn = figure.getFirstSquareCoordinate(figureRow)
            figureHeight = figure.getMaxHeight()
            figureWidth = figure.getMaxWidth()

            results = []
            #print("figHeight: " + str(figureHeight))
            #print("figWidth: " + str(figureWidth))

            # Check leftside space
            if (column < figureColumn):
                #print("no left space")
                continue
            # Check rightside space
            if (column > shape.getMaxWidth() - figureWidth - figureColumn):
                #print("no right space")
                continue

            if (shape.getMaxHeight() < figureHeight):
                #print("too small height")
                continue
            if (shape.getMaxWidth() < figureWidth):
                #print("too small width")
                continue



            subShapeData = shape.subFigure(row, column-figureColumn, figure, checkShape)
            #print("Subshape")
            #print(subShapeData)
            if not subShapeData:
                #print("FILLED")
                continue

            if(subShapeData == figure.fieldData):
                #print("EQUALS - PASSED")
                checkShapeResult = copy.deepcopy(checkShape)
                checkShapeResult.deleteFoundShape(figure, row, column)
                if(column < shape.getMaxWidth() - 1):
                    results.append(self.splitShape(shape, figure, checkShapeResult, row, column+1))
                elif(row < shape.getMaxHeight() - 1):
                    results.append(self.splitShape(shape, figure, checkShapeResult, row+1, column))
                if not results:
                    return False
                passed = True
                break
                    
            #else:
                ##print("Not equal")
                #print(subShapeData)
                #print(figure)

        if not passed:
            #print("NOT PASSED")
            return False
        

        return results


    def findShapes(self):
        # check xout'ed


        fieldFILO = list()
        shapeNo = 0
        curShape = []
        shapesFound = {}
        self.shapeNoToFigNo = {}

        for frameRow in range(len(self.returnedFrame)):
            for frameColumn in range(len(self.returnedFrame[frameRow])):
                if (self.checkSchema[frameRow][frameColumn] != 'X'):
                    continue
                shapeNo += 1
                figureNo = self.returnedFrame[frameRow][frameColumn]
                self.shapeNoToFigNo[shapeNo] = figureNo
                curShape = self.findFigure(frameRow, frameColumn, figureNo)
                shapesFound[shapeNo] = curShape

        #print(shapesFound)

        return shapesFound

    def findFigure(self, startRow, startColumn, figureNo):
        fieldFILO = list()
        fieldFILO.append((startRow, startColumn))
        figureCoordinates = []

        # while messages in FILO
        while fieldFILO:
            curRow, curColumn = fieldFILO.pop()
            for neighborRow, neighborColumn in self.returnNeighbors(curRow, curColumn):
                if self.checkSchema[neighborRow][neighborColumn] != 'X':
                    continue
                if self.returnedFrame[neighborRow][neighborColumn] != figureNo:
                    continue
                self.checkSchema[neighborRow][neighborColumn] = figureNo
                figureCoordinates.append((neighborRow, neighborColumn))
                fieldFILO.append((neighborRow, neighborColumn))

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

    def copyReturnedFigure(self, figure, frameReturned, frameRow,
                           frameColumn):
        returnedFigure = []

        for row in range(len(figure.figureData)):
            newRow = []
            for column in range(len(figure.figureData[row])):
                # check om frame row og column er for store
                figureRowIndx = frameRow + row
                figureColumnIndx = frameColumn + column
                if ((figureRowIndx > len(frameReturned)) or (figureColumnIndx > len(frameReturned[figureRowIndx]))):
                    return []
                if (figure.figureData[row][column]):
                    newRow += frameReturned[frameRow+row][frameColumn+column]
                else:
                    newRow += 0
            returnedFigure += newRow
            
        return returnedFigure
                
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

        #print(columnsToThrowInList)
        return choice(columnsToThrowInList)

    def setCurFigure(self):
        self.curFigureNo = randint(0, len(self.figures) - 1)
        self.curFigure = self.figures[self.curFigureNo]

    def setRotationDegree(self):
        self.rotationDegree = randint(0, 3)

    def rotateCurFigure(self):
        self.curFigure.rotate(self.rotationDegree)

    def throwFigure(self):
        #print('ENTERING throwFigure')
        self.setCurFigure()
        #print(self.curFigure)
        self.setRotationDegree()
        #print(self.rotationDegree)
        self.rotateCurFigure()
        #print(self.curFigure)
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
        self.frameData = [[0 for i in range(self.FRAME_WIDTH)] for j in range(self.FRAME_HEIGHT)]

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
                    if (otherFrame.frameData[frameRow][frameColumn] != 0):
                        return False

        return True
    
    def drawTetrisFigure(self, column, figure, freeSpaceRowNo):
        figureRowNo = figure.getMaxHeight() - 1
        figureColumnNo = 0
        for frameRowNo in range(freeSpaceRowNo, freeSpaceRowNo - figure.getMaxHeight(), -1):
            for frameColumnNo in range(column, column + figure.getMaxWidth()):
                if (figure.fieldData[figureRowNo][figureColumnNo]):
                    self.frameData[frameRowNo][frameColumnNo] = figure.fieldData[figureRowNo][figureColumnNo]
                figureColumnNo += 1
            figureRowNo -= 1
            figureColumnNo = 0

    def getXout(self):
        xoutFrameData = copy.deepcopy(self.frameData)
        for frameRow in range(self.FRAME_HEIGHT):
            for frameColumn in range(self.FRAME_WIDTH):
                if self.frameData[frameRow][frameColumn]:
                    xoutFrameData[frameRow][frameColumn] = 'X'
        return xoutFrameData

    def isFreeSpace(self, frameRow, startColumn, width):
        for column in range(startColumn, startColumn+width):
            if self.frameData[frameRow][column]:
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


def printDimensions(figur):
    dimensions = "----------------------------------\n"
    for row in range(len(figur.fieldData)):
        dimensions += "Row " + str(row) + " width: \t\t" + str(figur.measureWidth(row)) + "\n"
    dimensions += "----------------------------------\n"
    for column in range(len(figur.fieldData[0])):
        dimensions += "Column " + str(column) + " height: \t" + str(figur.measureHeight(column)) + "\n"
    dimensions += "----------------------------------\n"
    #print(dimensions)


def createTetrisFrame():
    tetrisFrame = TetrisFrame()
    tetrisGame = TetrisGame(tetrisFrame)
    for i in range(10):
        tetrisGame.throwFigure()
        print(tetrisGame.frame)

    xoutFrame = copy.deepcopy(tetrisGame.frame)
    xout = xoutFrame.getXout()
    xoutFrame.frameData = xout
    print(xoutFrame)

    checker = CheckTetrisGame(xout, tetrisGame.frame.frameData, tetrisGame.figures)
    shapes = checker.findShapes()
    allFiguresMatch = True
    for shapeNo, shape in shapes.items():
        figureNo = checker.shapeNoToFigNo[shapeNo]
        shapeMatrix = checker.createMatrixFromFigure(shape)
        figuresInShape = checker.extractFigures(shapeMatrix, figureNo)
        if not figuresInShape:
            allFiguresMatch = False

    print("Match: " + str(allFiguresMatch))

    """
    figures = [TetrisFigure(FIGURE1_DATA, "figure1"),
               TetrisFigure(FIGURE2_DATA, "figure2"),
               TetrisFigure(FIGURE3_DATA, "figure3"),
               TetrisFigure(FIGURE4_DATA, "figure4"),
               TetrisFigure(FIGURE5_DATA, "figure5"),
               TetrisFigure(FIGURE6_DATA, "figure6"),
               TetrisFigure(FIGURE7_DATA, "figure7")]

    for figure in figures:
        #print(figure)
        #printDimensions(figure)

    for figure in figures:
        figure.rotate(1)

    for figure in figures:
        #print(figure)
        #printDimensions(figure)

    for figure in figures:
        figure.rotate(1)

    for figure in figures:
        #print(figure)
        #printDimensions(figure)

    for figure in figures:
        figure.rotate(1)

    for figure in figures:
        #print(figure)
        #printDimensions(figure)
    """

if __name__ == "__main__":
    createTetrisFrame()
